from pydantic import BaseModel, Field, field_validator, model_validator
from pydantoc import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import numpy as np


class SensorReading(BaseModel):
    """
    Data model representing a single sensor reading
    """
    sensor_id: str = Field(..., description="Unique identifier for the sensor")
    timestamp: datetime = Field(..., description="Timestamp of the reading")
    value: float = Field(..., description="Sensor value")
    unit: str = Field("", description="Unit of measurement")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    sensor_type: str = Field(..., description="Type of sensor (e.g., 'visual', 'tactile')")

    class Config:
        orm_mode = True

class SensorFusionData(BaseModel):
    """
    Data model representing fused sensor data from multiple sources
    """
    visual_data: Optional[Dict[str, Any]] = None
    tactile_data: Optional[Dict[str, Any]] = None
    fused_output: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())
    confidence: float = Field(1.0, ge=0.0, le=1.0)