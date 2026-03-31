import pytest
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensors.orch_or_simulation import OrchORSimulator
import numpy as np

@pytest.fixture
def simulator():
    return OrchORSimulator()

@pytest.fixture
def mock_sensory_inputs():
    return {
        'visual': {'data': [0.1, 0.2, 0.3]},
        'auditory': {'frequency': 440, 'amplitude': 0.5},
        'tactile': {'pressure': 10.0, 'texture': 'smooth'}
    }

def test_orchor_simulator_initialization():
    simulator = OrchORSimulator()
    assert simulator.num_qubits == 32
    assert len(simulator.qr) == 32
    assert len(simulator.cr) == 32

def test_circuit_initialization_error():
    with patch('qiskit.QuantumCircuit.h', side_effect=Exception("Circuit error")):
        with pytest.raises(Exception, match="Circuit error"):
            simulator = OrchORSimulator()

def test_simulate_consciousness_state_success(simulator, mock_sensory_inputs):
    # Mock all the dependencies to return successful results
    with patch.multiple(simulator, 
                     qubit_processor=Mock(),
                     sensory_fusion=Mock(),
                     identity_manager=Mock(),
                     codonic_layer=Mock(),
                     quantum_perception=Mock(),
                     consciousness_interface=Mock()):
        simulator.qubit_processor.process_sensory_data.return_value = {'processed': True}
        simulator.sensory_fusion.fuse_sensory_inputs.return_value = {'fused': True}
        simulator.sensory_fusion.compute_entanglement_metrics.return_value = {'entanglement': 0.5}
        simulator.identity_manager.get_identity_metrics.return_value = {'identity': 'stable'}
        simulator.codonic_layer.encode_symbolic_representation.return_value = {'symbolic': True}
        simulator.quantum_perception.process_perception_quantum.return_value = {'perception': True}
        simulator.consciousness_interface.model_self_awareness.return_value = {'self_aware': True}
        simulator.qubit_processor.measure_quantum_state.return_value = {'probabilities': [0.5, 0.5]}
        
        result = simulator.simulate_consciousness_state(mock_sensory_inputs)
        
        assert 'consciousness_metrics' in result
        assert 'quantum_state' in result
        assert result['consciousness_metrics'] is not None

def test_simulate_consciousness_state_error(simulator, mock_sensory_inputs):
    with patch.object(simulator.qubit_processor, 'process_sensory_data', side_effect=Exception("Processing error")):
        result = simulator.simulate_consciousness_state(mock_sensory_inputs)
        assert 'error' in result
        assert result['error'] == "Processing error"

def test_process_perceptual_field_success(simulator, mock_sensory_inputs):
    with patch.multiple(simulator,
                     motor_feedback=Mock(),
                     ros2_bridge=Mock()):
        simulator.qubit_processor.process_sensory_data.return_value = {'processed': True}
        simulator.sensory_fusion.fuse_sensory_inputs.return_value = {'fused': True}
        simulator.identity_manager.get_identity_metrics.return_value = {'identity': 'stable'}
        simulator.codonic_layer.get_codon_metrics.return_value = {'codon': 'metrics'}
        simulator.codonic_layer.encode_symbolic_representation.return_value = {'symbolic': True}
        simulator.quantum_perception.process_perception_quantum.return_value = {'perception': True}
        simulator.sensory_fusion.compute_entanglement_metrics.return_value = {'entanglement': 0.5}
        
        result = simulator.process_perceptual_field(mock_sensory_inputs)
        
        assert 'perceptual_field' in result
        assert 'fusion_metrics' in result
        assert result['perceptual_field'] is not None

def test_process_perceptual_field_with_motor_data(simulator):
    perceptual_data = {
        'visual': {'data': [0.1, 0.2]},
        'motor_data': {'joints': [0.5, 0.3]}
    }
    
    with patch.multiple(simulator,
                     motor_feedback=Mock(),
                     ros2_bridge=Mock()):
        simulator.qubit_processor.process_sensory_data.return_value = {'processed': True}
        simulator.sensory_fusion.fuse_sensory_inputs.return_value = {'fused': True}
        simulator.identity_manager.get_identity_metrics.return_value = {'identity': 'stable'}
        simulator.codonic_layer.get_codon_metrics.return_value = {'codon': 'metrics'}
        simulator.codonic_layer.encode_symbolic_representation.return_value = {'symbolic': True}
        simulator.quantum_perception.process_perception_quantum.return_value = {'perception': True}
        simulator.sensory_fusion.compute_entanglement_metrics.return_value = {'entanglement': 0.5}
        
        result = simulator.process_perceptual_field(perceptual_data)
        
        assert 'perceptual_field' in result
        assert result['perceptual_field'] is not None

