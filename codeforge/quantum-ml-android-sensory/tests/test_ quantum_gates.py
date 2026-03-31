import pytest
import numpy as np
from unittest.mock import Mock, patch
from qml_framework.algorithms.quantum_gates import QuantumGates
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate

class TestQuantumGates:
    @pytest.fixture
    def quantum_gates(self):
        return QuantumGates()
    
    @pytest.fixture
    def mock_circuit(self):
        return Mock(spec=QuantumCircuit)
    
    def test_hadamard_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.hadamard_gate(0, mock_circuit)
        mock_circuit.h.assert_called_once_with(0)
    
    def test_pauli_x_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.pauli_x_gate(1, mock_circuit)
        mock_circuit.x.assert_called_once_with(1)
    
    def test_pauli_y_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.pauli_y_gate(1, mock_circuit)
        mock_circuit.y.assert_called_once_with(1)
    
    def test_pauli_z_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.pauli_z_gate(1, mock_circuit)
        mock_circuit.z.assert_called_once_with(1)
    
    def test_cnot_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.cnot_gate(0, 1, mock_circuit)
        mock_circuit.cx.assert_called_once_with(0, 1)
    
    def test_rotation_x_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.rotation_x_gate(0, np.pi/2, mock_circuit)
        mock_circuit.rx.assert_called_once_with(np.pi/2, 0)
    
    def test_rotation_y_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.rotation_y_gate(0, np.pi/2, mock_circuit)
        mock_circuit.ry.assert_called_once_with(np.pi/2, 0)
    
    def test_rotation_z_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.rotation_z_gate(0, np.pi/2, mock_circuit)
        mock_circuit.rz.assert_called_once_with(np.pi/2, 0)
    
    def test_phase_gate_valid_inputs(self, quantum_gates, mock_circuit):
        quantum_gates.phase_gate(0, np.pi/4, mock_circuit)
        mock_circuit.p.assert_called_once_with(np.pi/4, 0)
    
    def test_create_quantum_circuit(self, quantum_gates):
        circuit = quantum_gates.create_quantum_circuit(3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
    
    def test_apply_custom_gate_single_qubit(self, quantum_gates, mock_circuit):
        mock_gate = Mock(spec=Gate)
        quantum_gates.apply_custom_gate(mock_gate, 1, mock_circuit)
        mock_circuit.append.assert_called()
    
    def test_apply_custom_gate_multi_qubit(self, quantum_gates, mock_circuit):
        mock_gate = Mock(spec=Gate)
        quantum_gates.apply_custom_gate(mock_gate, [0, 1], mock_circuit)
        assert mock_circuit.append.call_count == 2
    
    def test_tensor_product(self, quantum_gates):
        matrix1 = np.array([[1, 0], [0, 1]])
        matrix2 = np.array([[0, 1], [1, 0]])
        result = quantum_gates.tensor_product(matrix1, matrix2)
        expected = np.array([[0, 1, 0, 0], 
                          [1, 0, 0, 0], 
                          [0, 0, 0, 1], 
                          [0, 0, 1, 0]])
        np.testing.assert_array_equal(result, expected)
    
    def test_create_gate_from_matrix_valid(self, quantum_gates):
        matrix = np.array([[1, 0], [0, 1]], dtype=complex)
        gate = quantum_gates.create_gate_from_matrix(matrix)
        assert isinstance(gate, Gate)
    
    def test_validate_circuit_valid(self, quantum_gates):
        circuit = QuantumCircuit(2)
        result = quantum_gates.validate_circuit(circuit)
        assert result is True
    
    def test_error_handling_invalid_qubit_index(self, quantum_gates, mock_circuit):
        with pytest.raises(ValueError):
            quantum_gates.hadamard_gate(-1, mock_circuit)
    
    def test_error_handling_none_circuit(self, quantum_gates):
        with pytest.raises(ValueError):
            quantum_gates.hadamard_gate(0, None)
    
    def test_error_handling_invalid_matrix_for_gate(self, quantum_gates):
        with pytest.raises(ValueError):
            quantum_gates.create_gate_from_matrix(np.array([[1, 2], [3, 4]]))
    
    def test_error_handling_empty_tensor_product(self, quantum_gates):
        with pytest.raises(ValueError):
            quantum_gates.tensor_product()
    
    def test_create_quantum_circuit_invalid_input(self, quantum_gates):
        with pytest.raises(ValueError):
            quantum_gates.create_quantum_circuit(0)
    
    def test_validate_circuit_no_qubits(self, quantum_gates):
        circuit = QuantumCircuit(0)
        with pytest.raises(ValueError):
            quantum_gates.validate_circuit(circuit)