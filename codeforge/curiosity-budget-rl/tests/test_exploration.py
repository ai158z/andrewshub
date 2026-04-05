import pytest
import torch
import numpy as np
from unittest.mock import Mock, patch
from curiosity_budget.exploration import (
    EpsilonGreedy, CuriosityDrivenExploration, CountBasedExploration,
    ThompsonSamplingExploration, UCBExploration, create_exploration_strategy
)

# EpsilonGreedy tests
def test_epsilon_greedy_initialization():
    strategy = EpsilonGreedy(epsilon_start=0.5, epsilon_end=0.05, epsilon_decay=0.99)
    assert strategy.epsilon_start == 0.5
    assert strategy.epsilon_end == 0.05
    assert strategy.epsilon_decay == 0.99
    assert strategy.epsilon == 0.5

def test_epsilon_greedy_explore_greedy():
    strategy = EpsilonGreedy(epsilon_start=0.0, epsilon_end=0.0, epsilon_decay=1.0)  # Always greedy
    q_values = torch.tensor([0.1, 0.2, 0.8, 0.3])  # Best action is index 2
    with patch('torch.argmax') as mock_argmax:
        mock_argmax.return_value = torch.tensor(2)
        action = strategy.explore(q_values)
        assert action == 2

def test_epsilon_greedy_explore_random():
    strategy = EpsilonGreedy(epsilon_start=1.0, epsilon_end=1.0, epsilon_decay=1.0)  # Always random
    q_values = torch.tensor([0.1, 0.2, 0.3, 0.4])
    with patch('numpy.random.random') as mock_random:
        mock_random.return_value = 0.5  # This will trigger random selection
        strategy.explore(q_values)
        assert strategy.epsilon < 1.0  # Should have decayed

def test_epsilon_greedy_epsilon_decay():
    strategy = EpsilonGreedy(epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=0.9)
    initial_epsilon = strategy.epsilon
    q_values = torch.tensor([0.1, 0.2])
    
    # First call
    strategy.explore(q_values)
    first_epsilon = strategy.epsilon
    
    strategy.explore(q_values)
    second_epsilon = strategy.epsilon
    
    assert first_epsilon > second_epsilon  # Should decay
    assert strategy.epsilon >= strategy.epsilon_end  # Should not go below minimum

def test_epsilon_greedy_reset():
    strategy = EpsilonGreedy(epsilon_start=0.5, epsilon_end=0.1, epsilon_decay=0.9)
    q_values = torch.tensor([0.1, 0.2])
    
    # Change epsilon
    strategy.explore(q_values)
    assert strategy.epsilon != 0.5
    
    # Reset should restore initial value
    strategy.reset()
    assert strategy.epsilon == 0.5
    assert strategy.step_count == 0

# CuriosityDrivenExploration tests
def test_curiosity_driven_initialization():
    agent = Mock()
    budget_manager = Mock()
    skill_selector = Mock()
    reward_system = Mock()
    skill_valuation = Mock()
    model = Mock()
    
    strategy = CuriosityDrivenExploration(
        agent, budget_manager, skill_selector, reward_system, skill_valuation, model
    )
    assert strategy.agent == agent
    assert strategy.budget_manager == budget_manager
    assert strategy.skill_selector == skill_selector
    assert strategy.reward_system == reward_system
    assert strategy.skill_valuation == skill_valuation
    assert strategy.model == model

def test_curiosity_driven_explore():
    agent = Mock()
    agent.act.return_value = torch.tensor([0.25, 0.25, 0.25, 0.25])
    
    budget_manager = Mock()
    skill_selector = Mock()
    reward_system = Mock()
    skill_valuation = Mock()
    model = Mock()
    
    strategy = CuriosityDrivenExploration(
        agent, budget_manager, skill_selector, reward_system, skill_valuation, model
    )
    
    state = np.array([1, 2, 3])
    action = strategy.explore(state)
    assert isinstance(action, int)
    assert 0 <= action < 4  # Should be one of 4 actions

