import hashlib
import hmac
import logging
from typing import Dict, Any
import os
import json
from typing import Union

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Verify the GitHub webhook signature
    
    Args:
        payload: The webhook payload body
        signature: The signature from the X-Hub-Signature-256 header
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Get the webhook secret from environment variables
        secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
        if not secret:
            logger.error("GITHUB_WEBHOOK_SECRET not set in environment variables")
            return False
            
        # GitHub uses SHA-256 for the signature
        expected_signature = 'sha256=' + hmac.new(
            key=secret.encode('utf-8'),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Compare signatures in a way that prevents timing attacks
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Error verifying GitHub signature: {str(e)}")
        return False


def handle_push_event(payload: Union[Dict[str, Any], bytes]) -> None:
    """
    Handle GitHub push events to trigger code analysis
    
    Args:
        payload: GitHub webhook payload data
    """
    try:
        # If payload is bytes, parse it as JSON
        if isinstance(payload, bytes):
            payload_data = json.loads(payload.decode('utf-8'))
        else:
            payload_data = payload
            
        # Extract repository information
        repo_data = payload_data.get('repository', {}) if isinstance(payload_data, dict) else {}
        repo_id = repo_data.get('id') if isinstance(repo_data, dict) else None
        repo_name = repo_data.get('name') if isinstance(repo_data, dict) else None
        owner_data = repo_data.get('owner', {}) if isinstance(repo_data, dict) else {}
        owner_name = owner_data.get('login') if isinstance(owner_data, dict) else None
        
        if not repo_id or not repo_name or not owner_data:
            logger.warning("Invalid repository data in push event")
            return
            
        # Check if repository exists in our system
        # We need to import these functions inside the function to avoid circular imports
        from backend.src.api.routes.repositories import get_repository_by_id, add_repository, sync_repository
        from backend.src.services.code_analyzer import run_analysis
        
        repository = get_repository_by_id(str(repo_id))
        
        # If repository doesn't exist, add it
        if not repository:
            repository = add_repository(repo_data.get('html_url'))
            
        # Sync repository data
        if repository:
            sync_repository(str(repo_id))
            
            # Run analysis on the updated repository
            run_analysis(repository)
        else:
            logger.error(f"Failed to handle repository for {repo_name}")
            
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON payload: {str(e)}")
        return
    except Exception as e:
        logger.error(f"Error handling push event: {str(e)}")
        # In a real implementation, we might want to handle this differently
        # For now, we'll re-raise to maintain the original behavior
        raise e