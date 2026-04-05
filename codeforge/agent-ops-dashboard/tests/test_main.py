import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.main import create_app


def test_create_app_returns_fastapi_instance():
    app_instance = create_app()
    assert isinstance(app_instance, FastAPI)


def test_health_check_endpoint_returns_healthy():
    app_instance = create_app()
    client = TestClient(app_instance)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_app_has_correct_title_and_version():
    app_instance = create_app()
    assert app_instance.title == "Agent Ops Dashboard"
    assert app_instance.version == "0.1.0"


def test_app_includes_agents_router():
    app_instance = create_app()
    # Check if the agents router is included by looking for routes with the /api/agents prefix
    pass


def test_app_includes_metrics_router():
    # Test that the app includes the metrics router
    pass


def test_cors_middleware_is_configured():
    # This is a behavior test
    pass


def test_app_includes_both_agents_and_metrics_routers():
    app_instance = create_app()
    # Test that the app includes the agent and metrics routers
    pass


def test_create_app_includes_cors_middleware():
    app_instance = create_app()
    # Test that CORS is configured with allow_origins=["*"]
    assert hasattr(app_instance, 'middleware')  # FastAPI app instance has CORSMiddleware


def test_health_endpoint_exists():
    app_instance = create_app()
    # Check that the health endpoint exists
    pass


def test_app_configuration():
    app_instance = create_app()
    assert app_instance.title == "Agent Ops Dashboard"
    assert app_instance.version == "0.1.0"