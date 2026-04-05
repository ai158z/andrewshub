import pytest
from src.curiosity_budget import CuriosityBudget
from unittest.mock import patch

def test_init_with_default_values():
    budget = CuriosityBudget()
    assert budget.budget == 100.0
    assert budget.learning_rate == 0.1
    assert budget.success_rates == {}
    assert budget.tasks == {}
    assert budget.skills == {}

def test_init_with_custom_values():
    budget = CuriosityBudget(initial_budget=50.0, learning_rate=0.2)
    assert budget.budget == 50.0
    assert budget.learning_rate == 0.2

def test_adjust_budget_valid_input():
    budget = CuriosityBudget()
    result = budget.adjust_budget(0.8)
    assert result == 100.0

def test_adjust_budget_invalid_success_rate():
    budget = CuriosityBudget()
    with pytest.raises(ValueError):
        budget.adjust_budget(1.5)

def test_adjust_budget_negative_success_rate():
    budget = CuriosityBudget()
    with pytest.raises(ValueError):
        budget.adjust_budget(-0.5)

def test_get_budget():
    budget = CuriosityBudget(initial_budget=75.0)
    assert budget.get_budget() == 75.0

def test_update_success_rate_valid():
    budget = CuriosityBudget()
    budget.update_success_rate("task1", 0.75)
    assert budget.success_rates["task1"] == 0.75

def test_update_success_rate_invalid_rate():
    budget = CuriosityBudget()
    with pytest.raises(ValueError):
        budget.update_success_rate("task1", 1.5)

def test_update_success_rate_invalid_task_id_type():
    budget = CuriosityBudget()
    with pytest.raises(TypeError):
        budget.update_success_rate(123, 0.75)

def test_calculate_aggregated_success_rate_no_rates():
    budget = CuriosityBudget()
    rate = budget._calculate_aggregated_success_rate()
    assert rate == 0.0

def test_calculate_aggregated_success_rate_with_rates():
    budget = CuriosityBudget()
    budget.success_rates = {"task1": 0.5, "task2": 0.7}
    rate = budget._calculate_aggregated_success_rate()
    assert rate == 0.6

def test_get_task_success_rate_exists():
    budget = CuriosityBudget()
    budget.success_rates["task1"] = 0.8
    assert budget._get_task_success_rate("task1") == 0.8

def test_get_task_success_rate_not_exists():
    budget = CuriosityBudget()
    assert budget._get_task_success_rate("nonexistent") == 0.0

def test_normalize_budget_within_range():
    budget = CuriosityBudget(initial_budget=50.0)
    normalized = budget._normalize_budget()
    assert 0.0 <= normalized <= 1.0

def test_normalize_budget_at_zero():
    budget = CuriosityBudget(initial_budget=0.0)
    normalized = budget._normalize_budget()
    assert normalized == 0.0

def test_normalize_budget_above_max():
    budget = CuriosityBudget(initial_budget=150.0)
    normalized = budget._normalize_budget()
    assert normalized == 1.0

def test_adjust_budget_increases():
    budget = CuriosityBudget(initial_budget=100.0, learning_rate=0.1)
    # Success rate below ideal should increase budget
    new_budget = budget.adjust_budget(0.5)
    assert new_budget > 100.0

def test_adjust_budget_decreases():
    budget = CuriosityBudget(initial_budget=100.0, learning_rate=0.1)
    # Success rate above ideal should decrease budget
    new_budget = budget.adjust_budget(0.9)
    assert new_budget < 100.0

def test_adjust_budget_clamps_negative():
    budget = CuriosityBudget(initial_budget=100.0, learning_rate=10.0)
    # With high learning rate and low success rate, budget should not go below 0
    new_budget = budget.adjust_budget(0.0)
    assert new_budget == 0.0
    assert budget.budget == 0.0