def test_calculate_coherence_with_valid_state(simulator):
    quantum_state = {'probabilities': [0.3, 0.4, 0.3]}
    coherence = simulator._calculate_coherence(quantum_state)
    assert isinstance(coherence, float)
    assert 0.0 <= coherence <= 1.0

def test_calculate_coherence_empty_state(simulator):
    coherence = simulator._calculate_coherence({})
    assert coherence == 0.0
    
    coherence = simulator._calculate_coherence(None)
    assert coherence == 0.0

def test_calculate_coherence_no_probabilities(simulator):
    quantum_state = {'other_data': [1, 2, 3]}
    coherence = simulator._calculate_coherence(quantum_state)
    assert coherence == 0.0

def test_get_consciousness_dynamics(simulator):
    dynamics = simulator.get_consciousness_dynamics()
    assert 'perception_history' in dynamics
    assert 'quantum_state_history' in dynamics
    assert 'identity_continuity' in dynamics
    assert 'codonic_stability' in dynamics

def test_update_simulation_parameters_qubits_change(simulator):
    original_qubits = simulator.num_qubits
    simulator.update_simulation_parameters({'num_qubits': 16})
    assert simulator.num_qubits == 16
    assert len(simulator.qr) == 16

def test_execute_orch_or_cycle_success(simulator):
    with patch.object(simulator, 'simulate_consciousness_state', return_value={'consciousness_metrics': {}}):
        with patch.object(simulator.qubit_processor, 'measure_quantum_state', return_value={'probabilities': [0.5]}):
            results = simulator.execute_orch_or_cycle({'input': 'test'}, 3)
            assert len(results) == 3
            assert all('consciousness_metrics' in result for result in results)

def test_execute_orch_or_cycle_error(simulator):
    with patch.object(simulator, 'simulate_consciousness_state', side_effect=Exception("Simulation error")):
        results = simulator.execute_orch_or_cycle({'input': 'test'}, 1)
        assert results == []

def test_get_quantum_state_metrics(simulator):
    metrics = simulator.get_quantum_state_metrics()
    assert 'quantum_state_history' in metrics
    assert 'num_qubits' in metrics
    assert 'coherence_metrics' in metrics
    assert metrics['num_qubits'] == 32

def test_get_quantum_state_metrics_error(simulator):
    with patch.object(simulator, '_calculate_system_coherence', side_effect=Exception("Metrics error")):
        metrics = simulator.get_quantum_state_metrics()
        assert 'quantum_state_history' in metrics
        assert metrics['coherence_metrics'] == {}

def test_reset_simulation(simulator):
    simulator.quantum_state_history = [{'test': 'data'}]
    simulator.perception_history = [{'test': 'data'}]
    simulator.perceptual_field = {'test': 'data'}
    
    simulator.reset_simulation()
    
    assert simulator.quantum_state_history == []
    assert simulator.perception_history == []
    assert simulator.perceptual_field is None

def test_calculate_system_coherence(simulator):
    metrics = simulator._calculate_system_coherence()
    assert 'overall_coherence' in metrics
    assert 'temporal_coherence' in metrics
    assert 'spatial_coherence' in metrics

@patch('src.quantum_sensors.orch_or_simulation.logger')
def test_initialize_circuit_error(mock_logger, simulator):
    with patch('qiskit.QuantumCircuit.h', side_effect=Exception("Qiskit error")):
        with pytest.raises(Exception, match="Qiskit error"):
            simulator._initialize_circuit()
        mock_logger.error.assert_called()

def test_process_perceptual_field_error(simulator):
    with patch.object(simulator.qubit_processor, 'process_sensory_data', side_effect=Exception("Processing error")):
        result = simulator.process_perceptual_field({'test': 'data'})
        assert 'error' in result

def test_process_perceptual_field_motor_feedback(simulator):
    perceptual_data = {
        'visual': {'data': [0.1, 0.2]},
        'motor_data': {'joints': [0.5, 0.3]}
    }
    
    with patch.multiple(simulator,
                     motor_feedback=Mock(),
                     ros2_bridge=Mock()):
        simulator.motor_feedback.update_joint_angles = Mock()
        simulator.motor_feedback.calibrate_feedback = Mock()
        
        result = simulator.process_perceptual_field(perceptual_data)
        
        simulator.motor_feedback.update_joint_angles.assert_called_once_with(perceptual_data['motor_data'])
        simulator.motor_feedback.calibrate_feedback.assert_called_once()