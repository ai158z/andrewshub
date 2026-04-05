from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class Repository(Base):
    __tablename__ = 'repositories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False, unique=True)
    url = Column(Text, nullable=False, unique=True)
    owner = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship to AnalysisResult
    analysis_results = relationship("AnalysisResult", back_populates="repository")
    
    def __init__(self, name: str, full_name: str, url: str, owner: str):
        self.name = name
        self.full_name = full_name
        self.url = url
        self.owner = owner
        self.is_active = True
    
    @validates('url')
    def validate_url(self, key, url):
        if not url:
            raise ValueError("Repository URL cannot be empty")
        if not url.startswith('http'):
            raise ValueError("Repository URL must be a valid HTTP/HTTPS URL")
        return url
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Repository name cannot be empty")
        if len(name) > 255:
            raise ValueError("Repository name too long")
        return name
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "url": self.url,
            "owner": self.owner,
            "is_active": self.is_active,
            "last_synced": self.last_synced.isoformat() if self.last_synced else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            full_name=data['full_name'],
            url=data['url'],
            owner=data['owner']
        )
    
    def update_last_synced(self):
        self.last_synced = datetime.utcnow()
        return self
    
    def deactivate(self):
        self.is_active = False
        return self
    
    def activate(self):
        self.is_active = True
        return self
    
    def __repr__(self):
        return f"<Repository(id={self.id}, name='{self.name}', owner='{self.owner}')>"