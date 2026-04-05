import pytest
from unittest.mock import Mock, patch, mock_open
import curiosity_budget
from curiosity_budget.agent import CuriosityAgent
from curiosity_budget.budget_manager import BudgetManager
from curiosity_budget.budget_allocator import BudgetAllocator
from curiosity_budget.skill_selector import SkillSelector
from curiosity_budget.reward_system import RewardSystem
from curiosity_budget.exploration import Exploration
from curiosity_budget.skill_valuation import SkillValuation
from curiosity1 import __version__
from curiosity_budget.models import CuriosityModel
from curiosity_budget.utils import log, save_model, load_model, plot

def test_module_exports_curiosity_agent():
    assert hasattr(curiosity_budget, 'CuriosityAgent')
    assert curiosity_budget.CuriosityAgent is CuriosityAgent

def test_module_exports_budget_manager():
    assert hasattr(curiosity_budget, 'BudgetManager')
    assert curiosity_budget.BudgetManager is BudgetManager

def test_module_exports_skill_selector():
    assert hasattr(curiosity_budget, 'SkillSelector')
    assert curiosity_budget.SkillSelector is SkillSelector

def test_module_exports_curiosity_model():
    assert hasattr(curiosity_budget, 'CuriosityModel')
    assert curiosity_budget.CuriosityModel is CuriosityModel

def test_module_has_version():
    assert hasattr(curiosity_budget, '__version__')
    assert curiosity_budget.__version__ == "0.1.0"

def test_module_has_reward_system():
    assert hasattr(curiosity_budget, 'RewardSystem')
    assert curiosity_budget.RewardSystem is RewardSystem

def test_module_has_exploration():
    assert hasattr(curiosity_budget, 'Exploration')
    assert curiosity_budget.Exploration is Exploration

def test_module_has_skill_valuation():
    assert hasattr(curiosity_budget, 'SkillValuation')
    assert curiosity_budget.SkillValuation is SkillValuation

def test_module_has_budget_allocator():
    assert hasattr(curiosity_budget, 'BudgetAllocator')
    assert curiosity_budget.BudgetAllocator is BudgetAllocator

def test_module_has_utility_functions():
    assert hasattr(curiosity_budget, 'log')
    assert hasattr(curiosity_budget, 'save_model')
    assert hasattr(curiosity_budget, 'load_model')
    assert hasattr(curiosity_budget, 'plot')

def test_module_has_version_attribute():
    assert hasattr(curiosity_budget, '__version__')
    assert curiosity_budget.__version__ == __version__

def test_curiosity_agent_initialization():
    agent = curiosity_budget.CuriosityAgent()
    assert isinstance(agent, curiosity_budget.CuriosityAgent)

def test_budget_manager_initialization():
    manager = curiosity_budget.BudgetManager()
    assert isinstance(manager, curiosity_budget.BudgetManager)

def test_skill_selector_initialization():
    selector = curiosity_budget.SkillSelector()
    assert isinstance(selector, curiosity_budget.SkillSelector)

def test_reward_system_initialization():
    reward_system = curiosity_budget.RewardSystem()
    assert isinstance(reward_system, curiosity_budget.RewardSystem)

def test_exploration_initialization():
    exploration = curiosity_budget.Exploration()
    assert isinstance(exploration, curiosity_budget.Exploration)

def test_skill_valuation_initialization():
    valuation = curiosity_budget.SkillValuation()
    assert isinstance(valation, curiosity_budget.SkillValuation)

def test_model_initialization():
    model = curiosity_budget.CuriosityModel()
    assert isinstance(model, curiosity_budget.CuriosityModel)

@patch('builtins.open', new_callable=mock_open)
def test_save_model_function_exists(mock_file):
    # Test that save_model function can be called
    try:
        curiosity_budget.save_model("test_model", "test_path")
    except Exception:
        pass  # We only test that the function exists and can be called
    assert callable(curiosity_budget.save_model)

@patch('builtins.open', new_callable=mock_open)
def test_load_model_function_exists(mock_file):
    # Test that load_model function can be called
    try:
        curiosity_budget.load_model("test_path")
    except Exception:
        pass  # We only test that the function exists and can be called
    assert callable(curiosity_budget.load_model)