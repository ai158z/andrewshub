import json
import pytest
from src.utils import flatten_dict, read_json_file
from unittest.mock import mock_open, patch

def test_flatten_dict_with_nested_dict():
    d = {"a": {"b": {"c": 1}}, "d": "test"}
    result = flatten_dict(d)
    expected = {"a_b_c": 1, "d": "test"}
    assert result == expected

def test_flatten_dict_type_error_on_non_dict():
    d = "not a dict"
    with pytest.raises(TypeError):
        flatten_dict(d)

def test_flatten_dict_with_list():
    d = {"list": [1, 2, 3], "key": "value"}
    result = flatten_dict(d)
    expected = {"0": 1, "1": 2, "2": 3, "key": "value"}
    assert result == expected

def test_flatten_dict_with_custom_separator():
    d = {"a": {"b": 1}}
    result = flatten_dict(d, separator='.')
    expected = {"a.b": 1}
    assert result == expected

def test_flatten_dict_with_empty_dict():
    d = {}
    result = flatten_dict(d)
    expected = {}
    assert result == expected

def test_flatten_dict_with_none_values():
    d = {"a": None, "b": {"c": None}}
    result = flatten_dict(d)
    expected = {"a": None, "b_c": None}
    assert result == expected

def test_read_json_file_normal():
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        data = read_json_file("test.json")
    expected = {"key": "value"}
    assert data == expected

def test_read_json_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_json_file("nonexistent.json")

def test_read_json_file_invalid_json():
    with patch("builtins.open", mock_open(read_data='{invalid: true}')):
        with pytest.raises(json.JSONDecodeError):
            read_json_file("test.json")

def test_flatten_dict_deeply_nested():
    d = {"a": {"b": {"c": {"d": 1}}}}
    result = flatten_dict(d)
    expected = {"a_b_c_d": 1}
    assert result == expected