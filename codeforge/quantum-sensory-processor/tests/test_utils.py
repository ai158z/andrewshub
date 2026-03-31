import pytest
import numpy as np
from src.utils import normalize_state, calculate_entropy, tensor_product

def test_normalize_state_normalizes_correctly():
    # Test that the function normalizes a state vector correctly
    state = [1+1j, 2-1j, -1+2j]
    result = normalize_state(state)
    expected_norm = np.linalg.norm(np.array(state, dtype=complex))
    assert abs(expected_norm - np.linalg.norm(np.array(result, dtype=complex))) < 1e-10

def test_normalize_state_empty_state_raises_error():
    with pytest.raises(ValueError, "State vector cannot be empty"):
        normalize_state([])

def test_normalize_state_handles_zero_state():
    with pytest.raises(ValueError, "Cannot normalize a zero state vector"):
        normalize_state([0j, 0j, 0j])

def test_calculate_entropy_valid_probabilities():
    state = {"00": 0.5, "01": 0.5, "10": 0.25, "11": 0.25}
    expected = 1.5
    entropy = calculate_entropy(state)
    assert abs(entropy - expected) < 1e-10, f"Calculated entropy: {entropy}"

def test_tensor_product_multiple_states():
    states = [[1+1j, 2-1j], [1-1j, 2+1j]]
    result = tensor_product(states)
    expected = np.kron(states[0], states[1])
    assert np.allclose(result, expected)

def test_tensor_product_empty_states_list():
    with pytest.raises(ValueError, "States list cannot be empty"):
        tensor_product([])

def test_tensor_product_single_qubit_states():
    # Test with single qubit states
    # This requires a mock or specific test values
    pass

class TestNormalizeState:
    
    def test_normalize_state_with_empty_list_raises_error(self):
        with pytest.raises(ValueError):
            normalize_state([])

    def test_normalize_state_with_valid_state(self):
        state = [3+4j, 2-3j]
        normalized = normalize_state(state)
        expected = np.array([3+4j, 2-3j]) / np.linalg.norm(np.array([3+4j, 2-3j], dtype=complex))
        assert np.allclose(normalized, expected)

    def test_normalize_valid_state_vector(self):
        # Test with valid state vector
        state = [1+1j, 2-1j, 3+1j]
        normalized = normalize_state(state)
        expected = [1+1j, 2-1j, 3+1j]
        assert np.allclose(normalized, expected)

    def test_calculate_entropy_valid_input(self):
        state = {"00": 0.5, "01": 0.3, "10": 0.2}
        entropy = calculate_entropy(state)
        expected = 1.5
        assert abs(entropy - expected) < 1e-10, "Calculated entropy does not match"

    def test_calculate_entropy_with_empty_state():
        with pytest.raises(ValueError, "State cannot be empty"):
            calculate_entropy({})

    def test_calculate_entropy_with_zero_probabilities():
        with pytest.raises(ValueError, "All state values must be probabilities between 0 and 1"):
            state = {"00": 0.5, "01": 0.3}
            calculate_entropy(state)

    def test_tensor_product_single_state():
        states = [[1, 2], [3, 4]]
        result = tensor_product(states)
        # Check if the result matches expected tensor product
        expected = np.kron(np.array([1, 2], dtype=complex), np.array([3, 4], dtype=complex))
        assert np.allclose(result, expected)

    def test_normalize_state_with_zero_norm():
        with pytest.raises(ValueError, "Cannot normalize a zero state vector"):
            state = [0, 0, 0, 0]
            normalize_state(state)

    def test_normalize_state_with_invalid_state():
        with pytest.raises(ValueError, "State vector cannot be empty"):
            state = []
            normalize_state(state)

    def test_calculate_entropy_with_invalid_state():
        with pytest.raises(ValueError, "State cannot be empty"):
            state = {}
            calculate_entropy(state)

    def test_tensor_product_empty_states():
        with pytest.raises(ValueError, "State cannot be empty"):
            tensor_product([])

    def test_tensor_product_invalid_states():
        states = [[], []]
        with pytest.raises(ValueError, "States list is empty"):
            tensor_product(states)