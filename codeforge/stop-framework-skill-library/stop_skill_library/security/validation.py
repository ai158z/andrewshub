import hashlib
import hmac
import json
import os
import secrets
from typing import Dict, Any, Optional, Union
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1
from cryptography.exceptions import InvalidSignature
from stop_skill_library.models import SecurityContext


class ModificationValidator:
    """Cryptographic validation of modifications to skills in the library."""
    
    def __init__(self, security_context: Optional[SecurityContext] = None):
        """Initialize the ModificationValidator with optional security context.
        
        Args:
            security_context: Optional security context for validation parameters
        """
        self.security_context = security_context
        self._private_key = None
        self._public_key = None
        self._generate_keys()
    
    def _generate_keys(self) -> None:
        """Generate RSA key pair for cryptographic operations."""
        # Generate a new RSA private key
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        # Get the public key
        self._public_key = self._private_key.public_key()
    
    def _hash_data(self, data: Union[Dict[str, Any], str, bytes]) -> bytes:
        """Create a SHA-256 hash of the data.
        
        Args:
            data: Data to hash - can be dict, str, or bytes
            
        Returns:
            bytes: SHA-256 hash of the data
        """
        if isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        elif isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            raise TypeError("Data must be dict, str, or bytes")
            
        return hashlib.sha256(data_bytes).digest()
    
    def validate(self, data: Dict[str, Any], signature: bytes, public_key_pem: Optional[bytes] = None) -> bool:
        """Validate data against a cryptographic signature.
        
        Args:
            data: Data to validate
            signature: Cryptographic signature to verify against
            public_key_pem: Optional PEM formatted public key
            
        Returns:
            bool: True if signature is valid, False otherwise
            
        Raises:
            TypeError: If data is not a dictionary
        """
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
            
        try:
            # If a specific public key is provided, use it
            if public_key_pem:
                public_key = serialization.load_pem_public_key(public_key_pem)
            else:
                public_key = self._public_key
                
            # Hash the data
            data_hash = self._hash_data(data)
            
            # Verify the signature
            public_key.verify(
                signature,
                data_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except (InvalidSignature, TypeError):
            return False
        except Exception:
            return False
    
    def sign(self, data: Dict[str, Any]) -> bytes:
        """Create a cryptographic signature for data.
        
        Args:
            data: Data to sign
            
        Returns:
            bytes: Cryptographic signature
            
        Raises:
            TypeError: If data is not a dictionary
        """
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
            
        # Hash the data
        data_hash = self._hash_data(data)
        
        # Sign the hash
        signature = self._private_key.sign(
            data_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    
    def verify(self, data: Dict[str, Any], signature: bytes, public_key_pem: Optional[bytes] = None) -> bool:
        """Verify data against a signature.
        
        Args:
            data: Data to verify
            signature: Signature to verify against
            public_key_pem: Optional PEM formatted public key
            
        Returns:
            bool: True if verification successful, False otherwise
        """
        return self.validate(data, signature, public_key_pem)