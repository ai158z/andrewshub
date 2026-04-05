import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class SkillVersion(BaseModel):
    version_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version_number: int = 1
    code: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = None
    description: Optional[str] = None

    def increment_version(self) -> "SkillVersion":
        """Create a new version based on this one"""
        new_version = self.model_copy()
        new_version.version_number += 1
        new_version.version_id = str(uuid.uuid4())
        new_version.created_at = datetime.now()
        return new_version


class PerformanceMetrics(BaseModel):
    execution_time: float = 0.0
    success_rate: float = 0.0
    error_rate: float = 0.0
    resource_utilization: Dict[str, Any] = Field(default_factory=dict)
    execution_count: int = 0
    last_executed: Optional[datetime] = None
    metrics_history: List[Dict] = Field(default_factory=list)

    def update_metrics(
        self, execution_time: float, success: bool, resources: Dict[str, Any]
    ) -> None:
        """Update performance metrics with new execution data"""
        self.execution_count += 1
        self.execution_time = (
            self.execution_time * (self.execution_count - 1) + execution_time
        ) / self.execution_count
        self.success_rate = (
            self.success_rate * (self.execution_count - 1) + (1.0 if success else 0.0)
        ) / self.execution_count
        self.error_rate = 1.0 - self.success_rate
        self.last_executed = datetime.now()
        self.metrics_history.append(
            {
                "timestamp": datetime.now(),
                "execution_time": execution_time,
                "success": success,
                "resources": resources,
            }
        )


class SecurityContext(BaseModel):
    owner_id: str = ""
    permissions: List[str] = Field(default_factory=list)
    access_control_list: Dict[str, List[str]] = Field(default_factory=dict)
    signature: Optional[str] = None
    last_modified_by: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    modification_log: List[Dict] = Field(default_factory=list)

    def add_permission(self, permission: str) -> None:
        """Add a permission to the security context"""
        if permission not in self.permissions:
            self.permissions.append(permission)

    def add_to_access_control(self, user: str, permissions: List[str]) -> None:
        """Add user permissions to access control list"""
        self.access_control_list[user] = permissions

    def log_modification(
        self, modifier_id: str, modification_details: Dict[str, Any]
    ) -> None:
        """Log a modification to the skill"""
        self.last_modified_by = modifier_id
        self.last_modified_at = datetime.now()
        self.modification_log.append(
            {
                "modifier_id": modifier_id,
                "timestamp": datetime.now(),
                "details": modification_details,
            }
        )


class Skill(BaseModel):
    skill_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    version: SkillVersion = Field(default_factory=SkillVersion)
    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    security: SecurityContext = Field(default_factory=SecurityContext)
    parent_id: Optional[str] = None
    children: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the skill"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def add_dependency(self, skill_id: str) -> None:
        """Add a dependency to this skill"""
        if skill_id not in self.dependencies:
            self.dependencies.append(skill_id)
            self.updated_at = datetime.now()

    def update_performance(self, execution_time: float, success: bool, resources: Dict[str, Any]) -> None:
        """Update performance metrics"""
        self.performance.update_metrics(execution_time, success, resources)
        self.updated_at = datetime.now()

    def add_child(self, child_id: str) -> None:
        """Add a child skill"""
        if child_id not in self.children:
            self.children.append(child_id)
            self.updated_at = datetime.now()

    def update_version(self, code: str, description: str = "") -> None:
        """Create a new version of the skill"""
        self.version = self.version.increment_version()
        self.version.code = code
        self.version.description = description
        self.updated_at = datetime.now()

    def set_parent(self, parent_id: str) -> None:
        """Set the parent skill ID"""
        self.parent_id = parent_id
        self.updated_at = datetime.now()