import pytest
import numpy as np
from unittest.mock import Mock, patch, call
from curiosity_budget.budget_manager import BudgetManager

@pytest.fixture
def budget_manager():
    config = {"test": True}
    return BudgetManager(config)

@pytest.fixture
def sample_performance_metrics():
    return {"metric1": 0.8, "metric2": 100}

@pytest.fixture
def sample_state():
    return np.array([1, 2, 3])

def test_init_budget_manager():
    config = {"test": True}
    bm = BudgetManager(config)
    assert bm.config == config
    assert bm.current_budget is None

def test_update_budget_valid_input(budget_manager, sample_performance_metrics):
    with patch("curiosity_budget.budget_manager.update_budget") as mock_update:
        mock_update.return_value = {"skill_a": 50.0, "skill_b": 30.0}
        budget_manager.update_budget(sample_performance_metrics)
        assert budget_manager.current_budget == {"skill_a": 50.0, "skill_b": 30.0}

def test_update_budget_invalid_input(budget_manager):
    with pytest.raises(ValueError, match="performance_metrics must be a dictionary"):
        budget_manager.update_budget("invalid")

def test_update_budget_exception_handling(budget_manager):
    with patch("curiosity_budget.budget_manager.update_budget") as mock_update:
        mock_update.side_effect = Exception("Update failed")
        with pytest.raises(Exception, match="Update failed"):
            budget_manager.update_budget({})

def test_allocate_budget_valid_input(budget_manager, sample_state):
    with patch("curiosity_budget.budget_manager.allocate_budget") as mock_allocate:
        mock_allocate.return_value = {"skill_x": 100.0}
        result = budget_manager.allocate_budget(sample_state, 1000.0)
        assert result == {"skill_x": 100.0}

def test_allocate_budget_invalid_state_type(budget_manager):
    with pytest.raises(ValueError, match="State must be a numpy array"):
        budget_manager.allocate_budget([1, 2, 3], 100.0)

def test_allocate_budget_invalid_budget_amount_type(budget_manager, sample_state):
    with pytest.raises(ValueError, match="budget_amount must be a non-negative number"):
        budget_manager.allocate_budget(sample_state, "invalid")

def test_allocate_budget_negative_budget_amount(budget_manager, sample_state):
    with pytest.raises(ValueError, match="budget_amount must be a non-negative number"):
        budget_manager.allocate_budget(sample_state, -50.0)

def test_allocate_budget_exception_handling(budget_manager, sample_state):
    with patch("curiosity_budget.budget_manager.allocate_budget") as mock_allocate:
        mock_allocate.side_effect = Exception("Allocation failed")
        with pytest.raises(Exception, match="Allocation failed"):
            budget_manager.allocate_budget(sample_state, 100.0)

def test_get_budget(budget_manager):
    budget_manager.current_budget = {"skill_a": 50.0}
    assert budget_manager.get_budget() == {"skill_a": 50.0}

def test_get_budget_empty(budget_manager):
    assert budget_manager.get_budget() is None

@patch("curiosity_budget.budget_manager.evaluate_skills")
@patch("curiosity_budget.budget_manager.calculate_reward")
@patch("curiosity_budget.budget_manager.explore")
def test_evaluate_current_state(mock_explore, mock_calculate, mock_evaluate, budget_manager):
    mock_evaluate.return_value = {"skill1": 0.8}
    mock_calculate.return_value = {"reward1": 10}
    mock_explore.return_value = {"explore1": 5}
    
    result = budget_manager._evaluate_current_state()
    assert result == {
        "skill_values": {"skill1": 0.8},
        "rewards": {"reward1": 10},
        "exploration": {"explore1": 5}
    }

@patch("curiosity_budget.budget_manager.evaluate_skills")
@patch("curiosity_budget.budget_manager.calculate_reward")
@patch("curiosity_budget.budget_manager.explore")
def test_evaluate_current_state_exception(mock_explore, mock_calculate, mock_evaluate, budget_manager):
    mock_evaluate.side_effect = Exception("Evaluation failed")
    with pytest.raises(Exception, match="Evaluation failed"):
        budget_manager._evaluate_current_state()

@patch("curiosity_budget.budget_manager.evaluate_skills")
@patch("curiosity_budget.budget_manager.calculate_reward")
@patch("curiosity_budget.budget_manager.explore")
@patch.object(BudgetManager, "_evaluate_current_state")
def test_update_allocation_strategy(mock_eval, mock_explore, mock_calculate, mock_evaluate, budget_manager):
    mock_eval.return_value = {
        "skill_values": {"skill1": 0.5},
        "rewards": {"reward1": 10},
        "exploration": {"explore1": 5}
    }
    budget_manager._update_allocation_strategy()
    mock_eval.assert_called_once()

@patch("curiosity_budget.budget_manager.evaluate_skills")
@patch("curiosity_budget.budget_manager.calculate_reward")
@patch("curiosity_budget.budget_manager.explore")
@patch.object(BudgetManager, "_evaluate_current_state")
def test_update_allocation_strategy_exception(mock_eval, mock_explore, mock_calculate, mock_evaluate, budget_manager):
    mock_evaluate.side_effect = Exception("State evaluation failed")
    with pytest.raises(Exception, match="State evaluation failed"):
        budget_manager._update_allocation_strategy()