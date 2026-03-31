import pytest
import pandas as pd
from unittest.mock import Mock, patch
import numpy as np

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_list():
    data = [{"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}]
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    processed_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == processed_values

def test_process_sensory_data_invalid_input():
    data = "invalid"
    with pytest.raises(ValueError):
        sensory_processor.process_sensory_data(data)

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    processed_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == processed_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:0Z", "sensor_type": "gyroscope", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "magnetometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values

# Create test
sensory_processor = SensoryInputProcessor()

def test_process_sensory_data_single_dict():
    data = {"timestamp": "2023-01-01T12:00:00Z", "sensor_type": "accelerometer", "values": [1.0, 2.0, 3.0]}
    result = sensory_processor.process_sensory_data(data)
    expected_values = [1.0, 2.0, 3.0]
    assert result["processed_data"][0]["values"] == expected_values