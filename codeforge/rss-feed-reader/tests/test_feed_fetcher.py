import pytest
import requests
import requests_mock
from unittest.mock import patch
from src.feed_fetcher import fetch_feed, fetch_with_retries, is_valid_url

def test_is_valid_url_valid():
    assert is_valid_url("http://example.com/feed") is True
    assert is_valid_url("https://example.com/feed") is True

def test_is_valid_url_invalid():
    assert is_valid_url("") is False
    assert is_valid_url("not_a_url") is False
    assert is_valid_url("http://example.com") is False  # Missing path

def test_fetch_feed_valid_url():
    with requests_mock.Mocker() as m:
        m.get("http://example.com/feed", text="feed content")
        result = fetch_feed("http://example.com/feed")
        assert result == "feed content"

def test_fetch_feed_invalid_url():
    with pytest.raises(ValueError, match="Invalid URL"):
        fetch_feed("invalid_url")

def test_fetch_feed_empty_url():
    with pytest.raises(ValueError, match="URL cannot be empty"):
        fetch_feed("")

def test_fetch_feed_timeout_error():
    with requests_mock.Mocker() as m:
        m.get("http://slow-url.com", exc=requests.exceptions.Timeout)
        with pytest.raises(requests.exceptions.Timeout):
            fetch_feed("http://slow-url.com")

def test_fetch_feed_connection_error():
    with requests_mock.Mocker() as m:
        m.get("http://no-connect.com", exc=requests.exceptions.ConnectionError)
        with pytest.raises(requests.exceptions.ConnectionError):
            fetch_feed("http://no-connect.com")

def test_fetch_feed_invalid_timeout_type():
    with requests_mock.Mocker() as m:
        m.get("http://example.com/feed", text="content")
        result = fetch_feed("http://example.com/feed", timeout="invalid")
        assert result == "content"

def test_fetch_feed_default_timeout():
    with requests_mock.Mocker() as m:
        m.get("http://example.com/feed", text="content")
        result = fetch_feed("http://example.com/feed")
        assert result == "content"

def test_fetch_with_retries_success():
    with requests_mock.Mocker() as m:
        m.get("http://example.com/feed", text="feed content")
        result = fetch_with_retries("http://example.com/feed")
        assert result == "feed content"

def test_fetch_with_retries_failure():
    with requests_mock.Mocker() as m:
        m.get("http://fail.com", exc=requests.exceptions.RequestException)
        with pytest.raises(requests.exceptions.RequestException):
            fetch_with_retries("http://fail.com")

def test_fetch_feed_valid_url_with_path_only():
    # URL with valid structure but no scheme
    with pytest.raises(ValueError, match="Invalid URL"):
        fetch_feed("example.com/feed")

def test_fetch_feed_none_url():
    with pytest.raises(ValueError, match="Invalid URL"):
        fetch_feed(None)

def test_fetch_feed_non_string_input():
    with pytest.raises(ValueError):
        is_valid_url(123)

def test_is_valid_url_edge_cases():
    assert is_valid_url("http://example.com/") is False  # trailing slash only
    assert is_valid_url("http://example.com") is False   # no path
    assert is_valid_url("http:///") is False           # malformed
    assert is_valid_url("https://example.com/feed") is True

def test_fetch_feed_exception_during_request():
    with requests_mock.Mocker() as m:
        m.get("http://error-url.com", exc=Exception)
        with pytest.raises(Exception):
            fetch_feed("http://error-url.com")

def test_fetch_feed_unexpected_exception():
    with requests_mock.Mocker() as m:
        m.get("http://unexpected.com", exc=Exception("Surprise!"))
        with pytest.raises(Exception, match="Surprise!"):
            fetch_with_retries("http://unexpected.com")

def test_fetch_with_retries_no_retry_logic():
    # This test verifies that there are no retries happening
    with requests_mock.Mocker() as m:
        m.get("http://example.com/feed", text="content")
        result = fetch_with_retries("http://example.com/feed")
        assert result == "content"

def test_fetch_feed_logs_and_raises():
    with requests_mock.Mocker() as m, patch('src.feed_fetcher.logger') as mock_logger:
        m.get("http://timeout-url.com", exc=requests.exceptions.Timeout)
        with pytest.raises(requests.exceptions.Timeout):
            fetch_feed("http://timeout-url.com")
        mock_logger.error.assert_called()

def test_fetch_feed_valid_url_with_special_chars():
    with requests_mock.Mocker() as m:
        url = "http://example.com/feed?param=value#fragment"
        m.get(url, text="feed content")
        result = fetch_feed(url)
        assert result == "feed content"