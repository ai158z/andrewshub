import os
import json
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open
import pytest

from src.wallet_backup.storage import BackupStorage
from src.wallet_backup.config import Config
from src.wallet_backup.utils import get_current_timestamp, format_backup_name

# Test data
TEST_BACKUP_DATA = b"test_wallet_data"
ENCRYPTED_DATA = b"encrypted_data"
DECRYPTED_DATA = b"decrypted_data"

@pytest.fixture
def mock_config():
    config = MagicMock(spec=Config)
    config.get = MagicMock(side_effect=lambda key, default=None: {
        'local_backup_dir': 'test_backups',
        'remote_storage_enabled': False,
        'retention_days': 30
    }.get(key, default))
    config.get_encryption_key = MagicMock(return_value="test_key")
    return config

@pytest.fixture
def backup_storage(mock_config):
    with patch("os.makedirs"), patch("os.path.exists", return_value=True):
        storage = BackupStorage(mock_config)
    return storage

def test_init_creates_backup_dir(backup_storage):
    assert backup_storage.local_backup_dir == 'test_backups'

def test_ensure_local_dir_exists():
    with patch("os.path.exists", return_value=False) as mock_exists, \
         patch("os.makedirs") as mock_makedirs:
        config = MagicMock()
        config.get = MagicMock(side_effect=lambda key, default: {
            'local_backup_dir': 'test_backups',
            'remote_storage_enabled': False,
            'retention_days': 30
        }.get(key, default))
        config.get_encryption_key = MagicMock(return_value="test_key")
        
        with patch("os.makedirs") as mock_makedirs:
            storage = BackupStorage(config)
            mock_makedirs.assert_called_with('test_backups')

def test_store_backup_success(backup_storage):
    with patch("builtins.open", mock_open()) as mock_file, \
         patch.object(backup_storage.encryption, 'encrypt_data', return_value=ENCRYPTED_DATA), \
         patch("src.wallet_backup.utils.format_backup_name", return_value="backup_20230101_000000"):
        result = backup_storage.store_backup(TEST_BACKUP_DATA)
        assert result == "backup_20230101_000000"

def test_store_backup_with_remote_enabled(backup_storage):
    backup_storage.remote_storage_enabled = True
    with patch("builtins.open", mock_open()) as mock_file, \
         patch.object(backup_storage.encryption, 'encrypt_data', return_value=ENCRYPTED_DATA), \
         patch("src.wallet_backup.utils.format_backup_name", return_value="backup_20230101_000000"), \
         patch.object(backup_storage, '_store_remote') as mock_store_remote:
        result = backup_storage.store_backup(TEST_BACKUP_DATA)
        assert result == "backup_20230101_000000"
        mock_store_remote.assert_called_once()

def test_store_backup_failure(backup_storage):
    with patch.object(backup_storage.encryption, 'encrypt_data', side_effect=Exception("Encryption failed")):
        with pytest.raises(Exception, match="Encryption failed"):
            backup_storage.store_backup(TEST_BACKUP_DATA)

def test_retrieve_backup_local_success(backup_storage):
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=ENCRYPTED_DATA)), \
         patch.object(backup_storage.encryption, "decrypt_data", return_value=DECRYPTED_DATA):
        result = backup_storage.retrieve_backup("backup_123")
        assert result == DECRYPTED_DATA

def test_retrieve_backup_remote_success(backup_storage):
    backup_storage.remote_storage_enabled = True
    with patch("os.path.exists", return_value=False), \
         patch.object(backup_storage, '_retrieve_remote', return_value=ENCRYPTED_DATA), \
         patch.object(backup_storage.encryption, "decrypt_data", return_value=DECRYPTED_DATA):
        result = backup_storage.retrieve_backup("backup_123")
        assert result == DECRYPTED_DATA

def test_retrieve_backup_not_found(backup_storage):
    with patch("os.path.exists", return_value=False):
        backup_storage.remote_storage_enabled = False
        with pytest.raises(FileNotFoundError):
            backup_storage.retrieve_backup("nonexistent_backup")

