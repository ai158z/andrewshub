import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings.sources import EnvSettingsSource


class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = Field(default="Code Review Analyzer")
    DEBUG: bool = Field(default=False)
    VERSION: str = Field(default="1.0.0")
    
    # Security settings
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Database settings
    DATABASE_URL: str = Field(...)
    DATABASE_POOL_SIZE: int = Field(default=20)
    DATABASE_MAX_OVERFLOW: int = Field(default=0)
    
    # Redis settings
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # GitHub settings
    GITHUB_TOKEN: str = Field(...)
    
    # Celery settings
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")
    
    # Analysis settings
    CODE_ANALYSIS_TIMEOUT: int = Field(default=300)
    MAX_FILE_SIZE: int = Field(default=1000000)
    
    # API settings
    API_V1_STR: str = Field(default="/api/v1")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # External service settings
    GITHUB_API_URL: str = Field(default="https://api.github.com")
    
    # Analysis tools configuration
    ENABLE_BANDIT: bool = Field(default=True)
    ENABLE_SAFETY: bool = Field(default=True)
    ENABLE_PYLINT: bool = Field(default=True)
    ENABLE_PYCODESTYLE: bool = Field(default=True)
    ENABLE_RADON: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Only create the settings instance when environment variables are available
# This prevents the ValidationError during import when required fields are missing
settings = None
if os.environ.get('SECRET_KEY') and os.environ.get('DATABASE_URL') and os.environ.get('GITHUB_TOKEN'):
    settings = Settings()