def test_curiosity_driven_reset():
    strategy = CuriosityDrivenExploration(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    strategy.state_visitation_count = {(1, 2): 5}
    strategy.reset()
    assert strategy.state_visitation_count == {}
    assert strategy.exploration_bonus == 0.0

# CountBasedExploration tests
def test_count_based_initialization():
    strategy = CountBasedExploration(bonus_coefficient=0.1)
    assert strategy.bonus_coefficient == 0.1

def test_count_based_explore():
    strategy = CountBasedExploration()
    state = np.array([1, 2, 3])
    action = strategy.explore(state)
    assert isinstance(action, int)
    assert 0 <= action < 10

def test_count_based_state_counting():
    strategy = CountBasedExploration()
    state = (1, 2, 3)
    
    # First visit
    strategy.explore(np.array(state))
    assert state in strategy.state_counts
    assert strategy.state_counts[state] == 1
    
    # Second visit
    strategy.explore(np.array(state))
    assert strategy.state_counts[state] == 2

def test_count_based_reset():
    strategy = CountBasedExploration()
    strategy.state_counts = {(1, 2): 5, (3, 4): 3}
    strategy.reset()
    assert strategy.state_counts == {}

# ThompsonSamplingExploration tests
def test_thompson_sampling_initialization():
    strategy = ThompsonSamplingExploration(n_arms=5)
    assert len(strategy.successes) == 5
    assert len(strategy.failures) == 5
    assert np.all(strategy.successes == 1.0)
    assert np.all(strategy.failures == 1.0)

def test_thompson_sampling_explore():
    strategy = ThompsonSamplingExploration(n_arms=3)
    action = strategy.explore()
    assert isinstance(action, int)
    assert 0 <= action < 3

def test_thompson_sampling_update():
    strategy = ThompsonSamplingExploration(n_arms=3)
    initial_successes = strategy.successes.copy()
    initial_failures = strategy.failures.copy()
    
    strategy.update(1, 1.0)  # Success
    assert strategy.successes[1] == initial_successes[1] + 1
    assert strategy.failures[1] == initial_failures[1]

def test_thompson_sampling_reset():
    strategy = ThompsonSamplingExploration(n_arms=3)
    strategy.successes = np.array([2, 3, 1])
    strategy.failures = np.array([1, 2, 3])
    strategy.reset()
    assert np.all(strategy.successes == 1.0)
    assert np.all(strategy.failures == 1.0)

# UCBExploration tests
def test_ucb_initialization():
    strategy = UCBExploration(n_arms=5, c_param=1.5)
    assert strategy.n_arms == 5
    assert strategy.c_param == 1.5
    assert len(strategy.counts) == 5
    assert len(strategy.values) == 5

def test_ucb_explore():
    strategy = UCBExploration(n_arms=3)
    action = strategy.explore()
    assert action == 0  # First action should be 0 since all are tied

def test_ucb_update():
    strategy = UCBExploration(n_arms=3)
    initial_values = strategy.values.copy()
    initial_counts = strategy.counts.copy()
    
    strategy.update(1, 10.0)
    assert strategy.total_count == 1
    assert strategy.counts[1] == 1
    assert strategy.values[1] == 10.0

def test_ucb_reset():
    strategy = UCBExploration(n_arms=3)
    strategy.counts = np.array([1, 2, 3])
    strategy.values = np.array([0.5, 1.0, 1.5])
    strategy.total_count = 6
    strategy.reset()
    assert np.all(strategy.counts == 0)
    assert np.all(strategy.values == 0)
    assert strategy.total_count == 0

# Factory function tests
def test_create_exploration_strategy_epsilon_greedy():
    strategy = create_exploration_strategy("epsilon_greedy")
    assert isinstance(strategy, EpsilonGreedy)

def test_create_exploration_strategy_invalid_type():
    with pytest.raises(ValueError, match="Unknown exploration strategy: invalid"):
        create_exploration_strategy("invalid")