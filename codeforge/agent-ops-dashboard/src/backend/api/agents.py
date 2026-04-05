from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import os
import logging

from src.backend.database import get_db
from src.backend.models.agent import Agent as AgentModel
from src.backend.models.metric import Metric as MetricModel
from src.backend.schemas.agent import AgentCreate, Agent
from src.backend.schemas.metric import MetricCreate

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get Redis URL from environment variable
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
def register_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """
    Register a new agent
    """
    try:
        # Create new agent instance
        db_agent = AgentModel(
            agent_id=agent.agent_id,
            name=agent.name,
            status=agent.status,
        )
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        logger.info(f"Agent registered: {agent.agent_id}")
        return db_agent
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering agent: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{agent_id}/status")
def update_agent_status(agent_id: str, status: str, db: Session = Depends(get_db)):
    """
    Update an agent's status
    """
    try:
        agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        agent.status = status
        db.commit()
        logger.info(f"Agent {agent_id} status updated to {status}")
        return {"message": f"Agent {agent_id} status updated to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating agent status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{agent_id}/heartbeat")
def agent_heartbeat(agent_id: str, db: Session = Depends(get_db)):
    """
    Record agent heartbeat
    """
    try:
        agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        agent.last_heartbeat = datetime.utcnow()
        db.commit()
        logger.info(f"Heartbeat received from agent: {agent_id}")
        return {"message": "Heartbeat recorded"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error recording heartbeat: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{agent_id}")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Get agent details
    """
    agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/", response_model=List[Agent])
def list_agents(db: Session = Depends(get_db)):
    """
    List all agents
    """
    try:
        agents = db.query(AgentModel).all()
        return agents
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{agent_id}/metrics")
def record_metrics(agent_id: str, metrics: List[MetricCreate], db: Session = Depends(get_db)):
    """
    Record metrics for an agent
    """
    try:
        # Verify agent exists
        agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Record each metric
        for metric in metrics:
            db_metric = MetricModel(
                agent_id=agent_id,
                metric_name=metric.metric_name,
                value=metric.value,
                timestamp=metric.timestamp or datetime.utcnow()
            )
            db.add(db_metric)
        
        db.commit()
        logger.info(f"Metrics recorded for agent: {agent_id}")
        return {"message": "Metrics recorded"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error recording metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{agent_id}/metrics")
def get_agent_metrics(agent_id: str, db: Session = Depends(get_db)):
    """
    Get metrics for an agent
    """
    try:
        # Verify agent exists
        agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Get metrics for the agent
        metrics = db.query(MetricModel).filter(MetricModel.agent_id == agent_id).all()
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health/agents")
def get_agent_health(db: Session = Depends(get_db)):
    """
    Get health status of all agents
    """
    try:
        # Get all agents
        agents = db.query(AgentModel).all()
        
        # Check for inactive agents (no heartbeat in last 5 minutes)
        active_threshold = datetime.utcnow() - timedelta(minutes=5)
        inactive_agents = [agent for agent in agents if agent.last_heartbeat < active_threshold]
        
        return {
            "total_agents": len(agents),
            "active_agents": len([agent for agent in agents if agent.last_heartbeat >= active_threshold]),
            "inactive_agents": len(inactive_agents),
            "agents": [
                {
                    "agent_id": agent.agent_id,
                    "name": agent.name,
                    "status": agent.status,
                    "last_heartbeat": agent.last_heartbeat
                }
                for agent in agents
            ]
        }
    except Exception as e:
        logger.error(f"Error getting agent health: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")