from curiosity_budget.models import CuriosityModel
from curiosity_budget.utils import log, save_model, load_model, plot

# Note: Due to circular import issues, we're using lazy imports for the main components
# This avoids importing modules that depend on each other during initialization

__version__ = "0.1.0"

# Define what should be accessible in the public API
__all__ = [
    "CuriosityAgent",
    "BudgetManager",
    "BudgetAllocator",
    "SkillSelector", 
    "RewardSystem",
    "Exploration",
    "SkillValuation",
    "CuriosityModel",
    "log",
    "save_model",
    "load_model",
    "plot",
    "__version__"
]

# Lazy loading to avoid circular imports
def __getattr__(name):
    """Lazily import classes to avoid circular dependencies at init time"""
    if name == "CuriosityAgent":
        from curiosity_budget.agent import CuriosityAgent
        return CuriosityAgent
    elif name == "BudgetManager":
        from curiosity_budget.budget_manager import BudgetManager
        return BudgetManager
    elif name == "BudgetAllocator":
        from curiosity_budget.budget_allocator import BudgetAllocator
        return BudgetAllocator
    elif name == "SkillSelector":
        from curiosity_budget.skill_selector import SkillSelector
        return SkillSelector
    elif name == "RewardSystem":
        from curiosity_budget.reward_system import RewardSystem
        return RewardSystem
    elif name == "Exploration":
        from curiosity_budget.exploration import Exploration
        return Exploration
    elif name == "SkillValuation":
        from curiosity_budget.skill_valuation import SkillValuation
        return SkillValuation
    else:
        raise AttributeError(f"module 'curiosity_budget' has no attribute '{name}'")

def __dir__():
    return __all__