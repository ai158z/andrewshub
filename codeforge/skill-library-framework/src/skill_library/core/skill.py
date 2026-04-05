import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from src.skill_library.storage.vector_db import VectorDB
from src.skill_library.storage.skill_repository import SkillRepository
from src.skill_library.core.domain import Domain
from src.skill_library.core.complexity import Complexity
from src.skill_library.core.utility import Utility
from src.skill_library.models.predictive_scoring import PredictiveScoringModel
from src.skill_library.models.task_scoring_model import TaskScoringModel
from src.skill_library.models.curiosity_budget import CuriosityBudget
import src.skill_library.integrations.memory_system as memory_system
import src.skill_library.integrations.pytorch_integration as pytorch_integration

# Setup logging
logger = logging.getLogger(__name__)

class Skill:
    def __init__(
        self,
        name: str,
        domain: str,
        version: str = "1.0",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.domain = domain
        self.version = version
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.performance_history = []
        self.efficiency_metrics = {}
        self._vector_db = VectorDB()
        self._skill_repository = SkillRepository()
        self._domain = Domain()
        self._complexity = Complexity()
        self._utility = Utility()
        self._predictive_model = PredictiveScoringModel()
        self._task_scoring_model = TaskScoringModel()
        self._curiosity_budget = CuriosityBudget()
        self._pytorch_integration = pytorch_integration.PyTorchIntegration()
        self._memory_system = memory_system.MemorySystem()

    def evaluate(self) -> Dict[str, Any]:
        """
        Evaluate the skill's current performance based on its metrics and update history
        """
        return {
            "name": self.name,
            "domain": self.domain,
            "version": self.version,
            "metadata": self.metadata
        }

    def update(self, new_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the skill with new metadata
        """
        self.metadata.update(new_metadata)
        self.updated_at = datetime.now()
        # Create a copy of metadata to avoid reference issues
        self.performance_history.append(new_metadata.copy())
        # Return the evaluation results
        return self.evaluate()