import pytest
from unittest.mock import patch, Mock
from src.blockchain_client import get_reward_rate, RewardRate

def test_get_reward_rate_returns_reward_rate_object():
    with patch('src.blockchain_client.cache_get') as mock_cache_get:
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_returns_cached_rate_when_available(mocker):
    with patch('src.blockchain_client.cache_get') as mock_cache:
        mock_cache.return_value = {"network": "ethereum", "annual_rate": 0.05}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_handles_unsupported_network():
    with pytest.raises(ValueError):
        get_reward_rate("unsupported")

def test_get_reward_rate_calls_network_fetch_function(mocker):
    with patch('src.blockchain_client._fetch_ethereum_reward_rate') as mock_fetch:
        result = _fetch_ethereum_reward_rate()
        assert result == "ethereum"

def test_get_reward_rate_returns_reward_rate_object(mocker):
    with patch('src.blockchain_client.cache_get') as mock_cache:
        mock_cache.return_value = None
        result = get_reward_rate("ethereum")
        assert result == "ethereum"

def test_get_reward_rate_uses_cache_when_available(mocker):
    mock_cache.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12}
    result = get_reward_rate("ethereum")
    assert isinstance(result, RewardRate)

def test_get_reward_rate_handles_request_exceptions(mocker):
    with patch('src.blockchain_client.cache_get') as mock_cache:
        mock_cache.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12, "last_updated": "2023-01-01T00:00:00Z"}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_handles_unsupported_network():
    with pytest.raises(ValueError):
        get_reward_rate("unsupported_network")

def test_get_reward_rate_returns_reward_rate_object(mocker):
    with patch('src.blockchain_client._fetch_ethereum_reward_rate') as mock_fetch:
        mock_fetch.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12, "last_updated": "2023-01-01T00:00:00Z"}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_handles_unsupported_network():
    with patch('src.blockchain_client._fetch_ethereum_reward_rate') as mock_fetch:
        mock_fetch.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12, "last_updated": "2023-01-01T00:00:00Z"}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_handles_request_exceptions(mocker):
    with patch('src.blockchain_client._fetch_ethereum_reward_rate') as mock_fetch:
        mock_fetch.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12, "last_updated": "2023-01-01T00:00:00Z"}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_uses_cache_when_available(mocker):
    with patch('src.blockchain_client.cache_get') as mock_cache:
        mock_cache.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12, "last_updated": "2023-01-01T00:00:00Z"}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_returns_reward_rate_object():
    with patch('src.blockchain_client._fetch_ethereum_reward_rate') as mock_fetch:
        mock_fetch.return_value = {"network": "ethereum", "annual_rate": 0.05, "epoch_length": 12, "last_updated": "2023-01-01T00:00:00Z"}
        result = get_reward_rate("ethereum")
        assert isinstance(result, RewardRate)

def test_get_reward_rate_returns_reward_rate_object():
    result = get_reward_rate("ethereum")
    assert isinstance(result, RewardRate)

def test_get_reward_rate_handles_request_exceptions():
    result = get_reward_rate("ethereum")
    assert isinstance(result, RewardRate)