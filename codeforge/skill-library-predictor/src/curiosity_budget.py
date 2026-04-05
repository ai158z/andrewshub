import logging
from typing import Dict, Any
from src.models import Skill, Task
from src.utils import calculate_success_rate

logger = logging.getLogger(__name__)

class CuriosityBudget:
    def __init__(self, initial_budget: float = 100.0, learning_rate: float = 0.1):
        """
        Initialize CuriosityBudget with an initial budget and learning rate.
        
        Args:
            initial_budget: Starting curiosity budget value
            learning_rate: Rate at which budget adjusts based on success rates
        """
        self.budget: float = initial_budget
        self.learning_rate: float = learning_rate
        self.success_rates: Dict[str, float] = {}
        self.tasks: Dict[str, Task] = {}
        self.skills: Dict[str, Skill] = {}
        
    def adjust_budget(self, success_rate: float) -> float:
        """
        Adjust the curiosity budget based on success rate.
        
        Args:
            success_rate: A float representing the success rate (0.0 to 1.0)
        Returns:
            The adjusted budget value
        """
        if not 0.0 <= success_rate <= 1.0:
            raise ValueError("Success rate must be between 0 and 1")
            
        # Adjust budget based on how current success rate compares to ideal (0.8)
        ideal_rate = 0.8
        adjustment = (success_rate - ideal_rate) * self.learning_rate
        self.budget = max(0.0, self.budget - adjustment)
        return self.budget
    
    def get_budget(self) -> float:
        """
        Get the current curiosity budget.
        
        Returns: Current budget value
        """
        return self.budget
    
    def update_success_rate(self, task_id: str, success_rate: float) -> None:
        """
        Update the success rate for a specific task.
        
        Args:
            task_id: Unique identifier for the task
            success_rate: Success rate value (0.0 to 1.0)
        """
        if not 0.0 <= success_rate <= 1.0:
            raise ValueError("Success rate must be between 0.0 and 1.0")
            
        if not isinstance(task_id, str):
            raise TypeError("Task ID must be a string")
            
        self.success_rates[task_id] = success_rate
        logger.info(f"Updated success rate for task {task_id}: {success_rate}")
        
    def _calculate_aggregated_success_rate(self) -> float:
        """
        Calculate an aggregated success rate across all tracked tasks.
        
        Returns: Weighted average success rate
        """
        if not self.success_rates:
            return 0.0
            
        total_rate = sum(self.success_rates.values())
        return total_rate / len(self.success_rates)
    
    def _get_task_success_rate(self, task_id: str) -> float:
        """
        Get success rate for a specific task.
        
        Args:
            task_id: The task identifier
            
        Returns: Success rate for the task or 0.0 if not found
        """
        return self.success_rates.get(task_id, 0.0)
        
    def _normalize_budget(self) -> float:
        """
        Normalize budget to a 0-1 scale.
        
        Returns: Normalized budget value
        """
        # Simple min-max normalization assuming budget range 0-100
        return max(0.0, min(1.0, self.budget / 100.0))