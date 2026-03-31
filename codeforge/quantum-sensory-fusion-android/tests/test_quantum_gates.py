import numpy as np
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.quantum_sensory_fusion.quantum_gates import QuantumSensoryGates

@pytest.fixture
def quantum_gates():
    return QuantumSensoryGates(num_qubits=4)

def test_quantum_gates_init():
    gates = QuantumSensoryGates(num_qubits=3)
    assert gates.num_qubits == 3
    assert gates.circuit.num_qubits == 3

def test_apply_sensory_gate_hadamard(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    
    with patch.object(quantum_gates.fusion_engine, 'preprocess_data', return_value=sensor_data), \
         patch.object(quantum_gates.clustering, 'transform_sensory_data', return_value=sensor_data), \
         patch.object(quantum_gates.qubit_manager, 'create_bosonic_state', return_value=sensor_data), \
         patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result, circuit = quantum_gates.apply_sensory_gate(sensor_data, 'hadamard')
        assert np.array_equal(result, sensor_data)
        assert circuit == quantum_gates.circuit

def test_apply_sensory_gate_pauli_x(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    
    with patch.object(quantum_gates.fusion_engine, 'preprocess_data', return_value=sensor_data), \
         patch.object(quantum_gates.clustering, 'transform_sensory_data', return_value=sensor_data), \
         patch.object(quantum_gates.qubit_manager, 'create_bosonic_state', return_value=sensor_data), \
         patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result, circuit = quantum_gates.apply_sensory_gate(sensor_data, 'pauli_x')
        assert np.array_equal(result, sensor_data)
        assert circuit == quantum_gates.circuit

def test_apply_sensory_gate_rotation(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    
    with patch.object(quantum_gates.fusion_engine, 'preprocess_data', return_value=sensor_data), \
         patch.object(quantum_gates.clustering, 'transform_sensory_data', return_value=sensor_data), \
         patch.object(quantum_gates.qubit_manager, 'create_bosonic_state', return_value=sensor_data), \
         patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result, circuit = quantum_gates.apply_sensory_gate(sensor_data, 'rotation')
        assert np.array_equal(result, sensor_data)
        assert circuit == quantum_gates.circuit

def test_apply_sensory_gate_default_hadamard(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    
    with patch.object(quantum_gates.fusion_engine, 'preprocess_data', return_value=sensor_data), \
         patch.object(quantum_gates.clustering, 'transform_sensory_data', return_value=sensor_data), \
         patch.object(quantum_gates.qubit_manager, 'create_bosonic_state', return_value=sensor_data), \
         patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result, circuit = quantum_gates.apply_sensory_gate(sensor_data, 'invalid_gate')
        assert np.array_equal(result, sensor_data)
        assert circuit == quantum_gates.circuit

def test_build_sensory_circuit(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    operations = ['hadamard', 'pauli_x', 'rotation_1.57']
    
    with patch.object(quantum_gates.fusion_engine, 'preprocess_data', return_value=sensor_data), \
         patch.object(quantum_gates.clustering, 'fit_predict', return_value=sensor_data), \
         patch.object(quantum_gates.qubit_manager, 'create_bosonic_state', return_value=sensor_data):
        circuit = quantum_gates.build_sensory_circuit(sensor_data, operations)
        assert isinstance(circuit, QuantumCircuit)

def test_apply_hadamard_gate(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    with patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result = quantum_gates._apply_hadamard_gate(sensor_data)
        assert np.array_equal(result, sensor_data)

def test_apply_pauli_x_gate(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    with patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result = quantum_gates._apply_pauli_x_gate(sensor_data)
        assert np.array_equal(result, sensor_data)

def test_apply_rotation_gate(quantum_gates):
    sensor_data = np.array([1, 2, 3, 4])
    with patch.object(quantum_gates, '_simulate_circuit', return_value=sensor_data):
        result = quantum_gates._apply_rotation_gate(sensor_data)
        assert np.array_equal(result, sensor_data)

def test_validate_sensor_data_valid(quantum_gates):
    data = np.array([1, 2, 3, 4])
    assert quantum_gates._validate_sensor_data(data) is True

def test_validate_sensor_data_invalid_type(quantum_gates):
    with pytest.raises(TypeError):
        quantum_gates._validate_sensor_data("invalid_data")

def test_validate_sensor_data_empty(quantum_gates):
    data = np.array([])
    with pytest.raises(ValueError):
        quantum_gates._validate_sensor_data(data)

def test_validate_sensor_data_wrong_dimensions(quantum_gates):
    data = np.array([[[1, 2], [3, 4]]])  # 3D array
    with pytest.raises(ValueError):
        quantum_gates._validate_sensor_data(data)

def test_get_optimal_qubit_count(quantum_gates):
    count = quantum_gates._get_optimal_qubit_count(8)
    assert count == 3  # log2(8) = 3, so minimum 3 is used
    
    count = quantum_gates._get_optimal_qubit_count(1)
    assert count == 3  # Minimum is 3

def test_simulate_circuit(quantum_gates):
    input_state = np.array([1, 2, 3, 4])
    result = quantum_gates._simulate_circuit(input_state)
    assert np.array_equal(result, input_state)