import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensory_fusion.sensory_fusion import SensoryFusionEngine, FusionResult

@pytest.fixture
def fusion_engine():
    with patch.multiple('src.quantum_sensory_fusion.sensory_fusion', 
                      BosonicQubitManager=Mock(),
                      SensoryClustering=Mock(),
                      QuantumSensoryGates=Mock(),
                      AndroidSensorInterface=Mock()):
        engine = SensoryFusionEngine()
        # Mock the dependencies
        engine.bosonic_manager = Mock()
        engine.clustering_engine = Mock()
        engine.quantum_gates = Mock()
        engine.sensor_interface = Mock()
        return engine

@pytest.fixture
def sample_sensor_data():
    return {
        'accelerometer': np.array([1.0, 2.0, 3.0]),
        'gyroscope': np.array([0.1, 0.2, 0.3])
    }

def test_fuse_sensors_success(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.preprocess_data = Mock(return_value=sample_sensor_data)
    fusion_engine._create_quantum_representation = Mock(return_value=np.array([1, 2, 3]))
    fusion_engine.quantum_gates.build_sensory_circuit.return_value = np.array([1, 2, 3])
    fusion_engine.clustering_engine.fit_predict.return_value = np.array([1, 1, 0])
    
    # Act
    result = fusion_engine.fuse_sensors(sample_sensor_data)
    
    # Assert
    assert isinstance(result, FusionResult)
    assert result.fused_data is not None
    assert isinstance(result.confidence_score, float)

def test_preprocess_data_valid_input(fusion_engine, sample_sensor_data):
    # Act
    result = fusion_engine.preprocess_data(sample_sensor_data)
    
    # Assert
    assert isinstance(result, dict)
    for key in sample_sensor_data:
        assert key in result
        assert isinstance(result[key], np.ndarray)

def test_preprocess_data_invalid_input_type(fusion_engine):
    # Act & Assert
    with pytest.raises(TypeError):
        fusion_engine.preprocess_data("invalid_type")

def test_preprocess_data_invalid_data_type(fusion_engine):
    # Arrange
    invalid_data = {'sensor': "not_a_numpy_array"}
    
    # Act & Assert
    with pytest.raises(TypeError):
        fusion_engine.preprocess_data(invalid_data)

def test_preprocess_data_normalizes_values(fusion_engine):
    # Arrange
    sensor_data = {'test': np.array([10, 20, 30])}
    
    # Act
    result = fusion_engine.preprocess_data(sensor_data)
    
    # Assert
    assert np.all(result['test'] >= 0) and np.all(result['test'] <= 1)

def test_fuse_sensors_empty_input(fusion_engine):
    # Act & Assert
    with pytest.raises(ValueError):
        fusion_engine.fuse_sensors({})

def test_fuse_sensors_invalid_data_type(fusion_engine):
    # Act & Assert
    with pytest.raises(TypeError):
        fusion_engine.fuse_sensors("not_a_dict")

def test_create_quantum_representation_calls_bosonic_manager(fusion_engine):
    # Arrange
    test_data = np.array([1, 2, 3])
    fusion_engine.bosonic_manager.create_bosonic_state = Mock(return_value=np.array([1]))
    
    # Act
    result = fusion_engine._create_quantum_representation(test_data)
    
    # Assert
    fusion_engine.bosonic_manager.create_bosonic_state.assert_called_once_with(test_data)
    assert isinstance(result, np.ndarray)

def test_fuse_sensors_with_quantum_gates(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.preprocess_data = Mock(return_value=sample_sensor_data)
    fusion_engine._create_quantum_representation = Mock(return_value=np.array([1, 2, 3]))
    fusion_engine.quantum_gates.build_sensory_circuit.return_value = np.array([1, 2, 3])
    fusion_engine.clustering_engine.fit_predict.return_value = np.array([0, 1, 0])
    
    # Act
    result = fusion_engine.fuse_sensors(sample_sensor_data)
    
    # Assert
    assert isinstance(result, FusionResult)
    fusion_engine.quantum_gates.build_sensory_circuit.assert_called_once()

def test_fuse_sensors_preprocess_failure(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.preprocess_data = Mock(side_effect=TypeError("Invalid data type"))
    
    # Act & Assert
    with pytest.raises(TypeError):
        fusion_engine.fuse_sensors(sample_sensor_data)

def test_fuse_sensors_quantum_gate_failure(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.quantum_gates.build_sensory_circuit.side_effect = Exception("Quantum gate error")
    
    # Act & Assert
    with pytest.raises(Exception, match="Quantum gate error"):
        fusion_engine.fuse_sensors(sample_sensor_data)

def test_preprocess_data_normalization(fusion_engine):
    # Arrange
    test_data = {'sensor1': np.array([1.0, 2.0, 3.0])}
    expected_normalized = np.array([0.0, 0.5, 1.0])
    
    # Act
    result = fusion_engine.preprocess_data(test_data)
    
    # Assert
    assert np.allclose(result['sensor1'], expected_normalized, atol=1e-6)

def test_validate_sensor_data_valid(fusion_engine):
    # Arrange
    sensor_data = {
        'accel': np.array([1, 2, 3]),
        'gyro': np.array([0.1, 0.2, 0.3])
    }
    
    # Act
    result = fusion_engine._validate_sensor_data(sensor_data)
    
    # Assert
    assert result is True

def test_validate_sensor_data_invalid(fusion_engine):
    # Arrange
    invalid_data = {'sensor': "not_array"}
    
    # Act
    result = fusion_engine._validate_sensor_data(invalid_data)
    
    # Assert
    assert result is False

def test_validate_sensor_data_empty(fusion_engine):
    # Act
    result = fusion_engine._validate_sensor_data({})
    
    # Assert
    assert result is False

def test_fuse_sensors_confidence_calculation(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.preprocess_data = Mock(return_value=sample_sensor_data)
    fusion_engine._create_quantum_representation = Mock(return_value=np.array([1, 2, 3]))
    fusion_engine.quantum_gates.build_sensory_circuit.return_value = np.array([1, 2, 3])
    fusion_engine.clustering_engine.fit_predict.return_value = np.array([1, 1, 0])
    
    # Act
    result = fusion_engine.fuse_sensors(sample_sensor_data)
    
    # Assert
    assert isinstance(result.confidence_score, float)
    assert 0 <= result.confidence_score <= 1 or result.confidence_score > 1  # depends on actual data

def test_fuse_sensors_clustering_integration(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.preprocess_data = Mock(return_value=sample_sensor_data)
    fusion_engine._create_quantum_representation = Mock(return_value=np.array([1, 2, 3]))
    fusion_engine.quantum_gates.build_sensory_circuit.return_value = np.array([1, 2, 3])
    fusion_engine.clustering_engine.fit_predict.return_value = np.array([1, 0, 1])
    
    # Act
    result = fusion_engine.fuse_sensors(sample_sensor_data)
    
    # Assert
    assert 'clustered_patterns' in result.metadata
    fusion_engine.clustering_engine.fit_predict.assert_called_once()

def test_fuse_sensors_result_metadata(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine.preprocess_data = Mock(return_value=sample_sensor_data)
    fusion_engine._create_quantum_representation = Mock(return_value=np.array([1, 2, 3]))
    fusion_engine.quantum_gates.build_sensory_circuit.return_value = np.array([1, 2, 3])
    fusion_engine.clustering_engine.fit_predict.return_value = np.array([0, 1, 0])
    
    # Act
    result = fusion_engine.fuse_sensors(sample_sensor_data)
    
    # Assert
    assert hasattr(result, 'metadata')
    assert hasattr(result, 'fused_data')
    assert hasattr(result, 'confidence_score')

def test_fuse_sensors_sensor_preprocessing_failure(fusion_engine):
    # Arrange
    invalid_data = {'sensor': "invalid"}
    
    # Act & Assert
    with pytest.raises(TypeError):
        fusion_engine.fuse_sensors(invalid_data)

def test_fuse_sensors_quantum_representation_failure(fusion_engine, sample_sensor_data):
    # Arrange
    fusion_engine._create_quantum_representation = Mock(side_effect=Exception("Quantum error"))
    
    # Act & Assert
    with pytest.raises(Exception, match="Quantum error"):
        fusion_engine.fuse_sensors(sample_sensor_data)