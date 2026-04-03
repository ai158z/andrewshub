import os
import pytest
from src.wallet_backup.config import Config


def test_get_moonpay_api_key_from_env():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = 'test-key-123'
    
    result = config.get_moonpay_api_key()
    
    assert result == 'test-key-123'


def test_get_moonpay_api_key_missing():
    config = Config()
    if 'MOONPAY_API_KEY' in os.environ:
        del os.environ['MOONPAY_API_KEY']
    
    result = config.get_moonpay_api_key()
    
    assert result is None


def test_get_moonpay_api_key_cached():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = 'test-key-123'
    
    # First call
    result1 = config.get_moonpay_api_key()
    # Remove from env to verify caching
    del os.environ['MOONPAY_API_KEY']
    # Second call
    result2 = config.get_moonpay_api_key()
    
    assert result1 == 'test-key-123'
    assert result2 == 'test-key-123'


def test_get_encryption_key_from_env():
    config = Config()
    os.environ['ENCRYPTION_KEY'] = 'my-secret-key'
    
    result = config.get_encryption_key()
    
    assert result == b'my-secret-key'


def test_get_encryption_key_missing():
    config = Config()
    if 'ENCRYPTION_KEY' in os.environ:
        del os.environ['ENCRYPTION_KEY']
    
    result = config.get_encryption_key()
    
    assert result is None


def test_get_encryption_key_cached():
    config = Config()
    os.environ['ENCRYPTION_KEY'] = 'my-secret-key'
    
    # First call
    result1 = config.get_encryption_key()
    # Remove from env to verify caching
    del os.environ['ENCRYPTION_KEY']
    # Second call
    result2 = config.get_encryption_key()
    
    assert result1 == b'my-secret-key'
    assert result2 == b'my-secret-key'


def test_empty_moonpay_api_key():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = ''
    
    result = config.get_moonpay_api_key()
    
    assert result == ''


def test_empty_encryption_key():
    config = Config()
    os.environ['ENCRYPTION_KEY'] = ''
    
    result = config.get_encryption_key()
    
    assert result == b''


def test_moonpay_api_key_with_special_chars():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = 'test-key_123!@#'
    
    result = config.get_moonpay_api_key()
    
    assert result == 'test-key_123!@#'


def test_encryption_key_with_special_chars():
    config = Config()
    os.environ['ENCRYPTION_KEY'] = 'key!@#$%^&*()'
    
    result = config.get_encryption_key()
    
    assert result == b'key!@#$%^&*()'


def test_multiple_config_instances_independent():
    config1 = Config()
    config2 = Config()
    os.environ['MOONPAY_API_KEY'] = 'key1'
    os.environ['ENCRYPTION_KEY'] = 'secret1'
    
    result1 = config1.get_moonpay_api_key()
    result2 = config1.get_encryption_key()
    
    os.environ['MOONPAY_API_KEY'] = 'key2'
    os.environ['ENCRYPTION_KEY'] = 'secret2'
    
    result3 = config2.get_moonpay_api_key()
    result4 = config2.get_encryption_key()
    
    # config1 should return cached values
    assert result1 == 'key1'
    assert result2 == b'secret1'
    # config2 should read new values
    assert result3 == 'key2'
    assert result4 == b'secret2'


def test_unicode_moonpay_api_key():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = 'test-🔑-key'
    
    result = config.get_moonpay_api_key()
    
    assert result == 'test-🔑-key'


def test_unicode_encryption_key():
    config = Config()
    os.environ['ENCRYPTION_KEY'] = 'secret-🔑-key'
    
    result = config.get_encryption_key()
    
    assert result == 'secret-🔑-key'.encode()


def test_config_initialization():
    config = Config()
    
    assert config._moonpay_api_key is None
    assert config._encryption_key is None


def test_get_moonpay_api_key_twice_same_result():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = 'consistent-key'
    
    result1 = config.get_moonpay_api_key()
    result2 = config.get_moonpay_api_key()
    
    assert result1 == result2 == 'consistent-key'


def test_get_encryption_key_twice_same_result():
    config = Config()
    os.environ['ENCRYPTION_KEY'] = 'consistent-secret'
    
    result1 = config.get_encryption_key()
    result2 = config.get_encryption_key()
    
    assert result1 == result2 == b'consistent-secret'


def test_empty_config_initialization():
    config = Config()
    
    assert config.get_moonpay_api_key() is None
    assert config.get_encryption_key() is None


def test_config_with_none_env_values():
    config = Config()
    os.environ['MOONPAY_API_KEY'] = 'test'
    os.environ['ENCRYPTION_KEY'] = 'secret'
    
    # Set to None explicitly in instance
    config._moonpay_api_key = None
    config._encryption_key = None
    
    # Should read from env again
    assert config.get_moonpay_api_key() == 'test'
    assert config.get_encryption_key() == b'secret'