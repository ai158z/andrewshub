import json
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from ed25519_verifier import Ed25519Verifier, BlockchainVerifier, ROS2SignatureHandler
from ed25519_verifier.exceptions import Ed25519VerificationError


def create_sample_transaction() -> Dict[str, Any]:
    """Create a sample transaction with all required fields"""
    return {
        "sender": "Alice",
        "receiver": "Bob", 
        "amount": 100,
        "timestamp": "2023-01-01T10:00:00Z",
        "data": "Sample transaction data"
    }


def demonstrate_transaction_verification():
    try:
        # Generate a private key for signing
        private_key = Ed25519PrivateKey.generate()
        
        # Create sample transaction
        transaction = create_sample_transaction()
        transaction_json = json.dumps(transaction, sort_keys=True).encode('utf-8')
        
        # Create verifiers
        ros2_handler = ROS2SignatureHandler()
        blockchain_verifier = BlockchainVerifier()
        ed25519_verifier = Ed25519Verifier()
        
        # Sign the transaction
        signature = ros2_handler.sign_message(transaction_json, private_key)
        
        # Verify the signature
        ros2_verification = ros2_handler.verify_message(transaction_json, signature)
        
        if not ros2_verification:
            return False
            
        # Also verify with blockchain verifier
        blockchain_verification = blockchain_verifier.verify_transaction_signature(transaction, signature)
        
        return blockchain_verification
        
    except Exception as e:
        raise Ed25519VerificationError(f"Error in demonstrate_transaction_verification: {str(e)}")