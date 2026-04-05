import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.models.agent import Agent
from app.schemas.agent import AgentUpdate
from app.ros2_bridge import get_agent_status

logger = logging.getLogger(__name__)

def get_all_agents(db: Session) -> List[Agent]:
    """Retrieve all agents from the database."""
    try:
        agents = db.query(Agent).all()
        return agents
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving agents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agents from database"
        )

def get_agent_by_id(db: Session, agent_id: int) -> Agent:
    """Retrieve a specific agent by its ID."""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with id {agent_id} not found"
            )
        return agent
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent"
        )

def update_agent(db: Session, agent_id: int, data: AgentUpdate) -> Agent:
    """Update an agent's information."""
    try:
        db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not db_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with id {agent_id} not found"
            )
            
        # Update agent fields
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_agent, key, value)
            
        db.commit()
        db.refresh(db_agent)
        return db_agent
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent"
        )

def get_agent_status_service(agent_id: int) -> Dict:
    """Get the current status of an agent from ROS2."""
    try:
        ros2_status = get_agent_status(str(agent_id))
        return ros2_status
    except Exception as e:
        logger.error(f"Error retrieving ROS2 status for agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent status from ROS2"
        )