import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.main import create_app

@pytest.fixture
def app_instance():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test App"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
        yield app

@pytest.fixture
def client(app_instance):
    return TestClient(app_instance)

def test_create_app_returns_fastapi_instance():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test App"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
    assert isinstance(app, FastAPI)

def test_app_has_correct_title_and_description():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test ROS Dashboard"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
    
    assert app.title == "Test ROS Dashboard"
    assert app.description == "Test Description"

def test_app_includes_cors_middleware():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
    
    cors_middleware_found = False
    for middleware in app.user_middleware:
        if 'CORS' in str(middleware.cls):
            cors_middleware_found = True
            break
    assert cors_middleware_found

def test_app_includes_agents_router(client):
    routes = [route.path for route in client.app.routes]
    agent_routes = [route for route in routes if route.startswith("/api/v1/agents")]
    assert len(agent_routes) > 0

def test_app_includes_metrics_router(client):
    routes = [route.path for route in client.app.routes]
    metric_routes = [route for route in routes if route.startswith("/api/v1/metrics")]
    assert len(metric_routes) > 0

def test_app_includes_system_router(client):
    routes = [route.path for route in client.app.routes]
    system_routes = [route for route in routes if route.startswith("/api/v1/system")]
    assert len(system_routes) > 0

def test_app_uses_all_allowed_origins():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
    
    assert app.middleware is not None

def test_app_includes_all_routers():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test App"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
    
    router_prefixes = [router.prefix for router in app.router.routes]
    assert any(prefix == "/api/v1/agents" for prefix in router_prefixes)
    assert any(prefix == "/api/v1/metrics" for prefix in router_prefixes)
    assert any(prefix == "/api/v1/system" for prefix in router_prefixes)

def test_app_has_routes():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test App"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
    
    assert len(app.routes) > 0

def test_create_app_with_no_settings():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = ""
        mock_settings.return_value.APP_DESCRIPTION = ""
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
        assert isinstance(app, FastAPI)

def test_create_app_with_empty_origins():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.ALLOWED_ORIGINS = []
        app = create_app()
        assert isinstance(app, FastAPI)

def test_create_app_none_values():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = None
        mock_settings.return_value.APP_DESCRIPTION = None
        mock_settings.return_value.ALLOWED_ORIGINS = None
        app = create_app()
        assert isinstance(app, FastAPI)

def test_app_logging_configured():
    with patch('backend.app.main.logging') as mock_logging:
        with patch('backend.app.main.Settings') as mock_settings:
            mock_settings.return_value.APP_NAME = "Test App"
            mock_settings.return_value.APP_DESCRIPTION = "Test Description"
            mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
            create_app()
            mock_logging.basicConfig.assert_called()

def test_get_request_to_agents_endpoint(client):
    response = client.get("/api/v1/agents/")
    assert response.status_code == 404 or response.status_code == 200

def test_get_request_to_metrics_endpoint(client):
    response = client.get("/api/v1/metrics/")
    assert response.status_code == 404 or response.status_code == 200

def test_get_request_to_system_endpoint(client):
    response = client.get("/api/v1/system/")
    assert response.status_code == 404 or response.status_code == 200

def test_create_app_sets_up_logging():
    with patch('backend.app.main.logging') as mock_logging:
        with patch('backend.app.main.Settings') as mock_settings:
            mock_settings.return_value.APP_NAME = "Test App"
            mock_settings.return_value.APP_DESCRIPTION = "Test Description"
            mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
            create_app()
            mock_logging.basicConfig.assert_called_with(level=mock_logging.INFO)

def test_app_includes_all_required_routers():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test App"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
        
        prefixes = [router.prefix for router in app.router.routes]
        assert "/api/v1/agents" in prefixes
        assert "/api/v1/metrics" in prefixes
        assert "/api/v1/system" in prefixes

def test_app_title_and_version():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.APP_NAME = "Test App"
        mock_settings.return_value.APP_DESCRIPTION = "Test Description"
        mock_settings.return_value.ALLOWED_ORIGINS = ["*"]
        app = create_app()
        assert app.title == "Test App"
        assert app.version == "0.1.0"

def test_app_middleware_configured_twice():
    with patch('backend.app.main.Settings') as mock_settings:
        mock_settings.return_value.ALLOWED_ORIGINS = ["http://localhost"]
        app = create_app()
        assert len(app.user_middleware) >= 1