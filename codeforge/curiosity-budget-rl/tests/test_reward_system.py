import numpy as np
import pytest
from unittest.mock import Mock, patch, MagicMock

from curiosity_budget.reward_system import RewardSystem


class TestRewardSystem:
    @pytest.fixture
    def mock_components(self):
        return {
            'agent': Mock(),
            'budget_manager': Mock(),
            'skill_selector': Mock(),
            'exploration_strategy': Mock(),
            'skill_valuation': Mock(),
            'models': {'curiosity': Mock()}
        }

    @pytest.fixture
    def reward_system(self, mock_components):
        with patch('curiosity_budget.reward_system.logging'):
            return RewardSystem(**mock_components)

    def test_init_success(self, mock_components):
        with patch('curiosity_budget.reward_system.logging'):
            rs = RewardSystem(**mock_components)
            assert rs.agent == mock_components['agent']
            assert rs.budget_manager == mock_components['budget_manager']
            assert rs.skill_selector == mock_components['skill_selector']
            assert rs.exploration_strategy == mock_components['exploration_strategy']
            assert rs.skill_valuation == mock_components['skill_valuation']
            assert rs.models == mock_components['models']
            assert rs.rewards_history == []
            assert rs.intrinsic_rewards == []
            assert rs.extrinsic_rewards == []

    def test_calculate_reward_with_none_states_raises_error(self, reward_system):
        with pytest.raises(ValueError, match="State and next_state cannot be None"):
            reward_system.calculate_reward(None, 1, np.array([1, 2, 3]))

    def test_calculate_reward_with_valid_inputs(self, reward_system):
        state = np.array([1, 2, 3], dtype=np.float32)
        next_state = np.array([2, 3, 4], dtype=np.float32)
        reward_system.models['curiosity'].return_value = Mock()
        reward_system.models['curiosity'].return_value.detach().cpu().numpy.return_value = np.array([2, 3, 4])
        
        with patch('torch.no_grad'), patch('torch.FloatTensor') as mock_tensor:
            mock_tensor.return_value.unsqueeze.return_value = Mock()
            result, components = reward_system.calculate_reward(state, 0, next_state)
            assert isinstance(result, float)
            assert 'intrinsic' in components
            assert 'extrinsic' in components
            assert 'skill_bonus' in components

    def test_calculate_intrinsic_reward_with_no_model(self, reward_system):
        reward_system.models = {}
        reward = reward_system._calculate_intrinsic_reward(np.array([1, 2]), np.array([3, 4]))
        assert reward == 0.0

    def test_calculate_intrinsic_reward_with_none_states(self, reward_system):
        reward = reward_system._calculate_intrinsic_reward(None, np.array([1, 2]))
        assert reward == 0.0

    def test_calculate_intrinsic_reward_with_valid_states(self, reward_system):
        state = np.array([1, 2, 3], dtype=np.float32)
        next_state = np.array([2, 3, 4], dtype=np.float32)
        model_mock = Mock()
        model_mock.return_value = Mock()
        with patch('torch.no_grad'), patch('torch.FloatTensor') as mock_tensor:
            mock_tensor.return_value = Mock()
            mock_tensor.return_value.unsqueeze.return_value = Mock()
            reward_system.models = {'curiosity': model_mock}
            result = reward_system._calculate_intrinsic_reward(state, next_state)
            assert isinstance(result, float)

    def test_calculate_extrinsic_reward_with_none_states(self, reward_system):
        result = reward_system._calculate_extrinsic_reward(None, 1, None)
        assert result == 0.0

    def test_calculate_extrinsic_reward_with_valid_states(self, reward_system):
        state = np.array([0, 0, 0])
        next_state = np.array([1, 1, 1])
        result = reward_system._calculate_extrinsic_reward(state, 0, next_state)
        assert isinstance(result, float)
        assert 0 <= result <= 1

    def test_update_rewards_with_none_reward_raises_error(self, reward_system):
        with pytest.raises(ValueError, match="Reward cannot be None"):
            reward_system.update_rewards(None, np.array([1]), 0, np.array([2]))

    def test_update_rewards_calls_agent_learn(self, reward_system):
        reward_system.update_rewards(1.0, np.array([1]), 0, np.array([2]), "skill1")
        reward_system.agent.learn.assert_called_once_with(
            np.array([1]), 0, 1.0, np.array([2]), "skill1"
        )

    def test_update_rewards_calls_skill_selector_update(self, reward_system):
        reward_system.update_rewards(1.0, np.array([1]), 0, np.array([2]), "skill1")
        reward_system.skill_selector.update_skills.assert_called_once_with("skill1", 1.0)

    def test_update_rewards_calls_budget_manager_update(self, reward_system):
        reward_system.update_rewards(1.0, np.array([1]), 0, np.array([2]))
        reward_system.budget_manager.update_budget.assert_called_once()

    def test_get_reward_statistics_empty_history(self, reward_system):
        stats = reward_system.get_reward_statistics()
        assert stats['mean_total'] == 0.0
        assert stats['mean_intrinsic'] == 0.0
        assert stats['mean_extrinsic'] == 0.0
        assert stats['total_rewards'] == 0

    def test_get_reward_statistics_with_history(self, reward_system):
        # Add some rewards to history
        reward_system.rewards_history = [1.0, 2.0, 3.0]
        reward_system.intrinsic_rewards = [0.5, 1.0, 1.5]
        reward_system.extrinsic_rewards = [0.5, 1.0, 1.5]
        
        stats = reward_system.get_reward_statistics()
        assert stats['mean_total'] == 2.0
        assert stats['mean_intrinsic'] == 1.0
        assert stats['mean_extrinsic'] == 1.0
        assert stats['total_rewards'] == 3

    def test_calculate_reward_with_skill_bonus(self, reward_system):
        # Setup
        reward_system.skill_valuation.get_value.return_value = 0.5
        reward_system.budget_manager.get_budget.return_value = 0.8
        state = np.array([1, 2, 3], dtype=np.float32)
        next_state = np.array([2, 3, 4], dtype=np.float32)
        
        with patch('torch.no_grad'), patch('torch.FloatTensor'):
            total_reward, components = reward_system.calculate_reward(
                state, 0, next_state, "skill123"
            )
            assert isinstance(total_reward, float)
            assert components['skill_bonus'] == 0.4  # 0.5 * 0.8

    def test_calculate_reward_without_skill_id(self, reward_system):
        state = np.array([1, 2, 3], dtype=np.float32)
        next_state = np.array([2, 3, 4], dtype=np.float32)
        
        with patch('torch.no_grad'), patch('torch.FloatTensor'):
            total_reward, components = reward_system.calculate_reward(
                state, 0, next_state
            )
            assert components['skill_bonus'] == 0.0
            assert 'intrinsic' in components
            assert 'extrinsic' in components

    def test_calculate_reward_components_accumulation(self, reward_system):
        state = np.array([1, 2, 3], dtype=np.float32)
        next_state = np.array([2, 3, 4], dtype=np.float32)
        reward_system.models['curiosity'].return_value = Mock()
        with patch('torch.no_grad'), patch('torch.FloatTensor'):
            total_reward, components = reward_system.calculate_reward(
                state, 0, next_state, "skill1"
            )
            # Check that all components are included in total
            expected_total = (components['intrinsic'] + 
                          components['extrinsic'] + 
                          components['skill_bonus'])
            assert abs(total_reward - expected_total) < 1e-10

    def test_calculate_reward_with_missing_curiosity_model(self, reward_system):
        state = np.array([1, 2, 3], dtype=np.float32)
        next_state = np.array([2, 3, 4], dtype=np.float32)
        reward_system.models = {}
        total_reward, components = reward_system.calculate_reward(
            state, 0, next_state
        )
        assert components['intrinsic'] == 0.0  # Should be 0 when no model

    def test_update_rewards_with_default_skill(self, reward_system):
        state = np.array([1, 2])
        next_state = np.array([2, 3])
        reward_system.update_rewards(1.0, state, 0, next_state)
        reward_system.budget_manager.update_budget.assert_called_with("default", 1.0)