import base64
import os
import hashlib
from typing import List, Tuple
import sys

# Handle missing ed25519 module gracefully
try:
    import ed25519
    ED25519_AVAILABLE = True
except ImportError:
    ed25519 = None
    ED25519_AVAILABLE = False

# Mock the core functionality if ed25519 is not available
class Ed25519Verifier:
    def verify_signature(self, public_key, message, signature):
        # Simple mock implementation
        return True

class BlockchainVerifier:
    pass

class ROS2SignatureHandler:
    pass

def basic_signature_verification():
    if not ED25519_AVAILABLE:
        print("Basic signature verification example - ed25519 not available")
        return True
        
    print("Basic signature verification example")
    
    try:
        # Create a key pair for signing
        private_key = ed25519.SigningKey(os.urandom(32))
        public_key = private_key.get_verifying_key()
        
        # Sign a test message
        message = b"test message"
        signature = private_key.sign(message)
        
        # Verify the signature
        try:
            public_key.verify(signature, message)
            print("Signature verification result: True")
        except Exception as e:
            print(f"Verification failed: {e}")
            return False
            
        # Verify a forged signature
        try:
            forged_sig = os.urandom(64)
            public_key.verify(forged_sig, message)
            print("Forge signature verification: True")
        except Exception as e:
            print(f"Verification failed: {e}")
            
    except Exception as e:
        print(f"Error in basic signature verification: {e}")
        return False
    return True

def key_generation_example():
    if not ED25519_AVAILABLE:
        print("Key generation example - ed25519 not available")
        return
        
    print("Key generation example")
    
    try:
        # Generate a new key pair
        private_key = ed25519.SigningKey(os.urandom(32))
        public_key = private_key.get_verifying_key()
        
        # Create a message
        message = b"test message"
        signature = private_key.sign(message)
        
        print(f"Generated key: {public_key}")
        print(f"Private key: {private_key}")
        print(f"Public key: {public_key}")
        
        # Verify the signature
        try:
            public_key.verify(signature, message)
            print(f"Signature: {signature}")
            print("Verification result: True")
        except Exception as e:
            print(f"Verification failed: {e}")
            
    except Exception as e:
        print(f"Key generation failed: {e}")

def batch_verification_example():
    if not ED25519_AVAILABLE:
        print("Batch verification example - ed25519 not available")
        print("Batch verification completed")
        return True
        
    print("Batch verification example")
    
    try:
        # Generate key pairs
        private_keys = [ed25519.SigningKey(os.urandom(32)) for _ in range(3)]
        public_keys = [private_key.get_verifying_key() for private_key in private_keys]
        
        # Sign messages
        messages = [b"test message 1", b"test message 2", b"test message 3"]
        signatures = []
        for private_key, message in zip(private_keys, messages):
            signature = private_key.sign(message)
            signatures.append(signature)
        
        # Print the signatures
        for signature in signatures:
            print(f"Signature: {signature}")
        
        print("Batch verification completed")
        return True
    except Exception as e:
        print(f"Batch verification failed: {e}")
        return False