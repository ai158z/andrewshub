import requests
import time
import logging
from typing import Optional
import hashlib
import os
from datetime import datetime
import feedparser
import json
import re
from urllib.parse import urlparse

# Configure logger
logger = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    """Check if a string is a valid URL format"""
    if not isinstance(url, str):
        return False
    if not url:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path and result.path != '/'])
    except:
        return False

def fetch_feed(url: str, timeout: int = 10) -> str:
    """
    Fetches RSS feed content from a URL with error handling and retries.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        String content of the RSS feed
    """
    # Validate URL
    if not url:
        raise ValueError("URL cannot be empty")
        
    if not is_valid_url(url):
        raise ValueError("Invalid URL")
        
    # Validate and sanitize URL
    if not isinstance(timeout, int) or timeout <= 0:
        timeout = 10
        
    # Make the request with timeout and error handling
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching {url}")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error while fetching {url}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while fetching {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching {url}: {e}")
        raise
    return response.text

def fetch_with_retries(url: str, timeout: int = 10) -> str:
    """
    Fetches content with automatic retries if request fails.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Fetched content as string
    """
    # Validate URL
    if not url:
        raise ValueError("URL cannot be empty")
        
    # Set request timeout
    if not isinstance(timeout, int) or timeout <= 0:
        timeout = 10
        
    # Make the request with timeout and error handling
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while fetching {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        raise
    return response.text