import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.main import create_app, run_app

@patch('src.main.connect_to_redis')
@patch('src.main.register_endpoints')
@patch('src.main.rate_limit_middleware')
def test_create_app_success(mock_rate_limit, mock_register, mock_redis):
    mock_redis.return_value = MagicMock()
    app = create_app()
    assert isinstance(app, Flask)
    assert mock_redis.called
    assert mock_register.called
    assert mock_rate_limit.called

@patch('src.main.connect_to_redis')
@patch('src.main.register_endpoints')
@patch('src.main.rate_limit_middleware')
def test_create_app_redis_failure(mock_rate_limit, mock_register, mock_redis):
    mock_redis.return_value = None
    with pytest.raises(Exception, match="Failed to connect to Redis"):
        create_app()
    assert mock_redis.called
    assert not mock_register.called
    assert not mock_rate_limit.called

@patch('src.main.connect_to_redis')
@patch('src.main.register_endpoints')
@patch('src.main.rate_limit_middleware')
def test_health_check_endpoint(mock_rate_limit, mock_register, mock_redis):
    mock_redis.return_value = MagicMock()
    app = create_app()
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'healthy'}

@patch('src.main.connect_to_redis')
def test_app_creation_calls_all_dependencies(mock_redis):
    mock_redis_client = MagicMock()
    mock_redis.return_value = mock_redis_client
    app = create_app()
    assert mock_redis.called

@patch('src.main.connect_to_redis')
def test_redis_connection_error_cascades(mock_redis):
    mock_redis.return_value = None
    with pytest.raises(Exception):
        create_app()

@patch.dict(os.environ, {'HOST': '0.0.0.0', 'PORT': '5000', 'DEBUG': 'False'})
@patch('src.main.create_app')
def test_run_app_with_env_vars(mock_create_app):
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app
    run_app()
    mock_create_app.assert_called_once()

@patch.dict(os.environ, {})
@patch('src.main.create_app')
def test_run_app_default_values(mock_create_app):
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app
    run_app()
    mock_app.run.assert_called_once_with(
        host='0.0.0.0',
        port=5000,
        debug=False
    )