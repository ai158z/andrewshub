import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from stop_skill_library.models import Skill, SkillVersion
from stop_skill_library.core import SkillLibrary


class VersionControl:
    """Version control system for skill modules management."""

    def __init__(self, skill_library: SkillLibrary):
        """Initialize the version control system.
        
        Args:
            skill_library: The skill library instance to manage versions for
        """
        self.skill_library = skill_library
        self.logger = logging.getLogger(__name__)
        self.versions = {}  # In-memory storage for versions: {skill_id: {version_id: version_data}}
        self.logger.info("VersionControl initialized")

    def commit(self, skill_id: str, changes: Dict[str, Any], message: str, author: str) -> str:
        """Commit changes to a skill as a new version.
        
        Args:
            skill_id: The ID of the skill to commit
            changes: Dictionary of changes to apply
            message: Commit message
            author: Author of the commit
            
        Returns:
            Version ID of the created commit
            
        Raises:
            ValueError: If skill_id is invalid or changes are not applicable
            Exception: For other commit-related errors
        """
        try:
            # Get current skill state
            skill = self.skill_library.get_skill(skill_id)
            if not skill:
                raise ValueError(f"Skill with ID {skill_id} not found")

            # Create new version
            version_data = {
                "skill_id": skill_id,
                "content": skill.dict() if hasattr(skill, 'dict') else skill.__dict__,
                "changes": changes,
                "message": message,
                "author": author,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            version_id = self._create_version(skill_id, version_data)
            self.logger.info(f"Created version {version_id} for skill {skill_id}")
            return version_id
            
        except Exception as e:
            self.logger.error(f"Failed to commit changes: {str(e)}")
            raise Exception(f"Commit failed: {str(e)}")

    def rollback(self, skill_id: str, version_id: str) -> bool:
        """Rollback a skill to a previous version.
        
        Args:
            skill_id: The ID of the skill to rollback
            version_id: The version ID to rollback to
            
        Returns:
            True if rollback was successful, False otherwise
            
        Raises:
            ValueError: If skill_id or version_id is invalid
        """
        try:
            # Get the version data
            version_data = self._get_version(skill_id, version_id)
            if not version_data:
                raise ValueError(f"Version {version_id} not found for skill {skill_id}")
            
            # Apply the version data to restore the skill
            skill = self.skill_library.get_skill(skill_id)
            if skill:
                # Restore the skill content from version
                restored_content = version_data.get('content', {})
                if isinstance(restored_content, dict):
                    # Update the existing skill with restored content
                    for key, value in restored_content.items():
                        if hasattr(skill, key):
                            setattr(skill, key, value)
                else:
                    # Create new skill from restored content
                    restored_skill = Skill(**restored_content)
                    self.skill_library.add_skill(restored_skill)
                self.logger.info(f"Rolled back skill {skill_id} to version {version_id}")
                return True
            else:
                self.logger.error(f"Failed to restore skill {skill_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            return False

    def get_history(self, skill_id: str) -> List[Dict[str, Any]]:
        """Get version history for a skill.
        
        Args:
            skill_id: The ID of the skill to get history for
            
        Returns:
            List of version information dictionaries
            
        Raises:
            ValueError: If skill_id is invalid
        """
        try:
            history = self._get_history(skill_id)
            if not history:
                return []
            
            # Format history entries
            formatted_history = []
            for version_id, version_data in history.items():
                formatted_history.append({
                    "version_id": version_id,
                    "skill_id": skill_id,
                    "message": version_data.get('message', ''),
                    "author": version_data.get('author', ''),
                    "timestamp": version_data.get('timestamp', ''),
                    "changes": version_data.get('changes', {})
                })
            
            # Sort by timestamp
            formatted_history.sort(key=lambda x: x['timestamp'], reverse=True)
            return formatted_history
            
        except Exception as e:
            self.logger.error(f"Failed to get history for skill {skill_id}: {str(e)}")
            raise ValueError(f"Failed to retrieve history: {str(e)}")

    def get_version(self, skill_id: str, version_id: str) -> Optional[SkillVersion]:
        """Get a specific version of a skill.
        
        Args:
            skill_id: The ID of the skill
            version_id: The version ID to retrieve
            
        Returns:
            SkillVersion object if found, None otherwise
            
        Raises:
            ValueError: If skill_id or version_id is invalid
        """
        try:
            version_data = self._get_version(skill_id, version_id)
            if not version_data:
                return None
            
            # Create SkillVersion object from version data
            skill_version = SkillVersion(
                version_id=version_id,
                skill_id=skill_id,
                content=version_data.get('content', {}),
                changes=version_data.get('changes', {}),
                message=version_data.get('message', ''),
                author=version_data.get('author', ''),
                timestamp=version_data.get('timestamp', '')
            )
            
            return skill_version
            
        except Exception as e:
            self.logger.error(f"Failed to get version {version_id} for skill {skill_id}: {str(e)}")
            return None

    def _create_version(self, skill_id: str, version_data: Dict) -> str:
        """Internal method to create a new version."""
        if skill_id not in self.versions:
            self.versions[skill_id] = {}
        version_id = f"ver_{len(self.versions[skill_id]) + 1}"
        self.versions[skill_id][version_id] = version_data
        return version_id

    def _get_version(self, skill_id: str, version_id: str) -> Optional[Dict]:
        """Internal method to get a specific version."""
        if skill_id in self.versions and version_id in self.versions[skill_id]:
            return self.versions[skill_id][version_id]
        return None

    def _get_history(self, skill_id: str) -> Dict:
        """Internal method to get version history."""
        return self.versions.get(skill_id, {})