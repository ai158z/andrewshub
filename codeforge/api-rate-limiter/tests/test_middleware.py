from unittest.mock import patch, Mock
from flask import Flask, request, jsonify
import pytest

# Test fixtures
@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def mock_request():
    with patch('src.middleware.request') as mock_req:
        mock_req.environ = {}
        yield mock_req

# Test cases
def test_rate_limit_middleware_applies_before_request_hook(app):
    with patch('src.middleware.connect_to_redis') as mock_redis:
        from src.middleware import rate_limit_middleware
        rate_limit_middleware(app)
        assert hasattr(app, 'before_request_funcs')
        assert len(app.before_request_funcs[None]) > 0

def test_check_rate_limit_with_invalid_ip():
    with patch('src.middleware._get_client_ip', return_value=""):
        response = check_rate_limit(None)
        assert response is not None
        assert response[1] == 400

def test_check_rate_limit_rate_limited():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=True):
        response = check_rate_limit(None)
        assert response is not None
        assert response[1] == 429

def test_check_rate_limit_not_limited():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=False), \
         patch('src.middleware.increment_counter') as mock_increment:
        response = check_rate_limit(None)
        assert response is None
        mock_increment.assert_called_once()

def test_check_rate_limit_rate_limit_check_fails():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', side_effect=Exception("Redis error")):
        response = check_rate_limit(None)
        assert response is None

def test_get_client_ip_from_x_forwarded_for():
    mock_req = Mock()
    mock_req.environ = {'HTTP_X_FORWARDED_FOR': '192.168.1.1, 10.0.0.1'}
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == "192.168.1.1"

def test_get_client_ip_from_x_real_ip():
    mock_req = Mock()
    mock_req.environ = {'HTTP_X_REAL_IP': '192.168.1.2'}
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == "192.168.1.2"

def test_get_client_ip_from_remote_addr():
    mock_req = Mock()
    mock_req.environ = {'REMOTE_ADDR': '192.168.1.3'}
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == "192.168.1.3"

def test_get_client_ip_no_ip():
    mock_req = Mock()
    mock_req.environ = {}
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == ""

def test_check_rate_limit_normal_flow():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=False), \
         patch('src.middleware.increment_counter') as mock_increment, \
         patch('src.middleware.get_counter', return_value=5):
        response = check_rate_limit(None)
        assert response is None
        mock_increment.assert_called_once()

def test_check_rate_limit_exceeds_limit():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=True):
        response = check_rate_limit(None)
        assert response[1] == 429

def test_check_rate_limit_redis_error_handling():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', side_effect=Exception("Redis error")):
        response = check_rate_limit(None)
        assert response is None

def test_check_rate_limit_json_response_content():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=True):
        response = check_rate_limit(None)
        assert 'error' in response[0].get_json()
        assert response[1] == 429

def test_check_rate_limit_no_error_when_not_limited():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=False), \
         patch('src.middleware.increment_counter'):
        response = check_rate_limit(None)
        assert response is None

def test_get_client_ip_multiple_headers():
    mock_req = Mock()
    mock_req.environ = {
        'HTTP_X_FORWARDED_FOR': '192.168.1.1, 10.0.0.1',
        'HTTP_X_REAL_IP': '192.168.2.1',
        'REMOTE_ADDR': '192.168.3.1'
    }
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == "192.168.1.1"

def test_get_client_ip_fallback_chain():
    mock_req = Mock()
    mock_req.environ = {
        'HTTP_X_FORWARDED_FOR': None,
        'HTTP_X_REAL_IP': None,
        'REMOTE_ADDR': '192.168.3.3'
    }
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == "192.168.3.3"

def test_get_client_ip_fallback_to_x_real_ip():
    mock_req = Mock()
    mock_req.environ = {
        'HTTP_X_FORWARDED_FOR': None,
        'HTTP_X_REAL_IP': '192.168.2.2'
    }
    with patch('src.middleware.request', mock_req):
        from src.middleware import _get_client_ip
        ip = _get_client_ip(mock_req)
        assert ip == "192.168.2.2"

def test_rate_limit_middleware_redis_connection():
    with patch('src.middleware.connect_to_redis') as mock_redis:
        from src.middleware import rate_limit_middleware
        mock_app = Mock()
        rate_limit_middleware(mock_app)
        mock_redis.assert_called_once()

def test_check_rate_limit_empty_ip():
    with patch('src.middleware._get_client_ip', return_value=""), \
         patch('src.middleware.is_rate_limited'):
        response = check_rate_limit(None)
        assert response[1] == 400

def test_check_rate_limit_valid_ip_no_limit():
    with patch('src.middleware._get_client_ip', return_value="192.168.1.1"), \
         patch('src.middleware.is_rate_limited', return_value=False), \
         patch('src.middleware.increment_counter') as mock_increment:
        response = check_rate_limit(None)
        assert response is None
        mock_increment.assert_called_once_with("rate_limit:192.168.1.1")