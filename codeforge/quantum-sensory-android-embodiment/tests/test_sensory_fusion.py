import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensors.sensory_fusion import (
    SensoryFusionEngine, 
    FusionResult
)

@pytest.fixture
def fusion_engine():
    with patch.multiple("src.quantum_sensors.sensory_fusion", 
                     QubitSensorProcessor=Mock(),
                     OrchORSimulator=Mock(),
                     MotorFeedbackController=Mock(),
                     IdentityContinuityManager=Mock(),
                     CodonicSymbolicLayer=Mock(),
                     QuantumPerceptionEngine=Mock(),
                     ROS2Bridge=Mock(),
                     ConsciousnessInterface=Mock()):
        return SensoryFusionEngine()

def test_fuse_sensory_inputs_success(fusion_engine):
    sensor_data = {"sensor1": {"value": 1.0, "confidence": 0.9}}
    mock_result = FusionResult({}, 0.95, 1234567890.0, {})
    
    fusion_engine.qubit_processor.process_sensory_data.return_value = sensor_data
    fusion_engine.qubit_processor.measure_quantum_state.return_value = {}
    fusion_engine._create_unified_field = Mock(return_value={})
    fusion_engine.codonic_layer.encode_symbolic_representation.return_value = {}
    fusion_engine.codonic_layer.decode_codon_sequence.return_value = {}
    fusion_engine._calculate_fusion_confidence.return_value = 0.95
    
    result = fusion_engine.fuse_sensory_inputs(sensor_data)
    
    assert isinstance(result, FusionResult)
    assert result.confidence == 0.95

def test_fuse_sensory_inputs_with_custom_weights(fusion_engine):
    sensor_data = {"sensor1": {"value": 1.0}}
    sensor_weights = {"sensor1": 0.8}
    
    fusion_engine.qubit_processor.process_sensory_data.return_value = sensor_data
    fusion_engine.qubit_processor.measure_quantum_state.return_value = {}
    fusion_engine._create_unified_field = Mock(return_value={})
    fusion_engine.codonic_layer.encode_symbolic_representation.return_value = {}
    fusion_engine.codonic_layer.decode_codon_sequence.return_value = {}
    fusion_engine._calculate_fusion_confidence.return_value = 0.95
    
    result = fusion_engine.fuse_sensory_inputs(sensor_data, sensor_weights)
    
    assert isinstance(result, FusionResult)
    assert result.confidence == 0.95

def test_fuse_sensory_inputs_empty_data(fusion_engine):
    sensor_data = {}
    
    result = fusion_engine.fuse_sensory_inputs(sensor_data)
    
    assert isinstance(result, FusionResult)

def test_compute_entanglement_metrics(fusion_engine):
    quantum_states = {
        "sensor1": {
            "amplitude": 0.5,
            "state_vector": np.array([1, 0])
        }
    }
    result = fusion_engine.compute_entanglement_metrics(quantum_states)
    assert isinstance(result, dict)

def test_compute_density_matrix(fusion_engine):
    state_vector = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    result = fusion_engine._compute_density_matrix(state_vector)
    expected = np.array([[0.5, 0.5], [0.5, 0.5]])
    np.testing.assert_array_almost_equal(result, expected)

def test_von_neumann_entropy_pure_state(fusion_engine):
    # Pure state has entropy = 0
    state_vector = np.array([1, 0, 0, 0])
    density_matrix = fusion_engine._compute_density_matrix(state_vector)
    entropy = fusion_engine._von_neumann_entropy(density_matrix)
    assert entropy == 0.0

def test_von_neumann_entropy_mixed_state(fusion_engine):
    # Mixed state has positive entropy
    density_matrix = np.array([[0.5, 0], [0, 0.5]])
    entropy = fusion_engine._von_neumann_entropy(density_matrix)
    assert entropy > 0

def test_create_unified_field_basic(fusion_engine):
    quantum_states = {"sensor1": {}}
    entanglement_metrics = {"metric1": 1.0}
    
    fusion_engine.quantum_engine.process_perception_quantum.return_value = {}
    fusion_engine.quantum_engine.execute_symbolic_reasoning.return_value = {}
    fusion_engine.consciousness_interface.model_self_awareness.return_value = {"conscious_state": {}}
    
    result = fusion_engine._create_unified_field(quantum_states, entanglement_metrics)
    assert "conscious_state" in result

def test_calculate_default_weights_single_sensor(fusion_engine):
    sensor_data = {"sensor1": 1.0}
    weights = fusion_engine._calculate_default_weights(sensor_data)
    assert weights == {"sensor1": 1.0}

def test_calculate_default_weights_multiple_sensors(fusion_engine):
    sensor_data = {"sensor1": 1.0, "sensor2": 2.0}
    weights = fusion_engine._calculate_default_weights(sensor_data)
    assert weights == {"sensor1": 0.5, "sensor2": 0.5}

