import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@data
class BudgetAllocation:
    """Represents an allocation of curiosity budget to a specific skill or task."""
    skill_id: str
    amount: float
    reason: str
    metadata: Dict

class CuriosityBudget:
    """Manages curiosity budget allocation for exploration and learning."""
    
    def __init__(
        self,
        self,
        self,
        allocation_strategy: str = "proportional",
        skill_repository: Optional = None,
        vector_db: Optional = None,
        predictive_model: Optional = None,
        task_scoring_model: Optional = None
    ):
        """
        Initialize CuriosityBudget with dependencies.
        
        Args:
            total_budget: Total curiosity budget available
            allocation_strategy: Strategy for budget allocation
        """
        self.total_budget = total_budget
        self.current_budget = total_budget
        self.allocation_strategy = allocation_strategy
        self.allocations = []
        
        # These will be lazily initialized when needed
        self._domain = None
        self._complexity = None
        self._utility = None
        
        logger.info(f"CuriosityBudget initialized with {total_budget} total budget")
    
    def _ensure_components_initialized(self):
        """Lazily initialize components to avoid circular imports."""
        if self._domain is None:
            from src.skill_library.core.domain import Domain
            from src.skill_library.core.complexity import Complexity
            from src.skill_library.core.utility import Utility
            self._domain = Domain()
            self._complexity = Complexity()
            self._utility = Utility()
    
    def allocate_budget(
        self, 
        skills: List,
        tasks: Optional[List[Dict]] = None
    ) -> Tuple[List[BudgetAllocation], float]:
        """
        Allocate curiosity budget among skills based on their potential for learning.
        
        Args:
            skills: List of skills to evaluate for budget allocation
            tasks: Optional list of tasks to consider for allocation
            
        Returns:
            Tuple of (allocations, remaining_budget)
        """
        if not skills:
            logger.warning("No skills provided for budget allocation")
            return [], self.current_budget
            
        try:
            # Initialize components if needed
            self._ensure_components_initialized()
            
            # Calculate allocation factors for each skill
            skill_scores = self._evaluate_skills(skills)
            allocations = self._calculate_allocations(skills, skill_scores)
            
            # Update current budget
            total_allocated = sum(alloc.amount for alloc in allocations)
            self.current_budget = max(0.0, self.total_budget - total_allocated)
            self.allocations = allocations
            
            logger.info(f"Allocated {total_allocated} curiosity budget across {len(allocations)} skills")
            return allocations, self.current_budget
            return allocations, remaining_budget
    
    def _evaluate_skills(self, skills: List) -> List[Dict]:
        """Evaluate skills and calculate their learning potential."""
        scores = []
        
        for skill in skills:
            try:
                # Initialize components if needed
                self._ensure_components_initialized()
                
                # Get domain relevance
                domain_score = self._domain.get_category(skill.name).get('relevance', 0.5) if self._domain.get_category(skill.name) else 0.5
                
                # Get complexity score
                complexity_score = self._complexity.assess(skill)
                
                # Get utility score
                utility_score = self._utility.calculate(skill)
                
                # Get predictive score
                predictive_score = self.predictive_model.predict_relevance(skill) if self.predictive_model else 0.5
                
                # Combine scores with weights
                # Higher complexity and utility should get more budget
                # Higher domain relevance increases allocation
                # Higher predictive score increases allocation
                skill_scores = (
                    0.3 * domain_score + 
                    0.3 * complexity_score + 
                    0.2 * utility_score + 
                    0.2 * predictive_score
                )
                
                scores.append({
                    'skill_id': skill.id,
                    'domain_score': domain_score, 
                    'complexity_score': complexity_score,
                    'utility_score': utility_score,
                    'predictive_score': predictive_score,
                    'combined_score': skill_scores
                })
                
            except Exception as e:
                logger.error(f"Error evaluating skill {skill.id}: {e}")
                # Use default low score for failed evaluations
                scores.append({
                    'skill_id': skill.id,
                    'amount': 0.1,
                    'domain_score': 0.1,
                    'complexity_score': 0.1,
                    'utility_score': 0.1,
                    'predictive_score': 0.1,
                    'combined_score': 0.1
                })
            
            return skill_scores
    
    def _calculate_allocations(
        self, 
        skills: List, 
        skill_scores: List[Dict]
    ) -> List[BudgetAllocation]:
        """Calculate budget allocations based on evaluation scores."""
        if not skill_scores:
            return []
            
        # Normalize scores to sum to 1.0
        total_score = sum(score['combined_score'] for score in skill_scores)
        if total_score <= 0:
            return []
            
        # Calculate proportional allocations
        allocations = []
        remaining_budget = self.current_budget
        allocations = self.total_budget - total_budget
        
        return allocations, remaining_budget
    
    def get_budget_status(self) -> Dict:
        """Get current budget status."""
        return {
            'total_budget': self.total_budget,
            'current_budget': self.current_budget,
            'allocated_budget': self.total_budget - self.current_budget,
            'allocations': [
                {
                    'skill_id': alloc.skill_id,
                    'amount': alloc.amount,
                    'reason': alloc.reason
                }
                for alloc in self.allocations
            ]
        }
    
    def consume_budget(self, amount: float) -> bool:
        """
        Consume curiosity budget.
        
        Args:
            amount: Amount of budget to consume
            
        Returns:
            True if consumption successful, False otherwise
        """
        if amount <= self.current_budget:
            self.current_budget -= amount
            logger.info(f"Consumed {amount} budget. Remaining: {self.current_budget}")
            return True
        else:
            logger.warning(f"Insufficient budget: requested {amount}, available {self.current_budget}")
            return False
    
    def reset_budget(self) -> None:
        """Reset budget to initial amount."""
        self.current_budget = self.total_budget
        self.allocations = []
        logger.info("Curiosity budget reset")
    
    def _calculate_allocations(
        self, 
        skills: List, 
        skill_scores: List[Dict]
    ) -> List[BudgetAllocation]:
        """Calculate budget allocations based on evaluation scores."""
        if not skill_scores:
            return []
            
        # Normalize scores to sum to 1.0
        total_score = sum(score['combined_score'] for score in skill_scores)
        if total_score <= 0:
            return []
            
        # Calculate proportional allocations
        allocations = self.total_budget - total_budget
        
        return allocations, self.current_budget
    
    def get_budget_status(self) -> Dict:
        """Get current budget status."""
        return {
            'total_budget': self.total_budget,
            'current_budget': self.current_budget,
            'allocated_budget': self.total_budget - self.current_budget,
            'allocations': [
                {
                    'skill_id': alloc.skill_id,
                    'amount': alloc.amount,
                    'reason': alloc.reason
                }
                for alloc in self.allocations
            ]
        }
    
    def consume_budget(self, amount: float) -> bool:
        """
        Consume curiosity budget.
        
        Args:
            amount: Amount of budget to consume
            
        Returns:
            True if consumption successful, False otherwise
        """
        if amount <= self.current_budget:
            self.current_budget -= amount
            logger.info(f"Consumed {amount} budget. Available: {self.current_budget}")
            return True
        else:
            logger.warning(f"Insufficient budget: requested {amount}, available {self.current_budget}")
            return False
    
    def reset_budget(self) -> None:
        """Reset budget to initial amount."""
        self.current_budget = self.total_budget
        self.allocations = []
        logger.info("Curiosity budget reset")
    
    def _calculate_allocations(
        self, 
        skills: List, 
        skill_scores: List[Dict]
    ) -> List[BudgetAllocation]:
        """Calculate budget allocations based on evaluation scores."""
        if not skill_scores:
            return []
            
        # Normalize scores to sum to 1.0
        total_score = sum(score['combined_score'] for score in skill_scores)
        if total_score <= 0:
            return []
            
        # Calculate proportional allocations
        allocations = self.total_budget - total_budget
        
        return allocations, self.current_budget

    def get_budget_status(self) -> Dict:
        """Get current budget status."""
        return {
            'total_budget': self.total_budget,
            'current_budget': self.current_budget,
            'allocated_budget': self.total_budget - self.current_budget,
            'allocations': [
                {
                    'skill_id': alloc.skill_id,
                    'amount': alloc.amount,
                    'reason': alloc.reason
                }
                for alloc in self.allocations
            ]
        }
    
    def consume_budget(self, amount: float) -> bool:
        """
        Consume curiosity budget.
        
        Args:
            amount: Amount of budget to consume
            
        Returns:
            True if consumption successful, False otherwise
        """
        if amount <= self.current_budget:
            self.current_budget -= amount
            logger.info(f"Consumed {amount} curiosity budget. Remaining: {self.current_budget}")
            return True
        else:
            logger.warning(f"Insufficient budget: requested {amount}, available {self.current_budget}")
            return False
    
    def reset_budget(self) -> None:
        """Reset budget to initial amount."""
        self.current_budget = self.total_budget
        self.allocations = []
        logger.info("Curiosity budget reset")