import pytest
from unittest.mock import Mock, patch, MagicMock
from src.wallet_backup.backup_manager import WalletBackupManager
from src.wallet_backup.config import Config

@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.get_encryption_key.return_value = "test-key"
    config.get_moonpay_api_key.return_value = "test-moonpay-key"
    return config

@pytest.fixture
def backup_manager(mock_config):
    with patch('src.wallet_backup.backup_manager.WalletEncryption') as mock_encryption, \
         patch('src.wallet_backup.backup_manager.BackupStorage') as mock_storage, \
         patch('src.wallet_backup.backup_manager.MoonPayClient') as mock_moonpay:
        manager = WalletBackupManager(mock_config)
        manager.encryption = mock_encryption.return_value
        manager.storage = mock_storage.return_value
        manager.moonpay_client = mock_moonpay.return_value
        return manager

def test_create_backup_all_wallets(backup_manager):
    backup_manager.moonpay_client.list_wallets.return_value = [
        {'id': 'wallet1'}, {'id': 'wallet2'}
    ]
    backup_manager.moonpay_client.get_wallet_data.side_effect = [
        'data1', 'data2'
    ]
    backup_manager.encryption.encrypt_data.return_value = "encrypted_data"
    backup_manager.storage.store_backup.return_value = "backup_123"
    
    result = backup_manager.create_backup()
    
    assert result == "backup_123"
    backup_manager.moonpay_client.list_wallets.assert_called_once()
    backup_manager.moonpay_client.get_wallet_data.assert_any_call('wallet1')
    backup_manager.moonpay_client.get_wallet_data.assert_any_call('wallet2')
    backup_manager.encryption.encrypt_data.assert_called_once()
    backup_manager.storage.store_backup.assert_called_once()

def test_create_backup_specific_wallet(backup_manager):
    backup_manager.moonpay_client.get_wallet_data.return_value = "wallet_data"
    backup_manager.encryption.encrypt_data.return_value = "encrypted_data"
    backup_manager.storage.store_backup.return_value = "backup_123"
    
    result = backup_manager.create_backup("wallet123")
    
    assert result == "backup_123"
    backup_manager.moonpay_client.get_wallet_data.assert_called_once_with("wallet123")
    backup_manager.encryption.encrypt_data.assert_called_once()
    backup_manager.storage.store_backup.assert_called_once()

def test_create_backup_failure(backup_manager):
    backup_manager.moonpay_client.list_wallets.side_effect = Exception("API Error")
    
    with pytest.raises(Exception, match="API Error"):
        backup_manager.create_backup()

def test_prune_backups_success(backup_manager):
    backup_manager.storage.prune_expired_backups.return_value = ["backup1", "backup2"]
    
    result = backup_manager.prune_backups(15)
    
    assert result == ["backup1", "backup2"]
    backup_manager.storage.prune_expired_backups.assert_called_once_with(15)

def test_prune_backups_failure(backup_manager):
    backup_manager.storage.prune_expired_backups.side_effect = Exception("Storage Error")
    
    with pytest.raises(Exception, match="Storage Error"):
        backup_manager.prune_backups()

def test_rotate_backups_no_action(backup_manager):
    backup_manager.storage.list_backups.return_value = [
        {'id': 'backup1', 'date': '2023-01-02'},
        {'id': 'backup2', 'date': '2023-01-01'}
    ]
    
    result = backup_manager.rotate_backups(5)
    
    assert result == []
    backup_manager.storage.list_backups.assert_called_once()
    backup_manager.storage.delete_backup.assert_not_called()

def test_rotate_backups_removes_old(backup_manager):
    backup_manager.storage.list_backups.return_value = [
        {'id': 'backup1', 'date': '2023-01-05'},
        {'id': 'backup2', 'date': '2023-01-04'},
        {'id': 'backup3', 'date': '2023-01-03'},
        {'id': 'backup4', 'date': '2023-01-02'},
        {'id': 'backup5', 'date': '2023-01-01'}
    ]
    backup_manager.storage.delete_backup.return_value = None
    
    result = backup_manager.rotate_backups(2)
    
    assert len(result) == 3
    assert "backup3" in result
    backup_manager.storage.list_backups.assert_called_once()

def test_restore_backup_all_wallets(backup_manager):
    encrypted_data = "encrypted_data"
    backup_data = {"wallet1": "data1", "wallet2": "data2"}
    
    backup_manager.storage.retrieve_backup.return_value = encrypted_data
    backup_manager.encryption.decrypt_data.return_value = backup_data
    with patch('src.wallet_backup.backup_manager.verify_backup_integrity', return_value=True):
        result = backup_manager.restore_backup("backup123")
        
        assert result == True
        backup_manager.storage.retrieve_backup.assert_called_once_with("backup123")
        backup_manager.encryption.decrypt_data.assert_called_once_with(encrypted_data)
        backup_manager.moonpay_client.restore_wallet_data.assert_any_call("wallet1", "data1")
        backup_manager.moonpay_client.restore_wallet_data.assert_any_call("wallet2", "data2")

def test_restore_backup_specific_wallet(backup_manager):
    encrypted_data = "encrypted_data"
    backup_data = {"wallet1": "data1", "wallet2": "data2"}
    
    backup_manager.storage.retrieve_backup.return_value = encrypted_data
    backup_manager.encryption.decrypt_data.return_value = backup_data
    with patch('src.wallet_backup.backup_manager.verify_backup_integrity', return_value=True):
        result = backup_manager.restore_backup("backup123", "wallet1")
        
        assert result == True
        backup_manager.moonpay_client.restore_wallet_data.assert_called_once_with("wallet1", "data1")

def test_restore_backup_integrity_failure(backup_manager):
    backup_manager.storage.retrieve_backup.return_value = "encrypted_data"
    backup_manager.encryption.decrypt_data.return_value = {}
    with patch('src.wallet_backup.backup_manager.verify_backup_integrity', return_value=False):
        with pytest.raises(ValueError, match="Backup integrity check failed"):
            backup_manager.restore_backup("backup123")

def test_restore_backup_wallet_not_found(backup_manager):
    backup_manager.storage.retrieve_backup.return_value = "encrypted_data"
    backup_manager.encryption.decrypt_data.return_value = {}
    with patch('src.wallet_backup.backup_manager.verify_backup_integrity', return_value=True):
        with pytest.raises(ValueError, match="wallet123 not found in backup"):
            backup_manager.restore_backup("backup123", "wallet123")

def test_restore_backup_encryption_error(backup_manager):
    backup_manager.storage.retrieve_backup.side_effect = Exception("Storage Error")
    
    with pytest.raises(Exception, match="Storage Error"):
        backup_manager.restore_backup("backup123")

def test_create_backup_encryption_error(backup_manager):
    backup_manager.encryption.encrypt_data.side_effect = Exception("Encryption Error")
    
    with pytest.raises(Exception, match="Encryption Error"):
        backup_manager.create_backup()

def test_prune_backups_storage_error(backup_manager):
    backup_manager.storage.prune_expired_backups.side_effect = Exception("Storage Error")
    
    with pytest.raises(Exception, match="Storage Error"):
        backup_manager.prune_backups()

def test_rotate_backups_storage_error(backup_manager):
    backup_manager.storage.list_backups.side_effect = Exception("Storage Error")
    
    with pytest.raises(Exception, match="Storage Error"):
        backup_manager.rotate_backups()