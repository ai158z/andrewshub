import pytest
import requests
import requests_mock
from unittest.mock import patch, MagicMock
from src.data_fetcher import fetch_data
from src.utils import cache_get, cache_set


def test_fetch_data_success():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            data = fetch_data(url, cache_key)
            assert data == test_response
            mock_cache_set.assert_called_with(cache_key, test_response)


def test_fetch_data_from_cache():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=test_response):
        with patch("src.utils.cache_set") as mock_cache_set:
            with requests_mock.Mocker() as m:
                m.get(url, json=test_response)
                data = fetch_data(url, cache_key)
                assert data == test_response
                # Should not call cache_set again when data comes from cache
                mock_cache_set.assert_not_called()


def test_fetch_data_network_error():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set"):
        with requests_mock.Mocker() as m:
            m.get(url, exc=requests.exceptions.ConnectionError)
            with pytest.raises(requests.exceptions.ConnectionError):
                fetch_data(url, cache_key)


def test_fetch_data_invalid_url():
    url = "invalid-url"
    cache_key = "test_data"
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set"):
        with requests_mock.Mocker() as m:
            m.get(url, status_code=404)
            with pytest.raises(requests.exceptions.HTTPError):
                fetch_data(url, cache_key)


def test_fetch_data_empty_response():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, text="")
            data = fetch_data(url, cache_key)
            assert data == ""
            mock_cache_set.assert_called_with(cache_key, "")


def test_fetch_data_cache_set_failure():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set", side_effect=Exception("Cache set failed")):
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            # Should still return data even if cache set fails
            data = fetch_data(url, cache_key)
            assert data == test_response


def test_fetch_data_with_none_cache_key():
    url = "https://api.example.com/data"
    cache_key = None
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            data = fetch_data(url, cache_key)
            assert data == test_response
            # When cache_key is None, cache_set should not be called
            mock_cache_set.assert_not_called()


def test_fetch_data_cache_get_exception():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", side_effect=Exception("Cache get failed")), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            data = fetch_data(url, cache_key)
            assert data == test_response
            mock_cache_set.assert_called_with(cache_key, test_response)


def test_fetch_data_with_existing_cache():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"cached": "data"}
    
    with patch("src.utils.cache_get", return_value=test_response):
        with patch("src.utils.cache_set") as mock_cache_set:
            with requests_mock.Mocker() as m:
                m.get(url, json={"new": "data"})
                data = fetch_data(url, cache_key)
                assert data == test_response
                # Should not call cache_set when data comes from cache
                mock_cache_set.assert_not_called()


def test_fetch_data_cache_miss_then_hit():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    # First call - cache miss
    with patch("src.utils.cache_get", return_value=None) as mock_cache_get, \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            # First request - should fetch and cache
            data = fetch_data(url, cache_key)
            assert data == test_response
            mock_cache_set.assert_called_with(cache_key, test_response)
            
            # Reset mock to track subsequent calls
            mock_cache_set.reset_mock()
            
            # Second call - should hit cache
            mock_cache_get.return_value = test_response
            data = fetch_data(url, cache_key)
            assert data == test_response
            mock_cache_set.assert_not_called()


def test_fetch_data_multiple_urls():
    url1 = "https://api.example.com/data1"
    url2 = "https://api.example.com/data2"
    cache_key1 = "data1"
    cache_key2 = "data2"
    test_response1 = {"data": "value1"}
    test_response2 = {"data": "value2"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url1, json=test_response1)
            m.get(url2, json=test_response2)
            
            data1 = fetch_data(url1, cache_key1)
            data2 = fetch_data(url2, cache_key2)
            
            assert data1 == test_response1
            assert data2 == test_response2


def test_fetch_data_json_decode_error():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set"):
        with requests_mock.Mocker() as m:
            m.get(url, text="invalid json")
            with pytest.raises(requests.exceptions.JSONDecodeError):
                fetch_data(url, cache_key)


def test_fetch_data_with_headers():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response, headers={'Content-Type': 'application/json'})
            data = fetch_data(url, cache_key)
            assert data == test_response


def test_fetch_data_timeout():
    url = "https://slow-api.example.com/data"
    cache_key = "test_data"
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set"):
        with requests_mock.Mocker() as m:
            m.get(url, exc=requests.exceptions.Timeout)
            with pytest.raises(requests.exceptions.Timeout):
                fetch_data(url, cache_key)


def test_fetch_data_redirect():
    url = "https://api.example.com/data"
    redirect_url = "https://api.new-example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, status_code=301, headers={'Location': redirect_url})
            m.get(redirect_url, json=test_response)
            data = fetch_data(url, cache_key)
            assert data == test_response
            mock_cache_set.assert_called_with(cache_key, test_response)


def test_fetch_data_with_none_response():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=None)
            data = fetch_data(url, cache_key)
            assert data is None
            mock_cache_set.assert_called_with(cache_key, None)


def test_fetch_data_concurrent_calls():
    url = "https://api.example.com/data"
    cache_key = "test_data"
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None) as mock_cache_get, \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            # Simulate concurrent access by calling twice
            data1 = fetch_data(url, cache_key)
            mock_cache_get.return_value = test_response
            data2 = fetch_data(url, cache_key)
            
            assert data1 == test_response
            assert data2 == test_response


def test_fetch_data_empty_cache_key():
    url = "https://api.example.com/data"
    cache_key = ""
    test_response = {"key": "value"}
    
    with patch("src.utils.cache_get", return_value=None), \
         patch("src.utils.cache_set") as mock_cache_set:
        with requests_mock.Mocker() as m:
            m.get(url, json=test_response)
            data = fetch_data(url, cache_key)
            assert data == test_response
            # Even with empty cache_key, should still cache the data
            if cache_key:  # Only cache if cache_key is not empty
                mock_cache_set.assert_called_with(cache_key, test_response)
            else:
                mock_cache_set.assert_not_called()