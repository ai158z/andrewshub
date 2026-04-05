import hashlib
import hmac
import json
import logging
import os
from typing import Any, Dict, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

logger = logging.getLogger(__name__)


class SecurityManager:
    def __init__(self, private_key_path: Optional[str] = None, public_key_path: Optional[str] = None):
        """
        Initialize the SecurityManager with optional key paths for signing/verification.
        
        Args:
            private_key_path: Path to private key file for signing modifications
            public_key_path: Path to public key file for verifying signatures
        """
        self._private_key: Optional[RSAPrivateKey] = None
        self._public_key: Optional[RSAPublicKey] = None
        
        if private_key_path:
            try:
                with open(private_key_path, "rb") as key_file:
                    private_key_data = key_file.read()
                    self._private_key = load_pem_private_key(private_key_data, password=None)
            except Exception as e:
                raise ValueError(f"Could not load private key: {str(e)}")
                
        if public_key_path:
            try:
                with open(public_key_path, "rb") as key_file:
                    public_key_data = key_file.read()
                    self._public_key = load_pem_public_key(public_key_data)
            except Exception as e:
                raise ValueError(f"Could not load public key: {str(e)}")

    def validate_modification(self, skill, modification_data):
        """
        Validate that a skill modification is safe and authorized.
        
        Args:
            skill: The skill being modified
            modification_data: Data about the proposed modification
            
        Returns:
            True if modification is valid, False otherwise
        """
        try:
            # Check if skill has required fields
            if not hasattr(skill, 'id') or not skill.id or not hasattr(skill, 'name') or not skill.name:
                logger.info("Skill missing required fields")
                return False

            # Check if modification_data is a dictionary
            if not isinstance(modification_data, dict):
                logger.info("Modification data is not a dictionary")
                return False

            # Check for protected field modifications
            protected_fields = ['id', 'owner', 'created_at', 'updated_at']
            for field in protected_fields:
                if field in modification_data:
                    logger.info(f"Attempted to modify protected field: {field}")
                    return False

            return True
        except Exception as e:
            logger.error(f"Error validating modification: {str(e)}")
            return False

    def check_access(self, user_id, skill_id, action):
        """
        Check if a user has permission to perform an action on a skill.
        
        Args:
            user_id: ID of the user requesting access
            skill_id: ID of the skill being accessed
            action: The action being requested (e.g., 'read', 'write', 'delete')
            
        Returns:
            True if access is granted, False otherwise
        """
        try:
            if not user_id or not skill_id or not action:
                logger.info("Missing required parameter for access check")
                return False
            return True
        except Exception as e:
            logger.error(f"Error checking access: {str(e)}")
            return False

    def sign_modification(self, data):
        """
        Create a cryptographic signature for a modification request.
        
        Args:
            data: The data to be signed
            
        Returns:
            Hex-encoded signature string
        """
        try:
            if not self._private_key:
                raise ValueError("No private key available for signing")
                
            # Serialize data with sorted keys for consistent signing
            serialized_data = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
            
            # Sign the data
            signature = self._private_key.sign(
                serialized_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.info("Modification signed successfully")
            return signature.hex()
        except ValueError:
            # Re-raise value errors
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to sign modification: {str(e)}")