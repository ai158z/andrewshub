import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from abc import ABC, abstractmethod
import logging

class BudgetAllocator(ABC):
    def __init__(self, 
                 agent: Any,
                 skill_selector: Any,
                 total_budget: float = 1000.0,
                 allocation_strategy: str = "proportional"):
        self.agent = agent
        self.skill_selector = skill_selector
        self.total_budget = total_budget
        self.allocation_strategy = allocation_strategy
        self.budget_allocation_history: List[Dict[str, float]] = []
        self.logger = logging.getLogger(__name__)
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        # We can't check the types due to circular import, so we'll do basic validation
        if not hasattr(self.agent, 'select_action'):
            raise TypeError("agent must have a select_action method")
        if not hasattr(self.skill_selector, 'select_skill'):
            raise TypeError("skill_selector must have a select_skill method")
        if not isinstance(self.total_budget, (int, float)) or self.total_budget < 0:
            raise ValueError("total_budget must be a non-negative number")
        if not isinstance(self.allocation_strategy, str):
            raise TypeError("allocation_strategy must be a string")

    @abstractmethod
    def allocate_budget(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def update_budget(self, performance_metrics: Dict[str, Any]) -> None:
        pass

    def _calculate_proportional_allocation(self, skill_values: Dict[str, float]) -> Dict[str, float]:
        total_value = sum(skill_values.values())
        if total_value == 0:
            return {skill: self.total_budget / len(skill_values) for skill in skill_values}
        
        allocation = {}
        for skill, value in skill_values.items():
            allocation[skill] = (value / total_value) * self.total_budget
        return allocation

    def _calculate_uniform_allocation(self, skills: List[str]) -> Dict[str, float]:
        if not skills:
            return {}
        uniform_budget = self.total_budget / len(skills)
        return {skill: uniform_budget for skill in skills}

class ProportionalBudgetAllocator(BudgetAllocator):
    def allocate_budget(self) -> Dict[str, float]:
        skills = self.skill_selector.select_skill()
        from curiosity_budget.skill_valuation import evaluate_skills
        skill_values = evaluate_skills(skills)
        return self._calculate_proportional_allocation(skill_values)

    def update_budget(self, performance_metrics: Dict[str, Any]) -> None:
        self.budget_allocation_history.append(performance_metrics)
        self.logger.info(f"Budget allocation updated with metrics: {performance_metrics}")

class UniformBudgetAllocator(BudgetAllocator):
    def allocate_budget(self) -> Dict[str, float]:
        skills = self.skill_selector.select_skill()
        return self._calculate_uniform_allocation(skills)

    def update_budget(self, performance_metrics: Dict[str, Any]) -> None:
        self.budget_allocation_history.append(performance_metrics)
        self.logger.info(f"Budget allocation updated with metrics: {performance_metrics}")

class PerformanceBasedBudgetAllocator(BudgetAllocator):
    def __init__(self, 
                 agent: Any,
                 skill_selector: Any,
                 total_budget: float = 1000.0,
                 allocation_strategy: str = "performance_based"):
        super().__init__(agent, skill_selector, total_budget, allocation_strategy)
        self.performance_history: List[Dict[str, Any]] = []

    def allocate_budget(self) -> Dict[str, float]:
        skills = self.skill_selector.select_skill()
        if not self.performance_history:
            return self._calculate_uniform_allocation(skills)
        
        latest_performance = self.performance_history[-1]
        total_performance = sum(latest_performance.values())
        if total_performance == 0:
            return {skill: self.total_budget / len(skills) for skill in skills}
            
        allocation = {}
        for skill in skills:
            performance_ratio = latest_performance.get(skill, 0) / total_performance
            allocation[skill] = performance_ratio * self.total_budget
        return allocation

    def update_budget(self, performance_metrics: Dict[str, Any]) -> None:
        self.performance_history.append(performance_metrics)
        self.logger.info(f"Performance-based budget allocation updated with metrics: {performance_metrics}")