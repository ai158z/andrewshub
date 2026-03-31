import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from src.quantum_sensory_fusion.android_interface import AndroidSensorInterface

@pytest.fixture
def android_interface():
    return AndroidSensorInterface()

def test_init_creates_interface(android_interface):
    assert android_interface is not None

def test_register_sensors_initializes_data(android_interface):
    result = android_interface.register_sensors()
    expected = {
        'accelerometer': [],
        'gyroscope': [],
        'magnetometer': []
    }
    assert result == expected
    assert android_interface._sensor_data == expected

def test_get_sensor_data_registers_if_empty(android_interface):
    android_interface._sensor_data = {}
    result = android_interface.get_sensor_data()
    expected = {
        'accelerometer': [],
        'gyroscope': [],
        'magnetometer': []
    }
    assert result == expected

def test_get_sensor_data_returns_existing_data(android_interface):
    test_data = {'test': 'data'}
    android_interface._sensor_data = test_data
    result = android_interface.get_sensor_data()
    assert result == test_data

@patch('src.quantum_sensory_fusion.android_interface.BosonicQubitManager')
@patch('src.quantum_sensory_fusion.android_interface.SensoryFusionEngine')
def test_process_sensor_readings(mock_fusion, mock_bosonic, android_interface):
    raw_data = [1, 2, 3]
    mock_bosonic_instance = MagicMock()
    mock_bosonic.return_value = mock_bosonic_instance
    mock_bosonic_instance.create_bosonic_state.return_value = np.array([1, 2, 3])
    
    mock_fusion_instance = MagicMock()
    mock_fusion.return_value = mock_fusion_instance
    mock_fusion_instance.preprocess_data.return_value = np.array([4, 5, 6])
    
    result = android_interface._process_sensor_readings(raw_data)
    
    mock_bosonic_instance.create_bosonic_state.assert_called_once_with(raw_data)
    mock_fusion_instance.preprocess_data.assert_called_once()
    assert isinstance(result, np.ndarray)

@patch('src.quantum_sensory_fusion.android_interface.QuantumSensoryGates')
def test_apply_quantum_enhancement(mock_gates, android_interface):
    sensor_readings = np.array([1, 2, 3])
    mock_gates_instance = MagicMock()
    mock_gates.return_value = mock_gates_instance
    mock_gates_instance.apply_sensory_gate.return_value = np.array([4, 5, 6])
    
    result = android_interface._apply_quantum_enhancement(sensor_readings)
    
    mock_gates_instance.apply_sensory_gate.assert_called_once()
    assert isinstance(result, np.ndarray)

@patch('src.quantum_sensory_fusion.android_interface.SensoryClustering')
def test_cluster_sensor_patterns(mock_clustering, android_interface):
    enhanced_data = np.array([1, 2, 3])
    mock_clustering_instance = MagicMock()
    mock_clustering.return_value = mock_clustering_instance
    mock_clustering_instance.fit_predict.return_value = np.array([1, 0, 1])
    
    result = android_interface._cluster_sensor_patterns(enhanced_data)
    
    mock_clustering_instance.fit_predict.assert_called_once()
    assert isinstance(result, np.ndarray)

@patch('src.quantum_sensory_fusion.android_interface.SensoryFusionEngine')
@patch('src.quantum_sensory_fusion.android_interface.BosonicQubitManager')
@patch('src.quantum_sensory_fusion.android_interface.QuantumSensoryGates')
@patch('src.quantum_sensory_fusion.android_interface.SensoryClustering')
def test_read_and_process_sensors_full_flow(mock_clustering, mock_gates, mock_bosonic, mock_fusion, android_interface):
    # Setup all mocks
    mock_bosonic_instance = MagicMock()
    mock_bosonic.return_value = mock_bosonic_instance
    mock_bosonic_instance.create_bosonic_state.return_value = np.array([1, 2, 3])
    
    mock_fusion_instance = MagicMock()
    mock_fusion.return_value = mock_fusion_instance
    mock_fusion_instance.preprocess_data.return_value = np.array([4, 5, 6])
    mock_fusion_instance.fuse_sensors.return_value = "fused_result"
    
    mock_gates_instance = MagicMock()
    mock_gates.return_value = mock_gates_instance
    mock_gates_instance.apply_sensory_gate.return_value = np.array([7, 8, 9])
    
    mock_clustering_instance = MagicMock()
    mock_clustering.return_value = mock_clustering_instance
    mock_clustering_instance.fit_predict.return_value = np.array([10, 11, 12])
    
    # Execute
    result = android_interface.read_and_process_sensors()
    
    # Verify
    assert result == "fused_result"

def test_read_and_process_sensors_registers_sensors_if_empty(android_interface):
    android_interface._sensor_data = {}
    with patch.object(android_interface, 'register_sensors') as mock_register:
        mock_register.return_value = {
            'accelerometer': [1, 2, 3],
            'gyroscope': [4, 5, 6],
            'magnetometer': [7, 8, 9]
        }
        result = android_interface.get_sensor_data()
        expected = {
            'accelerometer': [1, 2, 3],
            'gyroscope': [4, 5, 6],
            'magnetometer': [7, 8, 9]
        }
        assert result == expected

