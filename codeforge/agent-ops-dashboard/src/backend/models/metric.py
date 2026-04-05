from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from typing import Optional
import os
from datetime import datetime

# Create a local Base instance to avoid database connection during import
Base = declarative_base()

class MetricType(str, enum.Enum):
    system = "system"
    custom = "custom"

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    agent_id = Column(String, nullable=True)
    type = Column(String, default="system", nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.value = kwargs.get('value')
        self.timestamp = kwargs.get('timestamp')
        self.agent_id = kwargs.get('agent_id')
        self.type = kwargs.get('type', 'system')

    def __repr__(self):
        return f"<Metric(name='{self.name}', value={self.value}, timestamp={self.timestamp}, agent_id={self.agent_id})"

    def __str__(self):
        return f"Metric(id={self.id}, name='{self.name}', value={self.value}, timestamp={self.timestamp})"

    def __setattr__(self, name, value):
        if name == "type":
            if value not in ["system", "custom"]:
                raise ValueError(f"Invalid type: {value}")
        super().__setattr__(name, value)