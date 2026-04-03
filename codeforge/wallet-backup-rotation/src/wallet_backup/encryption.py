import os
import logging
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2H
from cryptography.hazmat.backends import default_backend
import base64
import hashlib
from typing import Optional


class WalletEncryption:
    def __init__(self, config=None):
        """
        Initialize the WalletEncryption class.
        
        Args:
            config: Configuration object to get the encryption key
        """
        self.config = config
        self._fernet = None
    
    def _get_fernet(self) -> Fernet:
        """
        Initialize and return a Fernet instance with the encryption key from config.
        If no key is provided, a new key will be generated.
        """
        if not self._fernet:
            key = None
            if self.config and hasattr(self.config, 'get_encryption_key'):
                key = self.config.get_encryption_key()
            
            if not key:
                key = self._get_encryption_key()
            
            self._fernet = Fernet(key)
        return self._fernet
    
    def encrypt_data(self, data: str) -> str:
        """
        Encrypt the provided data using Fernet encryption.
        
        Args:
            data: String data to encrypt
            
        Returns:
            Encrypted data as a string
        """
        if data is None:
            raise ValueError("Data to encrypt cannot be None")
            
        f = self._get_fernet()
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data.decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt the provided encrypted data using Fernet decryption.
        
        Args:
            encrypted_data: Encrypted string data
            
        Returns:
            Decrypted data as a string
        """
        f = self._get_fernet()
        decrypted_data = f.decrypt(encrypted_data.encode())
        return decrypted_data.decode()

    def _get_encryption_key(self) -> bytes:
        """
        Get the encryption key from environment variables or generate a new one.
        """
        key = os.environ.get('WALLET_BACKUP_ENCRYPTION_KEY')
        if key:
            # Fix: Use correct base64 decoding
            return base64.urlsafe_b64decode(key)
        else:
            return Fernet.generate_key()

    def _generate_key_from_password(self, password: str, salt: bytes) -> bytes:
        """
        Generate an encryption key from a password using PBKDF2.
        """
        kdf = PBKDF2H(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        # Fix: Return the raw key bytes, not base64 encoded version
        key = kdf.derive(password.encode())
        # Convert to Fernet key format (32-bit encoded key)
        return base64.urlsafe_b64encode(key)

    def _encrypt_with_password(self, data: str, password: str) -> str:
        """
        Encrypt data with a password.
        """
        salt = os.urandom(16)
        key = self._generate_key_from_password(password, salt)
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        # Fix: Return base64 encoded result to make it string compatible
        result = base64.b64encode(salt + encrypted_data).decode()
        return result

    def _decrypt_with_password(self, encrypted_data: str, password: str) -> str:
        """
        Decrypt data with a password.
        """
        # Fix: Correctly extract salt and encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        salt = encrypted_bytes[:16]
        encrypted_payload = encrypted_bytes[16:]
        key = self._generate_key_from_password(password, salt)
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_payload)
        return decrypted_data.decode()

    def _store_key(self, key: str) -> None:
        """
        Store the encryption key in an environment variable.
        """
        os.environ['WALLET_BACKUP_ENCRYPTION_KEY'] = key

    def _load_key(self, key: str) -> bytes:
        """
        Load the encryption key from environment variables.
        """
        # Fix: Use correct base64 decoding
        return base64.urlsafe_b64decode(key)