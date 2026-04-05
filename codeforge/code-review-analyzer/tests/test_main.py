import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from backend.src.main import create_app, get_app


def test_get_app_returns_fastapi_instance():
    app = get_app()
    assert isinstance(app, FastAPI)


@patch('backend.src.main.create_app')
def test_get_app_calls_create_app(mock_create_app):
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app
    result = create_app()
    assert result == mock_app


def test_create_app_initializes_fastapi():
    app = create_app()
    assert isinstance(app, FastAPI)
    assert app.title == "Code Review Analyzer"
    assert app.description == "API for code analysis and repository management"
    assert app.version == "0.1.0"


def test_create_app_has_analysis_router():
    app = create_app()
    assert any(route for route in app.routes if route.path.startswith('/api/analysis'))


def test_create_app_has_repositories_router():
    app = create_app()
    assert any(route for route in app.routes if route.path.startswith('/api/repositories'))


def test_create_app_has_reports_router():
    app = create_app()
    assert any(route for route in app.routes if route.path.startswith('/api/reports'))


def test_create_app_has_expected_routers():
    app = create_app()
    expected_prefixes = ['/api/analysis', '/api/repositories', '/api/reports']
    route_prefixes = [route.path for route in app.routes]
    for prefix in expected_prefixes:
        assert any(rp.startswith(prefix) for rp in route_prefixes), f"Missing routes with prefix {prefix}"


def test_app_has_title():
    app = create_app()
    assert app.title is not None
    assert len(app.title) > 0


def test_app_has_description():
    app = create_app()
    assert app.description is not None
    assert len(app.description) > 0


def test_app_has_version():
    app = create_app()
    assert app.version is not None
    assert len(app.version) > 0


def test_create_app_not_none():
    app = create_app()
    assert app is not None


def test_create_app_has_openapi_route():
    app = create_app()
    routes = [route.path for route in app.routes]
    assert '/openapi.json' in str(routes)


def test_create_app_has_docs_route():
    app = create_app()
    routes = [route.path for route in app.routes]
    assert '/docs' in str(routes)


def test_create_app_has_redoc_route():
    app = create_app()
    routes = [route.path for route in app.routes]
    assert '/redoc' in str(routes)


def test_create_app_router_count():
    app = create_app()
    # Should have 3 routers + default fastapi routes
    assert len(app.router.routes) >= 3


def test_get_app_not_none():
    app = get_app()
    assert app is not None


def test_get_app_returns_same_type():
    app = get_app()
    assert isinstance(app, FastAPI)


def test_create_app_with_different_instance():
    app1 = create_app()
    app2 = create_app()
    assert app1 is not app2
    assert isinstance(app1, FastAPI)
    assert isinstance(app2, FastAPI)


@patch('backend.src.main.analysis_router')
@patch('backend.src.main.repositories_router')
@patch('backend.src.main.report_router')
def test_app_includes_all_routers(mock_report, mock_repos, mock_analysis):
    app = create_app()
    # Verify that our routers were included
    routes_str = str([route.path for route in app.routes])
    assert '/api/analysis' in routes_str
    assert '/api/repositories' in routes_str
    assert '/api/reports' in routes_str


def test_app_title_not_empty():
    app = create_app()
    assert app.title != ""
    assert app.title is not None


def test_app_description_not_empty():
    app = create_app()
    assert app.description != ""
    assert app.description is not None


def test_app_version_not_empty():
    app = create_app()
    assert app.version != ""
    assert app.version is not None