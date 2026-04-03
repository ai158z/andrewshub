import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.wallet_backup.storage import BackupStorage


@pytest.fixture
def backup_storage():
    return BackupStorage()


@pytest.fixture
def test_backup_data():
    return {
        'wallet_id': 'test_wallet_123',
        'backup_content': 'encrypted_backup_data',
        'timestamp': '2023-01-01T12:00:00Z'
    }


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._save_backup')
def test_store_backup(mock_save, mock_load_config, backup_storage, test_backup_data):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 5
    }
    
    backup_id = backup_storage.store_backup(test_backup_data)
    
    assert backup_id is not None
    mock_save.assert_called_once()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._read_backup_file')
def test_retrieve_backup(mock_read, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups'
    }
    test_data = {'wallet_id': 'test_wallet_123', 'backup_content': 'data'}
    mock_read.return_value = test_data
    
    result = backup_storage.retrieve_backup('test_backup_id')
    
    mock_read.assert_called_once_with('test_backup_id')
    assert result == test_data


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('os.listdir')
@patch('os.path.getmtime')
@patch('os.remove')
def test_prune_expired_backups(mock_remove, mock_getmtime, mock_listdir, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 3
    }
    mock_listdir.return_value = ['backup_1', 'backup_2', 'backup_3', 'backup_4']
    mock_getmtime.side_effect = [
        (datetime.now() - timedelta(days=5)).timestamp(),
        (datetime.now() - timedelta(days=4)).timestamp(),
        (datetime.now() - timedelta(days=2)).timestamp(),
        (datetime.now() - timedelta(days=1)).timestamp()
    ]
    
    backup_storage.prune_expired_backups()
    
    assert mock_getmtime.call_count == 4
    assert mock_remove.call_count == 2


@patch('src.wallet_backup.storage.BackupStorage._load_config')
def test_store_backup_config_error(mock_load_config, backup_storage, test_backup_data):
    mock_load_config.side_effect = Exception("Config load failed")
    
    with pytest.raises(Exception):
        backup_storage.store_backup(test_backup_data)


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._save_backup')
def test_store_backup_save_error(mock_save, mock_load_config, backup_storage, test_backup_data):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 5
    }
    mock_save.side_effect = Exception("Save failed")
    
    with pytest.raises(Exception):
        backup_storage.store_backup(test_backup_data)


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._read_backup_file')
def test_retrieve_backup_file_error(mock_read, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups'
    }
    mock_read.side_effect = Exception("File read error")
    
    with pytest.raises(Exception):
        backup_storage.retrieve_backup('test_backup_id')


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('os.listdir')
def test_prune_expired_backups_listdir_error(mock_listdir, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 3
    }
    mock_listdir.side_effect = OSError("Cannot list directory")
    
    with pytest.raises(OSError):
        backup_storage.prune_expired_backups()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._save_backup')
def test_store_backup_empty_data(mock_save, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 5
    }
    
    empty_data = {}
    backup_id = backup_storage.store_backup(empty_data)
    
    assert backup_id is not None
    mock_save.assert_called_once()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._read_backup_file')
def test_retrieve_backup_not_found(mock_read, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups'
    }
    mock_read.return_value = None
    
    result = backup_storage.retrieve_backup('nonexistent_backup_id')
    
    assert result is None
    mock_read.assert_called_once_with('nonexistent_backup_id')


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('os.listdir')
@patch('os.path.getmtime')
def test_prune_expired_backups_no_files(mock_getmtime, mock_listdir, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 3
    }
    mock_listdir.return_value = []
    
    backup_storage.prune_expired_backups()
    
    mock_getmtime.assert_not_called()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('os.listdir')
@patch('os.path.getmtime')
@patch('os.remove')
def test_prune_expired_backups_all_valid(mock_remove, mock_getmtime, mock_listdir, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 5
    }
    mock_listdir.return_value = ['backup_1', 'backup_2', 'backup_3']
    mock_getmtime.side_effect = [
        (datetime.now() - timedelta(days=2)).timestamp(),
        (datetime.now() - timedelta(days=1)).timestamp(),
        (datetime.now() - timedelta(hours=12)).timestamp()
    ]
    
    backup_storage.prune_expired_backups()
    
    mock_remove.assert_not_called()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._save_backup')
def test_store_backup_max_backups_reached(mock_save, mock_load_config, backup_storage, test_backup_data):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 0
    }
    
    backup_id = backup_storage.store_backup(test_backup_data)
    
    assert backup_id is not None
    mock_save.assert_called_once()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._read_backup_file')
def test_retrieve_backup_invalid_id(mock_read, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups'
    }
    mock_read.return_value = None
    
    result = backup_storage.retrieve_backup(None)
    
    mock_read.assert_called_once_with(None)
    assert result is None


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('os.listdir')
@patch('os.path.getmtime')
@patch('os.remove')
def test_prune_expired_backups_removal_error(mock_remove, mock_getmtime, mock_listdir, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 2
    }
    mock_listdir.return_value = ['backup_1', 'backup_2', 'backup_3', 'backup_4']
    mock_getmtime.side_effect = [
        (datetime.now() - timedelta(days=5)).timestamp(),
        (datetime.now() - timedelta(days=4)).timestamp(),
        (datetime.now() - timedelta(days=2)).timestamp(),
        (datetime.now() - timedelta(days=1)).timestamp()
    ]
    mock_remove.side_effect = OSError("Permission denied")
    
    with pytest.raises(OSError):
        backup_storage.prune_expired_backups()


@patch('src.wallet_backup.storage.BackupStorage._load_config')
@patch('src.wallet_backup.storage.BackupStorage._save_backup')
def test_store_backup_large_data(mock_save, mock_load_config, backup_storage):
    mock_load_config.return_value = {
        'backup_location': '/tmp/backups',
        'max_backups': 5
    }
    
    large_data = {'wallet_id': 'large_wallet', 'backup_content': 'x' * 10000, 'timestamp': '2023-01-01T12:00:00Z'}
    backup_id = backup_storage.store_backup(large_data)
    
    assert backup_id is not None
    mock_save.assert_called_once()