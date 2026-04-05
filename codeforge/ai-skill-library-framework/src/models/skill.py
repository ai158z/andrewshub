import logging
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class Skill:
    def __init__(self, name: str, description: str = "A test skill", version: str = "1.0"):
        self.name = name
        self.description = description
        self.version = version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.name:
            raise ValueError("Name must be provided")
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("Skill name must be a non-empty string")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        return True

    def validate(self):
        """Validate the skill data"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a valid string")
        if not self.description:
            raise ValueError("Description is required")
        return True

class SkillModel:
    """Data model for skills with validation and serialization methods"""
    
    def __init__(self, name: str = "", description: str = "", version: str = ""):
        self.name = name
        self.description = description
        self.version = version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be provided")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Description must be a valid string")
        return True

    def validate(self):
        """Validate the skill model data"""
        if not self.name:
            raise ValueError("Name must be provided")
        return True

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version
        }

    def __repr__ (self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return json.dumps(self.to_dict())