import logging
from typing import Dict, Any, List
from src.skill_library.core.domain import Domain
from src.skill_library.core.complexity import Complexity
from src.skill_library.core.utility import Utility
from src.skill_library.models.predictive_scoring import PredictiveScoringModel
from src.skill_library.models.curiosity_budget import CuriosityBudget
from src.skill_library.storage.vector_db import VectorDB
from src.skill_library.storage.skill_repository import SkillRepository
from src.skill_library.integrations.memory_system import MemorySystem
from src.skill_library.intrerations.pytorch_integration import PyTorchIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskScoringModel:
    def __init__(self):
        """Initialize the TaskScoringModel with required dependencies."""
        self.domain = Domain()
        self.complexity = Complexity()
        self.utility = Utility()
        self.predictive_model = PredictiveScoringModel()
        self.budget_allocator = CuriosityBudget()
        self.vector_db = VectorDB()
        self.skill_repo = SkillRepository()
        self.memory_system = MemorySystem()
        self.pytorch_integration = PyTorchIntegration()

    def _initialize_model(self) -> None:
        """Initialize the PyTorch model for task scoring."""
        try:
            self.pytorch_integration.load_model("task_scoring_model")
            logger.info("Task scoring model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise

    def _calculate_relevance_score(self, task_description: str) -> float:
        """Calculate relevance score based on domain and predictive model."""
        try:
            category = self.domain.get_category(task_description)
            predicted_relevance = self.predictive_model.predict_relevance(task_description, category)
            return predicted_relevance
        except Exception as e:
            logger.warning(f"Error calculating relevance score: {e}")
            return 0.0

    def _calculate_novelty_score(self, task_description: str) -> float:
        """Calculate novelty score based on existing skills in vector database."""
        try:
            similar_skills = self.vector_db.find_similar_skills(task_description, threshold=0.7)
            if not similar_skills:
                return 1.0  # Completely novel
            return max(0.0, 1.0 - len(similar_skills) / 10.0)  # Normalize by max 10 similar skills
        except Exception as e:
            logger.warning(f"Error calculating novelty score: {e}")
            return 0.5  # Default neutral score

    def _calculate_resource_score(self, task_description: str) -> float:
        """Calculate resource requirement score based on complexity and utility."""
        try:
            complexity_score = self.complexity.assess(task_description)
            utility_score = self.utility.calculate(task_description)
            # Higher complexity and lower utility = higher resource requirement
            return (complexity_score * 0.7) + ((1.0 - utility_score) * 0.3)
        except Exception as e:
            logger.warning(f"Error calculating resource score: {e}")
            return 0.5  # Default neutral score

    def _calculate_curiosity_score(self, task_description: str) -> float:
        """Calculate curiosity score based on budget allocation."""
        try:
            budget_allocation = self.budget_allocator.allocate_budget(task_description)
            return min(1.0, budget_allocation / 100.0)  # Normalize to 0-1 scale
        except Exception as e:
            logger.error(f"Error calculating curiosity score: {e}")
            raise

    def score_task(self, task_description: str) -> Dict[str, Any]:
        """
        Calculate comprehensive task score based on relevance, novelty, resources, and curiosity.
        
        Args:
            task_description: Description of the task to score
            
        Returns:
            Dictionary containing individual scores and overall score
        """
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string")
        
        try:
            # Calculate component scores
            relevance = self._calculate_relevance_score(task_description)
            novelty = self._calculate_novelty_score(task_description)
            resources = self._calculate_resource_score(task_description)
            curiosity = self._calculate_curiosity_score(task_description)
            
            # Weighted combination (adjust weights as needed)
            # Relevance: 40%, Novelty: 30%, Resources: 20%, Curiosity: 10%
            overall_score = (
                (relevance * 0.4) + 
                (novelty * 0.3) + 
                ((1.0 - resources) * 0.2) +  # Invert resources (lower is better)
                (curiosity * 0.1)
            )
            
            # Store in memory system
            experience_data = {
                "task": task_description,
                "scores": {
                    "relevance": relevance,
                    "novelty": novelty,
                    "resources": resources,
                    "curiosity": curiosity,
                    "overall": overall_score
                }
            }
            self.memory_system.store_experience(experience_data)
            
            return {
                "relevance_score": relevance,
                "novelty_score": novelty,
                "resource_score": resources,
                "curiosity_score": curiosity,
                "task_description": task_description
            }
        except Exception as e:
            logger.error(f"Error scoring task: {e}")
            # Return default scores on error
            return {
                "relevance_score": 0.0,
                "novelty_score": 0.0,
                "resource_score": 0.0,
                "curiosity_score": 0.0,
                "overall_score": 0.0,
                "task_description": task_description,
                "error": str(e)
            }