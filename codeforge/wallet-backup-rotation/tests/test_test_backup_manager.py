import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.wallet_backup.backup_manager import WalletBackupManager
from src.wallet_backup.storage import BackupStorage
from src.wallet_backup.encryption import WalletEncryption

@pytest.fixture
def temp_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)

@pytest.fixture
def backup_manager():
    return WalletBackupManager()

def test_wallet_backup_manager_initialization():
    manager = WalletBackupManager()
    assert manager is not None
    assert hasattr(manager, 'storage')
    assert hasattr(manager, 'encryption')

@patch('src.wallet_backup.moonpay_client.MoonPayClient')
@patch('src.wallet_backup.encryption.WalletEncryption')
@patch('src.wallet_backup.storage.BackupStorage')
def test_create_backup(mock_moonpay, mock_encryption, mock_storage):
    mock_moonpay.return_value.get_wallet_data.return_value = b'wallet_data'
    mock_encryption.return_value.encrypt_data.return_value = b'encrypted_data'
    mock_storage.return_value.store_backup.return_value = 'backup_id'
    
    backup_manager = WalletBackupManager()
    result = backup_manager.create_backup("test_wallet_id")
    
    assert result is not None
    assert isinstance(result, str)

def test_create_backup_with_real_setup(temp_dir):
    backup_manager = WalletBackupManager()
    backup_manager.storage = BackupStorage(temp_dir)
    backup_manager.encryption = WalletEncryption("test_key_32bytes"[:32])
    
    with patch('src.wallet_backup.moonpay_client.MoonPayClient') as mock_moonpay:
        mock_moonpay.return_value.get_wallet_data.return_value = b'wallet_data'
        result = backup_manager.create_backup("test_wallet_id")
        assert isinstance(result, str)

def test_prune_backups_removes_old_files(temp_dir):
    # Create test files
    test_files = []
    for i in range(5):
        test_file = os.path.join(temp_dir, f"backup_{i}.dat")
        with open(test_file, 'w') as f:
            f.write("test")
        test_files.append(test_file)
    
    # Make some files appear old
    one_week_ago = datetime.now() - timedelta(weeks=1)
    for test_file in test_files[:3]:
        os.utime(test_file, (one_week_ago.timestamp(), one_week_ago.timestamp()))
    
    storage = BackupStorage(temp_dir)
    storage.prune_expired_backups(2)
    
    # Should have 2 backups remaining
    files = [f for f in os.listdir(temp_dir) if f.startswith('backup_')]
    assert len(files) == 2

def test_rotate_backups_keeps_correct_number(temp_dir):
    # Create 10 backup files
    for i in range(10):
        test_file = os.path.join(temp_dir, f"backup_{i}.dat")
        with open(test_file, 'w') as f:
            f.write("test")
    
    backup_manager = WalletBackupManager()
    backup_manager.storage = BackupStorage(temp_dir)
    backup_manager.rotate_backups(3)
    
    files = [f for f in os.listdir(temp_dir) if f.startswith('backup_')]
    assert len(files) == 3

def test_rotate_backups_with_empty_directory(temp_dir):
    backup_manager = WalletBackupManager()
    backup_manager.storage = BackupStorage(temp_dir)
    backup_manager.rotate_backups(3)
    
    # No files to rotate, should not error
    files = os.listdir(temp_dir)
    assert len(files) == 0

def test_prune_backups_keeps_newest(temp_dir):
    # Create test files
    for i in range(5):
        test_file = os.path.join(temp_dir, f"backup_{i}.dat")
        with open(test_file, 'w') as f:
            f.write("test")
    
    # Create storage and test pruning
    storage = BackupStorage(temp_dir)
    storage.prune_expired_backups(2)
    
    # Should have 2 backups remaining
    files = [f for f in os.listdir(temp_dir) if f.startswith('backup_')]
    assert len(files) == 2

def test_create_backup_with_encryption():
    backup_manager = WalletBackupManager()
    
    with patch.object(backup_manager, 'moonpay_client') as mock_client, \
         patch.object(backup_manager, 'encryption') as mock_encrypt, \
         patch.object(backup_manager, 'storage') as mock_storage:
        
        mock_client.get_wallet_data.return_value = b'wallet_data'
        mock_encrypt.encrypt_data.return_value = b'encrypted_data'
        mock_storage.store_backup.return_value = 'backup_id_123'
        
        result = backup_manager.create_backup("wallet_123")
        assert result == 'backup_id_123'

def test_create_backup_handles_moonpay_failure():
    backup_manager = WalletBackupManager()
    
    with patch.object(backup_manager, 'moonpay_client') as mock_client:
        mock_client.get_wallet_data.side_effect = Exception("MoonPay API error")
        
        with pytest.raises(Exception, match="MoonPay API error"):
            backup_manager.create_backup("wallet_123")

