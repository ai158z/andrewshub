import pytest
from unittest.mock import Mock, patch, MagicMock
import torch
import numpy as np
from curiosity_budget.agent import CuriosityAgent

@pytest.fixture
def config():
    return {"budget": 100, "skills": ["explore", "exploit"], "device": "cpu"}

@pytest.fixture
def agent(config):
    with patch("curiosity_budget.agent.ModelManager") as mock_model_manager, \
         patch("curiosity_budget.agent.BudgetManager") as mock_budget_manager, \
         patch("curiosity_budget.agent.BudgetAllocator") as mock_budget_allocator, \
         patch("curiosity_budget.agent.SkillSelector") as mock_skill_selector, \
         patch("curiosity_budget.agent.RewardSystem") as mock_reward_system, \
         patch("curiosity_budget.agent.ExplorationModule") as mock_exploration_module, \
         patch("curiosity_budget.agent.SkillValuation") as mock_skill_valuation, \
         patch("curiosity_budget.agent.Utils") as mock_utils:
        
        agent = CuriosityAgent(config)
        agent.model_manager = mock_model_manager
        agent.budget_allocator = mock_budget_allocator
        agent.skill_selector = mock_skill_selector
        agent.budget_manager = mock_budget_manager
        agent.reward_system = mock_reward_system
        agent.exploration_module = mock_exploration_module
        agent.skill_valuation = mock_skill_valuation
        agent.utils = mock_utils
        return agent

def test_init_with_valid_config(agent):
    assert agent is not None

def test_act_explore_mode(agent):
    state = np.array([1, 2, 3])
    agent.exploration_module.should_explore.return_value = True
    agent.skill_selector.select_skill.return_value = "explore_action"
    action = agent.act(state)
    assert action == "explore_action"

def test_act_exploit_mode(agent):
    state = np.array([1, 2, 3])
    agent.exploration_module.should_explore.return_value = False
    agent.baseline_policy.return_value = "exploit_action"
    action = agent.act(state)
    assert action == "exploit_action"

def test_learn_updates_when_done(agent):
    state, action, reward, next_state, done = np.array([1]), 0, 1.0, np.array([2]), True
    agent.learn(state, action, reward, next_state, done)
    agent.update.assert_called_once_with(state, action, reward, next_state)

def test_learn_resets_exploration_when_not_done(agent):
    state, action, reward, next_state, done = np.array([1]), 0, 1.0, np.array([2]), False
    agent.learn(state, action, reward, next_state, done)
    agent.exploration_module.reset.assert_called_once()

def test_load_model_success(agent):
    agent.utils.load_model.return_value = "mock_model"
    result = agent.load("fake_path")
    assert result is True

def test_load_model_failure(agent):
    agent.utils.load_model.return_value = None
    result = agent.load("fake_path")
    assert result is False

def test_save_model(agent):
    agent.utils.save_model.return_value = True
    result = agent.save("fake_path")
    assert result is True

def test_save_model_failure(agent):
    agent.utils.save_model.return_value = False
    result = agent.save("fake_path")
    assert result is False

def test_act_with_torch_tensor(agent):
    state = torch.tensor([1, 2, 3], dtype=torch.float32)
    agent.exploration_module.should_explore.return_value = True
    agent.skill_selector.select_skill.return_value = 0
    action = agent.act(state)
    assert action == 0

def test_act_with_numpy_array(agent):
    state = np.array([1, 2, 3])
    agent.exploration_module.should_explore.return_value = True
    agent.skill_selector.select_skill.return_value = 0
    action = agent.act(state)
    assert action == 0

def test_baseline_policy_not_implemented(agent):
    state = np.array([1, 2, 3])
    agent.exploration_module.should_explore.return_value = False
    agent.baseline_policy = Mock(return_value="mock_action")
    action = agent.act(state)
    agent.baseline_policy.assert_called_with(state)
    assert action == "mock_action"

def test_learn_calls_model_update_when_done(agent):
    state = np.array([1])
    action = 0
    reward = 1.0
    next_state = np.array([2])
    done = True
    agent.model = Mock()
    agent.learn(state, action, reward, next_state, done)
    agent.model.update.assert_called_once_with(state, action, reward, next_state)

def test_learn_initializes_model_when_none(agent):
    state = np.array([1])
    action = 0
    reward = 1.0
    next_state = np.array([2])
    done = True
    agent.model = None
    agent.model_manager.model = Mock(return_value=Mock())
    agent.learn(state, action, reward, next_state, done)
    agent.model_manager.model.assert_called_once_with(state)
    agent.model_manager.model.return_value.learn.assert_called_once_with(state, action, reward, next_state)

def test_device_initialization():
    with patch("curiosity_budget.agent.torch") as mock_torch:
        mock_torch.has_cuda = False
        mock_torch.device.return_value = "cpu_device"
        config = {}
        agent = CuriosityAgent(config)
        assert agent.device == "cpu_device"

def test_act_without_exploration_module(agent):
    state = np.array([1, 2, 3])
    agent.exploration_module = None
    agent.baseline_policy.return_value = "no_explore_action"
    action = agent.act(state)
    assert action == "no_explore_action"

def test_learn_with_none_model_and_done(agent):
    state, action, reward, next_state, done = np.array([1]), 0, 1.0, np.array([2]), True
    agent.model = None
    agent.model_manager.update.return_value = None
    agent.learn(state, action, reward, next_state, done)
    agent.model_manager.update.assert_called_once_with(state, action, reward, next_state)

def test_learn_resets_exploration_module(agent):
    state, action, reward, next_state, done = np.array([1]), 0, 1.0, np.array([2]), False
    agent.exploration_module.reset = Mock()
    agent.learn(state, action, reward, next_state, done)
    agent.exploration_module.reset.assert_called_once()

def test_save_returns_utils_result(agent):
    agent.utils.save_model = Mock(return_value=True)
    result = agent.save("test_path")
    assert result is True