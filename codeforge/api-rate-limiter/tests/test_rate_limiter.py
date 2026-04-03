import pytest
from unittest.mock import MagicMock, patch
from src.rate_limiter import is_rate_limited, increment_request_count, get_request_count, reset_rate_limit
import redis

@pytest.fixture
def mock_redis_client():
    with patch('src.rate_limiter.redis_client') as mock_client:
        yield mock_client

def test_is_rate_limited_under_limit():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zadd = MagicMock()
        mock_redis.expire = MagicMock()
        mock_redis.zremrangebyscore = MagicMock()
        mock_redis.zcard = MagicMock(return_value=5)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is False

def test_is_rate_limited_over_limit():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zadd = MagicMock()
        mock_redis.expire = MagicMock()
        mock_redis.zcard = MagicMock(return_value=15)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is True

def test_is_rate_limited_redis_error():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zadd = MagicMock(side_effect=redis.RedisError)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is False

def test_increment_request_count_success():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zadd = MagicMock()
        mock_redis.expire = MagicMock()
        mock_redis.zcard = MagicMock(return_value=5)
        result = increment_request_count("192.168.1.1")
        assert result is False

def test_increment_request_count_limit_exceeded():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zadd = MagicMock()
        mock_redis.zcard = MagicMock(return_value=15)
        result = increment_request_count("192.168.1.1")
        assert result is True

def test_get_request_count_success():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zcard = MagicMock(return_value=5)
        count = get_request_count("192.168.1.1")
        assert count == 5

def test_get_request_count_error():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zremrangebyscore = MagicMock()
        mock_redis.zcard = MagicMock(side_effect=redis.RedisError)
        count = get_request_count("192.168.1.1")
        assert count == 0

def test_reset_rate_limit_success():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.delete = MagicMock(return_value=1)
        result = reset_rate_limit("192.168.1.1")
        assert result is True

def test_reset_rate_limit_failure():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.delete = MagicMock(return_value=0)
        result = reset_rate_limit("192.168.1.1")
        assert result is False

def test_is_rate_limited_normal_case():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zcard = MagicMock(return_value=5)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is False

def test_is_rate_limited_edge_case():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zcard = MagicMock(return_value=15)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is True

def test_is_rate_limited_exception_handling():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zadd = MagicMock(side_effect=Exception)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is False

def test_increment_request_count_normal():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zcard = MagicMock(return_value=5)
        result = increment_request_count("192.168.1.1")
        assert result is False

def test_increment_request_count_limited():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zcard = MagicMock(return_value=15)
        result = increment_request_count("192.168.1.1")
        assert result is True

def test_get_request_count_normal():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zcard = MagicMock(return_value=7)
        count = get_request_count("192.168.1.1")
        assert count == 7

def test_get_request_count_exception():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.zremrangebyscore = MagicMock()
        mock_redis.zcard = MagicMock(side_effect=Exception)
        count = get_request_count("192.168.1.1")
        assert count == 0

def test_reset_rate_limit_normal():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.delete = MagicMock(return_value=1)
        result = reset_rate_limit("192.168.1.1")
        assert result is True

def test_reset_rate_limit_no_key():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.delete = MagicMock(return_value=0)
        result = reset_rate_limit("192.168.1.1")
        assert result is False

def test_reset_rate_limit_exception():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.delete = MagicMock(side_effect=Exception)
        result = reset_rate_limit("192.168.1.1")
        assert result is False

def test_is_rate_limited_with_pipelines():
    with patch('src.rate_limiter.redis_client') as mock_redis:
        mock_redis.pipeline = MagicMock()
        mock_redis.zadd = MagicMock()
        mock_redis.zcard = MagicMock(return_value=5)
        result = is_rate_limited("192.168.1.1", 10, 60)
        assert result is False