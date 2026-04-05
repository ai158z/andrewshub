import numpy as np
import pytest
from unittest.mock import patch, MagicMock
from src.utils import calculate_success_rate, normalize_data, format_response

def test_calculate_success_rate_normal_case():
    result = calculate_success_rate(50, 100)
    assert result == 50.0

def test_calculate_success_rate_zero_total():
    result = calculate_success_rate(0, 0)
    assert result == 0.0

def test_calculate_success_rate_zero_success():
    result = calculate_success_rate(0, 100)
    assert result == 0.0

def test_calculate_success_rate_fractional_result():
    result = calculate_success_rate(1, 3)
    assert isinstance(result, float)

def test_normalize_data_empty_list():
    result = normalize_data([])
    assert len(result) == 0
    assert isinstance(result, np.ndarray)

def test_normalize_data_empty_array():
    result = normalize_data(np.array([]))
    assert len(result) == 0
    assert isinstance(result, np.ndarray)

def test_normalize_data_1d_list():
    data = [1, 2, 3, 4, 5]
    result = normalize_data(data)
    assert isinstance(result, np.ndarray)
    assert len(result) == len(data)
    assert np.all(result >= 0) and np.all(result <= 1)

def test_normalize_data_2d_data():
    data = [[1, 2], [3, 4], [5, 6]]
    result = normalize_data(data)
    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 2)

def test_normalize_data_1d_array():
    data = np.array([10, 20, 30])
    result = normalize_data(data)
    assert isinstance(result, np.ndarray)
    assert len(result) == 3
    # Values should be normalized between 0 and 1
    assert np.min(result) >= 0 and np.max(result) <= 1

def test_normalize_data_different_feature_range():
    data = [1, 2, 3, 4, 5]
    result = normalize_data(data, feature_range=(0, 100))
    assert isinstance(result, np.ndarray)
    assert len(result) == 5
    assert np.min(result) >= 0 and np.max(result) <= 100

def test_format_response_normal_case():
    input_data = {"key": "value"}
    result = format_response(input_data)
    assert "status" in result
    assert "data" in result
    assert "message" in result
    assert result["status"] == "success"
    assert result["data"] == input_data

def test_format_response_empty_dict():
    result = format_response({})
    assert result["data"] == {}
    assert result["status"] == "success"

def test_format_response_nested_data():
    input_data = {"level1": {"level2": "value"}}
    result = format_response(input_data)
    assert result["data"] == input_data

def test_calculate_success_rate_high_success():
    result = calculate_success_rate(95, 100)
    assert result == 95.0

def test_calculate_success_rate_low_success():
    result = calculate_success_rate(5, 100)
    assert result == 5.0

def test_normalize_data_single_value():
    data = [42]
    result = normalize_data(data)
    assert len(result) == 1
    assert result[0] == 0  # Single value should normalize to 0

def test_normalize_data_negative_values():
    data = [-10, -5, 0, 5, 10]
    result = normalize_data(data)
    assert isinstance(result, np.ndarray)
    assert len(result) == 5
    assert np.min(result) == 0.0
    assert np.max(result) == 1.0

def test_normalize_data_identical_values():
    data = [5, 5, 5, 5]
    result = normalize_data(data)
    assert isinstance(result, np.ndarray)
    # All identical values should normalize to the same value (typically 0.0)
    assert all(x == 0.0 for x in result)

def test_format_response_none_data():
    result = format_response(None)
    assert result["data"] is None

def test_format_response_large_data():
    large_data = {"items": list(range(1000))}
    result = format_response(large_data)
    assert "items" in result["data"]
    assert len(result["data"]["items"]) == 1000