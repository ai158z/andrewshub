import numpy as np
from typing import List, Dict, Union
import math
import logging

logger = logging.getLogger(__name__)

def normalize_state(state: List[complex]) -> List[complex]:
    """
    Normalize a quantum state vector.
    
    Args:
        state: List of complex numbers representing quantum state amplitudes
        
    Returns:
        Normalized state vector
        
    Raises:
        ValueError: If state is empty or normalization fails
    """
    if not state:
        raise ValueError("State vector cannot be empty")
    
    # Convert to numpy array for easier computation
    state_array = np.array(state, dtype=complex)
    
    # Calculate the norm
    norm = np.linalg.norm(state_array)
    
    if norm == 0:
        raise ValueError("Cannot normalize a zero state vector")
    
    # Normalize the state
    normalized_state = state_array / norm
    
    return normalized_state.tolist()

def calculate_entropy(state: Dict[str, float]) -> float:
    """
    Calculate the von Neumann entropy of a quantum state.
    
    Args:
        state: Dictionary representing quantum state with probabilities
        
    Returns:
        Entropy value (in bits)
        
    Raises:
        ValueError: If state contains invalid probabilities
    """
    if not state:
        raise ValueError("State cannot be empty")
    
    # Validate that all values are probabilities
    total_prob = 0.0
    for prob in state.values():
        if not (0 <= prob <= 1):
            raise ValueError("All state values must be probabilities between 0 and 1")
        total_prob += prob
    
    if abs(total_prob - 1.0) > 1e-10:
        raise ValueError("Probabilities must sum to 1")
    
    # Calculate entropy
    entropy = 0.0
    for prob in state.values():
        if prob > 0:  # Avoid log(0)
            entropy -= prob * math.log2(prob)
    
    return entropy

def tensor_product(states: List[List[complex]]) -> List[complex]:
    """
    Calculate the tensor product of multiple quantum states.
    
    Args:
        states: List of quantum state vectors
        
    Returns:
        Resultant state vector from tensor product
        
    Raises:
        ValueError: If states list is empty or contains invalid states
    """
    if not states:
        raise ValueError("States list cannot be empty")
    
    # Validate input states
    for i, state in enumerate(states):
        if not state:
            raise ValueError(f"State {i} is empty")
    
    # Start with the first state
    result = np.array(states[0], dtype=complex)
    
    # Calculate tensor product iteratively
    for i in range(1, len(states)):
        # Tensor product with next state
        result = np.kron(result, np.array(states[i], dtype=complex))
    
    return result.tolist()