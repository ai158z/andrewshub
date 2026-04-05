import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agent_dashboard")

def get_database_url() -> str:
    """Get the database URL from environment variables."""
    url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agent_dashboard")
    if not url:
        raise ValueError("DATABASE_URL environment variable is not set")
    if url == "":
        raise ValueError("DATABASE_URL environment variable is not set")
    return url

# Database configuration
engine = create_engine(
    get_database_url(),
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)