import os
from typing import Optional
from pydantic import validator
from pydantic.types import conint, constr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./staking.db")
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: conint(ge=1) = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: constr(min_length=1) = "Staking Reward Calculator"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = []
    
    # Chain API settings
    COIN_GECKO_API_KEY: Optional[str] = os.getenv("COIN_GECKO_API_KEY")
    COIN_GECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
    
    # Staking settings
    MIN_STAKE_AMOUNT: float = 1.0
    MAX_STAKE_DURATION_DAYS: int = 3650  # 10 years
    DEFAULT_CURRENCY: str = "USD"
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v

    class Config:
        case_sensitive = True


settings = Settings()