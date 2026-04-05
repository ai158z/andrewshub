import pytest
from unittest.mock import patch
from src.curiosity_budget import CuriosityBudget

@pytest.fixture
def budget_manager():
    return CuriosityBudget()

def test_adjust_budget_reduces_by_success_rate(budget_manager):
    initial_budget = 100
    success_rate = 0.85
    adjustment_factor = 0.1
    adjusted = budget_manager.adjust_budget(initial_budget, success_rate, adjustment_factor)
    assert adjusted == 93.5  # 100 * (1 - 0.85 * 0.1)

def test_get_budget_returns_default(budget_manager):
    budget = budget_manager.get_budget()
    assert budget == 100

def test_update_success_rate_changes_budget(budget_manager):
    new_success_rate = 0.9
    budget_manager.update_success_rate(new_success_rate)
    expected_budget = 100 * (1 - new_success_rate * 0.1)
    adjusted_budget = budget_manager.get_budget()
    assert adjusted_budget == expected_budget

def test_adjust_budget_with_zero_success_rate(budget_manager):
    adjusted = budget_manager.adjust_budget(100, 0.0, 0.1)
    assert adjusted == 100.0

def test_adjust_budget_with_full_success_rate(budget_manager):
    adjusted = budget_manager.adjust_budget(100, 1.0, 0.1)
    assert adjusted == 90.0

def test_adjust_budget_with_zero_initial_budget(budget_manager):
    adjusted = budget_manager.adjust_budget(0, 0.5, 0.1)
    assert adjusted == 0.0

def test_update_success_rate_with_zero(budget_manager):
    budget_manager.update_success_rate(0.0)
    budget = budget_manager.get_budget()
    assert budget == 100.0

def test_update_success_rate_with_one(budget_manager):
    budget_manager.update_success_rate(1.0)
    expected_budget = 100 * (1 - 1.0 * 0.1)
    budget = budget_manager.get_budget()
    assert budget == expected_budget

def test_multiple_budget_adjustments(budget_manager):
    budget_manager.update_success_rate(0.8)
    first_adjustment = 100 * (1 - 0.8 * 0.1)
    
    budget_manager.update_success_rate(0.6)
    second_adjustment = first_adjustment * (1 - 0.6 * 0.1)
    
    assert budget_manager.get_budget() == second_adjustment

def test_negative_initial_budget(budget_manager):
    adjusted = budget_manager.adjust_budget(-100, 0.5, 0.1)
    assert adjusted == -95.0

def test_negative_success_rate(budget_manager):
    with pytest.raises(ValueError):
        budget_manager.adjust_budget(100, -0.5, 0.1)

def test_success_rate_over_one(budget_manager):
    with pytest.raises(ValueError):
        budget_manager.adjust_budget(100, 1.5, 0.1)

def test_zero_adjustment_factor(budget_manager):
    adjusted = budget_manager.adjust_budget(100, 0.5, 0.0)
    assert adjusted == 100.0

def test_get_budget_after_multiple_updates(budget_manager):
    budget_manager.update_success_rate(0.7)
    budget_manager.update_success_rate(0.3)
    expected = 100 * (1 - 0.7 * 0.1) * (1 - 0.3 * 0.1)
    assert budget_manager.get_budget() == expected

def test_adjust_budget_large_values(budget_manager):
    adjusted = budget_manager.adjust_budget(1000000, 0.99, 0.5)
    expected = 1000000 * (1 - 0.99 * 0.5)
    assert adjusted == expected

def test_adjust_budget_negative_adjustment_factor(budget_manager):
    adjusted = budget_manager.adjust_budget(100, 0.5, -0.1)
    assert adjusted == 105.0

def test_update_success_rate_negative_value(budget_manager):
    with pytest.raises(ValueError):
        budget_manager.update_success_rate(-0.5)

def test_update_success_rate_greater_than_one(budget_manager):
    with pytest.raises(ValueError):
        budget_manager.update_success_rate(1.2)

def test_consistent_budget_calculation(budget_manager):
    initial = 200
    success_rate = 0.75
    factor = 0.2
    first_result = budget_manager.adjust_budget(initial, success_rate, factor)
    expected = initial * (1 - success_rate * factor)
    assert first_result == expected

def test_chained_budget_updates(budget_manager):
    budget_manager.update_success_rate(0.8)
    budget_manager.update_success_rate(0.9)
    budget_manager.update_success_rate(0.5)
    assert budget_manager.get_budget() == 100 * (1 - 0.8 * 0.1) * (1 - 0.9 * 0.1) * (1 - 0.5 * 0.1)