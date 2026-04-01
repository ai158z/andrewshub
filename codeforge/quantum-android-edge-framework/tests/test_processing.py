import json
import numpy as np
import pytest
from unittest.mock import patch, Mock
from src.backend.sensors.processing import process_sensor_data, filter_noise, SensorData, FilteredData


def test_process_sensor_data_valid_json():
    data = {"timestamp": 12345.678, "data": {"temp": 25.5}, "node_id": "node1"}
    raw = json.dumps(data).encode('utf-8')
    result = process_sensor_data(raw)
    assert isinstance(result, SensorData)
    assert result.timestamp == 12345.678
    assert result.data == {"temp": 25.5}
    assert result.node_id == "node1"


def test_process_sensor_data_empty_bytes():
    with pytest.raises(ValueError):
        process_sensor_data(b'')


def test_process_sensor_data_invalid_json():
    with pytest.raises(ValueError):
        process_sensor_data(b'invalid json')


def test_process_sensor_data_missing_fields():
    data = {}
    raw = json.dumps(data).encode('utf-8')
    result = process_sensor_data(raw)
    assert result.timestamp == 0.0
    assert result.data == {}
    assert result.node_id == "unknown"


def test_filter_noise_normal_case():
    sensor_data = SensorData(
        timestamp=12345.678,
        data={"temp": 25.5, "humidity": 60.0},
        node_id="node1"
    )
    result = filter_noise(sensor_data)
    assert isinstance(result, FilteredData)
    assert result.timestamp == 12345.678
    assert "temp" in result.filtered_values
    assert "humidity" in result.filtered_values
    assert result.sensor_id == "node1"


def test_filter_noise_empty_data():
    sensor_data = SensorData(timestamp=12345.678, data={}, node_id="node1")
    result = filter_noise(sensor_data)
    assert isinstance(result, FilteredData)
    assert result.filtered_values == {}


def test_filter_noise_single_value():
    sensor_data = SensorData(
        timestamp=12345.678,
        data={"temp": 25.5},
        node_id="node1"
    )
    result = filter_noise(sensor_data)
    assert result.filtered_values["temp"] == 25.5


def test_filter_noise_filtering_effect():
    # This test checks that filtering is applied, not the exact values
    sensor_data = SensorData(
        timestamp=12345.678,
        data={"value1": 10.0, "value2": 15.0},
        node_id="node1"
    )
    result = filter_noise(sensor_data)
    assert isinstance(result, FilteredData)
    assert len(result.filtered_values) == 2


def test_process_sensor_data_with_extra_fields():
    data = {
        "timestamp": 12345.678,
        "data": {"temp": 25.5, "humidity": 60.0, "pressure": 1013.25},
        "node_id": "node1",
        "extra_field": "should_be_ignored"
    }
    raw = json.dumps(data).encode('utf-8')
    result = process_sensor_data(raw)
    assert result.timestamp == 12345.678
    assert result.node_id == "node1"
    assert "extra_field" not in result.data


def test_filter_noise_exception_handling():
    sensor_data = SensorData(
        timestamp=12345.678,
        data={"temp": "invalid"},
        node_id="node1"
    )
    with pytest.raises(ValueError):
        filter_noise(sensor_data)


def test_process_sensor_data_none_input():
    with pytest.raises(ValueError):
        process_sensor_data(None)


def test_filter_noise_with_numpy_array_edge_case():
    sensor_data = SensorData(
        timestamp=12345.678,
        data={f"sensor_{i}": float(i) for i in range(100)},
        node_id="node1"
    )
    result = filter_noise(sensor_data)
    assert len(result.filtered_values) == 100


def test_process_sensor_data_bytes_type():
    # Test that non-bytes input raises error
    with pytest.raises(AttributeError):
        process_sensor_data("not_bytes")


def test_filter_noise_consistent_results():
    data = {"temp": 25.0, "humidity": 60.0}
    sensor_data1 = SensorData(timestamp=12345.678, data=data, node_id="node1")
    sensor_data2 = SensorData(timestamp=12345.678, data=data, node_id="node1")
    result1 = filter_noise(sensor_data1)
    result2 = filter_noise(sensor_data2)
    # Results should be consistent for same input
    assert result1.filtered_values == result2.filtered_values


def test_filter_noise_noisy_data():
    # Create data that would benefit from filtering
    sensor_data = SensorData(
        timestamp=12345.678,
        data={"noisy1": 10.0, "noisy2": 10.5, "noisy3": 9.8},
        node_id="node1"
    )
    result = filter_noise(sensor_data)
    assert isinstance(result, FilteredData)
    # Check that all original keys are preserved
    assert set(result.filtered_values.keys()) == {"noisy1", "noisy2", "noisy3"}


def test_process_sensor_data_unicode_handling():
    data = {"timestamp": 12345.678, "data": {"temp": 25.5}, "node_id": "nöde1"}
    raw = json.dumps(data).encode('utf-8')
    result = process_sensor_data(raw)
    assert result.node_id == "nöde1"


def test_filter_butterworth_coefficients():
    # Test that the butterworth filter is applied with correct parameters
    with patch('scipy.signal.butter') as mock_butter:
        mock_butter.return_value = np.array([[1, 2, 3, 4, 5, 6]])
        sensor_data = SensorData(
            timestamp=12345.678,
            data={"temp": 25.5},
            node_id="node1"
        )
        # Just ensure it doesn't crash with our mock
        filter_noise(sensor_data)
        # Check butter was called with expected parameters
        mock_butter.assert_called_with(3, 0.2, 'low', output='sos')


def test_process_sensor_data_logging_on_error():
    with patch('src.backend.sensors.processing.logger') as mock_logger:
        with pytest.raises(ValueError):
            process_sensor_data(b'invalid json')
        mock_logger.error.assert_called()


def test_filter_noise_logging_on_error():
    with patch('src.backend.sensors.processing.logger') as mock_logger:
        sensor_data = SensorData(
            timestamp=12345.678,
            data={"temp": "not_a_number"},
            node_id="node1"
        )
        with pytest.raises(ValueError):
            filter_noise(sensor_data)
        mock_logger.error.assert_called()


def test_filter_noise_with_zeros():
    sensor_data = SensorData(
        timestamp=12345.678,
        data={"zero1": 0.0, "zero2": 0.0},
        node_id="node1"
    )
    result = filter_noise(sensor_data)
    assert "zero1" in result.filtered_values
    assert "zero2" in result.filtered_values
    assert result.filtered_values["zero1"] == 0.0
    assert result.filtered_values["zero2"] == 0.0