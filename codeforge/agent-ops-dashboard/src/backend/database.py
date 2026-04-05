import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the SQLAlchemy engine
engine: Engine = None
if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "Session" class
SessionLocal = None
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to provide database session to FastAPI endpoints.
    
    Yields:
        Session: Database session
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
def init_db():
    """Initialize database tables"""
    try:
        from src.backend.models.agent import Agent
        from src.backend.models.metric import Metric
        if engine:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created/updated successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

# Initialize only if DATABASE_URL is set
if DATABASE_URL:
    # Call init_db to create tables
    init_db()