import logging
from typing import Dict, Optional, Union
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Global state for testing purposes
_budget_data = {}

class CuriosityBudgetManager:
    """
    Manages curiosity budget allocation and tracking for AI agents.
    This class handles the distribution and monitoring of curiosity values to skills
    based on their learning potential and current usage.
    """

    def __init__(self, skill_catalog, curiosity_allocator, task_scorer, skill_manager):
        """
        Initialize the curiosity budget manager with required dependencies.

        Args:
            skill_catalog: Skill catalog instance for skill management
            curiosity_allocator: Allocator for distributing curiosity budgets
            task_scorer: scorer for tasks
            skill_manager: manager for skill execution and updates
        """
        self.skill_catalog = skill_catalog
        self.curiosity_allocator = curiosity_allocator
        self.task_scorer = task_scorer
        self.skill_manager = skill_manager

    def get_budget_status(self, skill_id: str) -> Dict[str, Union[str, float]]:
        """
        Get the current status of the curiosity budget for a specific skill.

        Args:
            skill_id (str): The unique identifier of the skill to check

        Returns:
            Dict containing:
                - current_curiosity: float - Current curiosity value
                - allocated_budget: float - Currently allocated budget amount
                - remaining_budget: float - Remaining curiosity budget
                - threshold: float - Curiosity threshold for triggering
        """
        return get_budget_status(skill_id)

    def allocate_budget(self, skill_id: str, amount: float = 0.0) -> None:
        """
        Allocate a curiosity budget to a specific skill.

        Args:
            skill_id (str): The skill identifier
            amount (float): Amount of curiosity units to allocate
        """
        allocate_budget(skill_id, amount)

    def adjust_budget(self, skill_id: str, delta: float) -> None:
        """
        Adjusts the curiosity budget by a delta amount for a specific skill.

        Args:
            skill_id (str): The unique identifier of the skill
            delta (float): Amount to adjust the curiosity budget
        """
        adjust_budget(skill_id, delta)


# Module level functions for external use
def allocate_budget(skill_id: str, amount: float = 0.0) -> None:
    """
    Allocate a curiosity budget to a skill.

    Args:
        skill_id: The skill to allocate budget for
        amount: The budget amount to allocate
    """
    # In a real implementation, this would interact with the allocator
    # For testing, we'll just store the allocation data
    _budget_data[skill_id] = _budget_data.get(skill_id, {})
    _budget_data[skill_id]['allocated_budget'] = _budget_data[skill_id].get('allocated_budget', 0) + amount


def adjust_budget(skill_id: str, delta: float) -> None:
    """
    Adjusts the curiosity budget for a given skill.

    Args:
        skill_id (str): Skill identifier
        delta (float): Change in budget amount
    """
    # In a real implementation, this would interact with the allocator
    # For testing, we'll just update the stored data
    _budget_data[skill_id] = _budget_data.get(skill_id, {})
    current = _budget_data[skill_id].get('allocated_budget', 0)
    _budget_data[skill_id]['allocated_budget'] = current + delta


def get_budget_status(skill_id: str) -> Dict[str, Union[str, float]]:
    """
    Get current curiosity budget.

    Returns:
        A dictionary with:
            - skill_id: The skill identifier
            - current_curiosity: Current curiosity value
            - allocated_budget: Total allocated budget
            - remaining_budget: Remaining curiosity after budget use
            - threshold: Minimum score threshold
    """
    # Return mock data based on what's stored, or defaults
    data = _budget_data.get(skill_id, {})
    return {
        'skill_id': skill_id,
        'current_curiosity': data.get('current_curiosity', 0.0),
        'allocated_budget': data.get('allocated_budget', 0.0),
        'remaining_budget': data.get('remaining_budget', 0.0),
        'threshold': data.get('threshold', 0.0)
    }

# Initialize the global state
_budget_data.clear()