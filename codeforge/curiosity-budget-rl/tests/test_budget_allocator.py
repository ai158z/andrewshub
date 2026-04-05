import pytest
import torch
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from curiosity_budget.budget_allocator import (
    BudgetAllocator, 
    ProportionalBudgetAllocator,
    UniformBudgetAllocator,
    PerformanceBasedBudgetAllocator
)
from curiosity_budget.agent import CuriosityAgent
from curiosity_budget.skill_selector import SkillSelector
from curiosity_budget.skill_valuation import evaluate_skills

@pytest.fixture
def mock_agent():
    return Mock(spec=CuriosityAgent)

@pytest.fixture
def mock_skill_selector():
    return Mock(spec=SkillSelector)

@pytest.fixture
def base_allocator(mock_agent, mock_skill_selector):
    # Using abstract class directly to test base functionality
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        allocator = BudgetAllocator(
            agent=mock_agent,
            skill_selector=mock_skill_selector,
            total_budget=1000.0,
            allocation_strategy="test"
        )
    return allocator

def test_budget_allocator_initialization(mock_agent, mock_skill_selector):
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        allocator = BudgetAllocator(mock_agent, mock_skill_selector, 1000.0, "test")
        assert allocator.total_budget == 1000.0
        assert allocator.allocation_strategy == "test"

def test_invalid_agent_type_raises_error(mock_skill_selector):
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        with pytest.raises(TypeError, match="agent must be an instance of CuriosityAgent"):
            BudgetAllocator("invalid_agent", mock_skill_selector, 1000.0, "test")

def test_invalid_skill_selector_type_raises_error(mock_agent):
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        with pytest.raises(TypeError, match="skill_selector must be an instance of SkillSelector"):
            BudgetAllocator(mock_agent, "invalid_skill_selector", 1000.0, "test")

def test_invalid_total_budget_type_raises_error(mock_agent, mock_skill_selector):
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        with pytest.raises(ValueError, match="total_budget must be a non-negative number"):
            BudgetAllocator(mock_agent, mock_skill_selector, "invalid", "test")

def test_invalid_total_budget_negative_raises_error(mock_agent, mock_skill_selector):
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        with pytest.raises(ValueError, match="total_budget must be a non-negative number"):
            BudgetAllocator(mock_agent, mock_skill_selector, -500.0, "test")

def test_invalid_allocation_strategy_type_raises_error(mock_agent, mock_skill_selector):
    with patch.object(BudgetAllocator, "__abstractmethods__", set()):
        with pytest.raises(TypeError, match="allocation_strategy must be a string"):
            BudgetAllocator(mock_agent, mock_skill_selector, 1000.0, 123)

def test_calculate_proportional_allocation_normal_case(base_allocator):
    skill_values = {"skill1": 300.0, "skill2": 700.0}
    allocation = base_allocator._calculate_proportional_allocation(skill_values)
    assert allocation["skill1"] == 300.0
    assert allocation["skill2"] == 700.0

def test_calculate_proportional_allocation_zero_total_value(base_allocator):
    skill_values = {"skill1": 0.0, "skill2": 0.0}
    allocation = base_allocator._calculate_proportional_allocation(skill_values)
    assert allocation["skill1"] == 500.0
    assert allocation["skill2"] == 500.0

def test_proportional_allocator_allocate_budget(mock_agent, mock_skill_selector):
    mock_skill_selector.select_skill.return_value = ["skill1", "skill2"]
    with patch('curiosity_budget.budget_allocator.evaluate_skills') as mock_evaluate:
        mock_evaluate.return_value = {"skill1": 400.0, "skill2": 600.0}
        allocator = ProportionalBudgetAllocator(mock_agent, mock_skill_selector, 1000.0)
        allocation = allocator.allocate_budget()
        assert allocation["skill1"] == 400.0
        assert allocation["skill2"] == 600.0

def test_uniform_allocator_allocate_budget(mock_agent, mock_skill_selector):
    mock_skill_selector.select_skill.return_value = ["skill1", "skill2"]
    allocator = UniformBudgetAllocator(mock_agent, mock_skill_selector, 1000.0)
    allocation = allocator.allocate_budget()
    assert allocation["skill1"] == 500.0
    assert allocation["skill2"] == 500.0

def test_performance_based_allocator_no_history(mock_agent, mock_skill_selector):
    mock_skill_selector.select_skill.return_value = ["skill1", "skill2"]
    allocator = PerformanceBasedBudgetAllocator(mock_agent, mock_skill_selector, 1000.0)
    allocation = allocator.allocate_budget()
    # Should allocate uniformly when no history
    assert allocation["skill1"] == 500.0
    assert allocation["skill2"] == 500.0

def test_performance_based_allocator_with_history(mock_agent, mock_skill_selector):
    allocator = PerformanceBasedBudgetAllocator(mock_agent, mock_skill_selector, 1000.0)
    allocator.performance_history = [{"skill1": 300, "skill2": 700}]
    mock_skill_selector.select_skill.return_value = ["skill1", "skill2"]
    allocation = allocator.allocate_budget()
    assert allocation["skill1"] == 300.0
    assert allocation["skill2"] == 700.0

def test_performance_based_allocator_zero_total_performance(mock_agent, mock_skill_selector):
    allocator = PerformanceBasedBudgetAllocator(mock_agent, mock_skill_selector, 1000.0)
    allocator.performance_history = [{"skill1": 0, "skill2": 0}]
    mock_skill_selector.select_skill.return_value = ["skill1", "skill2"]
    allocation = allocator.allocate_budget()
    assert allocation["skill1"] == 500.0
    assert allocation["skill2"] == 500.0

def test_update_budget_stores_history(base_allocator):
    metrics = {"metric1": 10, "metric2": 20}
    base_allocator.update_budget(metrics)
    assert base_allocator.budget_allocation_history[0] == metrics

def test_calculate_uniform_allocation_empty_skills(base_allocator):
    base_allocator.skill_selector.select_skill.return_value = []
    allocation = base_allocator._calculate_uniform_allocation()
    assert allocation == {}

def test_calculate_proportional_allocation_empty_skills(base_allocator):
    allocation = base_allocator._calculate_proportional_allocation({})
    assert allocation == {}