import numpy as np
from typing import Tuple, Union
import logging
from scipy.linalg import norm
import warnings

logger = logging.getLogger(__name__)

def normalize_state(state_vector: np.ndarray) -> np.ndarray:
    """
    Normalize a quantum state vector to unit length.
    
    Args:
        state_vector: Complex numpy array representing quantum state
        
    Returns:
        Normalized quantum state vector
        
    Raises:
        ValueError: If state_vector is not a valid numpy array or has zero norm
    """
    if not isinstance(state_vector, np.ndarray):
        raise ValueError("State vector must be a numpy array")
    
    if state_vector.size == 0:
        raise ValueError("State vector cannot be empty")
    
    state_norm = norm(state_vector)
    if state_norm == 0:
        raise ValueError("Cannot normalize zero vector")
    
    normalized = state_vector / state_norm
    logger.debug(f"State vector normalized with L2 norm: {state_norm}")
    return normalized

def tensor_product(states: Tuple[np.ndarray, ...]) -> np.ndarray:
    """
    Compute tensor product of multiple quantum state vectors.
    
    Args:
        states: Tuple of quantum state vectors
        
    Returns:
        Tensor product of all input states
        
    Raises:
        ValueError: If no states provided or if states have incompatible dimensions
    """
    if not states:
        raise ValueError("At least one state vector must be provided")
    
    # Validate all inputs are numpy arrays
    for i, state in enumerate(states):
        if not isinstance(state, np.ndarray):
            raise ValueError(f"State {i} is not a numpy array")
    
    # Compute tensor product using Kronecker product
    result = states[0]
    for state in states[1:]:
        result = np.kron(result, state)
    
    logger.debug(f"Tensor product computed with final dimension: {result.shape}")
    return result

def entanglement_entropy(density_matrix: np.ndarray, 
                       base: Union[str, int, float] = 'e') -> float:
    """
    Calculate the von Neumann entropy of a quantum state's density matrix.
    
    Args:
        density_matrix: Square numpy array representing density matrix
        base: Logarithm base for entropy calculation ('e', 2, 10, or custom)
        
    Returns:
        Entanglement entropy value (float)
        
    Raises:
        ValueError: If density matrix is invalid or not square
    """
    if not isinstance(density_matrix, np.ndarray):
        raise ValueError("Density matrix must be a numpy array")
    
    if density_matrix.ndim != 2 or density_matrix.shape[0] != density_matrix.shape[1]:
        raise ValueError("Density matrix must be a square matrix")
    
    # Calculate eigenvalues of the density matrix
    eigenvalues = np.linalg.eigvals(density_matrix)
    
    # Filter out zero eigenvalues to avoid log(0)
    # Use small epsilon to handle numerical errors
    epsilon = 1e-15
    valid_eigenvalues = eigenvalues[eigenvalues > epsilon]
    
    if valid_eigenvalues.size == 0:
        logger.warning("No valid eigenvalues found for entropy calculation")
        return 0.0
    
    # Calculate von Neumann entropy: S = -Tr(ρ*ln(ρ))
    if base == 'e':
        entropy = -np.sum(valid_eigenvalues * np.log(valid_eigenvalues))
    elif base == 2:
        entropy = -np.sum(valid_eigenvalues * np.log2(valid_eigenvalues))
    elif base == 10:
        entropy = -np.sum(valid_eigenvalues * np.log10(valid_eigenvalues))
    else:
        entropy = -np.sum(valid_eigenvalues * np.log(valid_eigenvalues) / np.log(base))
    
    logger.debug(f"Calculated entanglement entropy: {entropy}")
    return entropy

def fidelity_measure(state1: np.ndarray, state2: np.ndarray) -> float:
    """
    Calculate fidelity between two quantum states (vectors or density matrices).
    
    Args:
        state1: First quantum state
        state2: Second quantum state
        
    Returns:
        Fidelity value between 0 and 1
        
    Raises:
        ValueError: If states are not compatible
    """
    if not isinstance(state1, np.ndarray) or not isinstance(state2, np.ndarray):
        raise ValueError("Both states must be numpy arrays")
    
    if state1.shape != state2.shape:
        raise ValueError("States must have the same dimensions")
    
    # For state vectors, fidelity is |⟨ψ₁|ψ₂⟩|²
    if state1.ndim == 1 and state2.ndim == 1:
        # Normalize states if needed
        norm1, norm2 = norm(state1), norm(state2)
        if not np.isclose(norm1, 1.0):
            state1 = state1 / norm1
        if not np.isclose(norm2, 1.0):
            state2 = state2 / norm2
        # Fidelity for pure states: |⟨ψ₁|ψ₂⟩|²
        inner_product = np.dot(state1.conj(), state2)
        fidelity = abs(inner_product)**2
    # For density matrices, use Tr(√(√ρ₁ * ρ₂ * √ρ₁))²
    elif state1.ndim == 2 and state2.ndim == 2:
        # Use the proper formula for density matrices: Tr(√(√ρ₁ * ρ₂ * √ρ₁)) 
        # which simplifies to Tr(√(ρ₁*ρ₂)) for commuting matrices
        from scipy.linalg import sqrtm
        sqrt_rho1 = sqrtm(state1)
        product = np.dot(sqrt_rho1, np.dot(state2, sqrt_rho1))
        sqrt_product = sqrtm(product)
        fidelity = np.trace(sqrt_product).real
        fidelity = fidelity**2
        # Ensure fidelity is bounded between 0 and 1
        fidelity = np.clip(fidelity, 0.0, 1.0)
    else:
        raise ValueError("Incompatible state types for fidelity calculation")
    
    logger.debug(f"Calculated fidelity: {fidelity}")
    return float(fidelity)