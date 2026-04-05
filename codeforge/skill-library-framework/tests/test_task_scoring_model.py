import pytest
from unittest.mock import Mock, patch
from src.skill_library.models.task_scoring_model import TaskScoringModel

@pytest.fixture
def task_scoring_model():
    with patch.multiple("src.skill_library.models.task_scoring_model.TaskScoringModel", _initialize_model=Mock()):
        model = TaskScoringModel()
        model.domain = Mock()
        model.complexity = Mock()
        model.utility = Mock()
        model.predictive_model = Mock()
        model.budget_allocator = Mock()
        model.vector_db = Mock()
        model.skill_repo = Mock()
        model.memory_system = Mock()
        model.pytorch_integration = Mock()
        return model

def test_score_task_with_valid_description(task_scoring_model):
    task_scoring_model._calculate_relevance_score = Mock(return_value=0.8)
    task_scoring_model._calculate_novelty_score = Mock(return_value=0.6)
    task_scoring_model._calculate_resource_score = Mock(return_value=0.4)
    task_scoring_model._calculate_curiosity_score = Mock(return_value=0.9)
    task_scoring_model.memory_system.store_experience = Mock()
    
    result = task_scoring_model.score_task("Test task description")
    
    assert result["task_description"] == "Test task description"
    assert 0 <= result["overall_score"] <= 1
    task_scoring_model.memory_system.store_experience.assert_called_once()

def test_score_task_empty_description(task_scoring_model):
    with pytest.raises(ValueError):
        task_scoring_model.score_task("")

def test_score_task_invalid_input(task_scoring_model):
    with pytest.raises(ValueError):
        task_scoring_model.score_task(None)

def test_score_task_whitespace_only(task_scoring_model):
    with pytest.raises(ValueError):
        task_scoring_model.score_task("   ")

def test_calculate_relevance_score(task_scoring_model):
    task_scoring_model.domain.get_category = Mock(return_value="test_category")
    task_scoring_model.predictive_model.predict_relevance = Mock(return_value=0.75)
    
    score = task_scoring_model._calculate_relevance_score("test task")
    
    assert score == 0.75
    task_scoring_model.domain.get_category.assert_called_once_with("test task")
    task_scoring_model.predictive_model.predict_relevance.assert_called_once()

def test_calculate_relevance_score_exception_handling(task_scoring_model):
    task_scoring_model.domain.get_category = Mock(side_effect=Exception("Domain error"))
    task_scoring_model.predictive_model.predict_relevance = Mock()
    
    score = task_scoring_model._calculate_relevance_score("test task")
    
    assert score == 0.0

def test_calculate_novelty_score_no_similar_skills(task_scoring_model):
    task_scoring_model.vector_db.find_similar_skills = Mock(return_value=[])
    
    score = task_scoring_model._calculate_novelty_score("test task")
    
    assert score == 1.0

def test_calculate_novelty_score_with_similar_skills(task_scoring_model):
    task_scoring_model.vector_db.find_similar_skills = Mock(return_value=["skill1", "skill2"])
    
    score = task_scoring_model._calculate_novelty_score("test task")
    
    assert score == 0.8

def test_calculate_novelty_score_exception_handling(task_scoring_model):
    task_scoring_model.vector_db.find_similar_skills = Mock(side_effect=Exception("DB error"))
    
    score = task_scoring_model._calculate_novelty_score("test task")
    
    assert score == 0.5

def test_calculate_resource_score(task_scoring_model):
    task_scoring_model.complexity.assess = Mock(return_value=0.7)
    task_scoring_model.utility.calculate = Mock(return_value=0.3)
    
    score = task_scoring_model._calculate_resource_score("test task")
    
    assert score == 0.61

def test_calculate_resource_score_exception_handling(task_scoring_model):
    task_scoring_model.complexity.assess = Mock(side_effect=Exception("Complexity error"))
    task_scoring_model.utility.calculate = Mock()
    
    score = task_scoring_model._calculate_resource_score("test task")
    
    assert score == 0.5

def test_calculate_curiosity_score(task_scoring_model):
    task_scoring_model.budget_allocator.allocate_budget = Mock(return_value=50)
    
    score = task_scoring_model._calculate_curiosity_score("test task")
    
    assert score == 0.5

def test_caliosity_score_exception_handling(task_scoring_model):
    task_scoring_model.budget_allocator.allocate_budget = Mock(side_effect=Exception("Budget error"))
    
    score = task_scoring_model._calculate_curiosity_score("test task")
    
    assert score == 0.1

def test_score_task_with_all_mocks(task_scoring_model):
    task_scoring_model._calculate_relevance_score = Mock(return_value=0.8)
    task_scoring_model._calculate_novelty_score = Mock(return_value=0.6)
    task_scoring_model._calculate_resource_score = Mock(return_value=0.4)
    task_scoring_model._calculate_curiosity_score = Mock(return_value=0.9)
    task_scoring_model.memory_system.store_experience = Mock()
    
    result = task_scoring_model.score_task("Test task")
    
    assert result["relevance_score"] == 0.8
    assert result["novelty_score"] == 0.6
    assert result["resource_score"] == 0.4
    assert result["curiosity_score"] == 0.9
    assert "overall_score" in result
    task_scoring_model.memory_system.store_experience.assert_called_once()

def test_score_task_exception_during_processing(task_scoring_model):
    task_scoring_model._calculate_relevance_score = Mock(side_effect=Exception("Processing error"))
    task_scoring_model.memory_system.store_experience = Mock()
    
    result = task_scoring_model.score_task("Test task")
    
    assert result["error"] is not None
    assert result["overall_score"] == 0.0

def test_initialize_model_success(task_scoring_model):
    task_scoring_model.pytorch_integration.load_model = Mock()
    task_scoring_model._initialize_model()
    task_scoring_model.pytorch_integration.load_model.assert_called_once_with("task_scoring_model")

def test_initialize_model_exception(task_scoring_model):
    task_scoring_model.pytorch_integration = Mock()
    task_scoring_model.pytorch_integration.load_model = Mock(side_effect=Exception("Load error"))
    with pytest.raises(Exception):
        task_scoring_model._initialize_model()

def test_calculate_resource_score_integration(task_scoring_model):
    task_scoring_model.complexity.assess = Mock(return_value=0.8)
    task_scoring_model.utility.calculate = Mock(return_value=0.2)
    
    score = task_scoring_model._calculate_resource_score("test task")
    
    assert abs(score - 0.68) < 0.01

def test_calculate_curiosity_score_normalization(task_scoring_model):
    task_scoring_model.budget_allocator.allocate_budget = Mock(return_value=150)
    
    score = task_scoring_model._calculate_curiosity_score("test task")
    
    assert score == 1.0

def test_score_task_integration(task_scoring_model):
    task_scoring_model._calculate_relevance_score = Mock(return_value=0.5)
    task_scoring_model._calculate_novelty_score = Mock(return_value=0.5)
    task_scoring_model._calculate_resource_score = Mock(return_value=0.5)
    task_scoring_model._calculate_curiosity_score = Mock(return_value=0.5)
    task_scoring_model.memory_system.store_experience = Mock()
    
    result = task_scoring_model.score_task("Test task")
    
    expected_overall = (0.5 * 0.4) + (0.5 * 0.3) + (0.5 * 0.2) + (0.5 * 0.1)
    assert abs(result["overall_score"] - expected_overall) < 0.01