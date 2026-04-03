import logging
from unittest.mock import Mock, patch, call
import schedule
from src.wallet_backup.scheduler import BackupScheduler

def test_init_with_config():
    config = Mock()
    scheduler = BackupScheduler(config)
    assert scheduler.config == config

def test_init_without_config():
    with patch("src.wallet_backup.scheduler.Config") as mock_config:
        mock_config.return_value = Mock()
        scheduler = BackupScheduler()
        mock_config.assert_called_once()

@patch("src.wallet_backup.scheduler.schedule")
def test_schedule_daily_backup_success(mock_schedule):
    scheduler = BackupScheduler()
    with patch.object(scheduler, "_run_daily_backup_job") as mock_job:
        scheduler.schedule_daily_backup()
        mock_schedule.every.return_value.day.at.assert_called_once_with("02:00")

@patch("src.wallet_backup.scheduler.schedule")
def test_schedule_daily_backup_exception(mock_schedule):
    mock_schedule.every.side_effect = Exception("Schedule error")
    scheduler = BackupScheduler()
    try:
        scheduler.schedule_daily_backup()
        assert False, "Expected exception was not raised"
    except Exception:
        pass

@patch("src.wallet_backup.scheduler.schedule")
def test_schedule_monthly_backup_success(mock_schedule):
    scheduler = BackupScheduler()
    scheduler.schedule_monthly_backup()
    mock_schedule.every.return_value.month.do.assert_called_once()

@patch("src.wallet_backup.scheduler.schedule")
def test_schedule_monthly_backup_exception(mock_schedule):
    mock_schedule.every.side_effect = Exception("Schedule error")
    scheduler = BackupScheduler()
    try:
        scheduler.schedule_monthly_backup()
        assert False, "Expected exception was not raised"
    except Exception:
        pass

@patch("src.wallet_backup.scheduler.schedule")
def test_run_pending_jobs_success(mock_schedule):
    mock_schedule.run_pending = Mock()
    scheduler = BackupScheduler()
    scheduler.run_pending_jobs()
    mock_schedule.run_pending.assert_called_once()

@patch("src.wallet_backup.scheduler.schedule")
def test_run_pending_jobs_exception(mock_schedule):
    mock_schedule.run_pending.side_effect = Exception("Run error")
    scheduler = BackupScheduler()
    try:
        scheduler.run_pending_jobs()
        assert False, "Expected exception was not raised"
    except Exception:
        pass

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_run_daily_backup_job_success(mock_backup_manager):
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    scheduler._run_daily_backup_job()
    mock_backup_manager.create_backup.assert_called_once()
    mock_backup_manager.rotate_backups.assert_called_once()

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_run_daily_backup_job_exception(mock_backup_manager):
    mock_backup_manager.create_backup.side_effect = Exception("Backup failed")
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    try:
        scheduler._run_daily_backup_job()
        assert False, "Expected exception was not raised"
    except Exception:
        pass

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_run_monthly_backup_job_success(mock_backup_manager):
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    scheduler._run_monthly_backup_job()
    mock_backup_manager.create_backup.assert_called_once()
    mock_backup_manager.prune_backups.assert_called_once()

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_run_monthly_backup_job_exception(mock_backup_manager):
    mock_backup_manager.create_backup.side_effect = Exception("Backup failed")
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    try:
        scheduler._run_monthly_backup_job()
        assert False, "Expected exception was not raised"
    except Exception:
        pass

@patch("src.wallet_backup.scheduler.time")
@patch("src.wallet_backup.scheduler.schedule")
def test_start_scheduler_normal_flow(mock_schedule, mock_time):
    mock_schedule.run_pending = Mock()
    mock_time.sleep = Mock()
    scheduler = BackupScheduler()
    mock_time.sleep.side_effect = [None, KeyboardInterrupt]
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        pass
    mock_schedule.run_pending.assert_called_once()

@patch("src.wallet_backup.scheduler.time")
@patch("src.wallet_backup.scheduler.schedule")
def test_start_scheduler_exception_handling(mock_schedule, mock_time):
    mock_schedule.run_pending = Mock()
    mock_schedule.run_pending.side_effect = [Exception("Test error"), None]
    mock_time.sleep = Mock()
    mock_time.sleep.side_effect = [None, None, KeyboardInterrupt]
    scheduler = BackupScheduler()
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        pass

def test_start_scheduler_keyboard_interrupt():
    scheduler = BackupScheduler()
    with patch.object(schedule, "run_pending") as mock_run, \
         patch("src.wallet_backup.scheduler.time.sleep") as mock_sleep:
        mock_run.side_effect = KeyboardInterrupt()
        try:
            scheduler.start_scheduler()
        except KeyboardInterrupt:
            pass
        mock_run.assert_called_once()
        mock_sleep.assert_called_once_with(60)

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_start_scheduler_with_error_handling(mock_backup_manager):
    mock_backup_manager.create_backup.side_effect = Exception("Error")
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    try:
        scheduler._run_daily_backup_job()
        assert False, "Expected exception was not raised"
    except Exception:
        pass

def test_start_scheduler_continues_after_job_error():
    scheduler = BackupScheduler()
    with patch.object(schedule, "run_pending") as mock_run:
        mock_run.side_effect = Exception("Test error")
        with patch("src.wallet_backup.scheduler.time.sleep") as mock_sleep:
            mock_sleep.side_effect = [None, None, KeyboardInterrupt]
            try:
                scheduler.start_scheduler()
            except KeyboardInterrupt:
                pass

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_backup_manager_exception_propagation(mock_backup_manager):
    mock_backup_manager.create_backup.side_effect = Exception("Critical error")
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    try:
        scheduler._run_monthly_backup_job()
        assert False, "Expected exception was not raised"
    except Exception as e:
        assert "Critical error" in str(e)

@patch("src.wallet_backup.scheduler.schedule")
def test_schedule_methods_return_consistency(mock_schedule):
    scheduler = BackupScheduler()
    result = scheduler.schedule_daily_backup()
    assert result is None

@patch("src.wallet_backup.scheduler.schedule")
def test_run_pending_no_jobs(mock_schedule):
    mock_schedule.run_pending = Mock(return_value=None)
    scheduler = BackupScheduler()
    scheduler.run_pending_jobs()
    mock_schedule.run_pending.assert_called_once()

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_daily_backup_job_calls_correct_methods(mock_backup_manager):
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    scheduler._run_daily_backup_job()
    assert mock_backup_manager.create_backup.call_count == 1
    assert mock_backup_manager.rotate_backups.call_count == 1

@patch("src.wallet_backup.scheduler.WalletBackupManager")
def test_monthly_backup_job_calls_correct_methods(mock_backup_manager):
    scheduler = BackupScheduler()
    scheduler.backup_manager = mock_backup_manager
    scheduler._run_monthly_backup_job()
    assert mock_backup_manager.create_backup.call_count == 1
    assert mock_backup_manager.prune_backups.call_count == 1