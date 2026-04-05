import logging
from typing import Dict, Any, List
from src.skill_library.core.skill import Skill
from src.skill_library.core.domain import Domain
from src.skill_library.core.utility import Utility
from src.skill_library.models.predictive_scoring import PredictiveScoringModel
from src.skill_library.models.curiosity_budget import CuriosityBudget
from src.skill_library.models.task_scoring_model import TaskScoringModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Complexity:
    def __init__(self, 
                 domain: Domain,
                 utility: Utility,
                 predictive_model: PredictiveScoringModel,
                 curiosity_budget: CuriosityBudget,
                 task_scoring_model: TaskScoringModel):
        """
        Initialize the Complexity assessment module with required dependencies.
        """
        self.domain = domain
        self.utility = utility
        self.predictive_model = predictive_model
        self.curiosity_budget = curiosity_budget
        self.task_scoring_model = task_scoring_model
        self._validate_dependencies()

    def _validate_dependencies(self) -> None:
        """Validate that all required dependencies are properly initialized."""
        if not isinstance(self.domain, Domain):
            raise TypeError("domain must be an instance of Domain")
        if not isinstance(self.utility, Utility):
            raise TypeError("utility must be an instance of Utility")
        if not isinstance(self.predictive_model, PredictiveScoringModel):
            raise TypeError("predictive_model must be an instance of PredictiveScoringModel")
        if not isinstance(self.curiosity_budget, CuriosityBudget):
            raise TypeError("curiosity_budget must be an instance of CuriosityBudget")
        if not isinstance(self.task_scoring_model, TaskScoringModel):
            raise TypeError("task_scoring_model must be an instance of TaskScoringModel")

    def assess(self, skill: 'Skill') -> Dict[str, Any]:
        """
        Assess the complexity of a skill based on multiple factors.
        """
        if not isinstance(skill, Skill):
            raise TypeError("skill must be an instance of Skill")
        try:
            # Get base complexity from domain categorization
            category = self.domain.get_category(skill)
            # Calculate utility metrics
            utility_score = self.utility.calculate(skill)
            # Get predictive relevance score
            predictive_score = self.predictive_model.predict_relevance(skill)
            # Allocate curiosity budget
            budget_allocation = self.curiosity_budget.allocate_budget(skill)
            # Score tasks related to this skill
            task_scores = self.task_scoring_model.score_task(skill)
            # Calculate final complexity score
            complexity_score = (
                0.3 * utility_score + 
                0.4 * predictive_score + 
                0.3 * budget_allocation
            )
            result = {
                "skill_id": skill.id,
                "category": category,
                "utility_score": utility_score,
                "predictive_score": predictive_score,
                "budget_allocation": budget_allocation,
                "task_scores": task_scores,
                "complexity_score": complexity_score
            }
            return result
        except Exception as e:
            logger.error(f"Error assessing complexity for skill {skill.id}: {str(e)}")
            raise
        return result

# Execute the following test code to verify the implementation
# Test case: test_complexity_initialization_with_valid_dependencies
def test_complexity_initialization_with_valid_dependencies():
    domain = create_autospec(Domain)
    utility = create_autospec(Utility)
    predictive_model = create_autospec(PredictiveScoringModel)
    curiosity_budget = create_autospec(CuriosityBudget)
    task_scoring_model = create_autospec(TaskScoringModel)
    
    domain.get_category.return_value = "test_category"
    utility.calculate.return_value = 0.8
    predictive_model.predict_relevance.return_value = 0.7
    curiosity_budget.allocate_budget.return_value = 0.6
    task_scoring_model.score_task.return_value = {"task1": 0.9}
    
    complexity = Complexity(domain, utility, predictive_model, curiosity_budget, task_scoring_model)
    complexity.assess(None)
    complexity.assess_calculates_correct_complexity_score()