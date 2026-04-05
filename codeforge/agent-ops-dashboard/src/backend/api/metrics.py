import os
import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta

from src.backend.database import get_db
from src.backend.models.metric import Metric
from src.backend.models.agent import Agent
from src.backend.schemas.metric import MetricCreate
from src.backend.schemas.agent import AgentCreate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Constants
METRICS_STREAM_DELAY = 1.0  # seconds
METRICS_STREAM_RETRY_TIMEOUT = 15000  # milliseconds

@router.get("/metrics")
async def get_metrics(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current system metrics
    """
    try:
        # Get latest metrics for each agent
        latest_metrics = db.query(
            Metric
        ).join(
            Agent, Metric.agent_id == Agent.id
        ).filter(
            Metric.timestamp == db.query(func.max(Metric.timestamp)).filter(Metric.agent_id == Agent.id).correlate(Metric).scalar_subquery()
        ).all()
        
        metrics_data = []
        for metric in latest_metrics:
            metrics_data.append({
                "agent_id": metric.agent_id,
                "cpu_usage": metric.cpu_usage,
                "memory_usage": metric.memory_usage,
                "timestamp": metric.timestamp.isoformat() if metric.timestamp else None
            })
            
        return {"metrics": metrics_data}
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")

@router.post("/metrics", status_code=status.HTTP_201_CREATED)
async def create_metric(
    metric: MetricCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create a new metric entry
    """
    try:
        db_metric = Metric(**metric.dict())
        db.add(db_metric)
        db.commit()
        db.refresh(db_metric)
        return {"id": db_metric.id, "message": "Metric created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating metric: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create metric")

@router.get("/metrics/stream")
async def metrics_stream(
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    Stream real-time metrics updates
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        while True:
            try:
                # Get latest metrics
                latest_metrics = db.query(
                    Metric
                ).join(
                    Agent, Metric.agent_id == Agent.id
                ).filter(
                    Metric.timestamp == db.query(func.max(Metric.timestamp)).filter(Metric.agent_id == Agent.id).correlate(Metric).scalar_subquery()
                ).all()
                
                metrics_data = []
                for metric in latest_metrics:
                    metrics_data.append({
                        "agent_id": metric.agent_id,
                        "cpu_usage": metric.cpu_usage,
                        "memory_usage": metric.memory_usage,
                        "timestamp": metric.timestamp.isoformat() if metric.timestamp else None
                    })
                
                yield f"data: {json.dumps({'metrics': metrics_data})}\n\n"
                await asyncio.sleep(METRICS_STREAM_DELAY)
            except Exception as e:
                logger.error(f"Error in metrics stream: {str(e)}")
                yield f"data: {json.dumps({'error': 'Stream error'})}\n\n"
                break
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/metrics/summary")
async def get_metrics_summary(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get metrics summary including system health information
    """
    try:
        # Get system metrics summary
        avg_cpu = db.query(func.avg(Metric.cpu_usage)).scalar() or 0
        avg_memory = db.query(func.avg(Metric.memory_usage)).scalar() or 0
        total_agents = db.query(Agent).count()
        
        # Get recent metrics count
        recent_metrics_count = db.query(Metric).filter(
            Metric.timestamp > datetime.utcnow().replace(second=0, microsecond=0)
        ).count()
        
        return {
            "system_health": {
                "average_cpu": round(float(avg_cpu), 2),
                "average_memory": round(float(avg_memory), 2),
                "total_agents": total_agents,
                "metrics_per_minute": recent_metrics_count
            }
        }
    except Exception as e:
        logger.error(f"Error generating metrics summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate metrics summary")

@router.get("/metrics/history/{agent_id}")
async def get_agent_metrics_history(
    agent_id: int,
    hours: int = 24,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get metrics history for a specific agent
    """
    try:
        # Calculate time threshold
        time_threshold = datetime.utcnow().replace(second=0, microsecond=0)
        # Subtract hours from threshold
        time_threshold -= timedelta(hours=hours)
        
        # Get metrics history
        metrics_history = db.query(Metric).filter(
            and_(
                Metric.agent_id == agent_id,
                Metric.timestamp >= time_threshold
            )
        ).order_by(Metric.timestamp.desc()).all()
        
        history_data = []
        for metric in metrics_history:
            history_data.append({
                "cpu_usage": metric.cpu_usage,
                "memory_usage": metric.memory_usage,
                "timestamp": metric.timestamp.isoformat() if metric.timestamp else None
            })
            
        return {"history": history_data}
    except Exception as e:
        logger.error(f"Error fetching metrics history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics history")

@router.delete("/metrics/{metric_id}")
async def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Delete a specific metric by ID
    """
    try:
        metric = db.query(Metric).filter(Metric.id == metric_id).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
            
        db.delete(metric)
        db.commit()
        return {"message": "Metric deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting metric: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete metric")