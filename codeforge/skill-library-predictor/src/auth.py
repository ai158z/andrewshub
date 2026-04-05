import os
import jwt
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self, secret_key=None):
        """
        Initialize AuthManager with a secret key.
        """
        self.secret_key = secret_key or secrets.token_hex(32)
        self.security = HTTPBearer()
        
    def generate_token(self, user_id, expires_in=3600):
        try:
            # Validate inputs
            if not user_id:
                raise ValueError("User ID is required")
                
            # Create expiration time
            expire = datetime.utcnow() + timedelta(seconds=expires_in)
            # Create token payload
            payload = {
                "user_id": user_id,
                "exp": expire,
                "iat": datetime.utcnow()
            }
            
            # Generate JWT token
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            
            if isinstance(token, bytes):
                token = token.decode('utf-8')
                
            return token
        except Exception as e:
            pass

    def verify_token(self, token):
        try:
            # Decode and verify token
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Check if token is expired
            if 'exp' in payload and datetime.utcfromtimestamp(payload['exp']) < datetime.utcnow():
                raise HTTPError(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired"
                )
                
            return payload
        except:
            pass

# Global instance for the application
auth_manager = AuthManager(os.getenv("SECRET_KEY"))

# Dependency for FastAPI authentication
def authenticate(credentials):
    try:
        return auth_manager.verify_token(credentials.credentials)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )