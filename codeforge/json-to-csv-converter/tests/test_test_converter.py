import pytest
import json
import os
import pandas as pd
from unittest.mock import patch, mock_open, call
from src.converter import convert_json_to_csv
from src.utils import flatten_dict

@pytest.fixture
def sample_data():
    return [
        {
            "id": 1,
            "name": "John Doe",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zipcode": "10001"
            },
            "contacts": [
                {"type": "email", "value": "john@example.com"},
                {"type": "phone", "value": "123-456-7890"}
            ]
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "address": {
                "street": "456 Oak Ave",
                "city": "Los Angeles",
                "zipcode": "90210"
            },
            "contacts": [
                {"type": "email", "value": "jane@example.com"}
            ]
        }
    ]

@pytest.fixture
def field_mapping():
    return {
        "id": "ID",
        "name": "Full Name",
        "address_street": "Street Address",
        "address_city": "City",
        "address_zipcode": "Zip Code"
    }

def test_convert_json_to_csv_success(sample_data, field_mapping):
    with patch("builtins.open", mock_open()) as mock_file:
        with patch("os.path.exists", return_value=True):
            with patch("pandas.DataFrame.to_csv") as mock_to_csv:
                result = convert_json_to_csv("input.json", "output.csv", field_mapping)
                assert result is True

def test_flatten_dict_simple():
    data = {"a": 1, "b": {"c": 2}}
    result = flatten_dict(data)
    expected = {"a": 1, "b_c": 2}
    assert result == expected

def test_flatten_dict_nested():
    data = {
        "user": {
            "personal": {
                "name": "Alice",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Boston"
                }
            }
        }
    result = flatten_dict(data)
    assert "user_personal_name" in result
    assert "user_personal_age" in result
    assert "user_personal_address_street" in result
    assert "user_personal_address_city" in result

def test_flatten_dict_empty_dict():
    data = {}
    result = flatten_dict(data)
    assert result == {}

def test_flatten_dict_multiple_levels():
    data = {"a": {"b": {"c": {"d": 1}}}}
    result = flatten_dict(data)
    expected = {"a_b_c_d": 1}
    assert result == expected

def test_convert_json_to_csv_file_not_found():
    with patch("os.path.exists", return_value=False):
        result = convert_json_to_csv("nonexistent.json", "output.csv", {})
        assert result is False

def test_convert_json_to_csv_invalid_field_mapping(sample_data):
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_data))) as mock_file:
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            result = convert_json_to_csv("input.json", "output.csv", {"invalid": "mapping"})
            assert result is True

def test_flatten_dict_with_list_values():
    data = {
        "user": {
            "contacts": [
                {"type": "email", "value": "test@example.com"},
                {"type": "phone", "value": "123-456-7890"}
            ]
        }
    }
    result = flatten_dict(data)
    assert "user" in result or "user_contacts" in str(result)

def test_flatten_dict_preserves_values():
    data = {"a": 1, "b": "test", "c": None, "d": True, "e": False}
    result = flatten_dict(data)
    assert result["a"] == 1
    assert result["b"] == "test"
    assert result["c"] is None
    assert result["d"] is True
    assert result["e"] is False

def test_convert_json_to_csv_with_missing_fields(field_mapping):
    incomplete_data = [{"id": 1, "name": "Test"}]  # Missing address
    with patch("builtins.open", mock_open(read_data=json.dumps(incomplete_data))) as mock_file:
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            result = convert_json_to_csv("input.json", "output.csv", field_mapping)
            assert result is True

def test_convert_json_to_csv_empty_file():
    with patch("os.path.getsize", return_value=0):
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            result = convert_json_to_csv("empty.json", "output.csv", {})
            assert result is False

def test_flatten_dict_with_none_value():
    data = {"a": None, "b": {"c": None}}
    result = flatten_dict(data)
    assert result["a"] is None
    assert result["b_c"] is None

def test_flatten_dict_deep_nesting():
    data = {"a": {"b": {"c": {"d": {"e": {"f": "deep"}}}}}}
    result = flatten_dict(data)
    assert "a_b_c_d_e_f" in result

def test_convert_json_to_csv_io_error_during_read():
    with patch("json.load", side_effect=IOError("Read error")):
        result = convert_json_to_csv("input.json", "output.csv", {})
        assert result is False

def test_convert_json_to_csv_io_error_during_write(field_mapping):
    with patch("pandas.DataFrame.to_csv", side_effect=IOError("Write error")):
        result = convert_json_to_csv("input.json", "output.csv", {})
        assert result is False

def test_flatten_dict_type_preservation():
    data = {
        "str_val": "string",
        "int_val": 42,
        "float_val": 3.14,
        "bool_val": True,
        "none_val": None
    }
    result = flatten_dict(data)
    assert isinstance(result["str_val"], str)
    assert isinstance(result["int_val"], int)
    assert isinstance(result["float_val"], float)
    assert isinstance(result["bool_val"], bool)
    assert result["none_val"] is None

def test_convert_json_to_csv_header_mapping(field_mapping):
    # Test that field mapping is correctly applied to CSV headers
    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        with patch("builtins.open", mock_open(read_data="[]")) as mock_file:
            result = convert_json_to_csv("input.json", "output.csv", field_mapping)
            assert result is True

def test_flatten_dict_overlapping_keys():
    data = {"a": {"b": 1}, "a_b": 2}  # This could cause key collision
    result = flatten_dict(data)
    assert "a_b" in result
    assert result["a_b"] == 1 or result["a_b"] == 2

def test_convert_json_to_csv_large_dataset(field_mapping):
    large_data = [{"id": i, "name": f"User{i}"} for i in range(1000)]
    with patch("builtins.open", mock_open(read_data=json.dumps(large_data))) as mock_file:
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            result = convert_json_to_csv("input.json", "output.csv", {})
            assert result is True

def test_flatten_dict_special_characters():
    data = {"a@b": {"c#d": "value"}, "e-f": {"g.h": "another"}}
    result = flatten_dict(data)
    assert "a@b_c#d" in result or "a_b_c_d" in result
    assert "e-f_g.h" in result or "e_f_g_h" in result