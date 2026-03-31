import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensors.qubit_sensors import (
    QubitSensorProcessor, 
    QubitState, 
    get_quantum_fidelity, 
    normalize_quantum_state
)

def test_qubit_state_creation():
    state = QubitState(amplitude=complex(1, 1), phase=0.5, probability=0.5)
    assert state.amplitude == complex(1, 1)
    assert state.phase == 0.5
    assert state.probability == 0.5

def test_qubit_state_dataclass_frozen():
    state1 = QubitState(amplitude=complex(1, 0), phase=0.0, probability=1.0)
    state2 = QubitState(amplitude=complex(1, 0), phase=0.0, probability=1.0)
    assert state1 == state2

@patch('src.quantum_sensors.qubit_sensors.SensoryFusionEngine')
@patch('src.quantum_sensors.qubit_sensors.QuantumPerceptionEngine')
@patch('src.quantum_sensors.qubit_sensors.OrchORSimulator')
@patch('src.quantum_sensors.qubit_sensors.MotorFeedbackController')
@patch('src.quantum_sensors.qubit_sensors.IdentityContinuityManager')
@patch('src.quantum_sensors.qubit_sensors.CodonicSymbolicLayer')
@patch('src.quantum_sensors.qubit_sensors.ROS2Bridge')
@patch('src.quantum_sensors.qubit_sensors.ConsciousnessInterface')
def test_processor_initialization(
    mock_consciousness, 
    mock_ros2, 
    mock_codonic, 
    mock_identity, 
    mock_motor, 
    mock_orch, 
    mock_quantum, 
    mock_sensory
):
    # Mock all dependencies
    mock_sensory.return_value = Mock()
    mock_quantum.return_value = Mock()
    mock_orch.return_value = Mock()
    mock_motor.return_value = Mock()
    mock_identity.return_value = Mock()
    mock_codonic.return_value = Mock()
    mock_ros2.return_value = Mock()
    mock_consciousness.return_value = Mock()
    
    processor = QubitSensorProcessor()
    assert processor is not None
    assert processor.sensory_fusion is not None

