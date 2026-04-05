import pytest
import torch
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.rl_agent import RLAgent

@pytest.fixture
def mock_observation_space():
    obs_space = Mock()
    obs_space.shape = (4,)
    obs_space.n = 4
    return obs_space

@pytest.fixture
def mock_action_space():
    action_space = Mock()
    action_space.n = 2
    return action_space

@pytest.fixture
def basic_config():
    return {"learning_rate": 0.001, "max_buffer_size": 1000}

@pytest.fixture
def rl_agent(mock_observation_space, mock_action_space, basic_config):
    with patch('src.rl_agent.validate_observation_space'), \
         patch('src.rl_agent.validate_action_space'), \
         patch('src.rl_agent.SkillCatalog'), \
         patch('src.rl_agent.SkillManager'), \
         patch('src.rl_agent.CuriosityAllocator'), \
         patch('src.rl_agent.TaskScorer'):
        agent = RLAgent(
            observation_space=mock_observation_space,
            action_space=mock_action_space,
            config=basic_config
        )
    return agent

def test_init_validates_spaces(mock_observation_space, mock_action_space):
    with patch('src.rl_agent.validate_observation_space') as mock_validate_obs, \
         patch('src.rl_agent.validate_action_space') as mock_validate_act, \
         patch('src.rl_agent.SkillCatalog'), \
         patch('src.rl_agent.SkillManager'), \
         patch('src.rl_agent.CuriosityAllocator'), \
         patch('src.rl_agent.TaskScorer'):
        
        RLAgent(mock_observation_space, mock_action_space)
        mock_validate_obs.assert_called_once()
        mock_validate_act.assert_called_once()

def test_build_policy_network(rl_agent):
    assert rl_agent.policy_network is not None
    assert hasattr(rl_agent.policy_network, 'parameters')

def test_select_action(rl_agent):
    observation = np.array([0.1, 0.2, 0.3, 0.4])
    with patch('torch.randn', return_value=torch.tensor([0.1, 0.9])):
        action, info = rl_agent.select_action(observation)
        assert isinstance(action, int)
        assert 'action_prob' in info
        assert 'curiosity_bonus' in info

def test_learn(rl_agent):
    observations = np.array([[0.1, 0.2, 0.3, 0.4]])
    actions = np.array([1])
    rewards = np.array([1.0])
    next_observations = np.array([[0.2, 0.3, 0.4, 0.5]])
    dones = np.array([False])
    
    with patch.object(rl_agent.policy_network, 'parameters', return_value=iter([torch.nn.Parameter()])) as mock_params:
        mock_params.return_value = iter([torch.nn.Parameter(torch.randn(2, 2))])
        metrics = rl_agent.learn(observations, actions, rewards, next_observations, dones)
        assert 'loss' in metrics
        assert 'mean_curiosity' in metrics
        assert 'mean_reward' in metrics

def test_save_model(rl_agent, tmp_path):
    model_path = tmp_path / "test_model.pth"
    with patch('torch.save') as mock_save:
        rl_agent.save_model(str(model_path))
        mock_save.assert_called_once()

def test_load_model(rl_agent, tmp_path):
    model_path = tmp_path / "test_model.pth"
    with patch('torch.save'), patch('torch.load') as mock_load:
        mock_load.return_value = {
            'policy_network_state_dict': {},
            'optimizer_state_dict': {},
            'observation_space': None,
            'action_space': None
        }
        rl_agent.load_model(str(model_path))

def test_add_experience(rl_agent):
    observation = np.array([0.1, 0.2, 0.3, 0.4])
    action = 1
    reward = 1.0
    next_observation = np.array([0.2, 0.3, 0.4, 0.5])
    done = False
    
    rl_agent.add_experience(observation, action, reward, next_observation, done)
    assert len(rl_agent.replay_buffer) == 1

def test_get_exploration_bonus(rl_agent):
    state = np.array([0.1, 0.2, 0.3, 0.4])
    bonus = rl_agent.get_exploration_bonus(state)
    assert isinstance(bonus, float)

def test_select_action_deterministic(rl_agent):
    observation = np.array([0.1, 0.2, 0.3, 0.4])
    with patch('torch.randn', return_value=torch.tensor([0.1, 0.9])), \
         patch('numpy.random.rand', return_value=0.0):  # Below curiosity threshold
        action, info = rl_agent.select_action(observation)
        assert isinstance(action, int)
        assert 'action_prob' in info

def test_select_action_stochastic(rl_agent):
    observation = np.array([0.1, 0.2, 0.3, 0.4])
    with patch('torch.randn', return_value=torch.tensor([0.1, 0.9])), \
         patch('numpy.random.rand', return_value=0.9):  # Above curiosity threshold
        action, info = rl_agent.select_action(observation)
        assert isinstance(action, int)
        assert 'action_prob' in info

def test_learn_empty_arrays(rl_agent):
    observations = np.array([])
    actions = np.array([])
    rewards = np.array([])
    next_observations = np.array([])
    dones = np.array([])
    
    with pytest.raises(Exception):
        rl_agent.learn(observations, actions, rewards, next_observations, dones)

def test_add_experience_buffer_full(rl_agent):
    # Fill buffer to max size
    for i in range(rl_agent.max_buffer_size + 5):
        rl_agent.add_experience(
            np.array([0.1, 0.2, 0.3, 0.4]), 
            1, 
            1.0, 
            np.array([0.2, 0.3, 0.4, 0.5]), 
            False
        )
    assert len(rl_agent.replay_buffer) == rl_agent.max_buffer_size

def test_get_exploration_bonus_edge_case(rl_agent):
    state = np.array([0.0, 0.0, 0.0, 0.0])
    bonus = rl_agent.get_exploration_bonus(state)
    assert isinstance(bonus, float)

def test_select_action_with_empty_observation(rl_agent):
    observation = np.array([])
    with pytest.raises(Exception):
        rl_agent.select_action(observation)

def test_select_action_with_invalid_observation(rl_agent):
    observation = None
    with pytest.raises(Exception):
        rl_agent.select_action(observation)

def test_learn_with_mismatched_dimensions(rl_agent):
    observations = np.array([[0.1, 0.2, 0.3, 0.4]])
    actions = np.array([1, 2])  # Mismatched dimensions
    rewards = np.array([1.0])
    next_observations = np.array([[0.2, 0.3, 0.4, 0.5]])
    dones = np.array([False])
    
    with pytest.raises(Exception):
        rl_agent.learn(observations, actions, rewards, next_observations, dones)

def test_save_model_invalid_path(rl_agent):
    with pytest.raises(Exception):
        rl_agent.save_model("/invalid/path/model.pth")

def test_load_model_invalid_path(rl_agent):
    with pytest.raises(Exception):
        rl_agent.load_model("/invalid/path/model.pth")

def test_add_experience_with_none_values(rl_agent):
    with pytest.raises(Exception):
        rl_agent.add_experience(None, None, None, None, None)