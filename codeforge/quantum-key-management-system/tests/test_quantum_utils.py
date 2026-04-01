import numpy as np
import pytest
from qiskit import QuantumCircuit
from src.core.quantum_utils import (
    hadamard_transform, bell_state_measurement, quantum_fourier_transform,
    create_ghz_state, tensor_product, entangle_qubits, superposition_circuit
)

class TestHadamardTransform:
    def test_hadamard_transform_positive_qubits(self):
        circuit = hadamard_transform(3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
    
    def test_hadamard_transform_zero_qubits_raises_error(self):
        with pytest.raises(ValueError, match="qubit_count must be positive"):
            hadamard_transform(0)
    
    def test_hadamard_transform_negative_qubits_raises_error(self):
        with pytest.raises(ValueError, match="qubit_count must be positive"):
            hadamard_transform(-1)

class TestBellStateMeasurement:
    def test_bell_state_measurement_positive_indices(self):
        circuit, result = bell_state_measurement(0, 1)
        assert isinstance(circuit, QuantumCircuit)
        assert result == "00"
    
    def test_bell_state_measurement_negative_indices_raises_error(self):
        with pytest.raises(ValueError, match="Qubit indices must be non-negative"):
            bell_state_measurement(-1, 0)

class TestQuantumFourierTransform:
    def test_quantum_fourier_transform_positive_qubits(self):
        circuit = quantum_fourier_transform(3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
    
    def test_quantum_fourier_transform_zero_qubits_raises_error(self):
        with pytest.raises(ValueError, match="n must be positive"):
            quantum_fourier_transform(0)
    
    def test_quantum_fourier_transform_negative_qubits_raises_error(self):
        with pytest.raises(ValueError, match="n must be positive"):
            quantum_fourier_transform(-1)

class TestTensorProduct:
    def test_tensor_product_with_states(self):
        state1 = np.array([1, 0])
        state2 = np.array([0, 1])
        states = [state1, state2]
        result = tensor_product(states)
        expected = np.kron(state1, state2)
        assert np.allclose(result, expected)
    
    def test_tensor_product_empty_list(self):
        result = tensor_product([])
        assert np.array_equal(result, np.array([1.0]))

class TestCreateGHZState:
    def test_create_ghz_state_valid_qubits(self):
        circuit = create_ghz_state(3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
    
    def test_create_ghz_state_insufficient_qubits(self):
        with pytest.raises(ValueError, match="Need at least 2 qubits for entanglement"):
            create_ghz_state(1)
    
    def test_create_ghz_state_zero_qubits_raises_error(self):
        with pytest.raises(ValueError, match="Need at least 2 qubits for entanglement"):
            create_ghz_state(0)
    
    def test_create_ghz_state_negative_qubits_raises_error(self):
        with pytest.raises(ValueError, match="Need at least 2 qubits for entanglement"):
            create_ghz_state(-1)

class TestEntangleQubits:
    def test_entangle_qubits_valid_qubits(self):
        circuit = entangle_qubits(3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
    
    def test_entangle_qubits_insufficient_qubits(self):
        with pytest.raises(ValueError, match="Need at least 2 qubits for entanglement"):
            entangle_qubits(1)
    
    def test_entangle_qubits_zero_qubits_raises_error(self):
        with pytest.raises(ValueError, match="Need at least 2 qubits for entanglement"):
            entangle_qubits(0)

class TestSuperpositionCircuit:
    def test_superposition_circuit_valid_size(self):
        circuit = superposition_circuit(3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
    
    def test_superposition_circuit_zero_size_raises_error(self):
        with pytest.raises(ValueError, match="Size must be positive"):
            superposition_circuit(0)
    
    def test_superposition_circuit_negative_size_raises_error(self):
        with pytest.raises(ValueError, match="Size must be positive"):
            superposition_circuit(-1)