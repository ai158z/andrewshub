import pytest
from flask import Flask
from unittest.mock import MagicMock, patch
import os

# Set up the Redis URL from environment variables
if 'REDIS_URL' in os.environ:
    REDIS_URL = os.environ['REDIS_URL']
else:
    raise EnvironmentError("REDIS_URL environment variable not set")

# Mocked imports for testing purposes
with patch('tests.conftest.rate_limiter'), \
     patch('tests.conftest.redis_client'), \
     patch('tests.conftest.middleware'), \
     patch('tests.conftest.endpoint_scanner'), \
     patch('tests.conftest.config.rate_limit_config'):

    rate_limiter = MagicMock()
    redis_client = MagicMock()
    middleware = MagicMock()
    endpoint_scanner = MagicMock()
    config = MagicMock()
    
    # Configure the mocks
    rate_limiter.is_rate_limited = MagicMock()
    redis_client.connect_to_redis = MagicMock()
    redis_client.increment_counter = MagicMock()
    redis_client.get_counter = MagicMock()
    middleware.rate_limit_middleware = MagicMock()
    middleware.check_rate_limit = MagicMock()
    endpoint_scanner.scan_endpoints = MagicMock()
    endpoint_scanner.register_endpoints = MagicMock()
    config.rate_limit_config.RATE_LIMIT = MagicMock()
    config.rate_limit_config.WINDOW_SIZE = MagicMock()
    config.rate_limit_config.EXPIRATION = MagicMock()

@pytest.fixture
def app():
    """Create a Flask app instance for testing with rate limiting."""
    app = Flask(__name__)
    
    # Configure the app for testing
    app.config['TESTING'] = True

    # Register a test endpoint
    @app.route('/test')
    def test_endpoint():
        return 'Test response'

    # Register a limited endpoint for testing
    @app.route('/limited')
    def limited_endpoint():
        return 'Limited endpoint response'

    return app

@pytest.fixture
def mock_redis(monkeypatch):
    """Mock the Redis connection for testing."""
    mock_redis_instance = MagicMock()
    mock_redis_instance.get_counter = MagicMock(return_value=0)
    mock_redis_instance.increment_counter = MagicMock()
    return mock_redis_instance

def pytest_configure():
    """Configure pytest with custom markers and settings."""
    pass  # Configuration is handled by pytest directly

@pytest.fixture
def mock_redis_connection(monkeypatch):
    """Mock the Redis connection for testing."""
    mock_redis_instance = MagicMock()
    mock_redis_instance.get_counter = MagicMock(return_value=0)
    mock_redis_instance.increment_counter = MagicMock()
    return mock_redis_instance

@pytest.fixture
def mock_rate_limiter(monkeypatch):
    """Mock the rate limiter functions for testing."""
    mock_is_limited = MagicMock(return_value=False)
    monkeypatch.setattr('rate_limiter.is_rate_limited', mock_is_limited)
    return mock_is_limited

@pytest.fixture
def mock_config(monkeypatch):
    """Mock the configuration values for testing."""
    mock_rate_limit = MagicMock(return_value=100)
    mock_window_size = MagicMock(return_value=60)
    mock_expiration = MagicMock(return_value=3600)
    return mock_rate_limit, mock_window_size, mock_expiration

@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()

# Mock data for testing
@pytest.fixture
def mock_data():
    """Provide mock data for testing."""
    return {
        'test_data_1': {'key': 'value1'},
        'test_data_2': {'key': 'value2'}
    }