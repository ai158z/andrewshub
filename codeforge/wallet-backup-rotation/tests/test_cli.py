import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.wallet_backup.cli import main, backup_command, restore_command, schedule_command

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_config():
    with patch('src.wallet_backup.cli.Config') as mock:
        config_instance = MagicMock()
        config_instance.get_moonpay_api_key.return_value = 'test_api_key'
        config_instance.get_encryption_key.return_value = 'test_enc_key'
        mock.return_value = config_instance
        yield mock

@pytest.fixture
def mock_backup_manager():
    with patch('src.wallet_backup.cli.WalletBackupManager') as mock:
        yield mock

@pytest.fixture
def mock_scheduler():
    with patch('src.wallet_backup.cli.BackupScheduler') as mock:
        yield mock

def test_backup_command_success(runner, mock_config, mock_backup_manager):
    result = runner.invoke(main, ['backup', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Backup created successfully' in result.output
    mock_backup_manager.return_value.create_backup.assert_called_once()

def test_backup_command_with_custom_name(runner, mock_config, mock_backup_manager):
    result = runner.invoke(main, ['backup', '-w', 'wallet123', '-n', 'my_backup'])
    assert result.exit_code == 0
    mock_backup_manager.return_value.create_backup.assert_called_once_with('wallet123', 'my_backup')

def test_backup_command_error(runner, mock_config, mock_backup_manager):
    mock_backup_manager.return_value.create_backup.side_effect = Exception('Backup failed')
    result = runner.invoke(main, ['backup', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Error creating backup' in result.output

def test_restore_command_success(runner, mock_config, mock_backup_manager):
    result = runner.invoke(main, ['restore', '-b', 'backup123'])
    assert result.exit_code == 0
    assert 'Backup backup123 restored successfully' in result.output
    mock_backup_manager.return_value.restore_backup.assert_called_once_with('backup123')

def test_restore_command_error(runner, mock_config, mock_backup_manager):
    mock_backup_manager.return_value.restore_backup.side_effect = Exception('Restore failed')
    result = runner.invoke(main, ['restore', '-b', 'backup123'])
    assert result.exit_code == 0
    assert 'Error restoring backup' in result.output

def test_schedule_command_daily(runner, mock_config, mock_scheduler):
    result = runner.invoke(main, ['schedule', '-s', 'daily', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Daily backup scheduled successfully' in result.output
    mock_scheduler.return_value.schedule_daily_backup.assert_called_once_with('wallet123')

def test_schedule_command_monthly(runner, mock_config, mock_scheduler):
    result = runner.invoke(main, ['schedule', '-s', 'monthly', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Monthly backup scheduled successfully' in result.output
    mock_scheduler.return_value.schedule_monthly_backup.assert_called_once_with('wallet123')

def test_schedule_command_error(runner, mock_config, mock_scheduler):
    mock_scheduler.return_value.schedule_daily_backup.side_effect = Exception('Scheduling failed')
    result = runner.invoke(main, ['schedule', '-s', 'daily', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Error scheduling backup' in result.output

def test_backup_command_missing_wallet_id(runner):
    result = runner.invoke(main, ['backup'])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

def test_restore_command_missing_backup_id(runner):
    result = runner.invoke(main, ['restore'])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

def test_schedule_command_missing_schedule(runner):
    result = runner.invoke(main, ['schedule', '-w', 'wallet123'])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

def test_schedule_command_missing_wallet_id(runner):
    result = runner.invoke(main, ['schedule', '-s', 'daily'])
    assert result.exit_code != 0
    assert 'Missing option' in result.output

def test_main_command_help(runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Wallet Backup CLI' in result.output

def test_backup_command_help(runner):
    result = runner.invoke(main, ['backup', '--help'])
    assert result.exit_code == 0
    assert 'Create a backup of a wallet' in result.output

def test_restore_command_help(runner):
    result = runner.invoke(main, ['restore', '--help'])
    assert result.exit_code == 0
    assert 'Restore a wallet from backup' in result.output

def test_schedule_command_help(runner):
    result = runner.invoke(main, ['schedule', '--help'])
    assert result.exit_code == 0
    assert 'Schedule automatic backups' in result.output

def test_invalid_schedule_option(runner):
    result = runner.invoke(main, ['schedule', '-s', 'weekly', '-w', 'wallet123'])
    assert result.exit_code != 0
    assert 'Invalid value' in result.output

def test_backup_command_encryption_key_error(runner, mock_config):
    mock_config.return_value.get_encryption_key.side_effect = Exception('Config error')
    result = runner.invoke(main, ['backup', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Error creating backup' in result.output

def test_restore_command_encryption_key_error(runner, mock_config):
    mock_config.return_value.get_encryption_key.side_effect = Exception('Config error')
    result = runner.invoke(main, ['restore', '-b', 'backup123'])
    assert result.exit_code == 0
    assert 'Error restoring backup' in result.output

def test_schedule_command_encryption_key_error(runner, mock_config):
    mock_config.return_value.get_encryption_key.side_effect = Exception('Config error')
    result = runner.invoke(main, ['schedule', '-s', 'daily', '-w', 'wallet123'])
    assert result.exit_code == 0
    assert 'Error scheduling backup' in result.output