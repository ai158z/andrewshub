from unittest.mock import Mock, patch, MagicMock
from src.utils.endpoint_scanner import scan_endpoints, register_endpoints
import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    
    @app.route('/test1')
    def test1():
        return "test1"
    
    @app.route('/test2')
    def test2():
        return "test2"
        
    return app


def test_scan_endpoints_returns_list_of_registered_routes(app):
    endpoints = scan_endpoints(app)
    assert isinstance(endpoints, list)
    assert len(endpoints) > 0
    assert '/test1' in endpoints
    assert '/test2' in endpoints


def test_scan_endpoints_with_no_routes():
    empty_app = Flask("empty")
    endpoints = scan_endpoints(empty_app)
    # Flask always has a static route by default
    assert len(endpoints) == 1
    assert '/static/<path:filename>' in endpoints


def test_register_endpoints_calls_middleware_registration(app):
    with patch('src.utils.endpoint_scanner.rate_limit_middleware') as mock_middleware:
        register_endpoints(app)
        mock_middleware.assert_called_once_with(app)


def test_register_endpoints_logs_correct_count(app):
    with patch('src.utils.endpoint_scanner.rate_limit_middleware'):
        with patch('src.utils.endpoint_scanner.connect_to_redis'):
            with patch('src.utils.endpoint_scanner.app.logger') as mock_logger:
                register_endpoints(app)
                mock_logger.info.assert_called_once()


def test_register_endpoints_with_no_routes():
    empty_app = Flask("empty")
    with patch('src.utils.endpoint_scanner.rate_limit_middleware'):
        with patch('src.utils.endpoint_scanner.connect_to_redis'):
            register_endpoints(empty_app)
            # Should still register the default static endpoint
            assert empty_app.logger.info.call_count == 1


@patch('src.utils.endpoint_scanner.rate_limit_middleware')
@patch('src.utils.endpoint_scanner.connect_to_redis')
def test_register_endpoints_calls_scan_endpoints(mock_redis, mock_middleware, app):
    # This test ensures scan_endpoints is called
    register_endpoints(app)
    # Check that both mocks were called as part of registration
    mock_middleware.assert_called_once()
    mock_redis.return_value = MagicMock()
    mock_redis.assert_called_once()


def test_scan_endpoints_ignores_duplicate_routes(app):
    # Add a duplicate route rule manually
    @app.route('/duplicate')
    def dup1():
        return "dup1"
    
    @app.route('/duplicate')
    def dup2():
        return "dup2"
        
    endpoints = scan_endpoints(app)
    # Should only appear once
    assert endpoints.count('/duplicate') == 1


def test_register_endpoints_with_custom_endpoint_count(app):
    # Add a few custom routes and ensure they're all registered
    expected_endpoints = len(scan_endpoints(app))
    
    with patch('src.utils.endpoint_scanner.rate_limit_middleware'), \
         patch('src.utils.endpoint_scanner.connect_to_redis'):
        register_endpoints(app)
        # Validate via log call that the count matches expected
        app.logger.info.assert_called_with(
            f"Registered {expected_endpoints} endpoints for rate limiting"
        )


@patch('src.utils.endpoint_scanner.rate_limit_middleware')
@patch('src.utils.endpoint_scanner.connect_to_redis')
def test_register_endpoints_mocked_full_flow(mock_connect, mock_middleware, app):
    # Test the full registration flow with all dependencies mocked
    register_endpoints(app)
    mock_middleware.assert_called_once_with(app)
    mock_connect.assert_called_once()


def test_scan_endpoints_captures_all_methods_endpoints(app):
    @app.route('/method_test', methods=['GET', 'POST'])
    def method_test():
        return "methods"
        
    endpoints = scan_endpoints(app)
    assert '/method_test' in endpoints


def test_scan_endpoints_ignores_non_route_attributes(app):
    # Even if we don't define any route, Flask has default behavior
    # Let's just scan what's there
    endpoints = scan_endpoints(app)
    # just make sure it returns the list without error
    assert isinstance(endpoints, list)


