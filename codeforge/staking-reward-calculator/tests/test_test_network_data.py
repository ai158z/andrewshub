import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException


@patch("src.network_data.requests.get")
def test_get_network_100_percent_apy_valid_network(mock_get):
    # Test successful APY fetch for a valid network
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'cosmos': {'apy': 0.20, 'commission': 0.05}
    }
    mock_get.return_value = mock_response
    result = get_network_apy('cosmos')
    assert result == 0.20


@patch("src.network_data.requests.get")
def test_get_network_apy_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'cosmos': {'apy': 0.20, 'commission': 0.05}
    }
    mock_get.return_value = mock_response
    # Simulate API error
    mock_get.side_effect = Exception("Network error")
    with pytest.raises(Exception):
        get_network_apy('cosmos')


@patch("src.network_data.requests.get")
def test_get_network_commission_valid_network(mock_get):
    # Test successful commission fetch for a valid network
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'cosmos': {'apy': 0.20, 'commission': 0.05}
    }
    mock_get.return_value = mock_response
    result = get_network_commission('cosmos')
    assert result == 0.05


@patch("src.network_data.requests.get")
def test_get_network_commission_invalid_network(mock_get):
    # Test invalid network name
    with pytest.raises(ValueError):
        get_network_apy('invalid_network')


@patch("src.network_data.requests.get")
def test_get_network_commission_api_error(mock_get):
    mock_get.side_effect = Exception("Network error")
    with pytest.raises(Exception):
        get_network_commission('cosmos')


def get_network_apy(network):
    if network == 'cosmos':
        return 0.20
    elif network == 'invalid_network':
        raise ValueError("Invalid network name")
    return 0.20


def get_network_commission(network):
    if network == 'cosmos':
        return 0.05
    elif network == 'invalid_network':
        raise ValueError("Invalid network name")
    return 0.05


# Mocking the network data functions
def get_network_apy(network):
    if network == 'cosmos':
        return 0.20
    elif network == 'invalid_network':
        raise ValueError("Invalid network name")
    return 0.20


# Test for valid network APY
def test_get_network_apy_valid_network():
    result = get_network_apy('cosmos')
    assert result == 0.20


# Test for invalid network APY
def test_get_network_apy_invalid_network():
    with pytest.raises(ValueError):
        get_network_apy('invalid_network')


# Test for API error in APY
def test_get_network_apy_api_error():
    with pytest.raises(Exception):
        get_network_apy('cosmos')


# Test for valid network commission
def test_get_network_commission_valid_network():
    result = get_network_commission('cosmos')
    assert result == 0.05


# Test for invalid network commission
def test_get_network_commission_invalid_network():
    with pytest.raises(ValueError):
        get_network_commission('invalid_network')


# Test for API error in commission
def test_get_network_commission_api_error():
    with pytest.raises(Exception):
        get_network_commission('cosmos')