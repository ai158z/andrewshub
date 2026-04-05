import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from skill_library.core.skill import Skill
from skill_library.core.domain import Domain
from skill_library.core.complexity import Complexity
from skill_library.core.utility import Utility
from skill_library.models.predictive_scoring import PredictiveScoringModel
from skill_library.models.curiosity_budget import CuriosityBudget
from skill_library.models.task_scoring_model import TaskScoringModel
from skill_library.storage.vector_db import VectorDB
from skill_library.storage.skill_repository import SkillRepository
from skill_library.integrations.memory_system import MemorySystem
from skill_library.integrations.pytorch_integration import PyTorchIntegration
from skill_library.api.skill_endpoints import router as skill_router
from skill_library.api.task_endpoints import router as task_router
from skill_library.config.settings import Settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state for app dependencies
class AppState:
    def __init__(self):
        self.skill_repo = None
        self.vector_db = None
        self.predictive_model = None
        self.task_scorer = None
        self.curiosity_budget = None
        self.pytorch_integration = None
        self.memory_system = None

# Lifespan manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    logger.info("Initializing application...")
    
    # Initialize core components
    settings = Settings()
    
    # Initialize database
    try:
                engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        app.state.app_state = AppState()
        app.state.app_state.skill_repo = SkillRepository(SessionLocal)
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    
    # Initialize other components
    app.state.app_state.vector_db = VectorDB()
    app.state.app_state.predictive_model = PredictiveScoringModel()
    app.state.app_state.task_scorer = TaskScoringModel()
    app.state.app_state.curiosity_budget = CuriosityBudget()
    app.state.app_state.pytorch_integration = PyTorchIntegration()
    app.state.app_state.memory_system = MemorySystem()
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Import FastAPI components
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create FastAPI app
app = FastAPI(
    title="Skill Library Framework API",
    description="API for skill-based task evaluation and management",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(skill_router)
app.include_router(task_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Skill Library Framework API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Dependency injection for app state
def get_app_state():
    return app.state.app_state

# Error handlers
from fastapi import status
from fastapi.encoders import jsonable_encoder

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )