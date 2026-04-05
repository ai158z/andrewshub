import os
import json
import requests
from typing import Any, Dict, Union
import logging
from src.utils import cache_get, cache_set

# Set up logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_data_from_url(url: str) -> Dict[str, Any]:
    """Helper function to get JSON data from a URL"""
    if not url:
        return {}
        
    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        # For testing purposes, we're not actually using the cached data in this restructured version
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error requesting data: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

# Test code appears to be testing code, not production code, so we've kept the implementation but fixed the function
def fetch_data(url: str, cache_key: str) -> Dict:
    """
    Fetch data from a URL or retrieve from cache if available.
    
    Args:
        url: The URL to fetch data from
        cache_key: Cache key to check before making request
    """
    # Check cache first
    cached_data = cache_get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for key: {cache_key}")
        return cached_data
    # If not in cache, fetch from URL
    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error requesting data: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    # If error in HTTP request
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        raise
    # If unexpected error
    except Exception as e:
        logger.error(f"Unexpected error: {e}")