import os
import pytest
from unittest.mock import patch
from src.config.rate_limit_config import RateLimitConfig, get_rate_limit_config, configure_rate_limit


def test_default_initialization():
    """Test that RateLimitConfig initializes with default values."""
    config = RateLimitConfig()
    assert config.get_rate_limit() == 100
    assert config.get_window_size() == 60
    assert config.get_expiration() == 3600


@patch.dict(os.environ, {'RATE_LIMIT': '200', 'WINDOW_SIZE': '120', 'EXPIRATION': '7200'})
def test_initialization_with_env_vars():
    """Test that RateLimitConfig uses environment variables when set."""
    config = RateLimitConfig()
    assert config.get_rate_limit() == 200
    assert config.get_window_size() == 120
    assert config.get_expiration() == 7200


def test_get_rate_limit():
    """Test getting the rate limit value."""
    config = RateLimitConfig()
    assert config.get_rate_limit() == 100


def test_get_window_size():
    """Test getting the window size value."""
    config = RateLimitConfig()
    assert config.get_window_size() == 60


def test_get_expiration():
    """Test getting the expiration value."""
    config = RateLimitConfig()
    assert config.get_expiration() == 3600


def test_set_rate_limit_valid():
    """Test setting a valid rate limit."""
    config = RateLimitConfig()
    config.set_rate_limit(50)
    assert config.get_rate_limit() == 50


def test_set_window_size_valid():
    """Test setting a valid window size."""
    config = RateLimitConfig()
    config.set_window_size(30)
    assert config.get_window_size() == 30


def test_set_expiration_valid():
    """Test setting a valid expiration."""
    config = RateLimitConfig()
    config.set_expiration(1800)
    assert config.get_expiration() == 1800


def test_set_rate_limit_invalid():
    """Test setting an invalid rate limit raises ValueError."""
    config = RateLimitConfig()
    with pytest.raises(ValueError, match="Rate limit must be a positive integer"):
        config.set_rate_limit(-1)
    with pytest.raises(ValueError, match="Rate limit must be a positive integer"):
        config.set_rate_limit(0)


def test_set_window_size_invalid():
    """Test setting an invalid window size raises ValueError."""
    config = RateLimitConfig()
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        config.set_window_size(-1)
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        config.set_window_size(0)


def test_set_expiration_invalid():
    """Test setting an invalid expiration raises ValueError."""
    config = RateLimitConfig()
    with pytest.raises(ValueError, match="Expiration must be a positive integer"):
        config.set_expiration(-1)
    with pytest.raises(ValueError, match="Expiration must be a positive integer"):
        config.set_expiration(0)


def test_get_rate_limit_config_creates_instance():
    """Test that get_rate_limit_config creates a new instance when none exists."""
    # Reset the global config
    import src.config.rate_limit_config as rlc_module
    rlc_module.rate_limit_config = None
    
    config = get_rate_limit_config()
    assert isinstance(config, RateLimitConfig)


def test_get_rate_limit_config_returns_same_instance():
    """Test that get_rate_limit_config returns the same instance on subsequent calls."""
    # Reset the global config
    import src.config.rate_limit_config as rlc_module
    rlc_module.rate_limit_config = None
    
    config1 = get_rate_limit_config()
    config2 = get_rate_limit_config()
    assert config1 is config2


def test_configure_rate_limit_sets_all_values():
    """Test that configure_rate_limit sets all provided values."""
    # Reset the global config
    import src.config.rate_limit_config as rlc_module
    rlc_module.rate_limit_config = None
    
    configure_rate_limit(limit=50, window=30, expiration=1800)
    config = get_rate_limit_config()
    assert config.get_rate_limit() == 50
    assert config.get_window_size() == 30
    assert config.get_expiration() == 1800


def test_configure_rate_limit_sets_partial_values():
    """Test that configure_rate_limit sets only provided values."""
    # Reset the global config
    import src.config.rate_limit_config as rlc_module
    rlc_module.rate_limit_config = None
    
    configure_rate_limit(limit=75)
    config = get_rate_limit_config()
    assert config.get_rate_limit() == 75
    assert config.get_window_size() == 60  # default
    assert config.get_expiration() == 3600  # default


def test_configure_rate_limit_updates_existing_config():
    """Test that configure_rate_limit updates an existing configuration."""
    # Reset the global config
    import src.config.rate_limit_config as rlc_module
    rlc_module.rate_limit_config = None
    
    configure_rate_limit(limit=25)
    configure_rate_limit(window=15)
    config = get_rate_limit_config()
    assert config.get_rate_limit() == 25  # unchanged
    assert config.get_window_size() == 15  # updated
    assert config.get_expiration() == 3600  # default


def test_rate_limit_config_with_string_env_vars():
    """Test that RateLimitConfig handles string environment variables correctly."""
    with patch.dict(os.environ, {'RATE_LIMIT': 'invalid'}):
        with pytest.raises(ValueError):
            RateLimitConfig()


def test_rate_limit_config_with_float_env_vars():
    """Test that RateLimitConfig handles float environment variables correctly."""
    with patch.dict(os.environ, {'WINDOW_SIZE': '15.5'}):
        with pytest.raises(ValueError):
            RateLimitConfig()