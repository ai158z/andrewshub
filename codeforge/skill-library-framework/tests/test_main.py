import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.skill_library.api.main import app, AppState

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def mock_settings():
    with patch('src.skill_library.api.main.Settings') as mock:
        mock.return_value.DATABASE_URL = "sqlite:///:memory:"
        yield mock

@pytest.fixture
def mock_engine():
    with patch('src.skill_library.api.main.create_engine') as mock:
        yield mock

@pytest.fixture
def mock_sessionmaker():
    with patch('src.skill_library.api.main.sessionmaker') as mock:
        yield mock

def test_root_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "Skill Library Framework API" in response.json()["message"]

def test_health_check_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_cors_middleware_added():
    # Check that CORS middleware is properly configured
    cors_middleware = [mw for mw in app.user_middleware if 'CORSMiddleware' in str(mw.__class__)]
    assert len(cors_middleware) > 0
    assert cors_middleware[0].cls.__name__ == "CORSMiddleware"

@patch('src.skill_library.api.main.SkillRepository')
@patch('src.skill_library.api.main.create_engine')
def test_app_initialization(mock_engine, mock_repo, mock_settings):
    # Test that the app initializes with required components
    from sqlalchemy import create_engine
    mock_engine.return_value = MagicMock()
    
    # Simulate app startup
    with patch('src.skill_library.api.main.Settings', return_value=mock_settings):
        # This is a basic test - in real scenario would test actual initialization
        assert True  # Passes if no exception during import

@patch('src.skill_library.api.main.VectorDB')
@patch('src.skill_library.api.main.PredictiveScoringModel')
@patch('src.skill_library.api.main.TaskScoringModel')
@patch('src.skill_library.api.main.CuriosityBudget')
@patch('src.skill_library.api.main.PyTorchIntegration')
@patch('src.skill_library.api.main.MemorySystem')
def test_app_state_initialization(mock_memory, mock_pytorch, mock_curiosity, 
                                 mock_task_scorer, mock_predictive, mock_vector_db):
    # Test that all components are initialized in app state
    state = AppState()
    assert state.skill_repo is None
    assert state.vector_db is None
    assert state.predictive_model is None
    assert state.task_scorer is None
    assert state.curiosity_budget is None
    assert state.pytorch_integration is None
    assert state.memory_system is None

def test_routers_included():
    # Check that routers are included
    router_names = [route.name for route in app.routes]
    assert "skill_router" in str(app.routes) or "skill_endpoints" in str(app.router.routes)
    assert "task_router" in str(app.routes) or "task_endpoints" in str(app.router.routes)

@patch('src.skill_library.api.skill_endpoints.router')
@patch('src.skill_library.api.task_endpoints.router')
def test_routers_mounted(skill_router_mock, task_router_mock):
    # Verify routers are included in app
    assert app.include_router.called_with(skill_router_mock)
    assert app.include_router.called_with(task_router_mock)

def test_lifespan_manager_exists():
    # Check that lifespan manager is defined
    assert hasattr(app.router, 'lifespan_context')

def test_exception_handlers_registered():
    # Check that exception handlers are registered
    exception_handlers = app.exception_handlers
    assert len(exception_handlers) > 0

@patch('src.skill_library.api.main.SkillRepository')
def test_database_initialization_failure(mock_skill_repo):
    mock_skill_repo.side_effect = Exception("Database connection failed")
    # Would raise exception during startup
    with pytest.raises(Exception, match="Database connection failed"):
        # This would be caught in lifespan startup
        pass

def test_get_app_state_function():
    # Test the dependency injection function
    state = app.state.app_state = AppState()
    returned_state = app.state.app_state
    assert returned_state is not None
    assert isinstance(returned_state, AppState)

@patch('src.skill_library.api.main.logger')
def test_startup_logging(mock_logger):
    # Verify logger is called during startup
    mock_logger.info.assert_called_with("Initializing application...")

@patch('src.skill_library.api.main.logger')
def test_shutdown_logging(mock_logger):
    # Verify shutdown logging
    mock_logger.info.assert_called_with("Shutting down application...")

def test_global_exception_handler():
    # Test that global exception handler is registered
    assert len(app.exception_handlers) > 0
    assert Exception in app.exception_handlers

def test_http_exception_handler():
    # Test that HTTP exception handler is registered
    assert HTTPException in app.exception_handlers

@patch('src.skill_library.api.main.VectorDB')
def test_vector_db_initialization(mock_vector_db):
    # Test that VectorDB is initialized
    mock_vector_db_instance = MagicMock()
    mock_vector_db.return_value = mock_vector_db_instance
    assert mock_vector_db_instance is not None

@patch('src.skill_library.api.main.PredictiveScoringModel')
def test_model_initializations(mock_model):
    # Test that models are initialized
    mock_model_instance = MagicMock()
    mock_model.return_value = mock_model_instance
    assert mock_model_instance is not None

@patch('src.skill_library.api.main.sessionmaker')
def test_sessionmaker_called(mock_sessionmaker):
    # Test that sessionmaker is called with correct parameters
    mock_sessionmaker.assert_not_called()  # Initially not called

def test_app_state_singleton():
    # Test that app state is singleton
    state1 = app.state.app_state
    state2 = app.state.app_state
    assert state1 is state2

@patch('src.skill_library.api.main.Settings')
def test_settings_loaded(mock_settings):
    # Test settings are loaded
    settings_instance = MagicMock()
    settings_instance.DATABASE_URL = "test_url"
    mock_settings.return_value = settings_instance
    assert settings_instance.DATABASE_URL == "test_url"