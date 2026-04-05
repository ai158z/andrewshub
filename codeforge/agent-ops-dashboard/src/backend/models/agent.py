import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import List, Optional

# Create a simple Base class for testing without database connection
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE, nullable=False)
    last_heartbeat = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_online = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Remove the relationship for now to avoid circular import issues
    # We'll set it up after all models are defined
    metrics = None

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Agent name cannot be empty")
        if len(name) > 100:
            raise ValueError("Agent name must be less than 100 characters")
        return name

    @validates('port')
    def validate_port(self, key, port):
        if port is not None:
            if not isinstance(port, int) or not (1 <= port <= 65535):
                raise ValueError("Port must be an integer between 1 and 65535")
        return port

    def __init__(self, 
                 name: str,
                 description: Optional[str] = None,
                 status: AgentStatus = AgentStatus.ACTIVE,
                 is_online: bool = False,
                 ip_address: Optional[str] = None,
                 hostname: Optional[str] = None,
                 port: Optional[int] = None):
        self.name = name
        self.description = description
        self.status = status
        self.is_online = is_online
        self.ip_address = ip_address
        self.hostname = hostname
        self.port = port
        self.last_heartbeat = datetime.utcnow()

    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', status='{self.status}')>"