import pytest
import numpy as np
from unittest.mock import Mock, patch
from curiosity_budget.skill_selector import SkillSelector

class MockSkillValuation:
    def __init__(self):
        self.values = {}
    
    def get_value(self, skill_id):
        return self.values.get(skill_id, 0.0)
    
    def update(self, skill_id, reward):
        if skill_id not in self.values:
            self.values[skill_id] = 0.0
        self.values[skill_id] += reward

class MockBudgetManager:
    def __init__(self):
        self.budget = 0
    
    def update_budget(self, skill_id, reward):
        self.budget += reward

class MockExplorationStrategy:
    def get_exploration_bonus(self):
        return 0.1
    
    def get_temperature(self):
        return 1.0

def test_epsilon_greedy_selection_explores():
    # Setup
    skill_valuation = MockSkillValuation()
    budget_manager = MockBudgetManager()
    exploration_strategy = MockExplorationStrategy()
    
    selector = SkillSelector(
        num_skills=5,
        skill_valuation=skill_valuation,
        budget_manager=budget_manager,
        exploration_strategy=exploration_strategy,
        selection_strategy="epsilon_greedy",
        epsilon=1.0  # Force exploration
    )
    
    # Test that with epsilon=1.0, we always explore (random selection)
    with patch('random.randint') as mock_randint, patch('random.random', return_value=0.5):
        mock_randint.return_value = 2
        result = selector.select_skill()
        assert result == 2

def test_epsilon_greedy_selection_exploits():
    # Setup with high-value skill
    skill_valuation = MockSkillValuation()
    skill_valuation.values[0] = 10.0  # High value skill
    
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=skill_valuation,
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy",
        epsilon=0.0  # No exploration
    )
    
    # Mock exploration bonus to be small
    with patch.object(selector.exploration_strategy, 'get_exploration_bonus', return_value=0.1):
        result = selector.select_skill()
        # Should select skill 0 since it has highest value
        assert result == 0

def test_boltzmann_selection_with_temperature():
    skill_valuation = MockSkillValuation()
    skill_valuation.values = {0: 1.0, 1: 2.0, 2: 0.5}  # Different values
    
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=skill_valuation,
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="boltzmann"
    )
    
    # Should return one of the skill indices
    result = selector.select_skill()
    assert isinstance(result, int)
    assert 0 <= result < 3

def test_ucb_selection_first_run():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="ucb"
    )
    
    # First selection should be 0
    result = selector.select_skill()
    assert result == 0

def test_ucb_selection_unchosen_skill_priority():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="ucb"
    )
    
    # When all skills have equal counts, should pick first unchosen
    selector.total_selections = 1
    selector.selection_counts = np.array([1, 0, 0])
    
    result = selector.select_skill()
    # Should select skill 1 (first unchosen)
    assert result == 1

def test_update_skills_stores_performance():
    skill_valuation = MockSkillValuation()
    budget_manager = MockBudgetManager()
    exploration_strategy = MockExplorationStrategy()
    
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=skill_valuation,
        budget_manager=budget_manager,
        exploration_strategy=exploration_strategy,
        selection_strategy="epsilon_greedy"
    )
    
    # Update with a reward
    selector.update_skills(1, 5.0)
    
    # Check stats are updated
    stats = selector.get_skill_stats(1)
    assert stats["count"] == 1
    assert stats["total_reward"] == 5.0
    assert stats["average_reward"] == 5.0

def test_get_skill_stats_empty():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy"
    )
    
    stats = selector.get_skill_stats(0)
    assert stats["count"] == 0
    assert stats["total_reward"] == 0
    assert stats["average_reward"] == 0

def test_get_skill_stats_with_data():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy"
    )
    
    # Add some performance data
    selector.update_skills(0, 10.0)
    selector.update_skills(0, 5.0)
    
    stats = selector.get_skill_stats(0)
    assert stats["count"] == 2
    assert stats["total_reward"] == 15.0
    assert stats["average_reward"] == 7.5

