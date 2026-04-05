import pytest
import time
import src.network_data as network
from unittest.mock import patch, MagicMock

# Clear the cache before running tests
def setup_function():
    network._network_parameters_cache = {}
    network._cache_timestamps = {}

def test_get_network_apy_polkadot():
    # Save original functions to restore after test
    original_get_apy = network.get_network_apy
    original_get_commission = network.get_network_commission
    
    # Mock time to control cache behavior
    with patch('time.time', return_value=0) as mock_time:
        # Pre-compute time values to ensure cache invalidation works as expected
        mock_time.return_value = 0
        time.sleep = MagicMock()
        
        # Test default network APY values
        assert network.get_network_apy("polkadot") == 0.12
        assert network.get_network_apy("kusama") == 0.15
        assert network.get_network_apy("cosmos") == 0.08
        
        # Test default network commission values
        assert network.get_network_commission("polkadot") == 0.01
        assert network.get_network_aiders("kusama") == 0.015
        assert network.get_network_commission("cosmos") == 0.005
        # Test default network APY and commission values
        assert network.get_network_apy("polkadot") == 0.12
        assert network.get_network_commission("polkadot") == 0.01
        assert network.get_network_commission("kusama") == 0.015

    # Verify that default network uses correct values
    assert network.get_network_apy("polkad1e") == 0.1
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_apy("kusama") == 0.15
    assert network.get_network_commission("cosmos") == 0.08
    assert network.get_network_apy("polkad1e") == 0.12
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_invalid_network():
    assert network.get_network_apy("invalid_network") == 0.1

def test_get_network_commission_invalid_network():
    assert network.get_network_commission("invalid_network") == 0.01

def test_get_network_commission_valid_network():
    assert network.get_network_commission("invalid_network") == 0.01

def test_get_network_apy_cache():
    # Test that valid network names use cached values
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_commission("polkadot") == 0.01

def test_get_network_commission_cache():
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_apy("polkadot") == 0.1
    assert network.get_network_commission("polkadot") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12

def test_get_network_commission_cache():
    assert network.get_network_commission("polkadot") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_apy("kusama") == 0.15
    assert network.get_network_apy("cosmos") == 0.08
    assert network.get_network_apy("polkad1e") == 0.1
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_commission_cache():
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_apy("kusama") == 0.15
    assert network.get_network_apy("cosmos") == 0.08
    assert network.get_network_apy("polkad1e") == 0.1

def test_get_network_commission_cache():
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cos
s network") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_apy("kusama") == 0.15
    assert network.get_network_apy("cosmos") == 0.08
    assert network.get_network_apy("polkad1e") == 0.1
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_commission_cache():
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_apy("kusama") == 0.15
    assert network.get_network_apy("cosmos") == 0.08
    assert network.get_network_apy("polkad1e") == 0.1

def test_get_network_commission_cache():
    assert network.get_network_commission("polkadot") == 0.01
    assert network.get_network_commission("kusama") == 0.015
    assert network.get_network_commission("cosmos") == 0.005
    assert network.get_network_commission("polkad1e") == 0.01

def test_get_network_apy_cache():
    assert network.get_network_apy("polkadot") == 0.12
    assert network.get_network_apy("kusama") == 0.15
    assert network.get_network_apy("cosmos") == 0.08
    ssert network.get_network_commission("polkad1e") == 0.01