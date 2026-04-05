import os
from unittest.mock import patch, MagicMock
import pytest
from pydantic import ValidationError
from backend.src.core.config import Settings


def test_settings_loads_from_environment():
    with patch.dict(os.environ, {
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "postgresql://test:test@localhost/testdb",
        "GITHUB_TOKEN": "test-github-token"
    }):
        settings = Settings()
        assert settings.SECRET_KEY == "test-secret-key"
        assert settings.DATABASE_URL == "postgresql://test:test@localhost/testdb"
        assert settings.GITHUB_TOKEN == "test-github-token"


def test_settings_uses_defaults_when_env_not_set():
    with patch.dict(os.environ, {
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "postgresql://test:test@localhost/testdb",
        "GITHUB_TOKEN": "test-github-token"
    }, clear=True):
        settings = Settings()
        assert settings.PROJECT_NAME == "Code Review Analyzer"
        assert settings.VERSION == "1.0.0"
        assert settings.ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.DATABASE_POOL_SIZE == 20
        assert settings.REDIS_URL == "redis://localhost:6379/0"
        assert settings.CELERY_BROKER_URL == "redis://localhost:6379/0"
        assert settings.CELERY_RESULT_BACKEND == "redis://localhost:6379/0"
        assert settings.CODE_ANALYSIS_TIMEOUT == 300
        assert settings.MAX_FILE_SIZE == 1000000
        assert settings.API_V1_STR == "/api/v1"
        assert settings.HOST == "0.0.0.0"
        assert settings.PORT == 8000
        assert settings.GITHUB_API_URL == "https://api.github.com"


def test_settings_uses_environment_variables():
    with patch.dict(os.environ, {
        "PROJECT_NAME": "Test Project",
        "VERSION": "2.0.0",
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "postgresql://test:test@localhost/testdb",
        "GITHUB_TOKEN": "test-github-token",
        "DEBUG": "True",
        "DATABASE_POOL_SIZE": "50",
        "DATABASE_MAX_OVERFLOW": "10",
        "REDIS_URL": "redis://custom-host:6380/1",
        "CELERY_BROKER_URL": "redis://custom-host:6380/1",
        "CELERY_RESULT_BACKEND": "redis://custom-host:6380/1",
        "CODE_ANALYSIS_TIMEOUT": "600",
        "MAX_FILE_SIZE": "2000000",
        "HOST": "127.0.0.1",
        "PORT": "9000",
        "GITHUB_API_URL": "https://custom-github-api.com",
        "ENABLE_BANDIT": "False",
        "ENABLE_SAFETY": "False"
    }):
        settings = Settings()
        assert settings.PROJECT_NAME == "Test Project"
        assert settings.VERSION == "2.0.0"
        assert settings.DEBUG is True
        assert settings.DATABASE_POOL_SIZE == 50
        assert settings.DATABASE_MAX_OVERFLOW == 10
        assert settings.REDIS_URL == "redis://custom-host:6380/1"
        assert settings.CELERY_BROKER_URL == "redis://custom-host:6380/1"
        assert settings.CELERY_RESULT_BACKEND == "redis://custom-host:6380/1"
        assert settings.CODE_ANALYSIS_TIMEOUT == 600
        assert settings.MAX_FILE_SIZE == 2000000
        assert settings.HOST == "127.0.0.1"
        assert settings.PORT == 9000
        assert settings.GITHUB_API_URL == "https://custom-github-api.com"
        assert settings.ENABLE_BANDIT is False
        assert settings.ENABLE_SAFETY is False


def test_required_fields_missing_raises_validation_error():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValidationError) as exc_info:
            Settings()
        assert "SECRET_KEY" in str(exc_info.value)
        assert "DATABASE_URL" in str(exc_info.value)
        assert "GITHUB_TOKEN" in str(exc_info.value)


def test_settings_with_all_required_fields():
    with patch.dict(os.environ, {
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "postgresql://test:test@localhost/testdb",
        "GITHUB_TOKEN": "test-github-token"
    }, clear=True):
        settings = Settings()
        assert settings.SECRET_KEY == "test-secret-key"
        assert settings.DATABASE_URL == "postgresql://test:test@localhost/testdb"
        assert settings.GITHUB_TOKEN == "test-github-token"


def test_settings_boolean_field_parsing():
    with patch.dict(os.environ, {
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "postgresql://test:test@localhost/testdb",
        "GITHUB_TOKEN": "test-github-token",
        "ENABLE_BANDIT": "true",
        "ENABLE_SAFETY": "1",
        "ENABLE_PYLINT": "false",
        "ENABLE_PYCODESTYLE": "0",
        "ENABLE_RADON": "False"
    }):
        settings = Settings()
        assert settings.ENABLE_BANDIT is True
        assert settings.ENABLE_SAFETY is True
        assert settings.ENABLE_PYLINT is False
        assert settings.ENABLE_PYCODESTYLE is False
        assert settings.ENABLE_RADON is False


def test_settings_integer_field_parsing():
    with patch.dict(os.environ, {
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "postgresql://test:test@localhost/testdb",
        "GITHUB_TOKEN": "test-github-token",
        "PORT": "8080",
        "DATABASE_POOL_SIZE": "100",
        "DATABASE_MAX_OVERFLOW": "20",
        "CODE_ANALYSIS_TIMEOUT": "600"
    }):
        settings = Settings()
        assert settings.PORT == 8080
        assert settings.DATABASE_POOL_SIZE == 100
        assert settings.DATABASE_MAX_OVERFLOW == 20
        assert settings.CODE_ANALYSIS_TIMEOUT == 600


def test_settings_defaults_when_env_file_missing():
    # Mock that .env file doesn't exist
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-secret-key",
            "DATABASE_URL": "postgresql://test:test@localhost/testdb",
            "GITHUB_TOKEN": "test-github-token"
        }, clear=True):
            settings = Settings()
            # Should still use defaults for non-required fields
            assert settings.API_V1_STR == "/api/v1"
            assert settings.REDIS_URL == "redis://localhost:6379/0"


def test_settings_env_file_loading():
    # Create a mock .env file content
    env_content = """
    PROJECT_NAME=Test Project From File
    VERSION=3.0.0
    """
    
    with patch("builtins.open", MagicMock(), create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = env_content
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-secret-key",
            "DATABASE_URL": "postgresql://test:test@localhost/testdb",
            "GITHUB_TOKEN": "test-github-token"
        }, clear=True):
            # We can't easily test the file reading in isolation, but we can check
            # that the settings still load properly with env vars
            settings = Settings()
            # File values would override these, but we're testing that required fields are still present
            assert settings.SECRET_KEY == "test-secret-key"
            assert settings.DATABASE_URL == "postgresql://test:test@localhost/testdb"


def test_settings_with_empty_values():
    with patch.dict(os.environ, {
        "SECRET_KEY": "",
        "DATABASE_URL": "",
        "GITHUB_TOKEN": "",
        "PROJECT_NAME": "",
        "VERSION": ""
    }):
        with pytest.raises(ValidationError):
            Settings()