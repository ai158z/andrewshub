import os
from typing import List
from pydantic import validator
from typing import Optional
import logging

# Try to import BaseSettings from pydantic_settings first (for Pydantic v2)
# If that fails, fall back to pydantic v1
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALLOWED_ORIGINS: List[str] = ["*"]  # type: ignore
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agent_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "test")
    API_KEY_NAME: str = os.getenv("API_KEY_NAME", "X-API-KEY")
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    DATABASE_ECHO: bool = False
    DATABASE_POOL_RECYCLES: int = 5
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 0
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "agent_db")
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://user:password@localhost:5432/agent_db")
    
    # Redis configuration
    REDIS_OM: str = os.getenv("REDIS_OM", "standalone")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_USER: str = os.getenv("REDIS_USER", "user")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "password")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"