def test_reset_clears_state():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy"
    )
    
    # Add some data
    selector.update_skills(0, 10.0)
    selector.update_skills(1, 5.0)
    
    # Verify data exists
    assert selector.get_skill_stats(0)["count"] > 0
    
    # Reset and verify cleared
    selector.reset()
    assert selector.get_skill_stats(0)["count"] == 0
    assert selector.total_selections == 0

def test_unknown_selection_strategy_defaults_to_random():
    selector = SkillSelector(
        num_skills=5,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="unknown_strategy"
    )
    
    with patch('numpy.random.choice', return_value=3):
        result = selector.select_skill()
        assert result == 3  # Should use the random choice

def test_boltzmann_with_zero_temperature():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="boltzmann"
    )
    
    # Mock temperature to zero - should select highest value deterministically
    with patch.object(selector.exploration_strategy, 'get_temperature', return_value=0.0):
        # Since temp is 0, softmax will select the max value skill
        # But we need to check what happens when exp_values all become inf
        # In practice, this would be implementation specific
        result = selector.select_skill()
        assert isinstance(result, int)

def test_select_skill_calls_correct_strategy():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy"
    )
    
    # Test it goes through epsilon greedy path
    with patch.object(selector, '_epsilon_greedy_selection') as mock_method:
        mock_method.return_value = 1
        result = selector.select_skill()
        assert result == 1
        mock_method.assert_called_once()

def test_ucb_calculation():
    skill_valuation = MockSkillValuation()
    # Set some values to test UCB calculation
    skill_valuation.values = {0: 5.0, 1: 3.0, 2: 7.0}
    
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=skill_valuation,
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="ucb"
    )
    
    # Set up selection counts
    selector.selection_counts = np.array([2, 1, 3])
    selector.total_selections = 6
    
    result = selector.select_skill()
    assert isinstance(result, int)
    assert 0 <= result < 3

def test_epsilon_greedy_with_no_skills():
    selector = SkillSelector(
        num_skills=0,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy"
    )
    
    # Should handle 0 skills gracefully
    with pytest.raises(ValueError):
        selector.select_skill()

def test_update_with_invalid_skill_id():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="epsilon_greedy"
    )
    
    # Update with skill_id beyond range - should not crash
    selector.update_skills(10, 5.0)  # skill_id 10 doesn't exist
    stats = selector.get_skill_stats(10)
    assert stats["count"] == 0  # No data for this skill

def test_empty_boltzmann_probabilities():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="boltzmann"
    )
    
    # All zero values should result in uniform random selection
    with patch('numpy.random.choice') as mock_choice:
        mock_choice.return_value = 1
        result = selector.select_skill()
        assert result == 1

def test_exploration_strategy_integration():
    skill_valuation = MockSkillValuation()
    exploration_strategy = MockExplorationStrategy()
    
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=skill_valuation,
        budget_manager=MockBudgetManager(),
        exploration_strategy=exploration_strategy,
        selection_strategy="epsilon_greedy",
        epsilon=0.0  # Force exploitation
    )
    
    # Test that exploration bonus affects selection
    with patch.object(exploration_strategy, 'get_exploration_bonus', return_value=5.0):
        result = selector.select_skill()
        # Should still be valid skill id
        assert 0 <= result < selector.num_skills

def test_selection_counts_in_ucb():
    selector = SkillSelector(
        num_skills=3,
        skill_valuation=MockSkillValuation(),
        budget_manager=MockBudgetManager(),
        exploration_strategy=MockExplorationStrategy(),
        selection_strategy="ucb"
    )
    
    # Test that selection counts are properly tracked in UCB
    initial_total = selector.total_selections
    initial_counts = selector.selection_counts.copy()
    
    # Do one selection
    selector.select_skill()
    
    # Total selections should increment
    assert selector.total_selections == initial_total + 1