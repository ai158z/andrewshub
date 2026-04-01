import hashlib
import json
import os
import logging
from typing import Dict, List, Optional, Union
from cryptography.fernet import Fernet
import base64
import threading

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class KeyStorage:
    def __init__(self, storage_path: str = None):
        """Initialize the key storage system."""
        self.storage_path = storage_path or "key_storage.json"
        self._lock = threading.RLock()
        self.keys: Dict[str, Dict] = {}
        self._load_storage()
        # Generate a consistent encryption key instead of a new one each time
        self._generate_encryption_key()
        
    def _generate_encryption_key(self):
        """Generate or load encryption key for consistent decryption across instances."""
        # Use a fixed key for consistent behavior across restarts
        key_file = self.storage_path + ".key"
        if os.path.exists(key_file):
            try:
                with open(key_file, 'rb') as f:
                    self.encryption_key = f.read()
                self.cipher_suite = Fernet(self.encryption_key)
            except:
                # If key file is corrupted, generate new key
                self._create_cipher_suite()
        else:
            # Create key file if it doesn't exist
            self._create_cipher_suite()
            
    def _create_cipher_suite(self):
        """Create a new cipher suite with a new encryption key."""
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption
        # Save the key for persistence
        with open(self.storage_path + ".key", 'wb') as f:
            f.write(self.encryption_key)
    
    def _load_storage(self):
        """Load keys from persistent storage."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    self.keys = json.load(f)
                logger.info("Key storage loaded successfully")
            else:
                self.keys = {}
                logger.info("New key storage initialized")
        except Exception as e:
            logger.error(f"Error loading key storage: {e}")
            self.keys = {}
    
    def _save_storage(self):
        """Save keys to persistent storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.keys, f)
            logger.info("Key storage saved successfully
        except Exception as e:
            logger.error(f"Error saving key storage: {e}")
    
    def store_key(self, key_id: str, key_data: bytes, metadata: Optional[Dict] = None) -> bool:
        """
        Store a key securely in the key storage.
        
        Args:
            key_id: Unique identifier for the key
            key_data: The key data to store
            metadata: Additional metadata about the key
            
        Returns:
            bool: True if storage was successful, False otherwise
        """
        try:
            # Encrypt the key data before storing
            encrypted_data = self.cipher_suite.encrypt(key_data)
            key_hash = hashlib.sha256(key_data).hexdigest()
            
            self.keys[key_id] = {
                'data': encrypted_data.decode('utf-8'),
                'hash': key_hash,
                'metadata': metadata or {}
            }
            
            self._save_storage()
            logger.info(f"Key {key_id} stored successfully")
            return True
        except Exception as e:
            logger.error(f"Error storing key {key_id}: {e}")
            return False
    
    def retrieve_key(self, key_id: str) -> Optional[bytes]:
        """
        Retrieve a key from storage.
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            bytes: The decrypted key data or None if not found
        """
        try:
            if key_id not in self.keys:
                logger.warning(f"Key {key_id} not found in storage")
                return None
            
            # Retrieve and decrypt the key data
            encrypted_data = self.keys[key_id]['data'].encode('utf-8')
            key_data = self.cipher_suite.decrypt(encrypted_data)
            
            logger.info(f"Key {key_id} retrieved successfully")
            return key_data
        except Exception as e:
            logger.error(f"Error retrieving key {key_id}: {e}")
            return None
    
    def delete_key(self, key_id: str) -> bool:
        """
        Delete a key from storage.
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            if key_id in self.keys:
                del self.keys[key_id]
                self._save_storage()
                logger.info(f"Key {key_id} deleted successfully")
                return True
            else:
                logger.warning(f"Key {key_id} not found for deletion")
                return False
        except Exception as e:
            logger.error(f"Error deleting key {key_id}: {e}")
            return False
    
    def key_exists(self, key_id: str) -> bool:
        """
        Check if a key exists in storage.
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            bool: True if key exists, False otherwise
        """
        return key_id in self.keys
    
    def list_keys(self) -> List[str]:
        """
        List all key identifiers in storage.
        
        Returns:
            List of key identifiers
        """
        return list(self.keys.keys())
    
    def get_key_metadata(self, key_id: str) -> Optional[Dict]:
        """
        Get metadata for a specific key.
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            Metadata dictionary or None if key not found
        """
        if key_id in self.keys:
            return self.keys[key_id].get('metadata', {})
        return None
    
    def update_metadata(self, key_id: str, metadata: Dict) -> bool:
        """
        Update metadata for a specific key.
        
        Args:
            key_id: Unique identifier for the key
            metadata: Metadata to update
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if key_id in self.keys:
                if 'metadata' in self.keys[key_id]:
                    self.keys[key_id]['metadata'].update(metadata)
                else:
                    self.keys[key_id]['metadata'] = metadata
                self._save_storage()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating metadata for key {key_id}: {e}")
            return False