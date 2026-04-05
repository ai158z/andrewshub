import os
from unittest.mock import patch
from src.skill_library.config.settings import Settings

def test_default_database_url():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.DATABASE_URL == "sqlite:///./skill_library.db"

def test_custom_database_url_from_env():
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost/db"}):
        settings = Settings()
        assert settings.DATABASE_URL == "postgresql://user:pass@localhost/db"

def test_default_secret_key():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.SECRET_KEY == "default_secret_key_for_development"

def test_custom_secret_key_from_env():
    with patch.dict(os.environ, {"SECRET_KEY": "custom_secret_key"}):
        settings = Settings()
        assert settings.SECRET_KEY == "custom_secret_key"

def test_default_redis_url():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.REDIS_URL == "redis://localhost:6379/0"

def test_custom_redis_url_from_env():
    with patch.dict(os.environ, {"REDIS_URL": "redis://custom:6380/1"}):
        settings = Settings()
        assert settings.REDIS_URL == "redis://custom:6380/1"

def test_default_debug_false():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.DEBUG is False

def test_debug_true_from_env():
    with patch.dict(os.environ, {"DEBUG": "true"}):
        settings = Settings()
        assert settings.DEBUG is True

def test_debug_false_from_env():
    with patch.dict(os.environ, {"DEBUG": "false"}):
        settings = Settings()
        assert settings.DEBUG is False

def test_debug_uppercase_true_from_env():
    with patch.dict(os.environ, {"DEBUG": "True"}):
        settings = Settings()
        assert settings.DEBUG is True

def test_default_log_level():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.LOG_LEVEL == "INFO"

def test_custom_log_level_from_env():
    with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
        settings = Settings()
        assert settings.LOG_LEVEL == "DEBUG"

def test_default_database_pool_size():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.DATABASE_POOL_SIZE == 10

def test_custom_database_pool_size_from_env():
    with patch.dict(os.environ, {"DATABASE_POOL_SIZE": "15"}):
        settings = Settings()
        assert settings.DATABASE_POOL_SIZE == 15

def test_default_database_max_overflow():
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.DATABASE_MAX_OVERFLOW == 20

def test_custom_database_max_overflow_from_env():
    with patch.dict(os.environ, {"DATABASE_MAX_OVERFLOW": "25"}):
        settings = Settings()
        assert settings.DATABASE_MAX_OVERFLOW == 25

def test_mixed_environment_variables():
    with patch.dict(os.environ, {
        "DATABASE_URL": "mysql://test:test@localhost/testdb",
        "SECRET_KEY": "test_key",
        "DEBUG": "true",
        "LOG_LEVEL": "ERROR",
        "DATABASE_POOL_SIZE": "5",
        "DATABASE_MAX_OVERFLOW": "10"
    }):
        settings = Settings()
        assert settings.DATABASE_URL == "mysql://test:test@localhost/testdb"
        assert settings.SECRET_KEY == "test_key"
        assert settings.DEBUG is True
        assert settings.LOG_LEVEL == "ERROR"
        assert settings.DATABASE_POOL_SIZE == 5
        assert settings.DATABASE_MAX_OVERFLOW == 10

def test_settings_config_env_file():
    settings = Settings()
    assert settings.Config.env_file == ".env"
    assert settings.Config.env_file_encoding == "utf-8"

def test_type_conversion_for_int_fields():
    with patch.dict(os.environ, {
        "DATABASE_POOL_SIZE": "invalid",
        "DATABASE_MAX_OVERFLOW": "invalid"
    }):
        try:
            Settings()
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "invalid literal" in str(e)