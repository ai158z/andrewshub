import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from backend.app.config.settings import Settings

def test_settings_default_secret_key():
    settings = Settings()
    assert settings.SECRET_KEY == "supersecret"

def test_settings_default_agent_api_key():
    settings = Settings()
    assert settings.AGENT_API_KEY == "test"

def test_settings_default_debug():
    settings = Settings()
    assert not settings.DEBUG

def test_settings_default_database_url():
    settings = Settings()
    assert settings.DATABASE_URL == "postgresql://user:password@localhost:5432/agent_db"

def test_settings_default_redis_url():
    settings = Settings()
    assert settings.REDIS_URL == "redis://localhost:6379/0"

def test_settings_default_redis_om():
    settings = Settings()
    assert settings.REDIS_OM == "standalone"

def test_settings_default_redis_host():
    settings = Settings()
    assert settings.REDIS_HOST == "localhost"

def test_settings_default_redis_port():
    settings = Settings()
    assert settings.REDIS_PORT == 6379

def test_settings_default_redis_db():
    settings = Settings()
    assert settings.REDIS_DB == 0

def test_settings_default_redis_user():
    settings = Settings()
    assert settings.REDIS_USER == "user"

def test_settings_default_redis_password():
    settings = Settings()
    assert settings.REDIS_PASSWORD == "password"

def test_settings_default_postgres_user():
    settings = Settings()
    assert settings.POSTGRES_USER == "user"

def test_settings_default_postgres_password():
    settings = Settings()
    assert settings.POSTGRES_PASSWORD == "password"

def test_settings_default_postgres_server():
    settings = Settings()
    assert settings.POSTGRES_SERVER == "localhost"

def test_settings_default_postgres_port():
    settings = Settings()
    assert settings.POSTGRES_PORT == 5432

def test_settings_default_postgres_db():
    settings = Settings()
    assert settings.POSTGRES_DB == "agent_db"

def test_settings_default_sqlalchemy_database_url():
    settings = Settings()
    assert settings.SQLALCHEMY_DATABASE_URL == "postgresql://user:password@localhost:5432/agent_db"

def test_settings_environment_variable_override(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "testkey")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")
    
    settings = Settings()
    
    assert settings.SECRET_KEY == "testkey"
    assert settings.DATABASE_URL == "postgresql://test:test@localhost:5432/test_db"

def test_settings_default_log_level():
    settings = Settings()
    assert settings.LOG_LEVEL == "INFO"

def test_settings_default_database_echo():
    settings = Settings()
    assert not settings.DATABASE_ECHO

def test_settings_default_database_pool_recycles():
    settings = Settings()
    assert settings.DATABASE_POOL_RECYCLES == 5

def test_settings_default_database_pool_size():
    settings = Settings()
    assert settings.DATABASE_POOL_SIZE == 10

def test_settings_default_database_max_overflow():
    settings = Settings()
    assert settings.DATABASE_MAX_OVERFLOW == 0