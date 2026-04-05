import os
from unittest import mock
from pydantic import ValidationError
import pytest
from backend.src.config import Settings


def test_settings_default_values():
    with mock.patch.dict(os.environ, clear=True):
        settings = Settings()
        assert settings.DATABASE_URL == "sqlite:///./staking.db"
        assert settings.REDIS_URL == "redis://localhost:6379"
        assert settings.SECRET_KEY == "change_me_in_production"
        assert settings.ALGORITHM == "HS256"
        assert settings.API_V1_STR == "/api/v1"
        assert settings.PROJECT_NAME == "Staking Reward Calculator"


def test_settings_from_env():
    env_vars = {
        "DATABASE_URL": "postgresql://user:pass@localhost/test",
        "REDIS_URL": "redis://example.com:6379",
        "SECRET_KEY": "test_secret_key",
        "COIN_GECKO_API_KEY": "test_api_key"
    }
    
    with mock.patch.dict(os.environ, env_vars):
        settings = Settings()
        assert settings.DATABASE_URL == "postgresql://user:pass@localhost/test"
        assert settings.REDIS_URL == "redis://example.com:6379"
        assert settings.SECRET_KEY == "test_secret_key"
        assert settings.COIN_GECKO_API_KEY == "test_api_key"


def test_cors_origins_string_conversion():
    settings = Settings()
    result = settings.assemble_cors_origins("http://example.com, https://test.com", None)
    assert result == ["http://example.com", "https://test.com"]


def test_cors_origins_list_unchanged():
    settings = Settings()
    origins = ["http://example.com", "https://test.com"]
    result = settings.assemble_cors_origins(origins, None)
    assert result == origins


def test_database_url_validator_with_empty_string():
    with pytest.raises(ValidationError):
        Settings(DATABASE_URL="")


def test_database_url_validator_with_valid_url():
    settings = Settings(DATABASE_URL="postgresql://localhost/test")
    assert settings.DATABASE_URL == "postgresql://localhost/test"


def test_access_token_expire_minutes_default():
    with mock.patch.dict(os.environ, clear=True):
        settings = Settings()
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30


def test_access_token_expire_minutes_from_env():
    with mock.patch.dict(os.environ, {"ACCESS_TOKEN_EXPIRE_MINUTES": "60"}):
        settings = Settings()
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60


def test_min_stake_amount_default():
    settings = Settings()
    assert settings.MIN_STAKE_AMOUNT == 1.0


def test_max_stake_duration_default():
    settings = Settings()
    assert settings.MAX_STAKE_DURATION_DAYS == 3650


def test_default_currency():
    settings = Settings()
    assert settings.DEFAULT_CURRENCY == "USD"


def test_case_sensitive_config():
    assert Settings.Config.case_sensitive is True


def test_project_name_default():
    settings = Settings()
    assert settings.PROJECT_NAME == "Staking Reward Calculator"


def test_coin_gecko_base_url_default():
    settings = Settings()
    assert settings.COIN_GECKO_BASE_URL == "https://api.coingecko.com/api/v3"


def test_coin_gecko_api_key_from_env():
    with mock.patch.dict(os.environ, {"COIN_GECKO_API_KEY": "test_key"}):
        settings = Settings()
        assert settings.COIN_GECKO_API_KEY == "test_key"


def test_database_pool_settings():
    settings = Settings()
    assert settings.DATABASE_POOL_SIZE == 10
    assert settings.DATABASE_MAX_OVERFLOW == 20


def test_cors_origins_default_empty():
    settings = Settings()
    assert settings.BACKEND_CORS_ORIGINS == []


def test_algorithm_default():
    settings = Settings()
    assert settings.ALGORITHM == "HS256"


def test_api_v1_str_default():
    settings = Settings()
    assert settings.API_V1_STR == "/api/v1"