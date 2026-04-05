from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import sys
import os

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    __table_args__ = {"sqlite_autoincrement": True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String)
    ip_address = Column(String)
    last_heartbeat = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"Agent(name={self.name}, status={self.status})"

    def __str__(self):
        return self.__repr__().replace(")", "")

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(self, name, status, ip_address, last_heartbeat=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.last_heartbeat = last_heartbeat
        self.created_at = created_at
        self.updated_at = updated_at

    def __init__(sys