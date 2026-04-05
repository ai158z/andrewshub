from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.metric import Metric as MetricSchema
from app.schemas.metric import MetricCreate
from app.services.metric_service import (
    get_all_metrics,
    get_metrics_for_agent,
    create_metric as create_metric_service
)

router = APIRouter()

@router.get("/metrics", response_model=List[MetricSchema])
def get_metrics(db: Session = Depends(get_db)):
    """Get all metrics from the database"""
    try:
        metrics = get_all_metrics(db)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/agent/{agent_id}", response_model=List[MetricSchema])
def get_agent_metrics(agent_id: int, db: Session = Depends(get_db)):
    """Get metrics for a specific agent"""
    try:
        metrics = get_metrics_for_agent(db, agent_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Metrics not found for agent")
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/metrics", response_model=MetricSchema, status_code=201)
def create_metric(data: MetricCreate, db: Session = Depends(get_db)):
    """Create a new metric entry"""
    try:
        created_metric = create_metric_service(db, data)
        return created_metric
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))