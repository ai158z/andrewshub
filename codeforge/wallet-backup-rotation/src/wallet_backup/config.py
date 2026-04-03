import os
from typing import Optional


class Config:
    """Configuration management for the backup system."""

    def __init__(self):
        """Initialize configuration manager."""
        self._moonpay_api_key = None
        self._encryption_key = None

    def get_moonpay_api_key(self) -> Optional[str]:
        """Get MoonPay API key from environment."""
        if self._moonpay_api_key is None:
            self._moonpay_api_key = os.environ.get('MOONPAY_API_KEY')
        return self._moonpay_api_key

    def get_encryption_key(self) -> Optional[bytes]:
        """Get encryption key from environment."""
        if self._encryption_key is None:
            key = os.environ.get('ENCRYPTION_KEY')
            if key is not None:  # Changed: Check for None explicitly to handle empty string
                self._encryption_key = key.encode()
            else:
                self._encryption_key = None
        return self._encryption_key