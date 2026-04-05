import pytest
from unittest.mock import patch, MagicMock, call
from src.currency_converter import convert_to_fiat

def test_convert_btc_to_usd():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0,
                'ETH': 2000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(1.0, 'BTC', 'USD')
        assert result == 20000.0

def test_convert_eth_to_usd():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0,
                'ETH': 2000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(1.0, 'ETH', 'USD')
        assert result == 2000.0

def test_convert_btc_to_eur():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 17000.0,
                'ETH': 1700.0
            }
        }
        mock_get.return_value = mock_get()
        mock_get.return_value.json.return_value = mock_response.json.return_value
        
        result = convert_to_fiat(1.0, 'BTC', 'EUR')
        assert result == 17000.0

def test_api_request_failure():
    with patch('requests.get', side_effect=Exception("API request failed")):
        with pytest.raises(Exception, match="API request failed"):
            convert_to_fiat(1.0, 'BTC', 'USD')

def test_convert_zero_amount():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(0.0, 'BTC', 'USD')
        assert result == 0.0

def test_convert_negative_amount():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(-1.0, 'BTC', 'USD')
        assert result == -20000.0

def test_unsupported_crypto_currency():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {}
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(KeyError):
            convert_to_fiat(1.0, 'INVALID', 'USD')

def test_unsupported_fiat_currency():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0,
                'USD': 1.0
            }
        }
        mock_get.return_value = mock_get()
        mock_get.return_value.json.return_value = mock_response.json.return_value
        
        with pytest.raises(KeyError):
            convert_to_fiat(1.0, 'BTC', 'INVALID')

def test_partial_amount_conversion():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(0.5, 'BTC', 'USD')
        assert result == 10000.0

def test_multiple_conversions_same_session():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0,
                'ETH': 2000.0
            }
        }
        mock_get.return_value = mock_response
        
        result1 = convert_to_fiat(1.0, 'BTC', 'USD')
        result2 = convert_to_fiat(1.0, 'ETH', 'USD')
        assert result1 == 20000.0
        assert result2 == 2000.0
        assert mock_get.call_count == 2

def test_large_amount_conversion():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(10.0, 'BTC', 'USD')
        assert result == 200000.0

def test_very_small_amount():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(0.001, 'BTC', 'USD')
        assert result == 20.0

def test_missing_btc_rate():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'ETH': 2000.0
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(KeyError):
            convert_to_fiat(1.0, 'BTC', 'USD')

def test_response_caching():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.0
            }
        }
        mock_get.return_value = mock_response
        
        convert_to_fiat(1.0, 'BTC', 'USD')
        convert_to_fiat(1.0, 'BTC', 'USD')
        # Should make only one actual API call due to caching
        mock_get.assert_called_once()

def test_empty_response():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        with pytest.raises(KeyError):
            convert_to_fiat(1.0, 'BTC', 'USD')

def test_malformed_api_response():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'malformed': 'response'
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(KeyError):
            convert_to_fiat(1.0, 'BTC', 'USD')

def test_fiat_rate_zero():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 0.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(1.0, 'BTC', 'USD')
        assert result == 0.0

def test_same_crypto_fiat_currency():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'USD': 1.0
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(1.0, 'USD', 'USD')
        assert result == 1.0

def test_crypto_conversion_high_precision():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'BTC': 20000.123456789
            }
        }
        mock_get.return_value = mock_response
        
        result = convert_to_fiat(1.0, 'BTC', 'USD')
        assert result == 20000.123456789

def test_network_timeout_error():
    with patch('requests.get', side_effect=Exception("Connection timeout")):
        with pytest.raises(Exception, match="Connection timeout"):
            convert_to_fiat(1.0, 'BTC', 'USD')