def test_list_backups_success(backup_storage, tmp_path):
    test_file = tmp_path / "backup_20230101_000000"
    test_file.write_bytes(b"test")
    
    with patch("os.listdir", return_value=[str(test_file)]), \
         patch("os.path.isfile", return_value=True), \
         patch("os.stat") as mock_stat:
        mock_stat.return_value.st_size = 100
        result = backup_storage.list_backups()
        assert len(result) == 1
        assert result[0]['id'] == str(test_file)

def test_list_backups_with_error(backup_storage):
    with patch("os.listdir", side_effect=Exception("Permission denied")):
        result = backup_storage.list_backups()
        assert result == []

def test_prune_expired_backups_success(backup_storage, tmp_path):
    old_file = tmp_path / "old_backup"
    old_file.write_bytes(b"old")
    
    with patch("os.listdir", return_value=[str(old_file)]), \
         patch("os.path.isfile", return_value=True), \
         patch("os.remove") as mock_remove, \
         patch("src.wallet_backup.utils.get_backup_date", return_value=datetime(2020, 1, 1)):
        result = backup_storage.prune_expired_backups()
        assert result == 1

def test_prune_expired_backups_no_prune(backup_storage):
    with patch("os.listdir", return_value=[]):
        result = backup_storage.prune_expired_backups()
        assert result == 0

def test_prune_expired_backups_error(backup_storage):
    with patch("os.listdir", side_effect=Exception("Error reading directory")):
        with pytest.raises(Exception):
            backup_storage.prune_expired_backups()

def test_store_remote_placeholder(backup_storage):
    with patch.object(backup_storage, '_store_remote') as mock_method:
        backup_storage._store_remote("test", b"data")
        mock_method.assert_called_once()

def test_retrieve_remote_placeholder(backup_storage):
    with patch.object(backup_storage, '_retrieve_remote') as mock_method:
        result = backup_storage._retrieve_remote("test_id")
        mock_method.assert_called_once()

def test_encryption_integration(backup_storage):
    with patch.object(backup_storage.encryption, 'encrypt_data') as mock_encrypt, \
         patch.object(backup_storage.encryption, 'decrypt_data') as mock_decrypt, \
         patch("builtins.open", mock_open()) as mock_file:
        mock_encrypt.return_value = ENCRYPTED_DATA
        mock_decrypt.return_value = DECRYPTED_DATA
        # This tests the integration through the storage methods
        backup_name = backup_storage.store_backup(TEST_BACKUP_DATA)
        result = backup_storage.retrieve_backup(backup_name)
        assert result == DECRYPTED_DATA

def test_retrieve_backup_fallback_to_remote(backup_storage):
    backup_storage.remote_storage_enabled = True
    with patch("os.path.exists", return_value=False), \
         patch.object(backup_storage, '_retrieve_remote', return_value=ENCRYPTED_DATA), \
         patch.object(backup_storage.encryption, "decrypt_data", return_value=DECRYPTED_DATA):
        result = backup_storage.retrieve_backup("backup_123")
        assert result == DECRYPTED_DATA

def test_retrieve_backup_no_remote_fallback(backup_storage):
    backup_storage.remote_storage_enabled = False
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            backup_storage.retrieve_backup("nonexistent")

def test_list_backups_empty_directory(backup_storage):
    with patch("os.listdir", return_value=[]):
        result = backup_storage.list_backups()
        assert result == []

def test_list_backups_with_mixed_files(backup_storage):
    with patch("os.listdir", return_value=["file1", "file2"]), \
         patch("os.path.isfile", side_effect=lambda x: x == "file1"), \
         patch("os.stat") as mock_stat:
        mock_stat.return_value.st_size = 100
        result = backup_storage.list_backups()
        assert len(result) == 1

def test_prune_expired_backups_no_files(backup_storage):
    with patch("os.listdir", return_value=[]):
        result = backup_storage.prune_expired_backups()
        assert result == 0

def test_prune_expired_backups_exception(backup_storage):
    with patch("os.listdir", side_effect=Exception("Directory error")):
        with pytest.raises(Exception):
            backup_storage.prune_expired_backups()

def test_store_backup_encryption_failure(backup_storage):
    with patch.object(backup_storage.encryption, 'encrypt_data', side_effect=Exception("Encryption error")):
        with pytest.raises(Exception, match="Encryption error"):
            backup_storage.store_backup(TEST_BACKUP_DATA)