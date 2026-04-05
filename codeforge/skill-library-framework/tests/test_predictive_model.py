import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add the skill_library to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from skill_library.core.skill import Skill
    from skill_library.core.domain import Domain
    from skill_library.core.complexity import Complexity
    from skill_library.core.utility import Utility
    from skill_library.models.predictive_scoring import PredictiveScoringModel
    from skill_library.models.task_scoring_model import TaskScoringModel
    from skill_library.storage.vector_db import VectorDB
    from skill_library.storage.skill_repository import SkillRepository
    from skill_library.integrations.memory_system import MemorySystem
except ImportError:
    # Create mock classes for testing when the real modules aren't available
    class Skill:
        def __init__(self, name="", domain="", proficiency=0.0):
            self.name = name
            self.domain = domain
            self.proficiency = proficiency

    class Domain:
        pass

    class Complexity:
        pass

    class Utility:
        pass

    class PredictiveScoringModel:
        def __init__(self, vector_db, skill_repository, memory_system):
            self.vector_db = vector_db
            self.skill_repository = skill_repository
            self.memory_system = memory_system
            
        def predict_relevance(self, query):
            # Simple mock implementation
            return {}

    class TaskScoringModel:
        def __init__(self, domain, complexity, utility):
            self.domain = domain
            self.complexity = complexity
            self.utility = utility
            
        def score_task(self, task_data):
            return 0.5

    class VectorDB:
        pass

    class SkillRepository:
        pass

    class MemorySystem:
        pass


@pytest.fixture
def mock_predictive_model():
    mock_vector_db = MagicMock(spec=VectorDB)
    mock_repository = MagicMock(spec=SkillRepository)
    mock_memory = MagicMock(spec=MemorySystem)
    
    model = PredictiveScoringModel(
        vector_db=mock_vector_db,
        skill_repository=mock_repository,
        memory_system=mock_memory
    )
    return model, mock_vector_db, mock_repository, mock_memory


@pytest.fixture
def mock_task_model():
    mock_domain = MagicMock(spec=Domain)
    mock_complexity = MagicMock(spec=Complexity)
    mock_utility = MagicMock(spec=Utility)
    
    model = TaskScoringModel(
        domain=mock_domain,
        complexity=mock_complexity,
        utility=mock_utility
    )
    return model, mock_domain, mock_complexity, mock_utility


def test_predictive_scoring_with_results(mock_predictive_model):
    predictive_model, mock_vector_db, mock_repository, _ = mock_predictive_model
    
    # Setup mock skills
    mock_skills = [
        Skill(name="Python Programming", domain="Programming", proficiency=0.8),
        Skill(name="Data Analysis", domain="Analytics", proficiency=0.7),
        Skill(name="Machine Learning", domain="AI", proficiency=0.9)
    ]
    
    mock_vector_db.find_similar.return_value = mock_skills
    mock_repository.get.return_value = mock_skills[0]
    
    # Execute
    query = "data science techniques"
    scores = predictive_model.predict_relevance(query)
    
    # Verify
    assert scores is not None
    assert isinstance(scores, dict)
    assert len(scores) > 0


def test_predictive_scoring_empty_results(mock_predictive_model):
    predictive_model, mock_vector_db, _, _ = mock_predictive_model
    
    # Setup for empty results
    mock_vector_db.find_similar.return_value = []
    
    # Execute
    query = "nonexistent query"
    scores = predictive_model.predict_relevance(query)
    
    # Verify
    assert scores == {}


def test_predictive_scoring_none_query(mock_predictive_model):
    predictive_model, _, _, _ = mock_predictive_model
    
    with pytest.raises((TypeError, ValueError)):
        predictive_model.predict_relevance(None)


def test_task_scoring_valid_input(mock_task_model):
    task_model, _, mock_complexity, mock_utility = mock_task_model
    
    mock_complexity.assess.return_value = 0.7
    mock_utility.calculate.return_value = 0.8
    
    task_data = {
        "task_name": "Implement machine learning model",
        "domain": "AI",
        "required_skills": ["Python Programming", "Statistics"],
        "estimated_complexity": 0.7
    }
    
    score = task_model.score_task(task_data)
    
    assert score is not None
    assert isinstance(score, (int, float))
    assert 0.0 <= score <= 1.0


def test_task_scoring_missing_task_data(mock_task_model):
    task_model, _, _, _ = mock_task_model
    
    with pytest.raises(KeyError):
        task_data = {"incomplete": "data"}
        task_model.score_task(task_data)


def test_task_scoring_empty_task_data(mock_task_model):
    task_model, _, _, _ = mock_task_model
    
    task_data = {}
    with pytest.raises(KeyError):
        task_model.score_task(task_data)


def test_predictive_model_init():
    mock_vector_db = MagicMock()
    mock_repository = MagicMock()
    mock_memory = MagicMock()
    
    model = PredictiveScoringModel(
        vector_db=mock_vector_db,
        skill_repository=mock_repository,
        memory_system=mock_memory
    )
    
    assert model is not None
    assert model.vector_db == mock_vector_db
    assert model.skill_repository == mock_repository
    assert model.memory_system == mock_memory


def test_predictive_model_invalid_init():
    with pytest.raises(TypeError):
        PredictiveScoringModel(
            vector_db=None,
            skill_repository=None,
            memory_system=None
        )


def test_task_model_init():
    mock_domain = MagicMock()
    mock_complexity = MagicMock()
    mock_utility = MagicMock()
    
    model = TaskScoringModel(
        domain=mock_domain,
        complexity=mock_complexity,
        utility=mock_utility
    )
    
    assert model.domain == mock_domain
    assert model.complexity == mock_complexity
    assert model.utility == mock_utility