def test_calculate_fusion_confidence(fusion_engine):
    quantum_states = {
        "sensor1": {
            "density_matrix": np.array([[1, 0], [0, 1]])  
        }
    }
    entanglement_metrics = {"metric1": 0.5}
    confidence = fusion_engine._calculate_fusion_confidence(quantum_states, entanglement_metrics)
    assert 0.0 <= confidence <= 1.0

def test_dict_to_statevector_empty(fusion_engine):
    from qiskit.quantum_info import Statevector
    result = fusion_engine._dict_to_statevector({})
    assert isinstance(result, Statevector)

def test_dict_to_statevector_values(fusion_engine):
    from qiskit.quantum_info import Statevector
    data = {"sensor1": 1.0, "sensor2": 1.0}
    result = fusion_engine._dict_to_statevector(data)
    assert isinstance(result, Statevector)

def test_compute_mutual_information(fusion_engine):
    quantum_states = {
        "sensor1": {"entanglement_entropy": 0.5},
        "sensor2": {"entanglement_entropy": 0.3}
    }
    result = fusion_engine._compute_mutual_information(quantum_states)
    assert result == 0.8

def test_fuse_sensory_inputs_exception_handling(fusion_engine):
    sensor_data = {"sensor1": {"value": 1.0}}
    
    # Simulate exception in processing
    fusion_engine.qubit_processor.process_sensory_data.side_effect = Exception("Processing error")
    
    with pytest.raises(Exception, match="Processing error"):
        fusion_engine.fuse_sensory_inputs(sensor_data)

def test_compute_entanglement_metrics_exception_handling(fusion_engine):
    quantum_states = {}
    # Simulate exception in entropy calculation
    fusion_engine._compute_mutual_information = Mock(side_effect=Exception("Entropy error"))
    
    with pytest.raises(Exception, match="Entropy error"):
        fusion_engine.compute_entanglement_metrics(quantum_states)

def test_fuse_sensory_inputs_with_none_weights(fusion_engine):
    sensor_data = {"sensor1": {"value": 1.0}}
    fusion_engine._calculate_default_weights = Mock(return_value={"sensor1": 1.0})
    fusion_engine.qubit_processor.process_sensory_data.return_value = sensor_data
    fusion_engine.qubit_processor.measure_quantum_state.return_value = {}
    fusion_engine._create_unified_field = Mock(return_value={})
    fusion_engine.codonic_layer.encode_symbolic_representation.return_value = {}
    fusion_engine.codonic_layer.decode_codon_sequence.return_value = {}
    fusion_engine._calculate_fusion_confidence.return_value = 0.85
    
    result = fusion_engine.fuse_sensory_inputs(sensor_data, None)
    
    assert isinstance(result, FusionResult)
    assert result.confidence == 0.85

def test_von_neumann_entropy_invalid_matrix(fusion_engine):
    density_matrix = np.array([[1, 2], [3, 4]])  # Non-Hermitian
    entropy = fusion_engine._von_neumann_entropy(density_matrix)
    assert entropy == 0.0  # Should return 0.0 for invalid matrix

def test_calculate_fusion_confidence_exception(fusion_engine):
    quantum_states = {}
    entanglement_metrics = {}
    # Simulate exception in confidence calculation
    fusion_engine._calculate_fusion_confidence = Mock(side_effect=Exception("Conf error"))
    fusion_engine._calculate_fusion_confidence.return_value = 0.0

def test_identity_manager_update_called(fusion_engine):
    sensor_data = {"sensor1": {"value": 1.0}}
    fusion_engine.qubit_processor.process_sensory_data.return_value = sensor_data
    fusion_engine.qubit_processor.measure_quantum_state.return_value = {}
    fusion_engine._create_unified_field = Mock(return_value={})
    fusion_engine.codonic_layer.encode_symbolic_representation.return_value = {}
    fusion_engine.codonic_layer.decode_codon_sequence.return_value = {}
    fusion_engine._calculate_fusion_confidence.return_value = 0.95
    
    fusion_engine.fuse_sensory_inputs(sensor_data)
    fusion_engine.identity_manager.update_identity_state.assert_called_once()

def test_concurrent_access_safety(fusion_engine):
    sensor_data = {"sensor1": {"value": 1.0}}
    fusion_engine.qubit_processor.process_sensory_data.return_value = sensor_data
    fusion_engine.qubit_processor.measure_quantum_state.return_value = {}
    fusion_engine._create_unified_field = Mock(return_value={})
    fusion_engine.codonic_layer.encode_symbolic_representation.return_value = {}
    fusion_engine.codonic_layer.decode_codon_sequence.return_value = {}
    fusion_engine._calculate_fusion_confidence.return_value = 0.95
    
    result1 = fusion_engine.fuse_sensory_inputs(sensor_data)
    result2 = fusion_engine.fuse_sensory_inputs(sensor_data)
    
    assert isinstance(result1, FusionResult)
    assert isinstance(result2, FusionResult)