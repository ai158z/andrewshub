import logging
from typing import List, Optional
from datetime import datetime
from stop_skill_library.models import Skill, SkillVersion
from stop_skill_library.version_control import VersionControl
from stop_skill_library.storage.hierarchical_storage import HierarchicalStorage

logger = logging.getLogger(__name__)

class VersionManager:
    def __init__(self, storage, version_control):
        """
        Initialize the VersionManager with storage and version control dependencies.
        
        Args:
            storage: HierarchicalStorage instance for skill storage
            version_control: VersionControl instance for version operations
        """
        if not storage or not version_control:
            raise ValueError("Storage and version_control are required")
            
        self.storage = storage
        self.version_control = version_control
        self.versions = {}
        logger.info("VersionManager initialized")

    def create_version(self, skill_id: str, metadata: Optional[dict] = None) -> str:
        """
        Create a new version for a skill.
        
        Args:
            skill_id: Unique identifier for the skill
            metadata: Optional metadata for the version
            
        Returns:
            Version identifier of the created version
            
        Raises:
            ValueError: If skill_id is invalid or version creation fails
        """
        if not skill_id or not isinstance(skill_id, str):
            raise ValueError("Invalid skill_id provided")
            
        # Get current skill state from storage
        skill = self.storage.get(skill_id)
        if not skill:
            raise ValueError(f"Skill with id {skill_id} not found")
        
        try:
            # Create version through version control system
            version_id = self.version_control.commit(skill, metadata or {})
            
            # Store version information
            if skill_id not in self.versions:
                self.versions[skill_id] = []
                
            version = SkillVersion(
                version_id=version_id,
                skill_id=skill_id,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            self.versions[skill_id].append(version)
            
            logger.info(f"Created version {version_id} for skill {skill_id}")
            return version_id
            
        except Exception as e:
            logger.error(f"Failed to create version for skill {skill_id}: {str(e)}")
            raise

    def get_version(self, skill_id: str, version_id: str) -> Optional[Skill]:
        """
        Retrieve a specific version of a skill.
        
        Args:
            skill_id: Unique identifier for the skill
            version_id: Version identifier to retrieve
            
        Returns:
            Skill object at the specified version or None if not found
            
        Raises:
            ValueError: If skill_id or version_id is invalid
        """
        if not skill_id or not version_id:
            raise ValueError("skill_id and version_id are required")
            
        try:
            # Get version from version control system
            skill = self.version_control.get_version(version_id)
            if not skill:
                logger.warning(f"Version {version_id} not found for skill {skill_id}")
                return None
                
            return skill
            
        except Exception as e:
            logger.error(f"Failed to retrieve version {version_id} for skill {skill_id}: {str(e)}")
            raise

    def rollback_to_version(self, skill_id: str, version_id: str) -> bool:
        """
        Rollback a skill to a specific version.
        
        Args:
            skill_id: Unique identifier for the skill
            version_id: Version identifier to rollback to
            
        Returns:
            True if rollback was successful, False otherwise
            
        Raises:
            ValueError: If skill_id or version_id is invalid
        """
        if not skill_id or not version_id:
            raise ValueError("skill_id and version_id are required")
            
        try:
            # Get the version to rollback to
            skill_version = self.get_version(skill_id, version_id)
            if not skill_version:
                logger.error(f"Version {version_id} not found for skill {skill_id}")
                return False
                
            # Perform rollback through version control
            success = self.version_control.rollback(version_id)
            if not success:
                logger.error(f"Failed to rollback to version {version_id} for skill {skill_id}")
                return False
                
            # Update storage with rolled back version
            self.storage.remove(skill_id)
            self.storage.add(skill_id, skill_version)
            
            logger.info(f"Successfully rolled back skill {skill_id} to version {version_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback skill {skill_id} to version {version_id}: {str(e)}")
            raise

    def get_history(self, skill_id: str) -> List[SkillVersion]:
        """
        Get version history for a skill.
        
        Args:
            skill_id: Unique identifier for the skill
            
        Returns:
            List of SkillVersion objects representing the history
            
        Raises:
            ValueError: If skill_id is invalid
        """
        if not skill_id or not isinstance(skill_id, str):
            raise ValueError("Invalid skill_id provided")
            
        try:
            # Get history from version control
            history = self.version_control.get_history()
            
            # Filter for specific skill if history is not None
            if history:
                skill_history = [
                    version for version in history 
                    if hasattr(version, 'skill_id') and version.skill_id == skill_id
                ]
                return skill_history
            else:
                # Fallback to locally stored versions
                return self._get_skill_versions(skill_id)
                
        except Exception as e:
            logger.error(f"Failed to get history for skill {skill_id}: {str(e)}")
            raise

    def _get_skill_versions(self, skill_id: str) -> List[SkillVersion]:
        """
        Helper method to get versions for a specific skill.
        
        Args:
            skill_id: Skill identifier
            
        Returns:
            List of versions for the skill
        """
        return self.versions.get(skill_id, [])