import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import hashlib
import json

from src.wallet_backup.config import Config
from src.wallet_backup.utils import get_current_timestamp, format_backup_name, get_backup_date
from src.wallet_backup.encryption import WalletEncryption

logger = logging.getLogger(__name__)

class BackupStorage:
    def __init__(self, config: Config):
        self.config = config
        self.local_backup_dir = config.get('local_backup_dir', 'backups')
        self.remote_storage_enabled = config.get('remote_storage_enabled', False)
        self.retention_days = config.get('retention_days', 30)
        self.encryption = WalletEncryption(config.get_encryption_key())
        self._ensure_local_dir_exists()
        
    def _ensure_local_dir_exists(self) -> None:
        """Ensure the local backup directory exists."""
        if not os.path.exists(self.local_backup_dir):
            os.makedirs(self.local_backup_dir)
            
    def store_backup(self, backup_data: bytes) -> str:
        """Store an encrypted backup to local and optionally remote storage."""
        try:
            # Encrypt the backup data
            encrypted_data = self.encryption.encrypt_data(backup_data)
            
            # Generate backup name with timestamp
            backup_name = format_backup_name()
            backup_file_path = os.path.join(self.local_backup_dir, backup_name)
            
            # Store locally
            with open(backup_file_path, 'wb') as f:
                f.write(encrypted_data)
                
            logger.info(f"Backup stored locally: {backup_file_path}")
            
            # Store remotely if enabled
            if self.remote_storage_enabled:
                self._store_remote(backup_name, encrypted_data)
                
            return backup_name
        except Exception as e:
            logger.error(f"Failed to store backup: {str(e)}")
            raise
            
    def retrieve_backup(self, backup_id: str) -> bytes:
        """Retrieve and decrypt a backup by its ID (filename)."""
        try:
            # Try to retrieve from local storage first
            backup_file_path = os.path.join(self.local_backup_dir, backup_id)
            
            if os.path.exists(backup_file_path):
                with open(backup_file_path, 'rb') as f:
                    encrypted_data = f.read()
                return self.encryption.decrypt_data(encrypted_data)
            elif self.remote_storage_enabled:
                # Try remote storage
                encrypted_data = self._retrieve_remote(backup_id)
                if encrypted_data:
                    return self.encryption.decrypt_data(encrypted_data)
            
            raise FileNotFoundError(f"Backup {backup_id} not found in any storage")
        except Exception as e:
            logger.error(f"Failed to retrieve backup {backup_id}: {str(e)}")
            raise
            
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups with metadata."""
        backups = []
        
        # List local backups
        try:
            for filename in os.listdir(self.local_backup_dir):
                file_path = os.path.join(self.local_backup_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    backups.append({
                        'id': filename,
                        'timestamp': get_backup_date(filename),
                        'size': stat.st_size,
                        'location': 'local'
                    })
        except Exception as e:
            logger.error(f"Error listing local backups: {str(e)}")
            
        # TODO: If remote storage is enabled, list remote backups too
        
        return backups
    
    def prune_expired_backups(self) -> int:
        """Remove backups that have exceeded the retention period."""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            pruned_count = 0
            
            # Prune local backups
            for filename in os.listdir(self.local_backup_dir):
                file_path = os.path.join(self.local_backup_dir, filename)
                if os.path.isfile(file_path):
                    file_date = get_backup_date(filename)
                    if file_date and file_date < cutoff_date:
                        os.remove(file_path)
                        pruned_count += 1
                        logger.info(f"Pruned expired backup: {filename}")
                        
            # TODO: Prune remote backups if enabled
            
            return pruned_count
        except Exception as e:
            logger.error(f"Error during backup pruning: {str(e)}")
            raise
            
    def _store_remote(self, backup_name: str, encrypted_data: bytes) -> None:
        """Store backup to remote storage (placeholder for implementation)."""
        # This would contain the actual remote storage logic
        # For example, uploading to S3, Google Cloud Storage, etc.
        pass
    
    def _retrieve_remote(self, backup_id: str) -> Optional[bytes]:
        """Retrieve backup from remote storage (placeholder for implementation)."""
        # This would contain the actual remote retrieval logic
        return None