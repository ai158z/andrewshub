import pytest
from unittest.mock import patch, MagicMock
from src.blockchain_client import get_reward_rate
from src.models.reward_rate import RewardRate

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_success(mock_fetch_data):
    # Arrange
    mock_response = {
        "ethereum": {
            "reward_rate": 0.05
        }
    }
    mock_fetch_data.return_value = mock_response
    
    # Act
    result = get_reward_reate("ethereum")
    
    # Assert
    assert isinstance(result, RewardRate)
    assert result.reward_rate == 0.05
    mock_fetch_data.assert_called_once()

def test_get_reward_rate_invalid_network():
    with pytest.raises(ValueError, match="Unsupported network"):
        get_reward_rate("invalid_network")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_missing_data(mock_fetch_data):
    mock_fetch_data.return_value = {}
    
    with pytest.raises(KeyError):
        get_reward_rate("ethereum")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_network_case_insensitive(mock_fetch_data):
    mock_response = {
        "Ethereum": {
            "reward_rate": 0.03
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("ETHEREUM")
    assert isinstance(result, RewardRate)
    assert result.reward_rate == 0.03

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_handles_float_values(mock_fetch_data):
    mock_response = {
        "ethereum": {
            "reward_rate": 0.075
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("ethereum")
    assert result.reward_rate == 0.075

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_handles_zero_rate(mock_fetch_data):
    mock_response = {
        "ethereum": {
            "reward_rate": 0.0
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("ethereum")
    assert result.reward_rate == 0.0

def test_get_reward_rate_supported_networks():
    with pytest.raises(ValueError, match="Unsupported network"):
        get_reward_rate("bitcoin")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_large_reward_rate(mock_fetch_data):
    mock_response = {
        "ethereum": {
            "reward_rate": 100.5
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("ethereum")
    assert result.reward_rate == 100.5

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_negative_reward_rate(mock_fetch_data):
    mock_response = {
        "ethereum": {
            "reward_rate": -0.02
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("ethereum")
    assert result.reward_rate == -0.02

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_multiple_networks(mock_fetch_data):
    mock_response = {
        "polygon": {
            "reward_rate": 0.12
        },
        "avalanche": {
            "reward_rate": 0.08
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("polygon")
    assert result.reward_rate == 0.12
    
    result = get_reward_rate("avalanche")
    assert result.reward_rate == 0.08

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_fetch_data_exception(mock_fetch_data):
    mock_fetch_data.side_effect = Exception("Network error")
    
    with pytest.raises(Exception, match="Network error"):
        get_reward_rate("ethereum")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_none_response(mock_fetch_data):
    mock_fetch_data.return_value = None
    
    with pytest.raises(AttributeError):
        get_reward_rate("ethereum")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_empty_string_network(mock_fetch_data):
    mock_fetch_data.return_value = {"": {"reward_rate": 0.01}}
    
    with pytest.raises(ValueError, match="Unsupported network"):
        get_reward_rate("")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_special_characters_network(mock_fetch_data):
    mock_fetch_data.return_value = {"test-net": {"reward_rate": 0.04}}
    
    result = get_reward_rate("test-net")
    assert result.reward_rate == 0.04

def test_get_reward_rate_network_normalization():
    with pytest.raises(ValueError, match="Unsupported network"):
        get_reward_rate("ETH")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_network_with_underscores(mock_fetch_data):
    mock_response = {
        "binance_smart_chain": {
            "reward_rate": 0.06
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("binance_smart_chain")
    assert result.reward_rate == 0.06

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_very_small_reward_rate(mock_fetch_data):
    mock_response = {
        "ethereum": {
            "reward_rate": 0.0001
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("ethereum")
    assert result.reward_rate == 0.0001

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_network_with_spaces(mock_fetch_data):
    mock_fetch_data.return_value = {}
    
    with pytest.raises(ValueError, match="Unsupported network"):
        get_reward_rate("ethereum network")

@patch('src.blockchain_client.fetch_data')
def test_get_reward_rate_network_with_numbers(mock_fetch_data):
    mock_response = {
        "network123": {
            "reward_rate": 0.09
        }
    }
    mock_fetch_data.return_value = mock_response
    
    result = get_reward_rate("network123")
    assert result.reward_rate == 0.09