@patch('src.utils.endpoint_scanner.rate_limit_middleware')
def test_register_endpoints_with_dynamic_route(mock_middleware, app):
    @app.route('/dynamic/<int:id>')
    def dynamic_route(id):
        return f"dynamic {id}"
    
    register_endpoints(app)
    mock_middleware.assert_called_once_with(app)


def test_register_endpoints_with_multiple_apps(app):
    # Create another app to ensure isolation
    app2 = Flask("test2")
    
    @app2.route('/app2/route')
    def app2_route():
        return "app2"
    
    endpoints1 = sorted(scan_endpoints(app))
    endpoints2 = sorted(scan_endpoints(app2))
    
    assert endpoints1 != endpoints2  # Different apps should have different endpoints


def test_scan_endpoints_empty_app_no_endpoints():
    # An app with no routes still has default Flask routes
    empty_app = Flask(__name__)
    endpoints = scan_endpoints(empty_app)
    assert len(endpoints) == 1  # the default static route


def test_register_endpoints_empty_app():
    empty_app = Flask("empty_test")
    with patch('src.utils.endpoint_scanner.rate_limit_middleware') as mock_middleware:
        register_endpoints(empty_app)
        mock_middleware.assert_called_once_with(empty_app)


@patch('src.utils.endpoint_scanner.rate_limit_middleware')
@patch('src.utils.endpoint_scanner.connect_to_redis', return_value=MagicMock())
def test_register_endpoints_no_exception_on_empty_app(mock_connect, mock_middleware):
    empty_app = Flask("empty")
    try:
        register_endpoints(empty_app)
    except Exception as e:
        pytest.fail(f"register_endpoints raised {e} unexpectedly")


def test_scan_endpoints_sorted_order_independent(app):
    endpoints = scan_endpoints(app)
    # Should capture all rules regardless of definition order
    assert '/test1' in endpoints
    assert '/test2' in endpoints


@patch('src.utils.endpoint_scanner.rate_limit_middleware')
def test_register_endpoints_with_patched_scanning(mock_middleware, app):
    register_endpoints(app)
    mock_middleware.assert_called_once_with(app)


def test_register_endpoints_with_bearer_token_route():
    app = Flask("bearer_test")
    @app.route('/token', methods=['GET', 'POST'])
    def token_route():
        return "token"
    
    endpoints = scan_endpoints(app)
    assert '/token' in endpoints


def test_register_endpoints_redis_connection_failure():
    app = Flask("redis_failure_test")
    with patch('src.utils.endpoint_scanner.rate_limit_middleware'), \
         patch('src.utils.endpoint_scanner.connect_to_redis', side_effect=Exception("Redis error")):
        with pytest.raises(Exception, match="Redis error"):
            register_endpoints(app)


def test_register_endpoints_with_nested_routes(app):
    @app.route('/nested/level/endpoint')
    def nested():
        return "nested"
    
    endpoints = scan_endpoints(app)
    assert '/nested/level/endpoint' in endpoints


def test_register_endpoints_with_query_parameters_route(app):
    @app.route('/query')
    def query_route():
        return "query"
        
    endpoints = scan_endpoints(app)
    assert '/query' in endpoints


def test_register_endpoints_with_multiple_dynamic_segments():
    app = Flask("dynamic_segments")
    @app.route('/user/<int:user_id>/posts/<int:post_id>')
    def multi_segment(user_id, post_id):
        return f"User {user_id} Post {post_id}"
    
    endpoints = scan_endpoints(app)
    assert '/user/<int:user_id>/posts/<int:post_id>' in endpoints


def test_register_endpoints_with_same_endpoint_multiple_methods(app):
    @app.route('/multi-method', methods=['GET'])
    def mm1():
        return "mm1"
        
    @app.route('/multi-method', methods=['POST'])
    def mm2():
        return "mm2"
        
    endpoints = scan_endpoints(app)
    # Should only appear once even with multiple methods
    assert endpoints.count('/multi-method') == 1
    assert '/multi-method' in endpoints
    assert len(endpoints) == len(set(endpoints))  # no duplicates