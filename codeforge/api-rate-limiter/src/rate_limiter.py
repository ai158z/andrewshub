import time
import logging
from typing import Dict, List, Union
import redis
import os
from src.redis_client import connect_to_redis, increment_counter, get_counter
from src.config.rate_limit_config import RATE_LIMIT, WINDOW_SIZE, EXPIRATION

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Redis connection
redis_client = connect_to_redis()

def is_rate_limited(ip: str, limit: int, window: int) -> bool:
    """
    Check if the given IP has exceeded the rate limit using sliding window algorithm.
    
    Args:
        ip (str): The IP address to check
        limit (int): The maximum number of requests allowed
        window (int): The time window in seconds
        
    Returns:
        bool: True if rate limited, False otherwise
    """
    current_time = int(time.time())
    window_key = f"rate_limit:{ip}"
    
    try:
        # Add current request
        pipe = redis_client.pipeline()
        pipe.zadd(window_key, {str(current_time): current_time})
        pipe.expire(window_key, window + EXPIRATION)
        pipe.execute()
        
        # Remove old requests outside the window
        expire_time = current_time - window
        redis_client.zremrangebyscore(window_key, 0, expire_time)
        
        # Get request count
        request_count = redis_client.zcard(window_key)
        
        # Check if we're over the limit
        if request_count > limit:
            return True
            
        return False
    except redis.RedisError as e:
        logger.error(f"Redis error in rate limiting check: {e}")
        return False
    except Exception as e:
        logger.error(f"Error in rate limiting check: {e}")
        return False

def increment_request_count(ip: str) -> bool:
    """
    Increment the request count for an IP and check if rate limited.
    
    Args:
        ip (str): The IP address
        
    Returns:
        bool: True if rate limited, False otherwise
    """
    current_time = int(time.time())
    window_key = f"rate_limit:{ip}"
    
    try:
        # Add current request
        pipe = redis_client.pipeline()
        pipe.zadd(window_key, {str(current_time): current_time})
        pipe.expire(window_key, WINDOW_SIZE + EXPIRATION)
        pipe.execute()
        
        # Remove old requests outside the window
        expire_time = current_time - WINDOW_SIZE
        redis_client.zremrangebyscore(window_key, 0, expire_time)
        
        return redis_client.zcard(window_key) > RATE_LIMIT
    except redis.RedisError as e:
        logger.error(f"Redis error in incrementing request count: {e}")
        return False
    except Exception as e:
        logger.error(f"Error in incrementing request count: {e}")
        return False

def get_request_count(ip: str) -> int:
    """
    Get the current request count for an IP.
    
    Args:
        ip (str): The IP address
        
    Returns:
        int: The current request count
    """
    window_key = f"rate_limit:{ip}"
    current_time = int(time.time())
    
    try:
        # Remove expired entries first
        expire_time = current_time - WINDOW_SIZE
        redis_client.zremrangebyscore(window_key, 0, expire_time)
        
        # Return current count
        return redis_client.zcard(window_key)
    except redis.RedisError as e:
        logger.error(f"Redis error in getting request count: {e}")
        return 0
    except Exception as e:
        logger.error(f"Error in getting request count: {e}")
        return 0

def reset_rate_limit(ip: str) -> bool:
    """
    Reset the rate limit for an IP.
    
    Args:
        ip (str): The IP address
        
    Returns:
        bool: True if reset was successful
    """
    try:
        window_key = f"rate_limit:{ip}"
        result = redis_client.delete(window_key)
        return result == 1
    except redis.RedisError as e:
        logger.error(f"Redis error in reset rate limit: {e}")
        return False
    except Exception as e:
        logger.error(f"Error in reset rate limit: {e}")
        return False