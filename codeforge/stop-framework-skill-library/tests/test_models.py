import uuid
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel
import pytest
from unittest.mock import patch, MagicMock
from stop_skill_library.models import Skill, SkillVersion, PerformanceMetrics, SecurityContext


def test_skill_version_default_values():
    sv = SkillVersion()
    assert isinstance(sv.version_id, str)
    assert sv.version_number == 1
    assert sv.code == ""
    assert sv.metadata == {}
    assert isinstance(sv.created_at, datetime)
    assert sv.created_by is None
    assert sv.description is None


def test_skill_version_increment_version():
    original = SkillVersion(version_number=1, code="original_code")
    incremented = original.increment_version()
    assert incremented.version_number == 2
    assert incremented.code == "original_code"
    assert incremented.version_id != original.version_id
    assert incremented.created_at > original.created_at


def test_performance_metrics_default_values():
    pm = PerformanceMetrics()
    assert pm.execution_time == 0.0
    assert pm.success_rate == 0.0
    assert pm.error_rate == 0.0
    assert pm.resource_utilization == {}
    assert pm.execution_count == 0
    assert pm.last_executed is None
    assert pm.metrics_history == []


def test_performance_metrics_update_metrics():
    pm = PerformanceMetrics()
    pm.update_metrics(1.0, True, {"cpu": 50})
    assert pm.execution_count == 1
    assert pm.success_rate == 1.0
    assert pm.error_rate == 0.0
    assert pm.last_executed is not None
    assert len(pm.metrics_history) == 1


def test_security_context_default_values():
    sc = SecurityContext()
    assert sc.owner_id == ""
    assert sc.permissions == []
    assert sc.access_control_list == {}
    assert sc.signature is None
    assert sc.last_modified_by is None
    assert sc.last_modified_at is None
    assert sc.modification_log == []


def test_security_context_add_permission():
    sc = SecurityContext()
    sc.add_permission("read")
    assert "read" in sc.permissions
    sc.add_permission("read")  # Try adding duplicate
    assert sc.permissions.count("read") == 1


def test_security_context_add_to_access_control():
    sc = SecurityContext()
    sc.add_to_access_control("user1", ["read", "write"])
    assert sc.access_control_list["user1"] == ["read", "write"]


def test_security_context_log_modification():
    sc = SecurityContext()
    sc.log_modification("modifier1", {"action": "update"})
    assert sc.last_modified_by == "modifier1"
    assert sc.last_modified_at is not None
    assert len(sc.modification_log) == 1


def test_skill_default_values():
    s = Skill()
    assert isinstance(s.skill_id, str)
    assert s.name == ""
    assert s.description == ""
    assert isinstance(s.version, SkillVersion)
    assert isinstance(s.performance, PerformanceMetrics)
    assert isinstance(s.security, SecurityContext)
    assert s.parent_id is None
    assert s.children == []
    assert s.metadata == {}
    assert s.tags == []
    assert s.dependencies == []


def test_skill_add_tag():
    s = Skill()
    s.add_tag("important")
    assert "important" in s.tags
    s.add_tag("important")  # Add duplicate
    assert s.tags.count("important") == 1


def test_skill_add_dependency():
    s = Skill()
    s.add_dependency("skill_123")
    assert "skill_123" in s.dependencies
    s.add_dependency("skill_123")  # Add duplicate
    assert s.dependencies.count("skill_123") == 1


def test_skill_update_performance():
    s = Skill()
    s.update_performance(2.5, True, {"cpu": 75})
    assert s.performance.execution_count == 1
    assert s.performance.success_rate == 1.0


def test_skill_add_child():
    s = Skill()
    s.add_child("child_123")
    assert "child_123" in s.children
    s.add_child("child_123")  # Add duplicate
    assert s.children.count("child_123") == 1


def test_skill_update_version():
    s = Skill()
    original_version_id = s.version.version_id
    s.update_version("new_code", "Updated version")
    assert s.version.code == "new_code"
    assert s.version.description == "Updated version"
    assert s.version.version_id != original_version_id
    assert s.version.version_number == 2


def test_skill_set_parent():
    s = Skill()
    s.set_parent("parent_456")
    assert s.parent_id == "parent_456"


def test_skill_updated_at_changes():
    s = Skill()
    old_time = s.updated_at
    s.add_tag("test")
    assert s.updated_at > old_time


def test_performance_metrics_calculations():
    pm = PerformanceMetrics()
    pm.update_metrics(1.0, True, {"cpu": 50})
    pm.update_metrics(2.0, False, {"cpu": 60})
    assert pm.execution_count == 2
    assert pm.success_rate == 0.5
    assert pm.error_rate == 0.5
    assert len(pm.metrics_history) == 2


def test_security_context_modification_log():
    sc = SecurityContext()
    sc.log_modification("modifier1", {"action": "create"})
    sc.log_modification("modifier2", {"action": "update"})
    assert len(sc.modification_log) == 2
    assert sc.modification_log[0]["modifier_id"] == "modifier1"
    assert sc.modification_log[1]["modifier_id"] == "modifier2"


def test_skill_version_increment_preserves_data():
    sv = SkillVersion(version_number=3, code="old_code", description="Old version")
    new_sv = sv.increment_version()
    assert new_sv.version_number == 4
    assert new_sv.code == "old_code"
    assert new_sv.description == "Old version"


def test_skill_update_version_empty_description():
    s = Skill()
    s.update_version("new_code")
    assert s.version.code == "new_code"
    assert s.version.description == ""