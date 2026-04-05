from unittest.mock import Mock, patch
import pytest
from fastapi import HTTPException
from src.skill_library.api.task_endpoints import router, TaskRequest, TaskResponse
from src.skill_library.models.task_scoring_model import TaskScoringModel
from src.skill_library.storage.skill_repository import SkillRepository
from src.skill_library.integrations.pytorch_integration import PyTorchIntegration
from src.skill_library.core.domain import Domain
from src.skill_library.core.complexity import Complexity
from src.skill_library.core.utility import Utility
from src.skill_library.models.predictive_scoring import PredictiveScoringModel
from src.skill_library.models.curiosity_budget import CuriosityBudget
from src.skill_library.storage.vector_db import VectorDB
from src.skill_library.integrations.memory_system import MemorySystem

def test_score_task_success():
    # Arrange
    request = TaskRequest(
        task_description="Analyze user feedback",
        domain="customer_service",
        complexity=5,
        experience=3
    )
    
    # Mock all dependencies
    with patch('src.skill_library.api.task_endpoints.TaskScoringModel') as mock_model, \
         patch('src.skill_library.api.task_endpoints.SkillRepository') as mock_repo, \
         patch('src.skill_library.api.task_endpoints.PyTorchIntegration') as mock_pytorch, \
         patch('src.skill_library.api.task_endpoints.Domain') as mock_domain, \
         patch('src.skill_library.api.task_endpoints.Complexity') as mock_complexity, \
         patch('src.skill_library.api.task_endpoints.Utility') as mock_utility, \
         patch('src.skill_library.api.task_endpoints.PredictiveScoringModel') as mock_predictive, \
         patch('src.skill_library.api.task_endpoints.CuriosityBudget') as mock_budget, \
         patch('src.skill_library.api.task_endpoints.VectorDB') as mock_vector_db, \
         patch('src.skill_library.api.task_endpoints.MemorySystem') as mock_memory:
        
        # Setup return values
        mock_domain.return_value.get_category.return_value = "customer_service"
        mock_complexity.return_value.assess.return_value = 5
        mock_utility.return_value.calculate.return_value = 3
        mock_model.return_value.score_task.return_value = 0.85
        mock_predictive.return_value.predict_relevance.return_value = 0.7
        mock_budget.return_value.allocate_budget.return_value = 0.3
        mock_vector_db.return_value.find_similar_skills.return_value = ["skill1", "skill2"]
        mock_memory.return_value.recall.return_value = []
        
        # Act
        from src.skill_library.api.task_endpoints import score_task
        result = score_task.__wrapped__(request)
        
        # Assert
        assert isinstance(result, TaskResponse)
        assert result.score == 0.85
        assert "Task scored" in result.explanation

def test_score_task_empty_description_raises_400():
    request = TaskRequest(
        task_description="",
        domain="customer_service",
        complexity=5
    )
    
    with pytest.raises(HTTPException) as exc_info:
        from src.skill_library.api.task_endpoints import score_task
        score_task.__wrapped__(request)
    
    assert exc_info.value.status_code == 400
    assert "Task description is required" in str(exc_info.value.detail)

def test_score_task_invalid_complexity_raises_400():
    request = TaskRequest(
        task_description="Test task",
        domain="customer_service",
        complexity=15  # Invalid complexity
    )
    
    with pytest.raises(HTTPException) as exc_info:
        from src.skill_library.api.task_endpoints import score_task
        score_task.__wrapped__(request)
    
    assert exc_info.value.status_code == 400
    assert "Complexity must be between 1 and 10" in str(exc_info.value.detail)

def test_score_task_negative_experience_raises_400():
    request = TaskRequest(
        task_description="Test task",
        domain="customer_service",
        complexity=5,
        experience=-1
    )
    
    with pytest.raises(HTTPException) as exc_info:
        from src.skill_library.api.task_endpoints import score_task
        score_task.__wrapped__(request)
    
    assert exc_info.value.status_code == 400
    assert "Experience cannot be negative" in str(exc_info.value.detail)

def test_score_task_with_whitespace_description_raises_400():
    request = TaskRequest(
        task_description="   ",
        domain="customer_service",
        complexity=5
    )
    
    with pytest.raises(HTTPException) as exc_info:
        from src.skill_library.api.task_endpoints import score_task
        score_task.__wrapped__(request)
    
    assert exc_info.value.status_code == 400
    assert "Task description is required" in str(exc_info.value.detail)

@patch('src.skill_library.api.task_endpoints.TaskScoringModel')
@patch('src.skill_library.api.task_endpoints.SkillRepository')
@patch('src.skill_library.api.task_endpoints.PyTorchIntegration')
@patch('src.skill_library.api.task_endpoints.Domain')
@patch('src.skill_library.api.task_endpoints.Complexity')
@patch('src.skill_library.api.task_endpoints.Utility')
@patch('src.skill_library.api.task_endpoints.PredictiveScoringModel')
@patch('src.skill_library.api.task_endpoints.CuriosityBudget')
@patch('src.skill_library.api.task_endpoints.VectorDB')
@patch('src.skill_library.api.task_endpoints.MemorySystem')
def test_score_task_internal_error_raises_500(
    mock_memory, mock_vector_db, mock_budget, mock_predictive, 
    mock_utility, mock_complexity, mock_domain, mock_pytorch,
    mock_repo, mock_model):
    
    # Setup to cause internal error
    mock_domain.return_value.get_category.side_effect = Exception("Database error")
    
    request = TaskRequest(
        task_description="Test task",
        domain="customer_service",
        complexity=5
    )
    
    with pytest.raises(HTTPException) as exc_info:
        from src.skill_library.api.task_endpoints import score_task
        score_task.__wrapped__(request)
    
    assert exc_info.value.status_code == 500
    assert "Internal server error" in str(exc_info.value.detail)

def test_get_task_scoring_model_returns_instance():
    from src.skill_library.api.task_endpoints import get_task_scoring_model
    model = get_task_scoring_model()
    assert isinstance(model, TaskScoringModel)

def test_get_skill_repository_returns_instance():
    from src.skill_library.api.task_endpoints import get_skill_repository
    repo = get_skill_repository()
    assert isinstance(repo, SkillRepository)

def test_get_pytorch_integration_returns_instance():
    from src.skill_library.api.task_endpoints import get_pytorch_integration
    integration = get_pytorch_integration()
    assert isinstance(integration, PyTorchIntegration)

def test_get_domain_returns_instance():
    from src.skill_library.api.task_endpoints import get_domain
    domain = get_domain()
    assert isinstance(domain, Domain)

def test_get_complexity_returns_instance():
    from src.skill_library.api.task_endpoints import get_complexity
    complexity = get_complexity()
    assert isinstance(complexity, Complexity)

def test_get_utility_returns_instance():
    from src.skill_library.api.task_endpoints import get_utility
    utility = get_utility()
    assert isinstance(utility, Utility)

def test_get_predictive_model_returns_instance():
    from src.skill_library.api.task_endpoints import get_predictive_model
    model = get_predictive_model()
    assert isinstance(model, PredictiveScoringModel)

def test_get_curiosity_budget_returns_instance():
    from src.skill_library.api.task_endpoints import get_curiosity_budget
    budget = get_curiosity_budget()
    assert isinstance(budget, CuriosityBudget)

def test_get_vector_db_returns_instance():
    from src.skill_library.api.task_endpoints import get_vector_db
    db = get_vector_db()
    assert isinstance(db, VectorDB)

def test_get_memory_system_returns_instance():
    from src.skill_library.api.task_endpoints import get_memory_system
    memory = get_memory_system()
    assert isinstance(memory, MemorySystem)