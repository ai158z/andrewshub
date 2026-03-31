import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from codonic_layer.quantum_states import QuantumStates, QuantumState, StateType

class TestQuantumStates:
    def test_initialize_superposition_valid(self):
        manager = QuantumStates()
        state_id = manager.initialize_superposition("test_state", 2)
        assert state_id == "test_state"
        state = manager.get_state("test_state")
        assert state is not None
        assert state.state_type == StateType.SUPERPOSITION

    def test_initialize_superposition_invalid_dimensions(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.initialize_superposition("test", 0)

    def test_measure_existing_state(self):
        manager = QuantumStates()
        manager.initialize_superposition("test_state", 2)
        result = manager.measure("test_state")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_measure_nonexistent_state(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.measure("nonexistent")

    def test_collapse_valid_state(self):
        manager = QuantumStates()
        manager.initialize_superposition("test_state", 2)
        # Should not raise
        manager.collapse("test_state", 0)

    def test_collapse_invalid_target(self):
        manager = QuantumStates()
        manager.initialize_superposition("test_state", 2)
        with pytest.raises(ValueError):
            manager.collapse("test_state", 5)  # Invalid index

    def test_collapse_state_not_found(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.collapse("nonexistent", 0)

    def test_entangle_valid_states(self):
        manager = QuantumStates()
        manager.initialize_superposition("state1", 2)
        manager.initialize_superposition("state2", 2)
        entangled_id = manager.entangle("state1", "state2")
        assert entangled_id == "entangled_state1_state2"

    def test_entangle_nonexistent_state(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.entangle("state1", "nonexistent")

    def test_get_state_existing(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        state = manager.get_state("test")
        assert state is not None

    def test_get_state_nonexistent(self):
        manager = QuantumStates()
        state = manager.get_state("nonexistent")
        assert state is None

    def test_create_bell_state(self):
        manager = QuantumStates()
        manager.create_bell_state("bell_state")
        state = manager.get_state("bell_state")
        assert state is not None
        assert state.state_type == StateType.ENTANGLED

    def test_apply_hadamard_valid(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        # Should not raise
        manager.apply_hadamard("test", 0)

    def test_apply_hadamard_invalid_state(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.apply_hadamard("nonexistent", 0)

    def test_get_state_probability_valid(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        prob = manager.get_state_probability("test", 0)
        assert 0 <= prob <= 1

    def test_get_state_probability_invalid_state(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.get_state_probability("nonexistent", 0)

    def test_get_state_probability_invalid_index(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        with pytest.raises(ValueError):
            manager.get_state_probability("test", 5)

    def test_tensor_with_valid(self):
        manager = QuantumStates()
        manager.initialize_superposition("state1", 2)
        manager.initialize_superposition("state2", 2)
        manager.tensor_with("state1", "state2", "tensor_state")
        state = manager.get_state("tensor_state")
        assert state is not None

    def test_tensor_with_nonexistent(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.tensor_with("state1", "nonexistent", "tensor")

    def test_get_state_vector_existing(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        vector = manager.get_state_vector("test")
        assert len(vector) == 2

    def test_get_state_vector_nonexistent(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.get_state_vector("nonexistent")

    def test_get_state_vector_invalid(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.get_state_vector("nonexistent")

    def test_normalize_current_state(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        # Mock the current state
        original_norm = np.linalg.norm(manager.get_state_vector("test"))
        manager.normalize_current_state()
        # Normalization should result in unit vector
        normalized_norm = np.linalg.norm(manager.get_state_vector("test"))
        assert abs(normalized_norm - 1.0) < 1e-10

    def test_add_decoherence_existing(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        # Should not raise
        manager.add_decoherence("test")

    def test_add_decoherence_nonexistent(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.add_decoherence("nonexistent")

    def test_get_entanglement_entropy_existing(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        entropy = manager.get_entanglement_entropy("test")
        assert isinstance(entropy, float)

    def test_get_entanglement_entropy_nonexistent(self):
        manager = QuantumStates()
        with pytest.raises(ValueError):
            manager.get_entanglement_entropy("nonexistent")

    def test_str_representation(self):
        manager = QuantumStates()
        manager.initialize_superposition("test", 2)
        s = str(manager)
        assert "Quantum States:" in s