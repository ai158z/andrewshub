import numpy as np
import pytest
from codonic_layer.utils import (
    normalize_state,
    tensor_product,
    entanglement_entropy,
    fidelity_measure
)

def test_normalize_state_valid_input():
    state = np.array([1+1j, 2-1j, 3j])
    normalized = normalize_state(state)
    assert np.isclose(norm(normalized), 1.0)

def test_normalize_state_zero_vector():
    state = np.array([0, 0, 0])
    with pytest.raises(ValueError, match="Cannot normalize zero vector"):
        normalize_state(state)

def test_normalize_state_empty_array():
    state = np.array([])
    with pytest.raises(ValueError, match="State vector cannot be empty"):
        normalize_state(state)

def test_normalize_state_not_numpy_array():
    with pytest.raises(ValueError, match="State vector must be a numpy array"):
        normalize_state([1, 2, 3])  # type: ignore

def test_tensor_product_single_state():
    state = np.array([1, 0])
    result = tensor_product((state,))
    expected = state
    np.testing.assert_array_equal(result, expected)

def test_tensor_product_multiple_states():
    state1 = np.array([1, 0])
    state2 = np.array([0, 1])
    result = tensor_product((state1, state2))
    expected = np.kron(state1, state2)
    np.testing.assert_array_equal(result, expected)

def test_tensor_product_no_states():
    with pytest.raises(ValueError, match="At least one state vector must be provided"):
        tensor_product(())

def test_tensor_product_invalid_input():
    with pytest.raises(ValueError):
        tensor_product((None,))  # type: ignore

def test_entanglement_entropy_valid_input():
    # Pure state density matrix (should have 0 entropy)
    density_matrix = np.array([[1, 0], [0, 0]])
    entropy = entanglement_entropy(density_matrix)
    assert entropy == 0.0

def test_entanglement_entropy_invalid_density_matrix():
    with pytest.raises(ValueError, match="Density matrix must be a square matrix"):
        entanglement_entropy(np.array([1, 2, 3]))  # Not square

def test_entanglement_entropy_non_square_matrix():
    with pytest.raises(ValueError, match="Density matrix must be a square matrix"):
        entanglement_entropy(np.array([[1, 2]]))

def test_fidelity_measure_vector_states():
    state1 = np.array([1, 0])
    state2 = np.array([0, 1])
    fidelity = fidelity_measure(state1, state2)
    assert 0 <= fidelity <= 1

def test_fidelity_measure_density_matrices():
    state1 = np.array([[1, 0], [0, 0]], dtype=float)
    state2 = np.array([[0, 0], [0, 1]], dtype=float)
    fidelity = fidelity_measure(state1, state2)
    assert 0 <= fidelity <= 1

def test_fidelity_measure_incompatible_states():
    state1 = np.array([1, 0])  # Vector
    state2 = np.array([[0, 0], [0, 1]])  # Matrix - incompatible
    with pytest.raises(ValueError, match="Incompatible state types for fidelity calculation"):
        fidelity_measure(state1, state2)  # type: ignore

def test_fidelity_measure_invalid_input():
    state1 = "not_an_array"
    state2 = np.array([1, 0])
    with pytest.raises(ValueError, match="Both states must be numpy arrays"):
        fidelity_measure(state1, state2)  # type: ignore

def test_normalize_state_fidelity_with_self():
    state = np.array([1, 0, 0, 0])
    normalized = normalize_state(state)
    fidelity = fidelity_measure(state, state)
    assert np.isclose(fidelity, 1.0)

def test_fidelity_orthogonal_states():
    state1 = np.array([1, 0])
    state2 = np.array([0, 1])
    fidelity = fidelity_measure(state1, state2)
    # Orthogonal states should have 0 fidelity
    assert np.isclose(fidelity, 0.0)

def test_fidelity_same_state():
    state = np.array([1, 0])
    fidelity = fidelity_measure(state, state)
    # Same states should have fidelity 1
    assert np.isclose(fidelity, 1.0)

def test_fidelity_very_close_states():
    # Two very similar states should have high fidelity
    state1 = np.array([1, 1e-10])
    state2 = np.array([1, 2e-10])
    # Should be very close to 1
    assert fidelity_measure(state1, state2) > 0.99

def test_fidelity_orthogonal_example():
    # Create two orthogonal states
    state1 = np.array([1, 0])
    state2 = np.array([0, 1])
    # Fidelity should be 0
    assert np.isclose(fidelity_measure(state1, state2), 0.0)