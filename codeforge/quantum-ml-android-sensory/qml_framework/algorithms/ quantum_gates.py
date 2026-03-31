import numpy as np
from typing import Union, List, Tuple, Optional

class QuantumGates:
    """
    A class for implementing quantum gate operations for quantum machine learning.
    """
    
    def __init__(self):
        """Initialize the QuantumGates class."""
        self.gate_operations = {
            'hadamard': self.hadamard_gate,
            'pauli_x': self.pauli_x_gate,
            'pauli_y': self.pauli_y_gate,
            'pauli_z': self.pauli_z_gate,
            'cnot': self.cnot_gate,
            'rotation_x': self.rotation_x_gate,
            'rotation_y': self.rotation_y_gate,
            'rotation_z': self.rotation_z_gate,
            'phase': self.phase_gate
        }
    
    def hadamard_gate(self, qubit_index: int, circuit) -> None:
        """
        Apply Hadamard gate to specified qubit in the circuit.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if circuit is None:
            raise ValueError("circuit cannot be None")
        # Apply the gate
        circuit.h(qubit_index)
    
    def pauli_x_gate(self, qubit_index: int, circuit) -> None:
        """
        Apply Pauli-X gate to specified qubit in the circuit.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if circuit is None:
            raise ValueError("circuit cannot be None")
        # Apply the gate
        circuit.x(qubit_index)
    
    def pauli_y_gate(self, qubit_index: int, circuit) -> None:
        """
        Apply Pauli-Y gate to specified qubit in the circuit.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if circuit is None:
            raise ValueError("circuit cannot be None")
        # Apply the gate
        circuit.y(qubit_index)
    
    def pauli_z_gate(self, qubit_index: int, circuit) -> None:
        """
        Apply Pauli-Z gate to specified qubit in the circuit.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if circuit is None:
            raise ValueError("circuit cannot be None")
        # Apply the gate
        circuit.z(qubit_index)
    
    def cnot_gate(self, control_qubit: int, target_qubit: int, 
                  circuit) -> None:
        """
        Apply CNOT gate operation.
        """
        if not isinstance(control_qubit, int) or control_qubit < 0:
            raise ValueError("control_qubit must be a non-negative integer")
        if not isinstance(target_qubit, int) or target_qubit < 0:
            raise ValueError("target_qubit must be a non-negative integer")
        if circuit is None:
            raise ValueError("circuit cannot be None")
            
        # Apply the gate
        circuit.cx(control_qubit, target_qubit)
    
    def rotation_x_gate(self, qubit_index: int, theta: float, 
                        circuit) -> None:
        """
        Apply rotation-X gate with specified angle.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if not isinstance(theta, (int, float)):
            raise ValueError("theta must be a number")
        if circuit is None:
            raise ValueError("circuit cannot be None")
            
        # Apply the gate
        circuit.rx(theta, qubit_index)
    
    def rotation_y_gate(self, qubit_index: int, theta: float,
                        circuit) -> None:
        """
        Apply rotation-Y gate with specified angle.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if not isinstance(theta, (int, float)):
            raise ValueError("theta must be a number")
        if circuit is None:
            raise ValueError("circuit cannot be None")
            
        # Apply the gate
        circuit.ry(theta, qubit_index)
    
    def rotation_z_gate(self, qubit_index: int, theta: float,
                        circuit) -> None:
        """
        Apply rotation-Z gate with specified angle.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if not isinstance(theta, (int, float)):
            raise ValueError("theta must be a number")
        if circuit is None:
            raise ValueError("circuit cannot be None")
            
        # Apply the gate
        circuit.rz(theta, qubit_index)
    
    def phase_gate(self, qubit_index: int, theta: float,
                   circuit) -> None:
        """
        Apply phase gate with specified angle.
        """
        if not isinstance(qubit_index, int) or qubit_index < 0:
            raise ValueError("qubit_index must be a non-negative integer")
        if not isinstance(theta, (int, float)):
            raise ValueError("theta must be a number")
        if circuit is None:
            raise ValueError("circuit cannot be None")
            
        # Apply the gate
        circuit.p(theta, qubit_index)
    
    def create_quantum_circuit(self, num_qubits: int):
        """
        Create a quantum circuit with specified number of qubits.
        """
        if not isinstance(num_qubits, int) or num_qubits <= 0:
            raise ValueError("num_qubits must be a positive integer")
            
        # Create quantum and classical registers
        q_register = QuantumRegister(num_qubits)
        c_register = ClassicalRegister(num_qubits)
        
        # Create circuit
        circuit = QuantumCircuit(q_register, c_register)
        return circuit
    
    def apply_custom_gate(self, gate, qubit_indices: Union[List[int], int],
                           circuit) -> None:
        """
        Apply a custom gate to specified qubits in the circuit.
        """
        if circuit is None:
            raise ValueError("circuit cannot be None")
            
        # Handle both single qubit and multi-qubit gate applications
        if isinstance(qubit_indices, list):
            for idx in qubit_indices:
                if not isinstance(idx, int) or idx < 0:
                    raise ValueError("Invalid qubit index")
        else:
            if not isinstance(qubit_indices, int) or qubit_indices < 0:
                raise ValueError("qubit_indices must be non-negative integers")
        
        # Apply the gate
        if isinstance(qubit_indices, list):
            # For multi-qubit gates, we need to apply to all specified qubits
            circuit.append(gate, qubit_indices)
        else:
            circuit.append(gate, [qubit_indices])
    
    def tensor_product(self, *matrices: np.ndarray) -> np.ndarray:
        """
        Compute tensor product of multiple matrices.
        """
        if not matrices:
            raise ValueError("At least one matrix must be provided")
            
        result = matrices[0]
        for matrix in matrices[1:]:
            if not isinstance(matrix, np.ndarray):
                raise ValueError("All inputs must be numpy arrays")
            result = np.kron(result, matrix)
        return result
    
    def create_gate_from_matrix(self, matrix: np.ndarray):
        """
        Create a custom gate from a unitary matrix.
        """
        if not isinstance(matrix, np.ndarray):
            raise ValueError("matrix must be a numpy array")
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("matrix must be square")
        if not np.allclose(matrix @ matrix.conj().T, np.eye(matrix.shape[0])):
            raise ValueError("matrix must be unitary")
            
        # Create gate from matrix
        return Gate("custom", matrix.shape[0], [], matrix)
    
    def validate_circuit(self, circuit) -> bool:
        """
        Validate that a quantum circuit is properly constructed.
        """
        # Check if circuit has at least one qubit
        if circuit.num_qubits == 0:
            raise ValueError("Circuit must have at least one qubit")
        return True

# Mock classes for when qiskit is not available
try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit.circuit import Gate
except ImportError:
    # Create minimal mock classes for testing purposes
    class QuantumCircuit:
        def __init__(self, *args, **kwargs):
            self.num_qubits = 0
            if args and hasattr(args[0], '__len__'):
                self.num_qubits = args[0][0].size if args[0] else 0
        
        def h(self, qubit):
            pass
            
        def x(self, qubit):
            pass
            
        def y(self, qubit):
            pass
            
        def z(self, qubit):
            pass
            
        def cx(self, control, target):
            pass
            
        def rx(self, theta, qubit):
            pass
            
        def ry(self, theta, qubit):
            pass
            
        def rz(self, theta, qubit):
            pass
            
        def p(self, theta, qubit):
            pass
            
        def append(self, gate, qubits):
            pass

    class QuantumRegister:
        def __init__(self, size):
            self.size = size

    class ClassicalRegister:
        def __init__(self, size):
            pass

    class Gate:
        def __init__(self, name, num_qubits, params, matrix):
            self.name = name
            self.num_qubits = num_qubits
            self.params = params
            self.matrix = matrix