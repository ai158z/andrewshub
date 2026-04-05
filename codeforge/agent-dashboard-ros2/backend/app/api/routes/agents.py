from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from backend.app.models.agent import Agent
from backend.app.schemas.agent import AgentBase
from backend.app.database import get_db
from backend.app.services.agent_service import get_all_agents, get_agent_by_id, update_agent
from backend.app.services.metric_service import get_metrics_for_agent
from backend.app.ros2_bridge import get_agent_status as ros2_get_agent_status

logger = logging.getLogger(__name__)

# Create the router instance
router = APIRouter()

@router.get("/agents", response_model=List[AgentBase])
def get_agents(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    try:
        agents = get_all_agents(db)
        return agents
    except Exception as e:
        logger.error(f"Error fetching agents: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agents")

@router.get("/agents/{agent_id}", response_model=AgentBase)
def get_agent(agent_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        agent = get_agent_by_id(db, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except Exception as e:
        logger.error(f"Error fetching agent: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agent")

@router.put("/agents/{agent_id}/status")
def update_agent_status(agent_id: int, status: dict, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        updated_agent = update_agent(db, agent_id, status)
        if updated_agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return updated_agent
    except Exception as e:
        logger.error(f"Error updating agent {agent_id} status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update agent status")

@router.get("/agents/{agent_id}/status")
def get_agent_status(agent_id: int, db: Session = Depends(get_db)):
    try:
        # Try to get status from ROS2 bridge
        status = ros2_get_agent_status(str(agent_id))
        if status:
            return status
        # Fallback to database if ROS2 node is not available
        agent = get_agent_by_id(db, agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except Exception as e:
        logger.error(f"Error getting agent status for {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get agent status")

@router.get("/agents/{agent_id}/metrics")
def get_metrics(agent_id: int, db: Session = Depends(get_db)):
    try:
        metrics = get_metrics_for_agent(db, agent_id)
        return metrics
    except Exception as e:
        logger.error(f"Error fetching metrics for agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agent metrics")