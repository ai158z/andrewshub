import pytest
from unittest.mock import patch, MagicMock
from src.rate_limiter import is_rate_limited

def test_rate_limit_not_exceeded():
    """Test that rate limit is not exceeded when within limits"""
    with patch('src.redis_client.increment_counter') as mock_increment, \
         patch('src.redis_client.get_counter') as mock_get:
        
        mock_increment.return_value = None
        mock_get.return_value = 50  # Below rate limit
        
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is False

def test_rate_limit_exceeded():
    """Test that rate limit is properly exceeded"""
    with patch('src.redis_client.increment_counter') as mock_increment, \
         patch('src.redis_client.get_counter') as mock_get:
        
        mock_increment.return_value = None
        mock_get.return_value = 150  # Above rate limit
        
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is True

def test_zero_rate_limit():
    """Test rate limiting with zero limit"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 0
        result = is_rate_limited("127.0.0.1", 0, 60)
        assert result is True

def test_exact_rate_limit():
    """Test rate limiting at exact threshold"""
    with patch('src.redis_client.increment_counter') as mock_increment, \
         patch('src.redis_client.get_counter') as mock_get:
        
        mock_increment.return_value = None
        mock_get.return_value = 100  # Exactly at rate limit
        
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is True

def test_high_volume_rate_limit():
    """Test rate limiting with high volume request"""
    with patch('src.redis_client.increment_counter') as mock_increment, \
         patch('src.redis_client.get_counter') as mock_get:
        
        mock_increment.return_value = None
        mock_get.return_value = 1000  # Way above rate limit
        
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is True

def test_boundary_condition_at_limit():
    """Test rate limiting exactly at boundary"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 99  # Just below limit
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is False

def test_different_client_ip():
    """Test rate limiting with different IP addresses"""
    with patch('src.redis_client.increment_counter') as mock_increment, \
         patch('src.redis_client.get_counter') as mock_get:
        
        mock_increment.return_value = None
        mock_get.return_value = 75
        
        result1 = is_rate_limited("192.168.1.1", 100, 60)
        result2 = is_rate_limited("10.0.0.1", 100, 60)
        
        assert result1 is False
        assert result2 is False

def test_very_low_rate_limit():
    """Test with very low rate limit"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 1
        result = is_rate_limited("127.0.0.1", 1, 60)
        assert result is False

def test_very_high_rate_limit():
    """Test with very high rate limit"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 999
        result = is_rate_limited("127.0.0.1", 1000, 60)
        assert result is False

def test_negative_rate_limit():
    """Test with negative rate limit"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = -10
        result = is_rate_limited("127.0.0.1", -50, 60)
        assert result is True

def test_zero_time_window():
    """Test with zero time window"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 50
        result = is_rate_limited("127.0.0.1", 100, 0)
        assert result is False

def test_negative_time_window():
    """Test with negative time window"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 150
        result = is_rate_limited("127.0.0.1", 100, -60)
        assert result is True

def test_large_time_window():
    """Test with large time window"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 150
        result = is_rate_limited("127.0.0.1", 100, 3600)
        assert result is False

def test_small_time_window():
    """Test with small time window"""
    with patch('src.redis_client.get_counter') as mock_get:
        mock_get.return_value = 150
        result = is_rate_limited("127.0.0.1", 100, 1)
        assert result is True

def test_increment_counter_failure():
    """Test when increment_counter fails"""
    with patch('src.redis_client.increment_counter', side_effect=Exception("Redis error")), \
         patch('src.redis_client.get_counter') as mock_get:
        
        mock_get.return_value = 50
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is False

def test_get_counter_failure():
    """Test when get_counter fails"""
    with patch('src.redis_client.increment_counter') as mock_increment, \
         patch('src.redis_client.get_counter', side_effect=Exception("Redis error")):
        
        mock_increment.return_value = None
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is False

def test_both_redis_operations_fail():
    """Test when both Redis operations fail"""
    with patch('src.redis_client.increment_counter', side_effect=Exception("Increment error")), \
         patch('src.redis_client.get_counter', side_effect=Exception("Get error")):
        
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is False

def test_redis_connection_failure():
    """Test when Redis connection fails completely"""
    with patch('src.redis_client.connect_to_redis', side_effect=Exception("Connection failed")):
        result = is_rate_limited("127.0.0.1", 100, 60)
        assert result is False