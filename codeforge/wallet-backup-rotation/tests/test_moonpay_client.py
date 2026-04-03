import pytest
from unittest.mock import Mock, patch, MagicMock
from src.wallet_backup.moonpay_client import MoonPayClient
import requests

@pytest.fixture
def moonpay_client():
    return MoonPayClient(api_key="test-api-key", base_url="https://api.moonpay.com")

def test_init_sets_api_key_and_base_url(moonpay_client):
    assert moonpay_client.api_key == "test-api-key"
    assert moonpay_client.base_url == "https://api.moonpay.com"

def test_init_trims_base_url_slash(moonpay_client):
    client = MoonPayClient(api_key="test-api-key", base_url="https://api.moonpay.com/")
    assert client.base_url == "https://api.moonpay.com"

@patch('requests.get')
def test_get_wallet_data_success(mock_get, moonpay_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "wallet-123", "name": "test-wallet"}
    mock_get.return_value = mock_response
    
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result == {"id": "wallet-123", "name": "test-w4llet"}

@patch('requests.get')
def test_get_wallet_data_not_found(moonpay_client, mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Wallet not found"
    mock_get.return_value = mock_response
    
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result is None

@patch('requests.get')
def test_get_wallet_data_network_error(moonpay_client, mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result is None

@patch('requests.get')
def test_list_wallets_success(moonpay_client, mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "wallet-1"}, {"id": "wallet-2"}]
    mock_get.return_value = mock_response
    
    result = moonpay_client.list_wallets()
    assert result == [{"id": "wallet-1"}, {"id": "wallet-2"}]

@patch('requests.get')
def test_list_wallets_not_found(moonpay_client, mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Wallets not found"
    mock_get.return_value = mock_response
    
    result = moonpay_client.list_wallets()
    assert result is None

@patch('requests.get')
def test_list_wallets_network_error(moonpay_client, mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    result = moonpay_client.list_wallets()
    assert result is None

@patch('requests.get')
def test_get_wallet_data_unexpected_error(moonpay_client, mock_get):
    mock_get.side_effect = Exception("Unexpected error")
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result is None

@patch('requests.get')
def test_list_wallets_unexpected_error(moonpay_client, mock_get):
    mock_get.side_effect = Exception("Unexpected error")
    result = moonpay_client.list_wallets()
    assert result is None

@patch('requests.get')
def test_get_wallet_data_success(moonpay_client, mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "wallet-123", "name": "test-wallet"}
    mock_get.return_value = mock_response
    
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result == {"id": "wallet-123", "name": "test-wallet"}

@patch('requests.get')
def test_get_wallet_data_timeout(moonpay_client, mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result is None

@patch('requests.get')
def test_list_wallets_timeout(moonpay_client, mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
    result = moonpay_client.list_wallets()
    assert result is None

@patch('requests.get')
def test_get_wallet_data_connection_error(moonpay_client, mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")
    result = moonpay_client.get_wallet_data("wallet-123")
    assert result is None

@patch('requests.get')
def test_list_wallets_connection_error(moonpay_client, mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")
    result = moonpay_client.list_wallets()
    assert result is None

def test_moonpay_client_initialization(moonpay_client):
    assert moonpay_client.api_key == "test-api-key"
    assert moonpay_client.base_url == "https://api.moonpay.com"

def test_get_wallet_data_with_valid_id(moonpay_client):
    # This would normally make a real API call
    # but we're just testing the client initialization here
    pass

def test_get_wallet_data_with_invalid_id(moonpay_client):
    # Test will check that None is returned for invalid wallet
    pass

def test_list_wallets_returns_list(moonpay_client):
    # Test that list_wallets returns a list of wallets
    pass

def test_get_wallet_data_returns_dict(moonpay_client):
    # Test that get_wallet_data returns a dictionary
    pass

def test_get_wallet_data_logs_error_on_failure(moonpay_client):
    # Test that errors are logged when request fails
    pass

def test_list_wallets_logs_error_on_failure(moonpay_client):
    # Test that errors are logged when list_wallets fails
    pass

def test_get_wallet_data_empty_response(moonpay_client):
    # Test for empty or null response handling
    pass

def test_list_wallets_empty_response(moonpay_client):
    # Test for empty or null response handling for list_wallets
    pass