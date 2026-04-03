import os
import pytest
import redis
from unittest.mock import Mock, patch, MagicMock
from src.redis_client import connect_to_redis, increment_counter, get_counter

@pytest.fixture(autouse=True)
def reset_redis_client():
    """Reset the global Redis client before each test."""
    import src.redis_client
    src.redis_client._redis_client = None

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch('src.redis_client.redis.Redis') as mock_redis_class:
        mock_client = Mock()
        mock_redis_class.return_value = mock_client
        yield mock_client

@pytest.fixture
def mock_connection_pool():
    """Mock Redis connection pool."""
    with patch('src.redis_client.redis.ConnectionPool.from_url') as mock_pool:
        yield mock_pool

def test_connect_to_redis_success(mock_connection_pool, mock_redis):
    """Test successful Redis connection."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    
    client = connect_to_redis()
    
    assert client is not None
    mock_connection_pool.assert_called_once()
    mock_redis.ping.assert_called_once()

def test_connect_to_redis_no_url():
    """Test Redis connection fails when REDIS_URL is not set."""
    if 'REDIS_URL' in os.environ:
        del os.environ['REDIS_URL']
    
    with pytest.raises(ValueError, match="REDIS_URL environment variable is not set"):
        connect_to_redis()

def test_connect_to_redis_connection_error(mock_connection_pool):
    """Test Redis connection failure raises ConnectionError."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_connection_pool.side_effect = Exception("Connection failed")
    
    with pytest.raises(redis.ConnectionError):
        connect_to_redis()

def test_connect_to_redis_reuses_existing_connection(mock_connection_pool, mock_redis):
    """Test that existing connection is reused."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    
    client1 = connect_to_redis()
    client2 = connect_to_redis()
    
    assert client1 is client2
    mock_connection_pool.assert_called_once()

def test_increment_counter_success(mock_connection_pool, mock_redis):
    """Test successful counter increment."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.incr.return_value = 5
    
    with patch('src.redis_client.EXPIRATION', 60):
        result = increment_counter('test_key')
    
    assert result == 5
    mock_redis.incr.assert_called_once_with('test_key')

def test_increment_counter_empty_key():
    """Test incrementing with empty key raises ValueError."""
    with pytest.raises(ValueError, match="Key cannot be empty"):
        increment_counter('')

def test_increment_counter_redis_error(mock_connection_pool, mock_redis):
    """Test increment counter raises RedisError on failure."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.incr.side_effect = redis.RedisError("Redis error")
    
    with pytest.raises(redis.RedisError):
        increment_counter('test_key')

def test_increment_counter_first_time_sets_expiration(mock_connection_pool, mock_redis):
    """Test that expiration is set on first increment."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.incr.return_value = 1
    
    with patch('src.redis_client.EXPIRATION', 30):
        result = increment_counter('new_key')
    
    assert result == 1
    mock_redis.expire.assert_called_once_with('new_key', 30)

def test_get_counter_success(mock_connection_pool, mock_redis):
    """Test successful counter retrieval."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.get.return_value = '10'
    
    result = get_counter('test_key')
    
    assert result == 10
    mock_redis.get.assert_called_once_with('test_key')

def test_get_counter_empty_key():
    """Test getting counter with empty key raises ValueError."""
    with pytest.raises(ValueError, match="Key cannot be empty"):
        get_counter('')

def test_get_counter_key_not_found(mock_connection_pool, mock_redis):
    """Test getting counter that doesn't exist returns 0."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.get.return_value = None
    
    result = get_counter('nonexistent_key')
    
    assert result == 0

def test_get_counter_invalid_value(mock_connection_pool, mock_redis):
    """Test getting counter with invalid value returns 0."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.get.return_value = 'invalid'
    mock_redis.get.side_effect = ValueError("invalid literal for int")
    
    result = get_counter('bad_key')
    
    assert result == 0

def test_get_counter_redis_error(mock_connection_pool, mock_redis):
    """Test get counter raises RedisError on failure."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.get.side_effect = redis.RedisError("Redis error")
    
    with pytest.raises(redis.RedisError):
        get_counter('test_key')

def test_get_counter_unexpected_error(mock_connection_pool, mock_redis):
    """Test get counter handles unexpected errors."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.get.side_effect = Exception("Unexpected error")
    
    with pytest.raises(redis.RedisError):
        get_counter('test_key')

def test_increment_counter_unexpected_error(mock_connection_pool, mock_redis):
    """Test increment counter handles unexpected errors."""
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    mock_redis.ping.return_value = True
    mock_redis.incr.side_effect = Exception("Unexpected error")
    
    with patch('src.redis_client.EXPIRATION', 60):
        with pytest.raises(redis.RedisError):
            increment_counter('test_key')