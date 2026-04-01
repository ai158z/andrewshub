import hashlib
import os
import logging
from typing import Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import secrets

logger = logging.getLogger(__name__)

def hash_key(key: bytes) -> str:
    """
    Hash a key using SHA-256.
    
    Args:
        key (bytes): The key to be hashed
        
    Returns:
        str: Hex digest of the hashed key
    """
    if not isinstance(key, bytes):
        logger.error("Invalid input: key must be bytes")
        raise TypeError("Key must be bytes")
    
    try:
        hash_object = hashlib.sha256(key)
        result = hash_object.hexdigest()
        logger.debug("Key hashed successfully")
        return result
    except Exception as e:
        logger.error(f"Error hashing key: {str(e)}")
        raise

def generate_random_bytes(length: int) -> bytes:
    """
    Generate cryptographically secure random bytes.
    
    Args:
        length (int): Number of random bytes to generate
        
    Returns:
        bytes: Random bytes
    """
    if not isinstance(length, int) or length <= 0:
        logger.error("Invalid input: length must be a positive integer")
        raise ValueError("Length must be a positive integer")
    
    try:
        random_data = secrets.token_bytes(length)
        logger.debug(f"Generated {length} random bytes")
        return random_data
    except Exception as e:
        logger.error(f"Error generating random bytes: {str(e)}")
        raise

def encrypt_data(data: bytes, key: bytes) -> Tuple[bytes, bytes]:
    """
    Encrypt data using AES encryption with the provided key.
    
    Args:
        data (bytes): Data to encrypt
        key (bytes): Encryption key
        
    Returns:
        Tuple[bytes, bytes]: IV and encrypted data
    """
    if not isinstance(data, bytes) or not isinstance(key, bytes):
        logger.error("Invalid input: data and key must be bytes")
        raise TypeError("Data and key must be bytes")
    
    try:
        # Create a cipher object using the key
        backend = default_backend()
        iv = generate_random_bytes(16)  # 128-bit IV for AES
        
        # Pad the key to 32 bytes (256 bits) if necessary
        if len(key) < 32:
            key = key.ljust(32, b'\0')
        elif len(key) > 32:
            key = key[:32]
            
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        
        # Pad the data to be multiple of block size (16 bytes for AES)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data)
        padded_data += padder.finalize()
        
        # Encrypt the data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        logger.debug("Data encrypted successfully")
        return (iv, encrypted_data)
    except Exception as e:
        logger.error(f"Error encrypting data: {str(e)}")
        raise