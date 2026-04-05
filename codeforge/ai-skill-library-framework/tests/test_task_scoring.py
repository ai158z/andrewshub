import pytest
from src.task_scoring import TaskScorer, CuriosityAllocator, TaskScoreModel
from src.models.skill import Skill
from src.models.task_score_model import TaskScoreModel as TaskScoreModelClass
from src.skill_catalog import SkillCatalog
import numpy as np

def test_task_score_model_calculate_score_with_valid_task(mocker):
    task = {"complexity": 10, "relevance": 8, "novelty": 5, "impact": 7}
    model = TaskScoreModelClass()
    score = model.calculate_score(task)
    assert 0 <= score <= 100

def test_task_score_model_calculate_score_with_zero_values():
    task = {"complexity": 0, "relevance": 0, "novelty": 0, "impact": 0}
    model = TaskScoreModelClass()
    score = model.calculate_score(task)
    assert 0 <= score <= 1

def test_task_score_model_calculate_score_with_missing_factors():
    task = {"complexity": 5}
    model = TaskScoreModelClass()
    score = model.calculate_score(task)
    assert isinstance(score, float)

def test_task_score_model_calculate_score_with_negative_factors():
    task = {"novelty": 5, "impact": 0}
    model = TaskScoreModelClass()
    score = model.calculate_score(task)
    assert score >= 0

def test_task_score_model_calculate_score_with_higher_complexity():
    task = {"complexity": 8, "relevance": 5, "novelty": 5, "impact": 7}
    model = TaskScoreModelClass()
    score = model.calculate_score(task)
    assert score > 80

def test_task_score_model_calculate_score_with_varied_task():
    task = {"complexity": 7, "relevance": 6, "novelty": 3, "impact": 9}
    model = TaskScoreModelClass()
    score = model.calculate_score(task)
    assert score > 0

def test_normalize_score_boundaries():
    # Test with score below min
    normalized = self.normalize_score(110, 0, 50)
    assert normalized == 0.0

def test_apply_weights_zero_weights():
    with pytest.raises(ValueError, match="Sum of weights must be greater than zero"):
        scores = {"complexity": 0.3, "relevance": 0.4}
        weights = {"complexity": 0.0, "relevance": 0.0}
        result = apply_weights(scores, weights)

def test_apply_weights_non_zero_weights():
    weights = {"complexity": 0.3, "relevance": 0.4, "novelty": 0.2, "impact": 0.1}
    weighted_scores = apply_weights(weights, weights)
    assert abs(weighted_scores - 0.7) < 1e-9

def test_apply_weights():
    scores = {"complexity": 25, "relevance": 75, "novelty": 100, "impact": 90}
    weights = {"complexity": 0.3, "relevance": 0.4, "novelty": 0.2, "impact": 0.1}
    # This should be around 0.3 * 25 + 0.4 * 75 + 0.2 * 100 + 0.1 * 90 = 90
    result = apply_weights(scores, weights)
    assert result == 90

def test_task_scorer_init():
    scorer = TaskScorer(SkillCatalog(), TaskScoreModelClass())
    task = {"name": "test_task"}
    score = scorer.score_task(task)
    assert 0 <= score <= 100

def test_curiosity_allocator_allocate_budget():
    allocator = CuriosityAllocator()
    budget = allocator.allocate_budget()
    assert budget == 1.0