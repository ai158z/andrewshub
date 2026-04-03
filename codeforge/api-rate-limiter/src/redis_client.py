import os
import logging
from typing import Optional
import redis

# Configure logging
logger = logging.getLogger(__name__)

# Global Redis connection pool
_redis_client: Optional[redis.Redis] = None

def connect_to_redis() -> redis.Redis:
    """
    Establishes a connection to Redis using a connection pool.
    
    Returns:
        redis.Redis: Configured Redis client instance
        
    Raises:
        redis.ConnectionError: If connection to Redis fails
        ValueError: If REDIS_URL is not set
    """
    global _redis_client
    
    if _redis_client is not None:
        return _redis_client
        
    redis_url = os.environ.get('REDIS_URL')
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set")
    
    try:
        # Create connection pool for better performance
        connection_pool = redis.ConnectionPool.from_url(redis_url)
        _redis_client = redis.Redis(
            connection_pool=connection_pool,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        # Test connection
        _redis_client.ping()
        logger.info("Successfully connected to Redis")
        return _redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise redis.ConnectionError(f"Failed to connect to Redis: {e}")

def increment_counter(key: str) -> int:
    """
    Increments a counter in Redis by 1.
    
    Args:
        key (str): The Redis key to increment
        
    Returns:
        int: The new value of the counter after incrementing
        
    Raises:
        redis.RedisError: If Redis operation fails
        ValueError: If key is empty
    """
    if not key:
        raise ValueError("Key cannot be empty")
        
    try:
        client = connect_to_redis()
        value = client.incr(key)
        if value == 1:  # If this was the first increment, set expiration
            from src.config.rate_limit_config import EXPIRATION
            client.expire(key, EXPIRATION)
        return value
    except redis.RedisError as e:
        logger.error(f"Failed to increment counter {key}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error incrementing counter {key}: {e}")
        raise redis.RedisError(f"Unexpected error: {e}")

def get_counter(key: str) -> int:
    """
    Gets the current value of a counter from Redis.
    
    Args:
        key (str): The Redis key to retrieve
        
    Returns:
        int: The current value of the counter, or 0 if key doesn't exist
        
    Raises:
        redis.RedisError: If Redis operation fails
        ValueError: If key is empty
    """
    if not key:
        raise ValueError("Key cannot be empty")
        
    try:
        client = connect_to_redis()
        value = client.get(key)
        return int(value) if value is not None else 0
    except redis.RedisError as e:
        logger.error(f"Failed to get counter {key}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Counter value for {key} is not a valid integer: {e}")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error getting counter {key}: {e}")
        raise redis.RedisError(f"Unexpected error: {e}")

def get_counter(key: str) -> int:
    """
    Gets the current value of a counter from Redis.
    
    Args:
        key (str): The Redis key to retrieve
        
    Returns:
        int: The current value of the counter, or 0 if key doesn't exist
    """
    if not key:
        raise ValueError("Key cannot be empty")
        
    try:
        client = connect_to_redis()
        value = client.get(key)
        return int(value) if value is not None else 0
    except (redis.RedisError, ValueError) as e:
        logger.error(f"Error getting counter {key}: {e}")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error getting counter {key}: {e}")
        raise redis.RedisError(f"Unexpected error: {e}")