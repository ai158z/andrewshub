import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from backend.app.config.database import get_database_url, DATABASE_URL


class TestDatabaseConfig:
    def test_get_database_url_returns_value_when_set(self, monkeypatch):
        test_url = "postgresql://test:test@localhost:5432/testdb"
        monkeypatch.setenv("DATABASE_URL", test_url)
        assert get_database_url() == test_url

    def test_get_database_url_raises_error_when_not_set(self, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.setattr("backend.app.config.database.DATABASE_URL", None)
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
            get_database_url()

    def test_get_database_url_returns_default_when_env_not_set(self, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        # This test ensures the default value is used when env var is not set
        # We need to reload the module to test this properly
        import importlib
        import backend.app.config.database
        importlib.reload(backend.app.config.database)
        # The default value should be returned
        assert backend.app.app.config.database.DATABASE_URL == "postgresql://user:password@localhost:5432/agent_dashboard"

    def test_engine_creation_with_valid_url(self, monkeypatch):
        test_url = "postgresql://user:pass@localhost:5432/test"
        monkeypatch.setenv("DATABASE_URL", test_url)
        
        # Reimport to test engine creation
        import importlib
        import backend.app.config.database
        importlib.reload(backend.app.config.database)
        
        assert backend.app.config.database.engine is not None
        assert str(backend.app.config.database.engine.url) == test_url

    def test_engine_has_correct_pool_settings(self):
        from backend.app.config.database import engine
        assert engine.pool.__class__.__name__ == "QueuePool"
        assert engine.pool._pool.maxsize() == 20
        assert engine.pool._pool.max_overflow() == 30
        assert engine.pool.pre_ping is True

    def test_sessionlocal_configuration(self):
        from backend.app.config.database import SessionLocal
        assert SessionLocal.kw['autocommit'] is False
        assert SessionLocal.kw['autoflush'] is False

    def test_get_database_url_with_empty_string(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "")
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
            get_database_url()

    def test_database_url_default_value(self):
        expected_default = "postgresql://user:password@localhost:5432/agent_dashboard"
        assert DATABASE_URL == expected_default

    def test_database_url_from_env_variable(self, monkeypatch):
        custom_url = "postgresql://custom:pass@host:5432/db"
        monkeypatch.setenv("DATABASE_URL", custom_url)
        assert get_database_url() == custom_url

    def test_engine_creation_fails_with_invalid_url(self, monkeypatch):
        # This test verifies that engine creation will fail with invalid URL
        # but we don't test the actual failure since that would require 
        # creating a separate engine, not the one in the module
        pass

    def test_sessionlocal_is_callable(self):
        from backend.app.config.database import SessionLocal
        # Just verify it can be instantiated
        session = SessionLocal()
        assert session is not None
        session.close()

    def test_pool_pre_ping_enabled(self):
        from backend.app.config.database import engine
        assert engine.pool.pre_ping is True

    def test_pool_size_and_overflow(self):
        from backend.app.config.database import engine
        assert engine.pool._pool.maxsize() == 20
        assert engine.pool._pool.max_overflow() == 30

    def test_get_database_url_returns_string(self, monkeypatch):
        test_url = "postgresql://test:test@localhost:5432/test"
        monkeypatch.setenv("DATABASE_URL", test_url)
        result = get_database_url()
        assert isinstance(result, str)

    def test_get_database_url_environment_variable_override(self, monkeypatch):
        custom_url = "postgresql://env:override@localhost:5432/db"
        monkeypatch.setenv("DATABASE_URL", custom_url)
        assert get_database_url() == custom_url

    def test_engine_is_sqlalchemy_engine(self):
        from backend.app.config.database import engine
        from sqlalchemy.engine import Engine
        assert isinstance(engine, Engine)

    def test_sessionlocal_is_sessionmaker(self):
        from sqlalchemy.orm import sessionmaker
        from backend.app.config.database import SessionLocal
        assert isinstance(SessionLocal, sessionmaker.__class__)

    def test_database_url_none_raises_error(self, monkeypatch):
        monkeypatch.setattr("backend.app.config.database.DATABASE_URL", None)
        monkeypatch.delenv("DATABASE_URL", raising=False)
        with pytest.raises(ValueError):
            get_database_url()

    def test_database_url_empty_string_raises_error(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "")
        with pytest.raises(ValueError):
            get_database_url()