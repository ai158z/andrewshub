from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re


class AgentStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


class AgentBase(BaseModel):
    name: str = Field(..., example="Data Processing Agent")
    description: Optional[str] = Field(None, example="Handles data processing tasks")
    status: AgentStatus = Field(..., example=AgentStatus.ONLINE)
    version: str = Field(..., example="1.2.0")
    ip_address: str = Field(..., example="192.168.1.100")

    @validator('ip_address')
    def validate_ip_address(cls, v):
        # Simple IP address validation
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pattern.match(v):
            raise ValueError('Invalid IP address format')
        parts = v.split('.')
        if not all(0 <= int(part) <= 255 for part in parts):
            raise ValueError('Invalid IP address format')
        return v


class AgentCreate(AgentBase):
    pass


class Agent(AgentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True