def test_task_model_invalid_init():
    with pytest.raises(TypeError):
        TaskScoringModel(
            domain=None,
            complexity=None,
            utility=None
        )


def test_predictive_scoring_single_skill(mock_predictive_model):
    predictive_model, mock_vector_db, mock_repository, _ = mock_predictive_model
    
    mock_skills = [
        Skill(name="Single Skill", domain="Test", proficiency=0.5)
    ]
    
    mock_vector_db.find_similar.return_value = mock_skills
    mock_repository.get.return_value = mock_skills[0]
    
    query = "single skill test"
    scores = predictive_model.predict_relevance(query)
    
    assert "Single Skill" in scores
    assert 0.0 <= scores["Single Skill"] <= 1.0


def test_predictive_scoring_duplicate_skills(mock_predictive_model):
    predictive_model, mock_vector_db, mock_repository, _ = mock_predictive_model
    
    duplicate_skills = [
        Skill(name="Duplicate Skill", domain="Test", proficiency=0.5),
        Skill(name="Duplicate Skill", domain="Test", proficiency=0.6)
    ]
    
    mock_vector_db.find_similar.return_value = duplicate_skills
    mock_repository.get.return_value = duplicate_skills[0]
    
    query = "duplicate skills test"
    scores = predictive_model.predict_relevance(query)
    
    # Should handle duplicates gracefully - only one entry per skill name
    assert len(scores) == 1
    assert "Duplicate Skill" in scores


def test_task_scoring_boundary_values(mock_task_model):
    task_model, _, mock_complexity, mock_utility = mock_task_model
    
    mock_complexity.assess.return_value = 1.0  # Max complexity
    mock_utility.calculate.return_value = 0.0   # Min utility
    
    task_data = {
        "task_name": "Boundary Test",
        "domain": "Test",
        "required_skills": [],
        "estimated_complexity": 1.0
    }
    
    score = task_model.score_task(task_data)
    assert 0.0 <= score <= 1.0


def test_task_scoring_complexity_out_of_range(mock_task_model):
    task_model, _, mock_complexity, mock_utility = mock_task_model
    
    # Test with out of range complexity
    mock_complexity.assess.return_value = 1.5  # Invalid value
    mock_utility.calculate.return_value = 0.5
    
    task_data = {
        "task_name": "Range Test",
        "domain": "Test",
        "required_skills": ["Skill1"],
        "estimated_complexity": 1.5
    }
    
    score = task_model.score_task(task_data)
    # Should handle out of range gracefully
    assert 0.0 <= score <= 1.0


def test_predictive_scoring_large_dataset(mock_predictive_model):
    predictive_model, mock_vector_db, _, _ = mock_predictive_model
    
    # Simulate large number of skills
    large_skillset = [
        Skill(name=f"Skill{i}", domain="Test", proficiency=0.1)
        for i in range(1000)
    ]
    
    mock_vector_db.find_similar.return_value = large_skillset
    
    query = "large dataset"
    scores = predictive_model.predict_relevance(query)
    
    assert len(scores) == 1000
    # All skills should have scores
    for skill in scores.values():
        assert 0.0 <= skill <= 1.0


def test_task_scoring_no_required_skills(mock_task_model):
    task_model, _, _, _ = mock_task_model
    
    task_data = {
        "task_name": "No Skills Test",
        "domain": "Test",
        "required_skills": [],  # Empty list
        "estimated_complexity": 0.5
    }
    
    score = task_model.score_task(task_data)
    assert 0.0 <= score <= 1.0


def test_predictive_scoring_special_characters(mock_predictive_model):
    predictive_model, mock_vector_db, _, _ = mock_predictive_model
    
    mock_vector_db.find_similar.return_value = [
        Skill(name="Special@#$%Characters", domain="Test", proficiency=0.5)
    ]
    
    query = "special !@#$%^&*() characters"
    scores = predictive_model.predict_relevance(query)
    
    assert "Special@#$%Characters" in scores


def test_task_scoring_unicode_characters(mock_task_model):
    task_model, _, _, _ = mock_task_model
    
    task_data = {
        "task_name": "Unicode Task 🚀",
        "domain": "Test 🧪",
        "required_skills": ["技能测试"],
        "estimated_complexity": 0.5
    }
    
    score = task_model.score_task(task_data)
    assert 0.0 <= score <= 1.0


def test_predictive_scoring_performance(mock_predictive_model):
    predictive_model, mock_vector_db, _, _ = mock_predictive_model
    
    # Mock slow database response
    mock_vector_db.find_similar.return_value = [
        Skill(name=f"Skill{i}", domain="Test", proficiency=0.5)
        for i in range(100)
    ]
    
    import time
    start = time.time()
    query = "performance test"
    scores = predictive_model.predict_relevance(query)
    end = time.time()
    
    # Should complete in reasonable time
    assert (end - start) < 1.0
    assert len(scores) == 100


def test_task_scoring_consistent_results(mock_task_model):
    task_model, mock_complexity, mock_utility, _ = mock_task_model
    
    mock_complexity.assess.return_value = 0.7
    mock_utility.calculate.return_value = 0.8
    
    task_data1 = {
        "task_name": "Consistency Test 1",
        "domain": "Test",
        "required_skills": ["Skill1"],
        "estimated_complexity": 0.7
    }
    
    task_data2 = {
        "task_name": "Consistency Test 1",  # Same as test1
        "domain": "Test",
        "required_skills": ["Skill1"],
        "estimated_complexity": 0.7
    }
    
    score1 = task_model.score_task(task_data1)
    score2 = task_model.score_task(task_data2)
    
    # Should be deterministic
    assert score1 == score2