def test_create_backup_handles_encryption_failure():
    backup_manager = WalletBackupManager()
    
    with patch.object(backup_manager, 'moonpay_client') as mock_client, \
         patch.object(backup_manager, 'encryption') as mock_encrypt:
        
        mock_client.get_wallet_data.return_value = b'wallet_data'
        mock_encrypt.encrypt_data.side_effect = Exception("Encryption error")
        
        with pytest.raises(Exception, match="Encryption error"):
            backup_manager.create_backup("wallet_123")

def test_create_backup_handles_storage_failure():
    backup_manager = WalletBackupManager()
    
    with patch.object(backup_manager, 'moonpay_client') as mock_client, \
         patch.object(backup_manager, 'encryption') as mock_encrypt, \
         patch.object(backup_manager, 'storage') as mock_storage:
        
        mock_client.get_wallet_data.return_value = b'wallet_data'
        mock_encrypt.encrypt_data.return_value = b'encrypted_data'
        mock_storage.store_backup.side_effect = Exception("Storage error")
        
        with pytest.raises(Exception, match="Storage error"):
            backup_manager.create_backup("wallet_123")

def test_prune_backups_no_files_to_prune(temp_dir):
    storage = BackupStorage(temp_dir)
    # When no backup files exist, should not error
    storage.prune_expired_backups(2)
    files = os.listdir(temp_dir)
    assert len(files) == 0

def test_rotate_backups_no_backups_exist(temp_dir):
    backup_manager = WalletBackupManager()
    backup_manager.storage = BackupStorage(temp_dir)
    # Should not error when no files exist
    backup_manager.rotate_backups(3)
    files = os.listdir(temp_dir)
    assert len(files) == 0

def test_rotate_backups_fewer_files_than_requested(temp_dir):
    # Create only 2 files but request to keep 5
    for i in range(2):
        test_file = os.path.join(temp_dir, f"backup_{i}.dat")
        with open(test_file, 'w') as f:
            f.write("test")
    
    backup_manager = WalletBackupManager()
    backup_manager.storage = BackupStorage(temp_dir)
    backup_manager.rotate_backups(5)
    
    # Should keep the 2 files we have
    files = [f for f in os.listdir(temp_dir) if f.startswith('backup_')]
    assert len(files) == 2

def test_prune_backups_mixed_file_ages(temp_dir):
    # Create files with mixed ages
    for i in range(5):
        test_file = os.path.join(temp_dir, f"backup_{i}.dat")
        with open(test_file, 'w') as f:
            f.write("test")
    
    # Make some files old
    one_week_ago = datetime.now() - timedelta(weeks=1)
    files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.startswith('backup_')]
    for f in files[:3]:
        os.utime(f, (one_week_ago.timestamp(), one_week_ago.timestamp()))
    
    storage = BackupStorage(temp_dir)
    storage.prune_expired_backups(2)
    
    # Should keep 2 most recent files
    remaining_files = [f for f in os.listdir(temp_dir) if f.startswith('backup_')]
    assert len(remaining_files) == 2

def test_create_backup_empty_wallet_id():
    backup_manager = WalletBackupManager()
    
    with patch.object(backup_manager, 'moonpay_client') as mock_client, \
         patch.object(backup_manager, 'encryption') as mock_encrypt, \
         patch.object(backup_manager, 'storage') as mock_storage:
        
        mock_client.get_wallet_data.return_value = b''
        mock_encrypt.encrypt_data.return_value = b'encrypted_data'
        mock_storage.store_backup.return_value = 'backup_id'
        
        result = backup_manager.create_backup("")
        assert result is not None

def test_create_backup_none_wallet_id():
    backup_manager = WalletBackupManager()
    
    with patch.object(backup_manager, 'moonpay_client') as mock_client, \
         patch.object(backup_manager, 'encryption') as mock_encrypt, \
         patch.object(backup_manager, 'storage') as mock_storage:
        
        mock_client.get_wallet_data.return_value = None
        mock_encrypt.encrypt_data.return_value = b'encrypted_data'
        mock_storage.store_backup.return_value = 'backup_id'
        
        result = backup_manager.create_backup(None)
        assert result is not None

def test_rotate_backups_zero_keep():
    temp_dir = tempfile.mkdtemp()
    try:
        # Create some backup files
        for i in range(3):
            test_file = os.path.join(temp_dir, f"backup_{i}.dat")
            with open(test_file, 'w') as f:
                f.write("test")
        
        backup_manager = WalletBackupManager()
        backup_manager.storage = BackupStorage(temp_dir)
        backup_manager.rotate_backups(0)
        
        # Should keep 0 files (delete all)
        files = [f for f in os.listdir(temp_dir) if f.startswith('backup_')]
        assert len(files) == 0
    finally:
        shutil.rmtree(temp_dir)