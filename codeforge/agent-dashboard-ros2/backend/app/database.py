import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator

# Database connection configuration
DEFAULT_DATABASE_URL = "postgresql://user:password@localhost:5432/agent_dashboard"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

def get_database_url():
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

def get_db() -> Generator[Session, None, None]:
    """Dependency to get a database session for FastAPI endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()