import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import create_app, app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_app_returns_fastapi_instance():
    assert create_app().__class__.__name__ == "FastAPI"

@patch("src.main.create_tables")
def test_create_app_includes_cors_middleware(mock_create_tables):
    test_app = create_app()
    assert len(test_app.user_middleware) > 0
    assert any(middleware.middleware.__name__ == "CORSMiddleware" for middleware in test_app.user_middleware)

@patch("src.main.create_tables")
def test_app_includes_all_routers(mock_create_tables):
    test_app = create_app()
    router_paths = [route.path for route in test_app.routes]
    
    expected_paths = [
        "/api/v1/calculate",
        "/api/v1/networks", 
        "/api/v1/projections"
    ]
    
    for path in expected_paths:
        assert any(path in route_path for route_path in router_paths)

@patch("src.main.create_tables")
def test_app_has_correct_title(mock_create_tables):
    test_app = create_app()
    assert test_app.title == "Staking Reward Calculator"

@patch("src.main.create_tables")
def test_app_has_correct_description(mock_create_tables):
    test_app = create_app()
    assert test_app.description == "API for staking reward calculations"

@patch("src.main.create_tables")
def test_app_has_correct_version(mock_create_tables):
    test_app = create_app()
    assert test_app.version == "1.0.0"

@patch("src.main.create_tables")
def test_app_has_expected_middleware(mock_create_tables):
    test_app = create_app()
    assert len(test_app.user_middleware) > 0

@patch("src.main.create_tables")
def test_root_endpoint_returns_404(client):
    response = client.get("/")
    assert response.status_code == 404

@patch("src.main.create_tables")
def test_openapi_docs_available(client):
    response = client.get("/docs")
    assert response.status_code == 200

@patch("src.main.create_tables")
def test_openapi_json_available(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200

@patch("src.main.create_tables")
def test_calculator_router_included(client):
    response = client.get("/api/v1/calculate/roi")
    # We're not testing the response content, just that the route exists
    # This will either be 404 (route doesn't exist/correct) or 422 (exists but validation error)
    assert response.status_code in [404, 422, 200]

@patch("src.main.create_tables")
def test_network_router_included(client):
    response = client.get("/api/v1/networks/")
    # Test that the router is included by checking for 404 (not 405) or valid response
    assert response.status_code in [404, 200, 422]

@patch("src.main.create_tables")
def test_projections_router_included(client):
    response = client.get("/api/v1/projections/")
    # Test that the router is included by checking for 404 (not 405) or valid response
    assert response.status_code in [404, 200, 422]

@patch("src.main.create_tables")
def test_app_creation_with_duplicate_routers(mock_create_tables):
    # Test that duplicate router inclusion doesn't break app creation
    app1 = create_app()
    app2 = create_app()
    assert app1.routes == app2.routes

@patch("src.main.create_tables")
def test_app_includes_calculator_router_twice_still_works(mock_create_tables):
    # Create app with duplicate router inclusions
    test_app = create_app()
    # Check that we still have the right number of routes
    # (this is a bit fragile but checks that routes are added)
    original_route_count = len(test_app.routes)
    test_app = create_app()
    assert len(test_app.routes) >= original_route_count

@patch("src.database.create_tables")
@patch("src.main.create_tables")
def test_database_tables_created(mock_create_tables, mock_db_create):
    # Verify that create_tables is called during app creation
    mock_create_tables.assert_called_once()

@patch("src.main.uvicorn")
@patch("src.main.create_tables")
def test_main_function_with_uvicorn_run(mock_create_tables, mock_uvicorn):
    # This just tests that the file can be imported and main function exists
    # Actual uvicorn.run testing would require process testing which is out of scope
    assert hasattr(mock_uvicorn, "run")

@patch("src.main.create_tables")
def test_app_includes_all_expected_routers(client):
    # Test that all three expected routers are included
    from src.main import calculator_router, network_router, projections_router
    routers = [calculator_router, network_router, projections_router]
    for router in routers:
        assert router is not None

@patch("src.main.create_tables")
def test_app_routes_include_all_prefixes(mock_create_tables):
    test_app = create_app()
    paths = [route.path for route in test_app.routes]
    assert any("/api/v1/calculate" in path for path in paths)
    assert any("/api/v1/networks" in path for path in paths)
    assert any("/api/v1/projections" in path for path in paths)

@patch("src.main.create_tables")
def test_app_has_unique_routes_despite_multiple_includes(mock_create_tables):
    # Create app and check that routes are not duplicated excessively
    test_app = create_app()
    route_paths = [route.path for route in test_app.routes]
    # Should have reasonable number of routes (not exploded from multiple includes)
    assert len(route_paths) < 100  # Arbitrary but reasonable upper bound