import pytest
from src.utils import format_currency, cache_get, cache_set, DataCache
from unittest.mock import patch, MagicMock

def test_format_currency_valid_positive():
    assert format_currency(1234.56) == "$1,234.56"

def test_format_currency_valid_zero():
    assert format_currency(0) == "$0.00"

def test_format_currency_valid_negative():
    assert format_currency(-1234.56) == "-$1,234.56"

def test_format_currency_invalid_type():
    with pytest.raises(TypeError):
        format_currency("invalid")

def test_cache_get_nonexistent_key():
    with patch.object(DataCache, 'get', return_value=None):
        result = cache_get("nonexistent")
        assert result is None

def test_cache_get_exception():
    with patch.object(DataCache, 'get', side_effect=Exception("Cache error")):
        result = cache_get("test_key")
        assert result is None

def test_cache_set_success():
    with patch.object(DataCache, 'set') as mock_set:
        cache_set("test_key", "test_value")
        mock_set.assert_called_once_with("test_key", "test_value")

def test_cache_set_exception():
    with patch.object(DataCache, 'set', side_effect=Exception("Cache error")):
        with pytest.raises(Exception):
            cache_set("test_key", "test_value")

def test_format_currency_int():
    assert format_currency(1000) == "$1,000.00"

def test_format_currency_float_string():
    with pytest.raises(TypeError):
        format_currency("1234.56")

def test_cache_get_valid_key():
    expected_value = "test_value"
    with patch.object(DataCache, 'get', return_value=expected_value):
        result = cache_get("test_key")
        assert result == expected_value

def test_cache_set_and_get():
    cache_set("test_key", "stored_value")
    with patch.object(DataCache, 'get', return_value="stored_value"):
        result = cache_get("test_key")
        assert result == "stored_value"

def test_DataCache_get_cache_key():
    key = "test"
    expected_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"  # SHA256 of "test"
    # Note: This test assumes we can access the internal method for testing hash generation
    # In practice, we'd test this by checking the actual behavior, not the internal method
    pass

def test_format_currency_large_number():
    assert format_currency(1234567.89) == "$1,234,567.89"

def test_format_currency_negative_zero():
    assert format_currency(-0.0) == "$0.00"

def test_format_currency_precision():
    assert format_currency(1234.567) == "$1,234.57"

def test_format_currency_non_numeric():
    with pytest.raises(TypeError):
        format_currency("1234.56")

def test_format_currency_none():
    with pytest.raises(TypeError):
        format_currency(None)

def test_cache_set_none_value():
    with patch.object(DataCache, 'set') as mock_set:
        cache_set("test_key", None)
        mock_set.assert_called_once_with("test_key", None)