import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.backend.codonic.encoding import CodonicEncoder, encode_sensory_input, decode_motor_output

@pytest.fixture
def encoder():
    return CodonicEncoder()

@pytest.fixture
def sample_sensor_data():
    return {
        'timestamp': 1234567890,
        'node_id': 'node_001',
        'position': 150.5,
        'velocity': -45.2,
        'orientation': {'x': 30.1, 'y': -15.7}
    }

def test_encoder_initialization(encoder):
    assert encoder.sensory_symbols['position'] == 'POS'
    assert encoder.motor_symbols['rotation'] == 'ROT'

def test_encode_sensory_input_valid_data(encoder, sample_sensor_data):
    result = encoder.encode_sensory_input(sample_sensor_data)
    assert 'encoded_data' in result
    assert result['timestamp'] == sample_sensor_data['timestamp']
    assert result['node_id'] == sample_sensor_data['node_id']

def test_encode_sensory_input_invalid_type(encoder):
    with pytest.raises(ValueError, match="sensor_data must be a dictionary"):
        encoder.encode_sensory_input("invalid_data")

def test_encode_sensory_input_empty_dict(encoder):
    result = encoder.encode_sensory_input({})
    assert result == {'timestamp': None, 'node_id': None, 'encoded_data': {}}

def test_decode_motor_output_valid_data(encoder):
    encoded = {
        'timestamp': 1234567890,
        'node_id': 'node_001',
        'encoded_data': {
            'POS': 0.87,
            'VEL': -0.12
        }
    }
    result = encoder.decode_motor_output(encoded)
    assert result['timestamp'] == encoded['timestamp']
    assert result['node_id'] == encoded['node_id']
    assert 'POS' in result['decoded_data']

def test_decode_motor_output_invalid_type(encoder):
    with pytest.raises(ValueError, match="encoded_data must be a dictionary"):
        encoder.decode_motor_output("invalid_data")

def test_decode_motor_output_missing_encoded_data_key(encoder):
    with pytest.raises(ValueError, match="encoded_data must contain 'encoded_data' key"):
        encoder.decode_motor_output({'timestamp': 1234567890})

def test_normalize_value_numerical(encoder):
    result = encoder._normalize_value(100)
    expected = 1 / (1 + np.exp(-100/100))
    assert result == expected

def test_normalize_value_non_numerical(encoder):
    result = encoder._normalize_value("test")
    assert result == 0.0

def test_module_level_encode_function(sample_sensor_data):
    result = encode_sensory_input(sample_sensor_data)
    assert 'encoded_data' in result

def test_module_level_decode_function():
    encoded = {
        'timestamp': 1234567890,
        'node_id': 'node_001',
        'encoded_data': {
            'POS': 0.87,
            'VEL': -0.12
        }
    }
    result = decode_motor_output(encoded)
    assert 'decoded_data' in result

@patch('src.backend.codonic.encoding.logger')
def test_encode_logging(mock_logger, encoder, sample_sensor_data):
    encoder.encode_sensory_input(sample_sensor_data)
    mock_logger.debug.assert_called()

@patch('src.backend.codonic.encoding.logger')
def test_decode_logging(mock_logger, encoder):
    encoded = {
        'timestamp': 1234567890,
        'node_id': 'node_001',
        'encoded_data': {
            'POS': 0.87,
            'VEL': -0.12
        }
    }
    encoder.decode_motor_output(encoded)
    mock_logger.debug.assert_called()

def test_encode_sensory_with_vector_data(encoder):
    sensor_data = {
        'position': {'x': 100, 'y': -50},
        'node_id': 'test_node'
    }
    result = encoder.encode_sensory_input(sensor_data)
    assert 'position' in result['encoded_data']

def test_encode_unknown_sensor_type(encoder):
    sensor_data = {
        'unknown_sensor': 'some_value',
        'node_id': 'test_node'
    }
    result = encoder.encode_sensory_input(sensor_data)
    # Unknown sensors should not be in encoded data
    assert 'unknown_sensor' not in result['encoded_data']

def test_decode_unknown_symbol(encoder):
    encoded = {
        'encoded_data': {
            'UNKNOWN': 'test_value'
        }
    }
    result = encoder.decode_motor_output(encoded)
    # Should handle unknown symbols gracefully
    assert 'UNKNOWN' in result['decoded_data']

def test_normalize_edge_cases(encoder):
    # Test with zero
    result = encoder._normalize_value(0)
    assert result == 0.5  # sigmoid(0) = 0.5
    
    # Test with large positive number
    result = encoder._normalize_value(1000)
    assert result == 1.0  # sigmoid of large number approaches 1
    
    # Test with large negative number
    result = encoder._normalize_value(-1000)
    assert result == 0.0  # sigmoid of large negative number approaches 0

def test_encode_with_none_values(encoder):
    sensor_data = {
        'timestamp': None,
        'node_id': None,
        'position': 100
    }
    result = encoder.encode_sensory_input(sensor_data)
    assert result['timestamp'] is None
    assert result['node_id'] is None
    assert 'POS' in result['encoded_data']['encoded_data']

def test_encode_sensory_non_dict_input(encoder):
    with pytest.raises(ValueError):
        encoder.encode_sensory_input("not_a_dict")

def test_decode_motor_non_dict_input(encoder):
    with pytest.raises(ValueError):
        encoder.decode_motor_output("not_a_dict")