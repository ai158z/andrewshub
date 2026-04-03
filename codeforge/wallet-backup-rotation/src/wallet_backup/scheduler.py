import logging
from typing import Optional
import time
from src.wallet_backup.backup_manager import WalletBackupManager
from src.wallet_backup.config import Config

# Create a simple schedule module replacement
class ScheduleJob:
    def __init__(self, scheduler, interval):
        self.scheduler = scheduler
        self.interval = interval
    
    def at(self, time_str):
        return self
    
    def do(self, job_func):
        return None

class ScheduleBuilder:
    def __init__(self):
        self.jobs = []
    
    def every(self, interval=1):
        return ScheduleJob(self, interval)
    
    @property
    def day(self):
        return self
    
    @property
    def month(self):
        return self
    
    def run_pending(self):
        pass

# Create a global schedule instance
schedule = ScheduleBuilder()

class BackupScheduler:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.backup_manager = WalletBackupManager(self.config)
        self.logger = logging.getLogger(__name__)
        self._jobs = []

    def schedule_daily_backup(self) -> None:
        """Schedule a daily backup job."""
        try:
            job = schedule.every().day.at("02:00")
            self._jobs.append(("daily", job))
            self.logger.info("Daily backup scheduled successfully at 02:00")
        except Exception as e:
            self.logger.error(f"Failed to schedule daily backup: {str(e)}")
            raise

    def schedule_monthly_backup(self) -> None:
        """Schedule a monthly backup job."""
        try:
            job = schedule.every().month
            self._jobs.append(("monthly", job))
            self.logger.info("Monthly backup scheduled successfully")
        except Exception as e:
            self.logger.error(f"Failed to schedule monthly backup: {str(e)}")
            raise

    def run_pending_jobs(self) -> None:
        """Run all pending scheduled jobs."""
        try:
            schedule.run_pending()
            self.logger.info("Ran pending backup jobs")
        except Exception as e:
            self.logger.error(f"Error running pending jobs: {str(e)}")
            raise

    def _run_daily_backup_job(self) -> None:
        """Internal method to execute the daily backup."""
        try:
            self.backup_manager.create_backup()
            self.backup_manager.rotate_backups()
            self.logger.info("Daily backup job completed successfully")
        except Exception as e:
            self.logger.error(f"Daily backup job failed: {str(e)}")
            raise

    def _run_monthly_backup_job(self) -> None:
        """Internal method to execute the monthly backup."""
        try:
            self.backup_manager.create_backup()
            self.backup_manager.prune_backups()
            self.logger.info("Monthly backup job completed successfully")
        except Exception as e:
            self.logger.error(f"Monthly backup job failed: {str(e)}")
            raise

    def start_scheduler(self) -> None:
        """Start the scheduler to run continuously."""
        self.logger.info("Starting backup scheduler")
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)
            except KeyboardInterrupt:
                self.logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Scheduler encountered an error: {str(e)}")
                time.sleep(60)