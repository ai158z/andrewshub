from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union, Dict, Any
import datetime

class Skill(BaseModel):
    """Model representing a skill with ID, name, description, and category."""
    id: int
    name: str
    description: str
    category: str
    level: str = "beginner"

    @validator('level')
    def validate_level(cls, level):
        if level not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError("Level must be 'beginner', 'intermediate', or 'advanced'")
        return level

class Task(BaseModel):
    """Model representing a task."""
    id: int
    name: str
    description: str
    status: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class Prediction(BaseModel):
    """Model representing a prediction with skill and predicted outcome."""
    predicted_skills: List[Dict[str, Union[str, int]]]
    predicted_outcome: str
    user_id: int
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class User(BaseModel):
    """Model representing a user with user ID and name."""
    user_id: int
    name: str
    email: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class TaskRequest(BaseModel):
    """Request model for creating a task."""
    task_id: int
    name: str
    description: str
    status: str = "pending"
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class SkillCreate(Skill):
    """Request model for creating a new skill."""
    pass

class SkillUpdate(BaseModel):
    """Pydantic model for updating a skill."""
    name: str
    description: str
    category: str
    level: str
    user_id: int
    task_id: int
    task_name: str
    task_description: str
    task_status: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @validator('level')
    def validate_level(cls, level):
        if level not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError("Level must be 'beginner', 'intermediate', or 'advanced'")
        return level