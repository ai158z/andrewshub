import hashlib
import re
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def format_backup_name(wallet_id: str, timestamp: Optional[str] = None) -> str:
    """Format backup filename with wallet ID and timestamp."""
    if timestamp is None:
        timestamp = get_current_timestamp()
    return f"wallet_backup_{wallet_id}_{timestamp.replace(':', '-')}.dat"

def get_backup_date(backup_name: str) -> str:
    """Extract date from backup name."""
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})', backup_name)
    if match:
        return match.group(1)
    else:
        return ""

def verify_backup_integrity(backup_data: bytes, expected_hash: str) -> bool:
    """Verify backup data integrity using hash."""
    actual_hash = hashlib.sha256(backup_data).hexdigest()
    return actual_hash == expected_hash