import numpy as np
import pytest
from unittest.mock import Mock, patch
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qml_framework.algorithms.qubit_encoding import QubitEncoding

def test_qubit_encoding_init():
    encoder = QubitEncoding(4)
    assert encoder.num_qubits == 4

def test_qubit_encoding_init_invalid_qubits():
    with pytest.raises(ValueError):
        QubitEncoding(0)

def test_qubit_encoding_init_large_qubits():
    with pytest.warns(None) as record:
        encoder = QubitEncoding(25)
        assert len(record) > 0

def test_amplitude_encoding_valid_data():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    circuit = encoder.amplitude_encoding(data)
    assert isinstance(circuit, QuantumCircuit)

def test_amplitude_encoding_empty_data():
    encoder = QubitEncoding(4)
    with pytest.raises(ValueError):
        encoder.amplitude_encoding([])

def test_amplitude_encoding_zero_vector():
    encoder = QubitEncoding(4)
    with pytest.raises(ValueError):
        encoder.amplitude_encoding([0, 0, 0, 0])

def test_angle_encoding_valid_data():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0]
    circuit = encoder.angle_encoding(data)
    assert isinstance(circuit, QuantumCircuit)

def test_angle_encoding_empty_data():
    encoder = QubitEncoding(4)
    with pytest.raises(ValueError):
        encoder.angle_encoding([])

def test_quantum_encoding_valid_types():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    
    # Test amplitude encoding
    circuit1 = encoder.quantum_encoding(data, 'amplitude')
    assert isinstance(circuit1, QuantumCircuit)
    
    # Test angle encoding
    circuit2 = encoder.quantum_encoding(data, 'angle')
    assert isinstance(circuit2, QuantumCircuit)

def test_quantum_encoding_invalid_type():
    encoder = QubitEncoding(4)
    with pytest.raises(ValueError):
        encoder.quantum_encoding([1, 2, 3], 'invalid')

def test_decode_qubit_state():
    encoder = QubitEncoding(4)
    data = [1.0, 0.0, 0.0, 0.0]
    circuit = encoder.amplitude_encoding(data)
    state = encoder.decode_qubit_state(circuit)
    assert isinstance(state, np.ndarray)

def test_decode_qubit_state_invalid_input():
    encoder = QubitEncoding(4)
    with pytest.raises(TypeError):
        encoder.decode_qubit_state("invalid")

def test_create_encoding_circuit():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    circuit = encoder.create_encoding_circuit(data)
    assert isinstance(circuit, QuantumCircuit)

def test_create_encoding_circuit_with_feature_map():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    feature_map = QuantumCircuit(4)
    feature_map.ry(0.5, 0)
    
    circuit = encoder.create_encoding_circuit(data, feature_map)
    assert isinstance(circuit, QuantumCircuit)

def test_encode_sensory_data():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    
    # Test amplitude encoding
    circuit1 = encoder.encode_sensory_data(data, 'amplitude')
    assert isinstance(circuit1, QuantumCircuit)
    
    # Test angle encoding
    circuit2 = encoder.encode_sensory_data(data, 'angle')
    assert isinstance(circuit2, QuantumCircuit)

def test_encode_sensory_data_invalid_method():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    with pytest.raises(ValueError):
        encoder.encode_sensory_data(data, 'invalid')

def test_get_encoding_metrics():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    circuit = encoder.amplitude_encoding(data)
    metrics = encoder.get_encoding_metrics(circuit)
    assert 'amplitude' in metrics
    assert 'phase' in metrics
    assert 'fidelity' in metrics

def test_encoding_with_parameter():
    encoder = QubitEncoding(4)
    param = Parameter('θ')
    circuit = QuantumCircuit(1)
    circuit.ry(param, 0)
    
    # This should work with parameters
    assert circuit is not None

def test_process_encoded_data():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    # This should process and return encoded data
    processed = encoder.process_encoded_data(data)
    assert isinstance(processed, np.ndarray) or isinstance(processed, list)

def test_get_quantum_state():
    encoder = QubitEncoding(4)
    data = [1.0, 2.0, 3.0, 4.0]
    circuit = encoder.amplitude_encoding(data)
    state = encoder.get_quantum_state(circuit)
    assert isinstance(state, np.ndarray)