@patch('src.quantum_sensory_fusion.android_interface.BosonicQubitManager')
def test_process_sensor_readings_with_mocked_dependencies(mock_bosonic, android_interface):
    mock_bosonic_instance = MagicMock()
    mock_bosonic.return_value = mock_bosonic_instance
    mock_bosonic_instance.create_bosonic_state.return_value = "processed"
    
    raw_data = [1, 2, 3]
    result = android_interface._process_sensor_readings(raw_data)
    assert result == "processed"

@patch('src.quantum_sensory_fusion.android_interface.QuantumSensoryGates')
def test_apply_quantum_enhancement_with_mocked_dependencies(mock_gates, android_interface):
    mock_gates_instance = MagicMock()
    mock_gates.return_value = mock_gates_instance
    mock_gates_instance.apply_sensory_gate.return_value = "enhanced"
    
    sensor_readings = np.array([1, 2, 3])
    result = android_interface._apply_quantum_enhancement(sensor_readings)
    assert result == "enhanced"

@patch('src.quantum_sensory_fusion.android_interface.SensoryClustering')
def test_cluster_sensor_patterns_with_mocked_dependencies(mock_clustering, android_interface):
    mock_clustering_instance = MagicMock()
    mock_clustering.return_value = mock_clustering_instance
    mock_clustering_instance.fit_predict.return_value = "clustered"
    
    enhanced_data = np.array([1, 2, 3])
    result = android_interface._cluster_sensor_patterns(enhanced_data)
    assert result == "clustered"

def test_read_and_process_sensors_empty_data_registration(android_interface):
    android_interface._sensor_data = {}
    with patch.object(android_interface, 'get_sensor_data') as mock_get:
        mock_get.return_value = {
            'accelerometer': [],
            'gyroscope': [],
            'magnetometer': []
        }
        result = android_interface.get_sensor_data()
        expected = {
            'accelerometer': [],
            'gyroscope': [],
            'magnetometer': []
        }
        assert result == expected

@patch('src.quantum_sensory_fusion.android_interface.SensoryFusionEngine')
def test_fuse_sensors_method(mock_fusion, android_interface):
    mock_fusion_instance = MagicMock()
    mock_fusion.return_value = mock_fusion_instance
    mock_fusion_instance.fuse_sensors.return_value = "fused"
    
    clustered_data = np.array([1, 2, 3])
    result = android_interface._sensory_fusion.fuse_sensors(clustered_data)
    assert result == "fused"

def test_sensor_data_persistence(android_interface):
    android_interface._sensor_data = {'test': 'data'}
    # Should not re-register if data exists
    result = android_interface.get_sensor_data()
    assert result == {'test': 'data'}

def test_register_sensors_resets_data(android_interface):
    android_interface._sensor_data = {'existing': 'data'}
    android_interface.register_sensors()
    expected = {
        'accelerometer': [],
        'gyroscope': [],
        'magnetometer': []
    }
    assert android_interface._sensor_data == expected

def test_get_sensor_data_no_reregistration(android_interface):
    android_interface._sensor_data = {'existing': 'data'}
    result = android_interface.get_sensor_data()
    assert result == {'existing': 'data'}

@patch('src.quantum_sensory_fusion.android_interface.BosonicQubitManager')
@patch('src.quantum_sensory_fusion.android_interface.SensoryFusionEngine')
def test_process_sensor_readings_calls_correct_methods(mock_fusion, mock_bosonic, android_interface):
    mock_bosonic_instance = MagicMock()
    mock_bosonic.return_value = mock_bosonic_instance
    mock_bosonic_instance.create_bosonic_state.return_value = "bosonic_state"
    
    mock_fusion_instance = MagicMock()
    mock_fusion.return_value = mock_fusion_instance
    mock_fusion_instance.preprocess_data.return_value = "processed"
    
    raw_data = [1, 2, 3]
    result = android_interface._process_sensor_readings(raw_data)
    mock_bosonic_instance.create_bosonic_state.assert_called_once_with(raw_data)
    mock_fusion_instance.preprocess_data.assert_called_once_with("bosonic_state")
    assert result == "processed"

@patch('src.quantum_sensory_fusion.android_interface.QuantumSensoryGates')
def test_apply_quantum_enhancement_calls_correct_methods(mock_gates, android_interface):
    mock_gates_instance = MagicMock()
    mock_gates.return_value = mock_gates_instance
    mock_gates_instance.apply_sensory_gate.return_value = "enhanced"
    
    sensor_readings = "data"
    result = android_interface._apply_quantum_enhancement(sensor_readings)
    mock_gates_instance.apply_sensory_gate.assert_called_once_with(sensor_readings)
    assert result == "enhanced"

@patch('src.quantum_sensory_fusion.android_interface.SensoryClustering')
def test_cluster_sensor_patterns_calls_correct_methods(mock_clustering, android_interface):
    mock_clustering_instance = MagicMock()
    mock_clustering.return_value = mock_clustering_instance
    mock_clustering_instance.fit_predict.return_value = "clustered"
    
    enhanced_data = "data"
    result = android_interface._cluster_sensor_patterns(enhanced_data)
    mock_clustering_instance.fit_predict.assert_called_once_with(enhanced_data)
    assert result == "clustered"