def test_process_sensory_data_valid_input():
    with patch.multiple("src.quantum_sensors.qubit_sensors", 
                      SensoryFusionEngine=Mock,
                      QuantumPerceptionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      IdentityContinuityManager=Mock,
                      CodonicSymbolicLayer=Mock,
                      ROS2Bridge=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        processor.sensory_fusion.fuse_sensory_inputs = Mock(return_value={"fused": True})
        processor.quantum_perception.process_perception_quantum = Mock(return_value={"processed": True})
        processor.identity_manager.maintain_identity = Mock(return_value="identity")
        processor.codonic_layer.encode_symbolic_representation = Mock(return_value="symbolic")
        processor.quantum_perception.execute_symbolic_reasoning = Mock(return_value="reasoning")
        processor.motor_feedback.update_joint_angles = Mock(return_value={"motor": "commands"})
        processor.ros2_bridge.publish_sensor_data = Mock()
        
        result = processor.process_sensory_data({"sensor1": 1.0, "sensor2": 2.0})
        assert "processed_data" in result
        assert "identity_state" in result
        assert "symbolic_representation" in result

def test_process_sensory_data_invalid_input_type():
    with patch.multiple("src.quantum_sensors.qubit_sensors", 
                      SensoryFusionEngine=Mock,
                      QuantumPerceptionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      IdentityContinuityManager=Mock,
                      CodonicSymbolicLayer=Mock,
                      ROS2Bridge=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        with pytest.raises(TypeError):
            processor.process_sensory_data("invalid_input")

def test_process_sensory_data_empty_input():
    with patch.multiple("src.quantum_sensors.qubit_sensors", 
                      SensoryFusionEngine=Mock,
                      QuantumPerceptionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      IdentityContinuityManager=Mock,
                      CodonicSymbolicLayer=Mock,
                      ROS2Bridge=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        with pytest.raises(ValueError):
            processor.process_sensory_data({})

def test_measure_quantum_state_valid_input():
    with patch.multiple("src.quantum_sensors.qubit_sensors", 
                      SensoryFusionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        processor.orch_or_sim.simulate_consciousness_state = Mock(return_value={"consciousness": "state"})
        processor.orch_or_sim.process_perceptual_field = Mock(return_value={"perceptual": "field"})
        processor.sensory_fusion.compute_entanglement_metrics = Mock(return_value={"entanglement": 0.5})
        processor.motor_feedback.calibrate_feedback = Mock()
        processor.consciousness_interface.model_self_awareness = Mock()
        processor.consciousness_interface.integrate_cognitive_states = Mock()
        
        sensor_data = {"test": 1}
        state = processor.measure_quantum_state(sensor_data)
        assert isinstance(state, QubitState)
        assert state.probability >= 0

def test_measure_quantum_state_invalid_input():
    with patch.multiple("src.quantum_sensors.qubit_sensors", 
                      SensoryFusionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        with pytest.raises(TypeError):
            processor.measure_quantum_state("invalid_input")

@patch('src.quantum_sensors.qubit_sensors.OrchORSimulator')
@patch('src.quantum_sensors.qubit_sensors.SensoryFusionEngine')
def test_measure_quantum_state_error_handling(mock_sensory, mock_orch):
    mock_sensory.return_value.compute_entanglement_metrics.side_effect = Exception("Test error")
    mock_orch.return_value.simulate_consciousness_state.return_value = {"test": "data"}
    mock_orch.return_value.process_perceptual_field.return_value = {"test": "data"}
    
    processor = QubitSensorProcessor()
    # Should return default state when error occurs
    state = processor.measure_quantum_state({"test": 1})
    assert state.amplitude == complex(0.0)
    assert state.phase == 0.0
    assert state.probability == 0.0

def test_get_quantum_fidelity():
    state1 = QubitState(complex(1, 0), 0.0, 1.0)
    state2 = QubitState(complex(1, 0), 0.0, 1.0)
    fidelity = get_quantum_fidelity(state1, state2)
    assert 0 <= fidelity <= 1

def test_get_quantum_fidelity_orthogonal_states():
    state1 = QubitState(complex(1, 0), 0.0, 1.0)
    state2 = QubitState(complex(0, 1), 0.0, 1.0)
    fidelity = get_quantum_fidelity(state1, state2)
    # Orthogonal states should have 0 fidelity
    assert abs(fidelity) == 0

def test_normalize_quantum_state():
    state = QubitState(complex(3, 4), 0.0, 25.0)  # |3+4j| = 5, so needs normalization
    normalized = normalize_quantum_state(state)
    # After normalization, probability should be 1.0
    assert abs(normalized.amplitude) == pytest.approx(1.0)
    assert normalized.probability == 1.0

def test_normalize_quantum_state_zero_amplitude():
    state = QubitState(complex(0, 0), 0.0, 0.0)
    normalized = normalize_quantum_state(state)
    assert normalized.amplitude == complex(0, 0)
    assert normalized.phase == state.phase

def test_processor_module_level_instantiation():
    # Test that the module-level processor is created correctly
    from src.quantum_sensors.qubit_sensors import processor
    assert processor is not None
    assert hasattr(processor, 'sensory_fusion')

def test_process_sensory_data_integration():
    with patch.multiple("src.quantum_sensors.qubit_sensors",
                      SensoryFusionEngine=Mock,
                      QuantumPerceptionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      IdentityContinuityManager=Mock,
                      CodonicSymbolicLayer=Mock,
                      ROS2Bridge=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        # Setup all mocks
        processor.sensory_fusion.fuse_sensory_inputs = Mock(return_value={"fused": True})
        processor.quantum_perception.process_perception_quantum = Mock(return_value={"processed": True})
        processor.identity_manager.maintain_identity = Mock(return_value="identity")
        processor.codonic_layer.encode_symbolic_representation = Mock(return_value="symbolic")
        processor.quantum_perception.execute_symbolic_reasoning = Mock(return_value="reasoning")
        processor.motor_feedback.update_joint_angles = Mock(return_value={"motor": "commands"})
        processor.ros2_bridge.publish_sensor_data = Mock()
        
        result = processor.process_sensory_data({"sensor1": 1.0, "sensor2": 2.0})
        assert result is not None
        assert "processed_data" in result
        assert "timestamp" in result

@patch('src.quantum_sensors.qubit_sensors.time')
def test_get_timestamp(mock_time):
    mock_time.time.return_value = 1234567890.0
    processor = QubitSensorProcessor()
    timestamp = processor._get_timestamp()
    assert timestamp == 1234567890.0

def test_process_sensory_data_exception_handling():
    with patch.multiple("src.quantum_sensors.qubit_sensors",
                      SensoryFusionEngine=Mock,
                      QuantumPerceptionEngine=Mock,
                      OrchORSimulator=Mock,
                      MotorFeedbackController=Mock,
                      IdentityContinuityManager=Mock,
                      CodonicSymbolicLayer=Mock,
                      ROS2Bridge=Mock,
                      ConsciousnessInterface=Mock):
        processor = QubitSensorProcessor()
        # Force an exception in the pipeline
        processor.sensory_fusion.fuse_sensory_inputs = Mock(side_effect=Exception("Test error"))
        
        with pytest.raises(Exception):
            processor.process_sensory_data({"sensor": 1.0})