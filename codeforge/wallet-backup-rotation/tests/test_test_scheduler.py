import pytest
from unittest.mock import patch, MagicMock
import schedule
from src.wallet_backup.scheduler import BackupScheduler


@pytest.fixture
def backup_scheduler():
    return BackupScheduler()


@pytest.fixture
def clear_schedule():
    schedule.clear()
    yield
    schedule.clear()


def test_schedule_daily_backup(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        assert job is not None
        assert len(schedule.jobs) == 1


def test_schedule_monthly_backup(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_monthly_backup()
        assert job is not None
        assert len(schedule.jobs) == 1


def test_run_pending_jobs(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        assert job is not None
        
        schedule.run_pending()
        assert mock_create_backup.called
        assert mock_store_backup.called


def test_schedule_custom_backup(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_custom_backup("10:00")
        assert job is not None


def test_cancel_job(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        assert len(schedule.jobs) == 1
        backup_scheduler.cancel_job(job)
        assert len(schedule.jobs) == 0


def test_list_jobs(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        backup_scheduler.schedule_daily_backup()
        backup_scheduler.schedule_monthly_backup()
        jobs = backup_scheduler.list_jobs()
        assert len(jobs) == 2


def test_get_scheduled_time(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        scheduled_time = backup_scheduler.get_scheduled_time(job)
        assert scheduled_time is not None


def test_is_job_scheduled(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        assert backup_scheduler.is_job_scheduled(job) is True


def test_is_job_scheduled_false(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = "fake_job"
        assert backup_scheduler.is_job_scheduled(job) is False


@patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup')
@patch('src.wallet_backup.storage.BackupStorage.store_backup')
def test_perform_backup(mock_store_backup, mock_create_backup, backup_scheduler, clear_schedule):
    mock_create_backup.return_value = b"test_backup_data"
    mock_store_backup.return_value = None
    
    backup_scheduler.perform_backup()
    mock_create_backup.assert_called_once()
    mock_store_backup.assert_called_once()


def test_perform_backup_exception(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup:
        mock_create_backup.side_effect = Exception("Backup failed")
        
        with pytest.raises(Exception, match="Backup failed"):
            backup_scheduler.perform_backup()


def test_perform_backup_storage_exception(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.side_effect = Exception("Storage failed")
        
        with pytest.raises(Exception, match="Storage failed"):
            backup_scheduler.perform_backup()


def test_perform_backup_no_exception(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        backup_scheduler.perform_backup()
        mock_create_backup.assert_called_once()
        mock_store_backup.assert_called_once()


def test_schedule_job_with_tag(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        job.tag("daily")
        assert "daily" in job.tags


def test_cancel_job_by_tag(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        job.tag("daily")
        assert backup_scheduler.cancel_job_by_tag("daily") is True


def test_cancel_job_by_tag_not_found(backup_scheduler, clear_schedule):
    assert backup_scheduler.cancel_job_by_tag("nonexistent") is False


def test_clear_all_jobs(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        backup_scheduler.schedule_daily_backup()
        backup_scheduler.schedule_monthly_backup()
        backup_scheduler.clear_all_jobs()
        assert len(schedule.jobs) == 0


def test_clear_all_jobs_no_exception(backup_scheduler):
    try:
        backup_scheduler.clear_all_jobs()
        assert True
    except Exception:
        assert False


def test_get_tags(backup_scheduler, clear_schedule):
    with patch('src.wallet_backup.backup_manager.WalletBackupManager.create_backup') as mock_create_backup, \
         patch('src.wallet_backup.storage.BackupStorage.store_backup') as mock_store_backup:
        
        mock_create_backup.return_value = b"test_backup_data"
        mock_store_backup.return_value = None
        
        job = backup_scheduler.schedule_daily_backup()
        job.tag("daily", "backup")
        tags = backup_scheduler.get_tags(job)
        assert "daily" in tags
        assert "backup" in tags


def test_get_tags_no_tags(backup_scheduler, clear_schedule):
    job = "fake_job"
    tags = backup_scheduler.get_tags(job)
    assert tags == []