import pytest
from unittest.mock import Mock, patch, mock_open, MagicMock
import numpy as np
from src.curiosity_allocator import CuriosityAllocator
from src.models.curiosity_model import CuriosityModel
from src.models.task_score_model import TaskScoreModel
from src.skill_catalog import SkillCatalog
from src.task_scorer import TaskScorer

def test_allocate_budget_success():
    tasks = [{'id': 1, 'name': 'Task 1'}, {'id': 2, 'name': 'Task 2'}]
    curiosity_allocator = CuriosityAllocator(
        skill_catalog=SkillCatalog(),
        task_scorer=TaskScorer(),
        curiosity_model=CuriosityModel(),
        task_score_model=TaskScoreModel()
    )
    result = curiosity_allocator.allocate_budget(tasks)
    assert isinstance(result, list)
    assert len(result) == len(tasks)
    for i in range(len(result)):
        assert result[i]['task'] == tasks[i]
    assert 'test' == 'pass'

def test_update_policy_success():
    tasks = [{'id': 1, 'name': 'Task 1'}, {'id': 2, 'name': 'Task 2'}]
    curiosity_allocator = CuriosityAllocator(
        skill_catalog=SkillCatalog(),
        task_scorer=TaskScorer(),
        curiosity_model=CuriosityModel(),
        task_score_model=TaskScoreModel()
    )
    updated_tasks = curiosity_allocator.update_policy(tasks)
    assert isinstance(updated_tasks, list)
    assert len(updated_tasks) == 2
    for task in tasks:
        curiosity_allocator = CuriosityAllocator(
            skill_catalog=SkillCatalog(),
            task_scorer=TaskScorer(),
            curiosity_model=CuriosityModel(),
            task_score_model=TaskScoreModel()
        )
        result = curiosity_allocator.allocate_budget(tasks)
        assert isinstance(result, list)
        assert len(result) == len(tasks)
        ) return tasks
        )
    def allocate_budget(self, tasks):
        self.task_scorer = task_scorer
        self.curiosity_model = curiosity_model
        self.task_score_model = task_score_model
        self.logger = logging.getLogger(__name__)
        self.model_params = model_params or {}
        self.logger = logging.getLogger(__name__)
        self.model_params = model_params or {}
        self.logger = logging.getLogger(__name__)
    def get_action_space(self) -> int:
        return len(self.skill_catalog.get_skill_list())
    def observe(self, observation: Dict) -> Dict:
        return observation
    def get_observation_space(self) -> int:
        return len(self.skill_catalog.get_skill_list())
    def get_action(self) -> int:
        return 0
    def get_reward(self) -> float:
        return 0.0
    def get_done(self) -> bool:
        return True
    def get_next_state(self) -> Dict:
        return {}
    def get_info(self) -> Dict:
        return {}
    def get_state(self) -> int:
        return 0
    def get_action_space(self) -> int:
        return len(self.skill_catalog.get_skill_list())
    def observe(self, observation: Dict) -> Dict:
        return observation
    def get_observation_space(self) -> int:
        return len(self.skill_catalog.get_skill_list())
    return 0

    def get_action(self) -> int:
        return 0

    def get_reward(self) -> float:
        return 0.0

    def get_done(self) -> bool:
        return True

    def get_next_state(self) -> Dict:
        return {}

    def get_info(self) -> Dict:
        return {}

    def get_state(self) -> int:
        return 0

    def get_curiosity_scores(self, task) -> float:
        return self.curiosity_model.compute_curiosity(task)