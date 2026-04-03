import logging
from typing import List, Optional
from src.wallet_backup.storage import BackupStorage
from src.wallet_backup.moonpay_client import MoonPayClient
from src.wallet_backup.config import Config
from src.wallet_backup.utils import get_current_timestamp, format_backup_name, verify_backup_integrity


class WalletBackupManager:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.storage = BackupStorage()
        self.moonpay_client = MoonPayClient(config.get_moonpay_api_key())
        
    def create_backup(self, wallet_id: Optional[str] = None) -> str:
        """
        Create a backup for a specific wallet or all wallets.
        
        Args:
            wallet_id: Optional wallet ID to backup. If None, backup all wallets.
            
        Returns:
            Backup ID of the created backup
        """
        try:
            timestamp = get_current_timestamp()
            backup_name = format_backup_name(timestamp)
            
            if wallet_id:
                wallets_data = self.moonpay_client.get_wallet_data(wallet_id)
                backup_data = {wallet_id: wallets_data}
            else:
                # Backup all wallets
                wallet_list = self.moonpay_client.list_wallets()
                backup_data = {}
                for wallet in wallet_list:
                    wallet_id = wallet.get('id')
                    if wallet_id:
                        backup_data[wallet_id] = self.moonpay_client.get_wallet_data(wallet_id)
            
            # Store the backup
            backup_id = self.storage.store_backup(backup_name, backup_data)
            
            self.logger.info(f"Backup created successfully: {backup_id}")
            return backup_id
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            raise
    
    def prune_backups(self, max_age_days: int = 30) -> List[str]:
        """
        Remove backups older than max_age_days.
        
        Args:
            max_age_days: Maximum age of backups in days
            
        Returns:
            List of pruned backup IDs
        """
        try:
            pruned_backups = self.storage.prune_expired_backups(max_age_days)
            self.logger.info(f"Pruned {len(pruned_backups)} backups")
            return pruned_backups
        except Exception as e:
            self.logger.error(f"Failed to prune backups: {str(e)}")
            raise
    
    def rotate_backups(self, max_backups: int = 10) -> List[str]:
        """
        Keep only the most recent max_backups and remove older ones.
        
        Args:
            max_backups: Maximum number of backups to keep
            
        Returns:
            List of rotated out backup IDs
        """
        try:
            backups = self.storage.list_backups()
            
            # Sort backups by date (newest first)
            backups.sort(key=lambda x: x['date'], reverse=True)
            
            # If we have more backups than allowed, remove the oldest ones
            if len(backups) > max_backups:
                to_remove = backups[max_backups:]
                removed_ids = []
                
                for backup in to_remove:
                    backup_id = backup['id']
                    self.storage.delete_backup(backup_id)
                    removed_ids.append(backup_id)
                    
                self.logger.info(f"Rotated out {len(removed_ids)} backups")
                return removed_ids
            else:
                self.logger.info("No backups to rotate")
                return []
                
        except Exception as e:
            self.logger.error(f"Failed to rotate backups: {str(e)}")
            raise
    
    def restore_backup(self, backup_id: str, target_wallet_id: Optional[str] = None) -> bool:
        """
        Restore a backup to a wallet or wallets.
        
        Args:
            backup_id: ID of the backup to restore
            target_wallet_id: Optional specific wallet ID to restore to
            
        Returns:
            True if restoration was successful
        """
        try:
            # Retrieve the backup
            backup_data = self.storage.retrieve_backup(backup_id)
            
            # Verify integrity
            if not verify_backup_integrity(backup_data, backup_id):
                raise ValueError("Backup integrity check failed")
            
            # Restore to target wallet(s)
            if target_wallet_id:
                if target_wallet_id in backup_data:
                    self.moonpay_client.restore_wallet_data(target_wallet_id, backup_data[target_wallet_id])
                else:
                    raise ValueError(f"Wallet {target_wallet_id} not found in backup")
            else:
                # Restore all wallets in backup
                for wallet_id, wallet_data in backup_data.items():
                    self.moonpay_client.restore_wallet_data(wallet_id, wallet_data)
            
            self.logger.info(f"Backup {backup_id} restored successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup {backup_id}: {str(e)}")
            raise