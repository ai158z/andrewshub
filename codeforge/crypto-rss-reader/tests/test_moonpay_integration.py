import pytest
from unittest.mock import patch, MagicMock
from src.moonpay_integration import is_payment_relevant, send_alert, _extract_cryptocurrencies

def test_is_payment_relevant_with_payment_keyword_in_title():
    article = {"title": "How to buy Bitcoin with credit card", "summary": "A simple guide"}
    assert is_payment_relevant(article) is True

def test_is_payment_relevant_with_payment_keyword_in_summary():
    article = {"title": "Crypto News", "summary": "You can now purchase crypto with bank transfer"}
    assert is_payment_relevant(article) is True

def test_is_payment_relevant_without_payment_keywords():
    article = {"title": "Market Analysis", "summary": "Latest trends in technology"}
    assert is_payment_relevant(article) is False

def test_is_payment_relevant_empty_article():
    article = {}
    assert is_payment_relevant(article) is False

def test_is_payment_relevant_case_insensitive():
    article = {"title": "BUY CRYPTO EASY", "summary": "Guide for beginners"}
    assert is_payment_relevant(article) is True

def test_send_alert_missing_api_key():
    article = {"title": "Test", "summary": "Test article"}
    result = send_alert(article, "")
    assert result is False

@patch('requests.post')
def test_send_alert_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    article = {"title": "Test", "summary": "Test article", "link": "http://test.com", "published": "2023-01-01", "source": "TestSource"}
    result = send_alert(article, "valid_api_key")
    assert result is True

@patch('requests.post')
def test_send_alert_api_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_post.return_value = mock_response
    
    article = {"title": "Test", "summary": "Test article"}
    result = send_alert(article, "valid_api_key")
    assert result is False

@patch('requests.post')
def test_send_alert_network_error(mock_post):
    mock_post.side_effect = Exception("Network error")
    
    article = {"title": "Test", "summary": "Test article"}
    result = send_alert(article, "valid_api_key")
    assert result is False

def test_extract_cryptocurrencies_found():
    article = {"title": "Bitcoin and Ethereum rise", "summary": "BTC and ETH see gains"}
    result = _extract_cryptocurrencies(article)
    assert "Bitcoin" in result
    assert "Ethereum" in result

def test_extract_cryptocurrencies_none_found():
    article = {"title": "Normal news", "summary": "No crypto content here"}
    result = _extract_cryptocurrencies(article)
    assert result == []

def test_extract_cryptocurrencies_case_insensitive():
    article = {"title": "BITCOIN NEWS", "summary": "Bitcoin is rising"}
    result = _extract_cryptocurrencies(article)
    assert "Bitcoin" in result

@patch('requests.post')
def test_send_alert_returns_false_when_exception(mock_post):
    mock_post.side_effect = Exception("API Error")
    article = {"title": "Test", "summary": "Test article"}
    result = send_alert(article, "valid_api_key")
    assert result is False

def test_send_alert_with_valid_data():
    article = {"title": "Payment Methods for Crypto", "summary": "How to use bank transfer for crypto purchases"}
    result = is_payment_relevant(article)
    assert result is True

def test_send_alert_with_no_relevant_content():
    article = {"title": "Random News", "summary": "Just random stuff"}
    result = is_payment_relevant(article)
    assert result is False

@patch('requests.post')
def test_send_alert_headers_correctly_set(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    article = {"title": "Test", "summary": "Test article", "link": "http://test.com", "published": "2023-01-01", "source": "TestSource"}
    send_alert(article, "valid_api_key")
    
    args, kwargs = mock_post.call_args
    assert "Authorization" in kwargs['headers']
    assert "Bearer valid_api_key" == kwargs['headers']['Authorization']
    assert kwargs['headers']['Content-Type'] == "application/json"

def test_send_alert_with_none_article_values():
    article = {"title": None, "summary": None, "link": None, "published": None, "source": None}
    result = send_alert(article, "valid_api_key")
    assert result is False

def test_send_alert_with_empty_article():
    article = {}
    result = send_alert(article, "valid_api_key")
    assert result is False

def test_extract_cryptocurrencies_from_title_and_summary():
    article = {"title": "Ethereum and Bitcoin", "summary": "SOL and ADA also mentioned"}
    result = _extract_cryptocurrencies(article)
    assert "Ethereum" in result
    assert "Bitcoin" in result
    assert "SOL" in result
    assert "ADA" in result

def test_is_payment_relevant_partial_keyword_match():
    article = {"title": "purchase orders", "summary": "How to handle payments"}
    assert is_payment_relevant(article) is True

def test_is_payment_relevant_multiple_keywords():
    article = {"title": "buy and sell crypto", "summary": "transaction processing"}
    assert is_payment_relevant(article) is True