import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

# Configure logging
logger = logging.getLogger(__name__)

class StateType(Enum):
    """Enumeration of quantum state types"""
    GROUND = "ground"
    EXCITED = "excited"
    SUPERPOSITION = "superposition"
    ENTANGLED = "entangled"

@dataclass
class QuantumState:
    """Dataclass representing a quantum state"""
    amplitudes: np.ndarray
    state_type: StateType
    entangled_with: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class QuantumStates:
    """Manages quantum state initialization, superposition, and measurement operations for codonic systems"""
    
    def __init__(self):
        """Initialize the quantum states manager"""
        self.states: Dict[str, QuantumState] = {}
        self.current_state_id: Optional[str] = None
        self.logger = logging.getLogger(__name__)
        
    def initialize_superposition(self, state_id: str, dimensions: int = 2) -> str:
        """
        Initialize a quantum system in superposition state
        
        Args:
            state_id: Unique identifier for the state
            dimensions: Number of quantum state dimensions (default 2 for qubit)
            
        Returns:
            str: State identifier
            
        Raises:
            ValueError: If dimensions is invalid
        """
        if dimensions <= 0:
            raise ValueError("Dimensions must be positive")
            
        # Create equal probability superposition state
        amplitude = 1.0 / np.sqrt(dimensions)
        amplitudes = np.full(dimensions, amplitude, dtype=complex)
        
        # Normalize state vector
        norm = np.linalg.norm(amplitudes)
        if norm > 0:
            amplitudes = amplitudes / norm
            
        self.states[state_id] = QuantumState(
            amplitudes=amplitudes,
            state_type=StateType.SUPERPOSITION,
            entangled_with=[]
        )
        
        self.current_state_id = state_id
        self.logger.info(f"Initialized superposition state {state_id} with {dimensions} dimensions")
        return state_id
    
    def measure(self, state_id: str) -> Tuple[int, float]:
        """
        Perform quantum measurement on a state
        
        Args:
            state_id: State identifier to measure
            
        Returns:
            Tuple of (measured_state, probability)
            
        Raises:
            ValueError: If state_id doesn't exist
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
            
        state = self.states[state_id]
        probabilities = np.abs(state.amplitudes) ** 2
        
        # Perform measurement using probabilistic selection
        measured_index = np.random.choice(len(probabilities), p=probabilities)
        measured_probability = probabilities[measured_index]
        
        # Collapse state to measured result
        new_amplitudes = np.zeros_like(state.amplitudes)
        new_amplitudes[measured_index] = 1.0 + 0j  # Complex one
        
        self.states[state_id] = QuantumState(
            amplitudes=new_amplitudes,
            state_type=StateType.GROUND,
            entangled_with=state.entangled_with,
            metadata=state.metadata
        )
        
        self.logger.info(f"Measured state {state_id}: result={measured_index}, probability={measured_probability}")
        return measured_index, measured_probability
    
    def collapse(self, state_id: str, target_state: int) -> None:
        """
        Collapse a quantum state to a specific basis state
        
        Args:
            state_id: State to collapse
            target_state: Target basis state index
            
        Raises:
            ValueError: If state_id doesn't exist or target_state is invalid
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
            
        state = self.states[state_id]
        dimensions = len(state.amplitudes)
        
        if target_state < 0 or target_state >= dimensions:
            raise ValueError(f"Target state {target_state} out of bounds for {dimensions}-dimensional system")
            
        # Create collapsed state
        new_amplitudes = np.zeros(dimensions, dtype=complex)
        new_amplitudes[target_state] = 1.0 + 0j
        
        self.states[state_id] = QuantumState(
            amplitudes=new_amplitudes,
            state_type=StateType.GROUND,
            entangled_with=state.entangled_with,
            metadata=state.metadata
        )
        
        self.logger.info(f"Collapsed state {state_id} to basis state {target_state}")
    
    def entangle(self, state_id_1: str, state_id_2: str) -> str:
        """
        Entangle two quantum states
        
        Args:
            state_id_1: First state identifier
            state_id_2: Second state identifier
            
        Returns:
            str: Entangled state identifier
            
        Raises:
            ValueError: If either state doesn't exist
        """
        if state_id_1 not in self.states or state_id_2 not in self.states:
            raise ValueError("One or both states not found")
            
        # Create entangled state ID
        entangled_id = f"entangled_{state_id_1}_{state_id_2}"
        
        # Tensor product of the two states
        state1 = self.states[state_id_1]
        state2 = self.states[state_id_2]
        
        # Perform tensor product of amplitudes
        entangled_amplitudes = np.kron(state1.amplitudes, state2.amplitudes)
        
        # Normalize the result
        norm = np.linalg.norm(entangled_amplitudes)
        if norm > 0:
            entangled_amplitudes = entangled_amplitudes / norm
        
        # Create new entangled state
        self.states[entangled_id] = QuantumState(
            amplitudes=entangled_amplitudes,
            state_type=StateType.ENTANGLED,
            entangled_with=[state_id_1, state_id_2]
        )
        
        self.current_state_id = entangled_id
        self.logger.info(f"Entangled states {state_id_1} and {state_id_2} into {entangled_id}")
        return entangled_id
    
    def get_state(self, state_id: str) -> Optional[QuantumState]:
        """
        Get the current quantum state
        
        Args:
            state_id: State identifier to retrieve
            
        Returns:
            QuantumState: The requested state or None if not found
        """
        return self.states.get(state_id, None)
    
    def create_bell_state(self, state_id: str, qubit1: int = 0, qubit2: int = 1) -> None:
        """
        Create a Bell state (|00> + |11>) / sqrt(2)
        
        Args:
            state_id: Identifier for the new state
            qubit1: First qubit index (default 0)
            qubit2: Second qubit index (default 1)
        """
        # Create 4-dimensional state vector for two qubits
        bell_state = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
        
        self.states[state_id] = QuantumState(
            amplitudes=bell_state,
            state_type=StateType.ENTANGLED,
            entangled_with=[f"q{qubit1}", f"q{qubit2}"]
        )
        
        self.current_state_id = state_id
        self.logger.info(f"Created Bell state {state_id}")
    
    def apply_hadamard(self, state_id: str, qubit_index: int) -> None:
        """
        Apply Hadamard gate to a specific qubit
        
        Args:
            state_id: State to apply gate to
            qubit_index: Index of qubit to apply gate
            
        Raises:
            ValueError: If state doesn't exist or index invalid
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
            
        state = self.states[state_id]
        dimensions = len(state.amplitudes)
        
        # For a qubit system, qubit index should be 0 for single qubit
        if dimensions == 2 and qubit_index != 0:
            raise ValueError(f"Invalid qubit index {qubit_index} for single qubit state")
        
        # Hadamard matrix for single qubit
        H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        
        # Apply to the state vector
        if len(state.amplitudes) == 2:
            # Single qubit case
            new_amplitudes = H @ state.amplitudes
            self.states[state_id].amplitudes = new_amplitudes
        else:
            # Multi-qubit case - apply H to specific qubit (more complex)
            # This is a simplified implementation
            self.logger.warning("Multi-qubit Hadamard application is not fully implemented")
            
        self.logger.info(f"Applied Hadamard gate to state {state_id}")

    def get_state_vector(self, state_id: str) -> np.ndarray:
        """
        Get the state vector for a given state ID
        
        Args:
            state_id: State identifier
            
        Returns:
            np.ndarray: State vector amplitudes
            
        Raises:
            ValueError: If state doesn't exist
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
        return self.states[state_id].amplitudes

    def get_state_probability(self, state_id: str, index: int) -> float:
        """
        Get probability of measuring a specific state index
        
        Args:
            state_id: State identifier
            index: Index to get probability for
            
        Returns:
            float: Probability of measuring that state index
            
        Raises:
            ValueError: If state doesn't exist or index invalid
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
            
        state = self.states[state_id]
        if index < 0 or index >= len(state.amplitudes):
            raise ValueError(f"Index {index} out of bounds")
            
        amplitude = state.amplitudes[index]
        return float(np.abs(amplitude) ** 2)

    def normalize_current_state(self) -> None:
        """Normalize the amplitudes of the current state"""
        if self.current_state_id and self.current_state_id in self.states:
            state = self.states[self.current_state_id]
            norm = np.linalg.norm(state.amplitudes)
            if norm > 0:
                state.amplitudes = state.amplitudes / norm
            self.logger.debug("Normalized current state vector")

    def add_decoherence(self, state_id: str, rate: float = 0.01) -> None:
        """
        Add decoherence effect to a state
        
        Args:
            state_id: State to apply decoherence to
            rate: Decoherence rate (default 0.01)
            
        Raises:
            ValueError: If state doesn't exist
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
            
        state = self.states[state_id]
        # Apply small random noise to amplitudes
        noise = np.random.normal(0, rate, len(state.amplitudes)) + \
                 1j * np.random.normal(0, rate, len(state.amplitudes))
        state.amplitudes = state.amplitudes + noise
        
        # Renormalize
        norm = np.linalg.norm(state.amplitudes)
        if norm > 0:
            state.amplitudes = state.amplitudes / norm
            
        self.logger.debug(f"Applied decoherence to state {state_id} with rate {rate}")

    def tensor_with(self, state_id_1: str, state_id_2: str, new_id: str) -> None:
        """
        Create tensor product of two states
        
        Args:
            state_id_1: First state
            state_id_2: Second state
            new_id: ID for new tensor product state
            
        Raises:
            ValueError: If states don't exist
        """
        if state_id_1 not in self.states or state_id_2 not in self.states:
            raise ValueError("One or both states not found")
            
        state1 = self.states[state_id_1]
        state2 = self.states[state_id_2]
        
        # Tensor product
        new_amplitudes = np.kron(state1.amplitudes, state2.amplitudes)
        
        # Normalize
        norm = np.linalg.norm(new_amplitudes)
        if norm > 0:
            new_amplitudes = new_amplitudes / norm
        
        self.states[new_id] = QuantumState(
            amplitudes=new_amplitudes,
            state_type=StateType.SUPERPOSITION,
            entangled_with=[state_id_1, state_id_2]
        )
        
        self.current_state_id = new_id
        self.logger.info(f"Created tensor product state {new_id} from {state_id_1} and {state_id_2}")

    def get_entanglement_entropy(self, state_id: str) -> float:
        """
        Calculate entanglement entropy of a state
        
        Args:
            state_id: State to calculate entropy for
            
        Returns:
            float: Entanglement entropy
            
        Raises:
            ValueError: If state doesn't exist
        """
        if state_id not in self.states:
            raise ValueError(f"State {state_id} not found")
            
        state = self.states[state_id]
        # Simplified entropy calculation
        # For a pure state, entropy is -sum(p_i * log(p_i)) where p_i = |amplitude_i|^2
        probabilities = np.abs(state.amplitudes) ** 2
        # Avoid log(0)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-50))
        return float(entropy)

    def __str__(self) -> str:
        """String representation of current quantum states"""
        if not self.states:
            return "No quantum states initialized"
        
        result = "Quantum States:\n"
        for state_id, state in self.states.items():
            result += f"  {state_id}: {state.state_type.value} with {len(state.amplitudes)} dimensions\n"
        return result.strip()