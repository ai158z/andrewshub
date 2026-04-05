import pytest
from datetime import datetime
from src.utils import (
    normalize_text, parse_date, is_valid_crypto_symbol, extract_crypto_symbols,
    format_article_summary, get_env_variable, validate_url, sanitize_input,
    truncate_text
)
from unittest.mock import patch


def test_normalize_text_valid_string():
    result = normalize_text("  Hello   World  ")
    assert result == "Hello World"


def test_normalize_text_with_unicode_replacement():
    result = normalize_text("Hello \ufffd World")
    assert result == "Hello  World"


def test_normalize_text_non_string_input():
    with pytest.raises(TypeError):
        normalize_text(123)


def test_parse_date_rfc_format():
    date_str = "Mon, 20 Jan 2020 12:00:00 +0000"
    result = parse_date(date_str)
    assert isinstance(result, datetime)


def test_parse_date_empty_string():
    with pytest.raises(ValueError):
        parse_date("")


def test_parse_date_non_string_input():
    with pytest.raises(TypeError):
        parse_date(123)


def test_parse_date_invalid_format():
    with pytest.raises(ValueError):
        parse_date("invalid date")


def test_is_valid_crypto_symbol_valid():
    assert is_valid_crypto_symbol("BTC") is True


def test_is_valid_crypto_symbol_invalid():
    assert is_valid_crypto_symbol("INVALID") is False


def test_is_valid_crypto_symbol_case_insensitive():
    assert is_valid_crypto_symbol("btc") is True


def test_extract_crypto_symbols():
    symbols = extract_crypto_symbols("Check BTC and ETH prices")
    assert "BTC" in symbols
    assert "ETH" in symbols


def test_format_article_summary():
    article = {
        "title": "Test Article",
        "summary": "This is a test summary with a lot of content that should be truncated",
        "published": "2023-01-01"
    }
    result = format_article_summary(article)
    assert "Title: Test Article" in result
    assert "Date: 2023-01-01" in result
    assert "Summary: This is a..." in result


def test_format_article_summary_empty():
    result = format_article_summary({})
    assert result == ""


def test_get_env_variable_exists():
    with patch.dict("mocked_key", {"mocked_value": "test"}):
        with patch("os.environ", return_value="test"):
            result = get_env_variable("mocked_key", "default")
            assert result == "test"


def test_get_env_variable_default():
    result = get_env_variable("NON_EXISTENT_KEY", "default")
    assert result == "default"


def test_validate_url_valid():
    assert validate_url("https://example.com") is True


def test_validate_url_invalid():
    assert validate_url("") is False
    assert validate_url("not a url") is False


def test_sanitize_input():
    result = sanitize_input("<script>alert('test')</script>")
    assert result == "alert /test"


def test_truncate_text():
    text = "Short text"
    result = truncate_text(text, 5)
    assert result == "Short..."


def test_truncate_text_long():
    text = "This is a very long text that should be truncated"
    result = truncate_text(text, 10)
    assert result == "This is..."


def test_truncate_text_short():
    text = "This is a short text"
    result = truncate_text(text)
    assert result == "This is a short text"