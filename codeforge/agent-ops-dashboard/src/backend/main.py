import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the src directory to Python path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import after adding to path
from src.backend.api.agents import router as agent_router
from src.backend.api.metrics import router as metric_router

def create_app() -> FastAPI:
    app = FastAPI(title="Agent Ops Dashboard", version="0.1.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(agent_router, prefix="/api/agents", tags=["agents"])
    app.include_router(metric_router, prefix="/api/metrics", tags=["metrics"])
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
        
    return app

# Create the app instance
app = create_app()