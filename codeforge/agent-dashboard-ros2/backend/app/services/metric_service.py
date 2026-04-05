import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session as DatabaseSession
from app.models.metric import Metric
from app.models.agent import Agent
from app.schemas.metric import MetricCreate

logger = logging.getLogger(__name__)

def get_all_metrics(db: DatabaseSession) -> List[Metric]:
    """Retrieve all metrics from the database."""
    try:
        metrics = db.query(Metric).all()
        return metrics
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        raise

def get_metrics_for_agent(db: DatabaseSession, agent_id: int) -> List[Metric]:
    """Retrieve metrics for a specific agent."""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent with id {agent_id} not found")
        
        metrics = db.query(Metric).filter(Metric.agent_id == agent_id).all()
        return metrics
    except Exception as e:
        logger.error(f"Error retrieving metrics for agent {agent_id}: {str(e)}")
        raise

def create_metric(db: DatabaseSession, data: MetricCreate) -> Metric:
    """Create a new metric entry."""
    try:
        # Validate agent exists
        agent = db.query(Agent).filter(Agent.id == data.agent_id).first()
        if not agent:
            raise ValueError(f"Agent with id {data.agent_id} not found")
        
        # Create the metric
        db_metric = Metric(
            agent_id=data.agent_id,
            metric_type=data.metric_type,
            value=data.value,
            timestamp=data.timestamp
        )
        
        db.add(db_metric)
        db.commit()
        db.refresh(db_metric)
        return db_metric
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating metric: {str(e)}")
        raise

def get_metric_by_id(db: DatabaseSession, metric_id: int) -> Optional[Metric]:
    """Retrieve a specific metric by its ID."""
    try:
        return db.query(Metric).filter(Metric.id == metric_id).first()
    except Exception as e:
        logger.error(f"Error retrieving metric {metric_id}: {str(e)}")
        raise

def delete_metric(db: DatabaseSession, metric_id: int) -> bool:
    """Delete a metric by its ID."""
    try:
        metric = db.query(Metric).filter(Metric.id == metric_id).first()
        if not metric:
            raise ValueError(f"Metric with id {metric_id} not found")
        
        db.delete(metric)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting metric {metric_id}: {str(e)}")
        raise