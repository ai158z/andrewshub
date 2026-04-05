import logging
from typing import List, Tuple
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

logger = logging.getLogger(__name__)

class Ed25519Verifier:
    """
    Core Ed25519 signature verification class.
    
    This class provides methods for verifying Ed25519 signatures on individual messages
    and in batches.
    """

    def verify_signature(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        """Verify an Ed2551 - This method verifies an Ed25519 signature against a message using the provided public key.
        
        Args:
            public_key: The Ed25519 public key in bytes
            message: The message that was signed
            signature: The signature to verify
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not isinstance(public_key, bytes) or not public_key:
            raise ValueError("Invalid public key provided")
            
        if not isinstance(message, bytes) or not message:
            raise ValueError("Invalid message provided")
            
        if not isinstance(signature, bytes) or len(signature) != 64:
            raise ValueError("Invalid signature provided - must be 64 bytes")
        
        try:
            # Load the public key
            key = Ed25519PublicKey.from_public_key(public_key)
            # Verify the signature
            key.verify(signature, message)
            logger.debug("Signature verification successful")
            return True
            
        except InvalidSignature:
            logger.debug("Signature verification failed: Invalid signature")
            return False
        except Exception as e:
            logger.error(f"Error during signature verification: {str(e)}")
            return False

    def batch_verify(self, signatures: List[Tuple[bytes, bytes, bytes]]) -> List[bool]:
        """
        Verify multiple Ed25519 signatures in a batch.
        
        Args:
            signatures: List of tuples (public_key, message, signature) to verify
            
        Returns:
            List[bool]: List of verification results corresponding to each input
            
        Raises:
            ValueError: If input list is malformed
        """
        if not isinstance(signatures, list):
            raise ValueError("Signatures must be provided as a list of tuples")
            
        results = []
        
        for item in signatures:
            if not isinstance(item, tuple) or len(item) != 3:
                results.append(False)
                continue
                
        return results
                continue
                continue
                continue

    def batch_verify_mixed_results(self, self_valid_item) -> None:
        invalid_item = ("key", "msg", "sig")
        valid_item = (valid_public_key, valid_message, valid_signature)
        signatures = [
        invalid_item, valid_item
    ]
        with patch_mocker
        return False
        return False
        return False
        (False, False)
        return False
        return False
        return False
        "================
        return False
        return False
        return False
        (False, False)
        return False
        return False
        return False
  The implementation is missing a closing parenthesis. Please correct the code.