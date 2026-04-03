import click
import logging
from typing import Optional

from src.wallet_backup.backup_manager import WalletBackupManager
from src.wallet_backup.encryption import WalletEncryption
from src.wallet_backup.storage import BackupStorage
from src.wallet_backup.scheduler import BackupScheduler
from src.wallet_backup.moonpay_client import MoonPayClient
from src.wallet_backup.config import Config
from src.wallet_backup.utils import get_current_timestamp

logger = logging.getLogger(__name__)

@click.group()
@click.version_option()
def main() -> None:
    """Wallet Backup CLI - A tool for managing wallet backups with encryption and scheduling capabilities."""
    pass

@main.command()
@click.option('--wallet-id', '-w', help='Wallet ID to backup', required=True)
@click.option('--name', '-n', help='Custom name for the backup')
def backup_command(wallet_id: str, name: Optional[str] = None) -> None:
    """Create a backup of a wallet."""
    try:
        config = Config()
        moonpay_client = MoonPayClient(config.get_moonpay_api_key())
        encryption = WalletEncryption(config.get_encryption_key())
        storage = BackupStorage()
        backup_manager = WalletBackupManager(moonpay_client, encryption, storage)
        
        backup_name = name or f"backup_{wallet_id}_{get_current_timestamp()}"
        backup_manager.create_backup(wallet_id, backup_name)
        click.echo(f"Backup created successfully: {backup_name}")
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        click.echo(f"Error creating backup: {str(e)}", err=True)

@main.command()
@click.option('--backup-id', '-b', help='Backup ID to restore', required=True)
def restore_command(backup_id: str) -> None:
    """Restore a wallet from backup."""
    try:
        config = Config()
        moonpay_client = MoonPayClient(config.get_moonpay_api_key())
        encryption = WalletEncryption(config.get_encryption_key())
        storage = BackupStorage()
        backup_manager = WalletBackupManager(moonpay_client, encryption, storage)
        
        backup_manager.restore_backup(backup_id)
        click.echo(f"Backup {backup_id} restored successfully")
    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")
        click.echo(f"Error restoring backup: {str(e)}", err=True)

@main.command()
@click.option('--schedule', '-s', 
              type=click.Choice(['daily', 'monthly']), 
              help='Backup schedule type',
              required=True)
@click.option('--wallet-id', '-w', help='Wallet ID to backup', required=True)
def schedule_command(schedule: str, wallet_id: str) -> None:
        """Schedule automatic backups."""
    try:
        config = Config()
        moonpay_client = MoonPayClient(config.get_moonpay_api_key())
        encryption = WalletEncryption(config.get_encryption_key())
        storage = BackupStorage()
        scheduler = BackupScheduler()
        
        if schedule == 'daily':
            scheduler.schedule_daily_backup(wallet_id)
            click.echo("Daily backup scheduled successfully")
        elif schedule == 'monthly':
            scheduler.schedule_monthly_backup(wallet_id)
            click.echo("Monthly backup scheduled successfully")
    except Exception as e:
        logger.error(f"Scheduling failed: {str(e)}")
        click.echo(f"Error scheduling backup: {str(e)}", err=True)

if __name__ == '__main__':
    main()