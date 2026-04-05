import pytest
import requests
import json
from unittest.mock import patch, MagicMock
from src.data_fetcher import fetch_data

def test_fetch_data_returns_cached_data_when_available():
    with patch('src.data_fetcher.cache_get') as mock_cache_get:
        mock_cache_get.return_value = {'cached': 'data'}
        result = fetch_data('http://example.com', 'test_key')
        assert result == {'cached': 'data'}

def test_fetch_data_makes_request_when_cache_miss():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'api': 'data'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com', 'test_key')
        assert result == {'api': 'data'}
        mock_get.assert_called_once_with('http://example.com', timeout=30)

def test_fetch_data_caches_result_after_fetch():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set') as mock_cache_set, \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'api': 'data'}
        mock_get.return_value = mock_response
        
        fetch_data('http://example.com', 'test_key')
        mock_cache_set.assert_called_once_with('test_key', {'api': 'data'})

def test_fetch_data_raises_request_exception_on_http_error():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         pytest.raises(requests.exceptions.RequestException):
        with patch('requests.get', side_effect=requests.exceptions.RequestException("HTTP error")):
            fetch_data('http://example.com', 'test_key')

def test_fetch_data_raises_json_decode_error_on_invalid_json():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get, \
         pytest.raises(json.JSONDecodeError):
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        fetch_data('http://example.com', 'test_key')

def test_fetch_data_returns_uncached_data_when_cache_empty():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set') as mock_cache_set, \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'fetched': 'data'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com', 'test_key')
        assert result == {'fetched': 'data'}
        mock_cache_set.assert_called_once_with('test_key', {'fetched': 'data'})

def test_fetch_data_logs_error_on_request_failure(caplog):
    with patch('src.data_fetcher.cache_get', return_value=None), \
         caplog.at_level('ERROR'), \
         patch('requests.get', side_effect=requests.exceptions.RequestException("Network error")):
        with pytest.raises(requests.exceptions.RequestException):
            fetch_data('http://example.com', 'test_key')
        assert "Error fetching data from http://example.com" in caplog.text

def test_fetch_data_logs_cache_hit_when_data_cached(caplog):
    with patch('src.data_fetcher.cache_get') as mock_cache_get, \
         caplog.at_level('INFO'):
        mock_cache_get.return_value = {'cached': 'data'}
        result = fetch_data('http://example.com', 'test_key')
        assert "Cache hit for key: test_key" in caplog.text
        assert result == {'cached': 'data'}

def test_fetch_data_logs_fetching_message(caplog):
    with patch('src.data_fetcher.cache_get', return_value=None), \
         caplog.at_level('INFO'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'api': 'data'}
        mock_get.return_value = mock_response
        
        fetch_data('http://example.com', 'test_key')
        assert "Fetching data from http://example.com" in caplog.text

def test_fetch_data_with_empty_url_and_cache_key():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response
        
        result = fetch_data('', 'test_key')
        assert result == {'data': 'test'}

def test_fetch_data_with_none_url_raises_exception():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         pytest.raises(Exception):
        fetch_data(None, 'test_key')

def test_fetch_data_with_none_cache_key():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com', None)
        assert result == {'data': 'test'}

def test_fetch_data_with_both_none_params():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        result = fetch_data(None, None)
        assert result == {}

def test_fetch_data_with_empty_cache_key():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com', '')
        assert result == {'data': 'test'}

def test_fetch_data_with_special_chars_in_url():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'special': 'chars'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com/path?param=value#anchor', 'special_key')
        assert result == {'special': 'chars'}

def test_fetch_data_with_very_long_url():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'long': 'url'}
        mock_get.return_value = mock_response
        
        long_url = 'http://example.com/' + 'a' * 2000
        result = fetch_data(long_url, 'long_url_key')
        assert result == {'long': 'url'}

def test_fetch_data_with_very_long_cache_key():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set') as mock_cache_set, \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'long_key'}
        mock_get.return_value = mock_response
        
        long_key = 'key_' + 'a' * 2000
        result = fetch_data('http://example.com', long_key)
        assert result == {'data': 'long_key'}
        mock_cache_set.assert_called_once_with(long_key, {'data': 'long_key'})

def test_fetch_data_with_cache_key_containing_spaces():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set') as mock_cache_set, \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'with spaces'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com', 'key with spaces')
        assert result == {'data': 'with spaces'}

def test_fetch_data_with_cache_key_containing_special_chars():
    with patch('src.data_fetcher.cache_get', return_value=None), \
         patch('src.data_fetcher.cache_set'), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'special': 'chars'}
        mock_get.return_value = mock_response
        
        result = fetch_data('http://example.com', 'key/with/special!@#$.chars')
        assert result == {'special': 'chars'}