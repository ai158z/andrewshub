import requests
import logging
from typing import Dict
import time


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# In-memory cache for network parameters
_network_parameters_cache: Dict[str, float] = {}
_cache_timestamps: Dict[str, float] = {}


def get_network_apy(network: str) -> float:
    """
    Fetch the network APY from external APIs or cache.
    
    Args:
        network: The network name (e.g., 'polkadot', 'kusama', etc.)
        
    Returns:
        float: The APY for the specified network.
    """
    # Check if we have a cached value that's still valid
    cache_key = f"{network}_apy"
    if cache_key in _network_parameters_cache and time.time() - _cache_timestamps.get(cache_key, 0) < 300:  # 5 min cache
        return _network_parameters_cache[cache_key]
        
    # For networks not in the cache, we would fetch the data from an API
    # For now, we'll return example values for specific networks
    if network == "polkadot":
        apy = 0.20  # 20% APY as example
        _network_parameters_cache[cache_key] = apy
        _cache_timestamps[cache_key] = time.time()
        return apy
    elif network == "kusama":
        apy = 0.20  # 20% APY as example
        _network_parameters_cache[cache_key] = apy
        _cache_timestamps[cache_key] = time.time()
        return apy
    elif network == "cosmos":
        apy = 0.20  # 20% APY as example
        _network_parameters_cache[cache_key] = apy
        _cache_timestamps[cache_key] = time.time()
        return apy
    else:
        apy = 0.20  # 20% default APY
        _network_parameters_cache[cache_key] = apy
        _cache_timestamps[cache_key] = time.time()
        return apy


def get_network_commission(network: str) -> float:
    """
    Fetch the network commission (fee) for a given network.
    
    Args:
        network: The network name (e.g., 'polkadot', 'kusama', etc.)
        
    Returns:
        float: The commission rate for the specified network.
    """
    # Check if we have a cached value that's still valid
    cache_key = f"{network}_commission"
    if cache_key in _network_parameters_cache and time.time() - _cache_timestamps.get(cache_key, 0) < 300:  # 5 min cache
        return _network_parameters_cache[cache_key]
        
    # For networks not in the cache, we would fetch the data from an API
    # For now, we'll return example values for specific networks
    if network == "polkadot":
        commission = 0.05  # 5% commission as example
        _network_parameters_cache[cache_key] = commission
        _cache_timestamps[cache_key] = time.time()
        return commission
    elif network == "kusama":
        commission = 0.05  # 5% commission as example
        _network_parameters_cache[cache_key] = commission
        _cache_timestamps[cache_key] = time.time()
        return commission
    elif network == "cosmos":
        commission = 0.05  # 5% commission as example
        _network_parameters_cache[cache_key] = commission
        _cache_timestamps[cache_key] = time.time()
        return commission
    else:
        commission = 0.05  # 5% default commission
        _network_parameters_cache[cache_key] = commission
        _cache_timestamps[cache_key] = time.time()
        return commission