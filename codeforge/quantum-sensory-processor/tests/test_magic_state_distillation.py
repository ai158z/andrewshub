import pytest
import numpy as np
from src.magic_state_distillation import MagicStateDistillation

class TestMagicStateDistillation:
    
    def test_distill_empty_states_raises_error(self):
        msd = MagicStateDistillation()
        with pytest.raises(ValueError, match="No states provided for distillation"):
            msd.distill([])
    
    def test_distill_invalid_states_type_raises_error(self):
        msd = MagicStateDistillation()
        with pytest.raises(TypeError):
            msd._validate_states("not a list")
    
    def test_distill_valid_states_returns_refined(self):
        msd = MagicStateDistillation()
        states = [[1+0j, 0+0j], [0+0j, 1+0j]]
        result = msd.distill(states)
        assert len(result) == len(states)
        # Verify states are normalized
        for state in result:
            norm = np.linalg.norm(np.array(state))
            np.testing.assert_allclose(norm, 1.0, atol=1e-10)
    
    def test_purify_states_empty_raises_error(self):
        msd = MagicStateDistillation()
        with pytest.raises(ValueError, match="No noisy states provided for purification"):
            msd.purify_states([])
    
    def test_purify_states_valid_input(self):
        msd = MagicStateDistillation()
        noisy = [[0.8+0j, 0.6+0j], [0.5+0j, 0.5+0j]]
        result = msd.purify_states(noisy)
        assert len(result) == len(noisy)
        for state in result:
            assert isinstance(state, list)
    
    def test_calculate_fidelity_none_state_raises(self):
        msd = MagicStateDistillation()
        with pytest.raises(ValueError, match="State cannot be None"):
            msd.calculate_fidelity(None)
    
    def test_calculate_fidelity_valid_input(self):
        msd = MagicStateDistillation()
        state = [1+0j, 0+0j]
        fidelity = msd.calculate_fidelity(state)
        assert isinstance(fidelity, float)
        assert 0 <= fidelity <= 1.0
    
    def test_normalize_state_zero_norm_raises(self):
        msd = MagicStateDistillation()
        with pytest.raises(ValueError, match="Cannot normalize zero state"):
            msd._normalize_state([0+0j, 0+0j])
    
    def test_validate_states_empty_state_raises(self):
        msd = MagicStateDistillation()
        with pytest.raises(ValueError, match="Empty state vector provided"):
            msd._validate_states([[]])
    
    def test_validate_states_invalid_type_raises(self):
        msd = MagicStateDistillation()
        with pytest.raises(TypeError, match="Each state must be a list of complex numbers"):
            msd._validate_states(["not_a_list"])
    
    def test_purify_state_empty(self):
        msd = MagicStateDistillation()
        result = msd._purify_state([])
        assert result == []
    
    def test_purify_state_zero_norm(self):
        msd = MagicStateDistillation()
        result = msd._purify_state([0, 0])
        assert result == [0, 0]
    
    def test_normalize_state_valid(self):
        msd = MagicStateDistillation()
        state = [3+0j, 4+0j]
        result = msd._normalize_state(state)
        expected = [3/5+0j, 4/5+0j]
        np.testing.assert_allclose(result, expected, atol=1e-10)
    
    def test_calculate_state_purity(self):
        msd = MagicStateDistillation()
        state = [1/np.sqrt(2), 1/np.sqrt(2)]
        purity = msd._calculate_state_purity(state)
        assert 0 <= purity <= 1.0
    
    def test_apply_distillation_empty(self):
        msd = MagicStateDistillation()
        with pytest.raises(ValueError):
            msd._apply_distillation([])
    
    def test_apply_distillation_valid(self):
        msd = MagicStateDistillation()
        states = [[1+0j, 0+0j], [0+0j, 1+0j]]
        result = msd._apply_distillation(states)
        assert len(result) == 2
        for state in result:
            norm = np.linalg.norm(np.array(state))
            np.testing.assert_allclose(norm, 1.0, atol=1e-10)
    
    def test_purify_states_empty_input(self):
        msd = MagicStateDistillation()
        result = msd.purify_states([])
        assert result == []
    
    def test_purify_states_valid_input_states(self):
        msd = MagicStateDistillation()
        noisy = [[0.6+0j, 0.8+0j], [0.8+0j, 0.6+0j]]
        result = msd.purify_states(noisy)
        assert len(result) == 2
        for state in result:
            assert isinstance(state, list)
    
    def test_validate_states_validates_correctly(self):
        msd = MagicStateDistillation()
        states = [[1+0j, 0+0j], [0+0j, 1+0j]]
        # Should not raise any exception
        msd._validate_states(states)
    
    def test_validate_states_invalid_input_type(self):
        msd = MagicStateDistillation()
        with pytest.raises(TypeError, match="States must be provided as a list"):
            msd._validate_states("invalid")
    
    def test_validate_states_invalid_state_type(self):
        msd = MagicStateDistillation()
        with pytest.raises(TypeError, match="Each state must be a list of complex numbers"):
            msd._validate_states([1, 2, 3])  # Not lists of complex numbers
    
    def test_fidelity_with_list_state(self):
        msd = MagicStateDistillation()
        state = [0.6+0j, 0.8+0j]
        fidelity = msd.calculate_fidelity(state)
        # For normalized state, fidelity should be 1.0
        np.testing.assert_allclose(fidelity, 1.0, atol=1e-10)