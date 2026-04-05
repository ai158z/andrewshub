import os
import json
import logging
from typing import Any, Dict
from functools import lru_cache
import hashlib
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory cache with LRU eviction policy
CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))  # Default to 5 minutes if not set

class DataCache:
    _cache: Dict[str, Any] = {}
    _cache_info: Dict[str, float] = {}  # key -> expiry time

    @classmethod
    def _get_cache_key(cls, key: str) -> str:
        """Generate a consistent hash for the cache key."""
        return hashlib.sha256(key.encode('utf-8')).hexdigest()

    @classmethod
    def get(cls, key: str) -> Any:
        """Get value from cache if it exists and hasn't expired."""
        cache_key = cls._get_cache_key(key)
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        return None

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a value in the cache with an expiration time."""
        cache_key = cls._get_cache_key(key)
        cls._cache[cache_key] = value
        logger.info(f"Set cache key: {key}")

# Initialize simple cache
cache = DataCache()

def format_currency(value: float) -> str:
    """
    Format a float value as currency string with 2 decimal places and a dollar sign.
    
    Args:
        value: The numeric value to format
        
    Returns:
        Formatted currency string
    """
    try:
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric")
        
        # Handle negative zero specifically
        if isinstance(value, float) and value == 0.0:
            value = 0.0
            
        if value < 0:
            # For negative values, we want the minus sign before the dollar sign
            formatted = "-$" + "{:,.2f}".format(abs(value))
        else:
            formatted = "${:,.2f}".format(value)
        return formatted
    except Exception as e:
        logger.error(f"Error formatting currency: {e}")
        if isinstance(e, TypeError):
            raise  # Re-raise TypeError directly
        raise ValueError(f"Invalid currency value: {value}")

def cache_get(key: str) -> Any:
    """
    Retrieve a value from cache by key.
    
    Args:
        key: Cache key to retrieve
        
    Returns:
        Cached value or None if not found
    """
    try:
        return cache.get(key)
    except Exception as e:
        logger.error(f"Error retrieving cache key {key}: {e}")
        return None

def cache_set(key: str, value: Any) -> None:
    """
    Store a value in cache with the specified key.
    
    Args:
        key: Cache key
        value: Value to store in cache
    """
    try:
        cache.set(key, value)
    except Exception as e:
        logger.error(f"Error setting cache key {key}: {e}")
        raise