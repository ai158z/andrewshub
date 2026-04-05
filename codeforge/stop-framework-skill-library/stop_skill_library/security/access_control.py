import logging
from typing import Dict, Set, Optional, List
from stop_skill_library.models import Skill
from stop_skill_library.security.validation import ModificationValidator

class AccessController:
    def __init__(self, validator: Optional[ModificationValidator] = None):
        """
        Initialize the AccessController with optional validator.
        
        Args:
            validator: Optional ModificationValidator instance for modification validation
        """
        self.permissions: Dict[str, Set[str]] = {}
        self.validator = validator
        self.logger = logging.getLogger(__name__)
        
    def check_permission(self, user_id: str, skill: Skill, action: str) -> bool:
        """
        Check if a user has permission to perform an action on a skill.
        
        Args:
            user_id: User identifier
            skill: Skill object to check access for
            action: Action to perform (e.g., 'read', 'write', 'execute')
            
        Returns:
            bool: True if permission is granted, False otherwise
        """
        try:
            # Check if user has global permissions
            if user_id in self.permissions:
                if '*' in self.permissions[user_id] or action in self.permissions[user_id]:
                    return True
                    
            # Check skill-specific permissions
            if hasattr(skill, 'permissions') and skill.permissions:
                if user_id in skill.permissions:
                    if '*' in skill.permissions[user_id] or action in skill.permissions[user_id]:
                        return True
                        
            # Default deny
            return False
        except Exception as e:
            self.logger.error(f"Error checking permission: {e}")
            return False
            
    def grant_access(self, user_id: str, skill_id: str, permissions: List[str]) -> bool:
        """
        Grant access permissions to a user for a specific skill.
        
        Args:
            user_id: User identifier
            skill_id: Skill identifier
            permissions: List of permissions to grant (e.g., ['read', 'write'])
            
        Returns:
            bool: True if access was granted successfully
        """
        try:
            # Initialize user permissions if not exists
            if user_id not in self.permissions:
                self.permissions[user_id] = set()
                
            # Add permissions
            for perm in permissions:
                self.permissions[user_id].add(perm)
                
            self.logger.info(f"Access granted to user {user_id} for skill {skill_id}: {permissions}")
            return True
        except Exception as e:
            self.logger.error(f"Error granting access: {e}")
            return False
            
    def revoke_access(self, user_id: str, skill_id: str, permissions: List[str]) -> bool:
        """
        Revoke access permissions from a user for a specific skill.
        
        Args:
            user_id: User identifier
            skill_id: Skill identifier
            permissions: List of permissions to revoke
            
        Returns:
            bool: True if access was revoked successfully
        """
        try:
            if user_id in self.permissions:
                # Remove specific permissions
                for perm in permissions:
                    self.permissions[user_id].discard(perm)
                    
                # Clean up empty permission sets
                if not self.permissions[user_id]:
                    del self.permissions[user_id]
                    
            self.logger.info(f"Access revoked for user {user_id} on skill {skill_id}: {permissions}")
            return True
        except Exception as e:
            self.logger.error(f"Error revoking access: {e}")
            return False
            
    def set_validator(self, validator: ModificationValidator) -> None:
        """Set the modification validator for this controller."""
        self.validator = validator
        
    def get_permissions(self, user_id: str) -> Set[str]:
        """Get all permissions for a user."""
        return self.permissions.get(user_id, set())
        
    def list_users_with_access(self, skill_id: str) -> List[str]:
        """List all users with access to a specific skill."""
        try:
            users = []
            for user, perms in self.permissions.items():
                if any(perm in perms for perm in ['read', 'write', 'execute', '*']):
                    users.append(user)
            return users
        except Exception as e:
            self.logger.error(f"Error listing users with access: {e}")
            return []