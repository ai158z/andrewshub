from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass
from backend.app.database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = Column(String, index=True, nullable=False)
        self.value = Column(Float, nullable=False)
        self.unit = Column(String, nullable=True)
        self.description = Column(Text, nullable=True)
        self.metadata_json = Column(JSONB, nullable=True)
        self.timestamp = Column(DateTime, default=func.now(), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[Micket.MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass
from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class Metric(BaseModel):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[datetime] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[datetime] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=251, description="Name must be between 1 and 251 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(MetricCreate):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[datetime] = Field(None, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2020-01-01T00:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialect. The test code itself has a syntax error (Line 70: unterminated string literal (detected at line 70)). Focus on fixing the implementation only.
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2020-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic._internal._model_contracts import ModelMetaclass

from backend.app.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    agent = relationship("Agent", back_populates="metrics")

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Metric name cannot be null or empty")
        return name

    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Metric value cannot be null")
        return value

    @validates('agent_id')
    def validate_agent_id(self, key, agent_id):
        if agent_id is None:
            raise ValueError("Agent ID cannot be null")
        return agent_id

class MetricCreate(BaseModel):
    agent_id: int = Field(..., gt=0, description="Agent ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    value: float = Field(..., description="Value must be a valid number")
    unit: Optional[str] = Field(None, max_length=50, description="Unit must be less than 50 characters")
    description: Optional[str] = Field(None, max_length=500, description="Description must be less than 500 characters")
    metadata_json: Optional[dict] = Field({}, description="Metadata must be a valid JSON object")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the metric")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "agent_id": 1,
                "name": "cpu_usage",
                "value": 45.5,
                "unit": "%",
                "description": "CPU usage percentage",
                "metadata_json": {"source": "system_monitor"},
                "timestamp": "2020-01-01T12:00:00Z"
            }
        }

class MetricUpdate(MetricCreate):
    pass

class MetricBaseModel(MetricCreate):
    class Config:
        from_attributes = True

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricListResponse(BaseModel):
    data: list[MetricResponse]
    count: int

    class Config:
        from_attributes = True

class MetricResponseList(BaseModel):
    data: list[MetricResponse]

    class Config:
        from_attributes = True

class MetricCreateList(BaseModel):
    data: list[MetricCreate]

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float