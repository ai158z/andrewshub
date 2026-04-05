import pytest
import requests
from unittest.mock import patch, Mock
from src.currency_converter import convert_to_fiat, CurrencyConverter


def test_convert_to_fiat_valid_conversion():
    converter = CurrencyConverter()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'bitcoin': {'usd': 50000.0}
        }
        mock_get.return_value = mock_response
        
        result = converter.convert_to_fiat(1.0, 'BTC', 'USD')
        assert result == 50000.0


def test_convert_to_fiat_with_cached_rate():
    converter = CurrencyConverter()
    converter._cache['BTC_USD'] = 50000.0
    
    result = converter.convert_to_fiat(2.0, 'BTC', 'USD')
    assert result == 100000.0


def test_convert_to_fiat_invalid_amount_negative():
    converter = CurrencyConverter()
    with pytest.raises(ValueError, match="Amount must be a non-negative number"):
        converter.convert_to_fiat(-1.0, 'BTC', 'USD')


def test_convert_to_fiat_invalid_amount_type():
    converter = CurrencyConverter()
    with pytest.raises(ValueError, match="Amount must be a non-negative number"):
        converter.convert_to_fiat("invalid", 'BTC', 'USD')


def test_convert_to_fiat_invalid_crypto_symbol():
    converter = CurrencyConverter()
    with pytest.raises(ValueError, match="Crypto must be a non-empty string"):
        converter.convert_to_fiat(1.0, '', 'USD')


def test_convert_to_fiat_invalid_fiat_currency():
    converter = CurrencyConverter()
    with pytest.raises(ValueError, match="Fiat must be a non-empty string"):
        converter.convert_to_fiat(1.0, 'BTC', '')


def test_convert_to_fiat_network_error():
    converter = CurrencyConverter()
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError()):
        with pytest.raises(RuntimeError, match="Network error"):
            converter.convert_to_fiat(1.0, 'BTC', 'USD')


def test_convert_to_fiat_api_failure_status():
    converter = CurrencyConverter()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="Failed to fetch price data"):
            converter.convert_to_fiat(1.0, 'BTC', 'USD')


def test_convert_to_fiat_missing_crypto_data():
    converter = CurrencyConverter()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="Failed to get price for BTC"):
            converter.convert_to_fiat(1.0, 'BTC', 'USD')


def test_convert_to_fiat_missing_fiat_data():
    converter = CurrencyConverter()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'bitcoin': {}}
        mock_get.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="Failed to get GBP price for BTC"):
            converter.convert_to_fiat(1.0, 'BTC', 'GBP')


def test_convert_to_fiat_valid_crypto_mapping():
    converter = CurrencyConverter()
    crypto_id = converter._get_coingecko_id('BTC')
    assert crypto_id == 'bitcoin'


def test_convert_to_fiat_lowercase_inputs_normalized():
    converter = CurrencyConverter()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'bitcoin': {'usd': 50000.0}
        }
        mock_get.return_value = mock_response
        
        result = converter.convert_to_fiat(1.0, 'btc', 'usd')
        assert result == 50000.0


def test_convert_to_fiat_unknown_crypto_uses_lowercase_id():
    converter = CurrencyConverter()
    crypto_id = converter._get_coingecko_id('UNKNOWN')
    assert crypto_id == 'unknown'


def test_public_api_function_success():
    with patch.object(CurrencyConverter, 'convert_to_fiat') as mock_convert:
        mock_convert.return_value = 50000.0
        result = convert_to_fiat(1.0, 'BTC', 'USD')
        assert result == 50000.0
        mock_convert.assert_called_once_with(1.0, 'BTC', 'USD')


def test_public_api_function_uses_converter_instance():
    with patch('src.currency_converter._converter') as mock_converter:
        mock_converter.convert_to_fiat.return_value = 75000.0
        result = convert_to_fiat(1.5, 'BTC', 'USD')
        assert result == 75000.0
        mock_converter.convert_to_fiat.assert_called_with(1.5, 'BTC', 'USD')


def test_convert_to_fiat_caching_works():
    converter = CurrencyConverter()
    converter._cache['ETH_USD'] = 3000.0
    
    result = converter.convert_to_fiat(2.0, 'ETH', 'USD')
    assert result == 6000.0


def test_convert_to_fiat_different_fiat_currency():
    converter = CurrencyConverter()
    converter._cache['BTC_EUR'] = 45000.0
    
    result = converter.convert_to_fiat(1.0, 'BTC', 'EUR')
    assert result == 45000.0


def test_convert_to_fiat_case_insensitive_caching():
    converter = CurrencyConverter()
    converter._cache['BTC_USD'] = 50000.0
    
    result1 = converter.convert_to_fiat(1.0, 'btc', 'usd')
    result2 = converter.convert_to_fiat(1.0, 'BTC', 'USD')
    assert result1 == result2 == 50000.0


def test_convert_to_fiat_multiple_calls_same_cache():
    converter = CurrencyConverter()
    assert 'BTC_USD' not in converter._cache
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'bitcoin': {'usd': 50000.0}
        }
        mock_get.return_value = mock_response
        
        result = converter.convert_to_fiat(1.0, 'BTC', 'USD')
        assert result == 50000.0
        assert 'BTC_USD' in converter._cache