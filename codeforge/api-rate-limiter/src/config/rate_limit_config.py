import os
from typing import Optional

class RateLimitConfig:
    """Configuration class for rate limiting parameters."""
    
    def __init__(self) -> None:
        """Initialize rate limit configuration with default values that can be overridden by environment variables."""
        try:
            self.rate_limit: int = int(os.getenv('RATE_LIMIT', '100'))
            self.window_size: int = int(os.getenv('WINDOW_SIZE', '60'))
            self.expiration: int = int(os.getenv('EXPIRATION', '3600'))
        except ValueError:
            raise ValueError("Environment variables must be valid integers")

    def get_rate_limit(self) -> int:
        """Get the rate limit value."""
        return self.rate_limit

    def get_window_size(self) -> int:
        """Get the window size in seconds."""
        return self.window_size

    def get_expiration(self) -> int:
        """Get the expiration time in seconds."""
        return self.expiration

    def set_rate_limit(self, limit: int) -> None:
        """Set the rate limit value."""
        if limit <= 0:
            raise ValueError("Rate limit must be a positive integer")
        self.rate_limit = limit

    def set_window_size(self, window: int) -> None:
        """Set the window size in seconds."""
        if window <= 0:
            raise ValueError("Window size must be a positive integer")
        self.window_size = window

    def set_expiration(self, expiration: int) -> None:
        """Set the expiration time in seconds."""
        if expiration <= 0:
            raise ValueError("Expiration must be a positive integer")
        self.expiration = expiration


# Global configuration instance
rate_limit_config: Optional[RateLimitConfig] = None


def get_rate_limit_config() -> RateLimitConfig:
    """Get or create the global rate limit configuration."""
    global rate_limit_config
    if rate_limit_config is None:
        rate_limit_config = RateLimitConfig()
    return rate_limit_config


def configure_rate_limit(limit: Optional[int] = None, window: Optional[int] = None, expiration: Optional[int] = None) -> None:
    """Configure rate limiting parameters."""
    config = get_rate_limit_config()
    
    if limit is not None:
        config.set_rate_limit(limit)
    if window is not None:
        config.set_window_size(window)
    if expiration is not None:
        config.set_expiration(expiration)