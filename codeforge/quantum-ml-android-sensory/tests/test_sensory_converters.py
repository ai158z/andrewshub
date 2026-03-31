import numpy as np
import pytest
from unittest.mock import patch, MagicMock
from qml_framework.utils.sensory_converters import SensoryDataConverter

@pytest.fixture
def converter():
    return SensoryDataConverter()

@pytest.fixture
def valid_accel_data():
    return [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

@pytest.fixture
def valid_gyro_data():
    return [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]

def test_convert_accelerometer_data_valid(converter, valid_accel_data):
    result = converter.convert_accelerometer_data(valid_accel_data)
    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 3)
    assert np.all(result >= -1) and np.all(result <= 1)

def test_convert_accelerometer_data_empty(converter):
    with pytest.raises(ValueError, match="Accelerometer data cannot be None or empty"):
        converter.convert_accelerometer_data([])

def test_convert_accelerometer_data_none(converter):
    with pytest.raises(ValueError, match="Accelerometer data cannot be None or empty"):
        converter.convert_accelerometer_data(None)

def test_convert_accelerometer_data_invalid_shape(converter):
    with pytest.raises(ValueError, match="Accelerometer data must be a 2D array with 3 columns"):
        converter.convert_accelerometer_data([[1, 2], [3, 4]])

def test_convert_gyroscope_data_valid(converter, valid_gyro_data):
    result = converter.convert_gyroscope_data(valid_gyro_data)
    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 3)

def test_convert_gyroscope_data_empty(converter):
    with pytest.raises(ValueError, match="Gyroscope data cannot be None or empty"):
        converter.convert_gyroscope_data([])

def test_convert_gyroscope_data_invalid_shape(converter):
    with pytest.raises(ValueError, match="Gyroscope data must be a 2D array with 3 columns"):
        converter.convert_gyroscope_data([[1, 2], [3, 4]])

def test_convert_to_quantum_states_amplitude_encoding(converter):
    data = np.array([1, 2, 3, 4])
    result = converter.convert_to_quantum_states(data, 'amplitude_encoding')
    assert result is not None

def test_convert_to_quantum_states_angle_encoding(converter):
    data = np.array([1, 2, 3, 4])
    result = converter.convert_to_quantum_states(data, 'angle_encoding')
    assert result is not None

def test_convert_to_quantum_states_invalid_method(converter):
    data = np.array([1, 2, 3, 4])
    with pytest.raises(ValueError, match="Unknown encoding method"):
        converter.convert_to_quantum_states(data, 'invalid_method')

def test_convert_to_quantum_states_empty_data(converter):
    with pytest.raises(ValueError, match="Data cannot be None or empty for quantum encoding"):
        converter.convert_to_quantum_states([], 'amplitude_encoding')

def test_convert_gps_data_valid(converter):
    gps_data = {'latitude': 40.7128, 'longitude': -74.0060, 'altitude': 10.0}
    result = converter.convert_gps_data(gps_data)
    assert 'normalized_latitude' in result
    assert 'normalized_longitude' in result
    assert 'normalized_altitude' in result

def test_convert_gps_data_missing_keys(converter):
    gps_data = {'altitude': 10.0}
    with pytest.raises(ValueError, match="Missing required GPS data key"):
        converter.convert_gps_data(gps_data)

def test_convert_gps_data_invalid_type(converter):
    with pytest.raises(ValueError, match="GPS data must be a dictionary"):
        converter.convert_gps_data("invalid_data")

def test_convert_environmental_data_valid(converter):
    env_data = {'temperature': 25.0, 'humidity': 60.0, 'pressure': 1013.0}
    result = converter.convert_environmental_data(env_data)
    assert 'temperature' in result
    assert 'humidity' in result
    assert 'pressure' in result

def test_convert_environmental_data_invalid_type(converter):
    with pytest.raises(ValueError, match="Environmental data must be a dictionary"):
        converter.convert_environmental_data("invalid_data")

def test_batch_convert_sensory_data(converter, valid_accel_data, valid_gyro_data):
    gps_data = {'latitude': 40.7128, 'longitude': -74.0060}
    env_data = {'temperature': 25.0, 'humidity': 60.0}
    
    result = converter.batch_convert_sensory_data(
        accelerometer_data=valid_accel_data,
        gyroscope_data=valid_gyroscope_data,
        gps_data=gps_data,
        env_data=env_data
    )
    
    assert 'accelerometer' in result
    assert 'gyroscope' in result
    assert 'gps' in result
    assert 'environmental' in result

def test_batch_convert_sensory_data_partial(converter, valid_accel_data):
    result = converter.batch_convert_sensory_data(accelerometer_data=valid_accel_data)
    assert 'accelerometer' in result
    assert len(result) == 1

@patch('qml_framework.utils.sensory_converters.logger')
def test_logging(mock_logger, converter):
    data = [[1, 2, 3], [4, 5, 6]]
    converter.convert_accelerometer_data(data)
    mock_logger.debug.assert_called()

def test_get_sensory_converter():
    from qml_framework.utils.sensory_converters import get_sensory_converter
    converter = get_sensory_converter()
    assert isinstance(converter, SensoryDataConverter)