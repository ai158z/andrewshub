import logging
from typing import Dict, Any, Optional
import numpy as np

# Import functions instead of modules to avoid circular imports
from curiosity_budget.budget_allocator import allocate_budget, update_budget
from curiosity_budget.skill_valuation import evaluate_skills
from curiosity_budget.reward_system import calculate_reward
from curiosity_budget.exploration import explore

class BudgetManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_budget: Optional[Dict[str, float]] = None
        self.logger = logging.getLogger(__name__)
        # Initialize skill selector after resolving circular import
        from curiosity_budget.skill_selector import SkillSelector
        self.skill_selector = SkillSelector()
        
    def update_budget(self, performance_metrics: Dict[str, Any]) -> None:
        try:
            if not isinstance(performance_metrics, dict):
                raise ValueError("performance_metrics must be a dictionary")
                
            self.current_budget = update_budget(performance_metrics)
            self.logger.info("Budget updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating budget: {str(e)}")
            raise

    def allocate_budget(self, state: np.ndarray, budget_amount: float) -> Dict[str, Any]:
        try:
            if not isinstance(state, np.ndarray):
                raise ValueError("State must be a numpy array")
            if not isinstance(budget_amount, (int, float)) or budget_amount < 0:
                raise ValueError("budget_amount must be a non-negative number")
                
            allocation = allocate_budget(state, budget_amount)
            self.current_budget = allocation
            self.logger.info("Budget allocated successfully")
            return allocation
        except Exception as e:
            self.logger.error(f"Error allocating budget: {str(e)}")
            raise

    def get_budget(self) -> Optional[Dict[str, float]]:
        return self.current_budget

    def _evaluate_current_state(self) -> Dict[str, Any]:
        try:
            # Evaluate current skills
            skill_values = evaluate_skills()
            # Calculate rewards
            rewards = calculate_reward()
            # Explore possibilities
            exploration_data = explore()
            
            return {
                "skill_values": skill_values,
                "rewards": rewards,
                "exploration": exploration_data
            }
        except Exception as e:
            self.logger.error(f"Error evaluating current state: {str(e)}")
            raise

    def _update_allocation_strategy(self) -> None:
        try:
            state_evaluation = self._evaluate_current_state()
            # Update skill selector with new data
            self.skill_selector.update_skills(state_evaluation["skill_values"])
            # Update rewards system
            # This would be a no-op in this simplified version but could be extended
            # Update exploration module
            # This would be a no-op in this simplified version but could be extended
        except Exception as e:
            self.logger.error(f"Error updating allocation strategy: {str(e)}")
            raise