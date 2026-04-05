import json
import os
import logging
from typing import Dict, Optional, List
from src.models.skill import Skill

class SkillCatalog:
    def __init__(self, catalog_file: str = None):
        self.catalog_file = catalog_file
        self.skills: Dict[str, Skill] = {}
        self.logger = logging.getLogger(__name__)
        
        if self.catalog_file and os.path.exists(self.catalog_file):
            self.load_skills()
    
    def load_skills(self) -> None:
        """Load skills from catalog file"""
        try:
            if not self.catalog_file or not os.path.exists(self.catalog_file):
                self.skills = {}
                return
            
            with open(self.catalog_file, 'r') as f:
                data = json.load(f)
            
            self.skills = {}
            for skill_id, skill_data in data.items():
                try:
                    skill = Skill(
                        skill_id=skill_data.get('id'),
                        name=skill_data.get('name'),
                        description=skill_data.get('description'),
                        parameters=skill_data.get('parameters', {}),
                        metadata=skill_data.get('metadata', {})
                    )
                    self.skills[skill_id] = skill
                except Exception as e:
                    self.logger.error(f"Failed to load skill {skill_id}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error loading skills from {self.catalog_file}: {str(e)}")
            self.skills = {}

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID"""
        if not skill_id or not isinstance(skill_id, str):
            raise ValueError("Skill ID must be a non-empty string")
        
        return self.skills.get(skill_id)

    def add_skill(self, skill: Skill) -> bool:
        """Add a skill to the catalog"""
        if not isinstance(skill, Skill):
            raise TypeError("Skill must be an instance of Skill class")
        
        if not skill.skill_id:
            raise ValueError("Skill must have a valid skill_id")
        
        self.skills[skill.skill_id] = skill
        return True

    def remove_skill(self, skill_id: str) -> bool:
        """Remove a skill from the catalog"""
        if not skill_id or not isinstance(skill_id, str):
            raise ValueError("Skill ID must be a non-empty string")
        
        if skill_id in self.skills:
            del self.skills[skill_id]
            return True
        return False

    def list_skills(self) -> List[str]:
        """List all skill IDs in the catalog"""
        return list(self.skills.keys())

    def save_catalog(self) -> None:
        """Save skills to catalog file"""
        if not self.catalog_file:
            raise ValueError("Catalog file path not set")
        
        try:
            # Convert skills to dictionary format for saving
            data = {}
            for skill_id, skill in self.skills.items():
                data[skill_id] = {
                    'id': skill.skill_id,
                    'name': skill.name,
                    'description': skill.description,
                    'parameters': skill.parameters,
                    'metadata': skill.metadata
                }
            
            with open(self.catalog_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving skills to {self.catalog_file}: {str(e)}")
            raise