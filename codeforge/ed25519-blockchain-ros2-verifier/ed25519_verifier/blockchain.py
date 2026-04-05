import base64
import json
import logging
from typing import Dict, List, Tuple
from ed25519_verifier.core import Ed25519Verifier
from ed25519_verifier.utils import decode_signature
from ed25519_verifier.exceptions import Ed25519VerificationError, InvalidSignatureFormatError

logger = logging.getLogger(__name__)

class BlockchainVerifier:
    def __init__(self):
        self.verifier = Ed25519Verifier()
        
    def verify_transaction_signature(self, transaction_data: dict, public_key: str, signature: str) -> bool:
        """
        Verify a blockchain transaction signature.
        
        Args:
            transaction_data: Dictionary containing transaction data
            public_key: Base64 encoded public key string
            signature: Base64 encoded signature string
            
        Returns:
            bool: True if signature is valid, False otherwise
            
        Raises:
            InvalidSignatureFormatError: If the signature or key format is invalid
            Ed25519VerificationError: If verification fails
        """
        try:
            # Validate inputs
            if not isinstance(transaction_data, dict):
                raise Ed25519VerificationError("Transaction data must be a dictionary")
            
            if not isinstance(public_key, str) or not isinstance(signature, str):
                raise InvalidSignatureFormatError("Public key and signature must be strings")
            
            # Decode the public key from base64
            try:
                public_key_bytes = base64.b64decode(public_key)
            except Exception as e:
                raise InvalidSignatureFormatError(f"Invalid public key format: {str(e)}")
            
            # Serialize transaction data to create the message
            message = json.dumps(transaction_data, sort_keys=True).encode('utf-8')
            
            # Decode the signature from base64
            try:
                signature_bytes = base64.b64decode(signature)
            except Exception as e:
                raise InvalidSignatureFormatError(f"Invalid signature format: {str(e)}")
            
            # Perform verification
            result = self.verifier.verify_signature(public_key_bytes, message, signature_bytes)
            
            return result
            
        except Exception as e:
            logger.error(f"Error during transaction signature verification: {str(e)}")
            raise Ed25519VerificationError(f"Verification failed: {str(e)}")

    def validate_blockchain_format(self, signature_format: str) -> bool:
        """
        Validate if the provided signature format is supported.
        
        Args:
            signature_format: String identifier for the signature format
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        # Supported formats for blockchain transactions
        supported_formats = {
            'ed25519-base64',
            'ed25519-base58',
            'ed25519-hex',
            'ed25519-raw'
        }
        
        if not isinstance(signature_format, str):
            return False
            
        return signature_format in supported_formats