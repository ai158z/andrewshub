import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from stop_skill_library.version_control import VersionControl
from stop_skill_library.models import Skill

@pytest.fixture
def skill():
    return Skill(
        id="test_skill_1",
        name="Test Skill",
        description="A test skill for version control",
        version="1.0.0"
    )

@pytest.fixture
def version_control():
    version_manager = Mock()
    return VersionControl(version_manager)

def test_version_creation_initial(version_control, skill):
    """Test creating the initial version of a skill."""
    version_control.version_manager.create_version.return_value = "v1.0"
    
    version = version_control.commit(skill, "Initial version", "test_user")
    
    assert version == "v1.0"
    version_control.version_manager.create_version.assert_called_once()

def test_version_creation_multiple_versions(version_control, skill):
    """Test creating multiple versions of the same skill."""
    version_control.version_manager.create_version.return_value = "v2.0"
    
    updated_skill = Skill(
        id=skill.id,
        name="Updated Test Skill",
        description="An updated test skill for version control",
        version="1.1.0"
    )
    
    version1 = version_control.commit(skill, "Initial version", "test_user")
    version2 = version_control.commit(updated_skill, "Updated version", "test_user")
    
    assert version1 is not None
    assert version2 is not None
    assert version1 != version2

def test_get_history(version_control, skill):
    """Test retrieving version history."""
    version_control.version_manager.get_history.return_value = ["v1.0", "v1.1"]
    
    history = version_control.get_history(skill.id)
    
    assert len(history) == 2
    version_control.version_manager.get_history.assert_called_once_with(skill.id)

def test_rollback_success(version_control, skill):
    """Test successful rollback to a previous version."""
    version_control.version_manager.rollback.return_value = True
    version_control.version_manager.get_version.return_value = skill
    
    result = version_control.rollback(skill.id, "v1.0", "test_user")
    
    assert result is True

def test_rollback_failure(version_control, skill):
    """Test rollback failure when version doesn't exist."""
    version_control.version_manager.rollback.return_value = False
    
    result = version_control.rollback("nonexistent_skill", "v9.9", "test_user")
    
    assert result is False

def test_get_version(version_control, skill):
    """Test retrieving a specific version of a skill."""
    version_control.version_manager.get_version.return_value = skill
    
    retrieved = version_control.get_version(skill.id, "v1.0")
    
    assert retrieved is not None
    assert isinstance(retrieved, Skill)

def test_get_version_not_found(version_control, skill):
    """Test retrieving a version that doesn't exist."""
    version_control.version_manager.get_version.return_value = None
    
    retrieved = version_control.get_version("nonexistent", "v9.9")
    
    assert retrieved is None

def test_version_creation_empty_message(version_control, skill):
    """Test version creation with empty commit message."""
    version_control.version_manager.create_version.return_value = "v1.0"
    
    version = version_control.commit(skill, "", "test_user")
    
    assert version is not None

def test_version_creation_none_message(version_control, skill):
    """Test version creation with None commit message."""
    version_control.version_manager.create_version.return_value = "v1.0"
    
    version = version_control.commit(skill, None, "test_user")
    
    assert version is not None

def test_version_creation_no_user(version_control, skill):
    """Test version creation with empty user."""
    version_control.version_manager.create_version.return_value = "v1.0"
    
    version = version_control.commit(skill, "Test message", "")
    
    assert version is not None

def test_get_history_empty(version_control):
    """Test getting history for skill with no versions."""
    version_control.version_manager.get_history.return_value = []
    
    history = version_control.get_history("nonexistent")
    
    assert len(history) == 0

def test_rollback_no_user(version_control, skill):
    """Test rollback with empty user."""
    version_control.version_manager.rollback.return_value = True
    
    result = version_control.rollback(skill.id, "v1.0", "")
    
    assert result is True

def test_version_creation_with_special_characters(version_control, skill):
    """Test version creation with special characters in message."""
    version_control.version_manager.create_version.return_value = "v1.0"
    
    version = version_control.commit(skill, "Version with !@#$%^&*()", "test_user")
    
    assert version is not None

def test_get_history_multiple_entries(version_control, skill):
    """Test getting history with multiple entries."""
    versions = ["v1.0", "v1.1", "v1.2"]
    version_control.version_manager.get_history.return_value = versions
    
    history = version_control.get_history(skill.id)
    
    assert len(history) == 3

def test_version_creation_same_skill_twice(version_control, skill):
    """Test creating two versions of the same skill."""
    version_control.version_manager.create_version.return_value = "v1.0"
    version1 = version_control.commit(skill, "First version", "test_user")
    
    updated_skill = Skill(
        id=skill.id,
        name="Updated Skill",
        description="Updated description",
        version="1.1.0"
    )
    version_control.version_manager.create_version.return_value = "v1.1"
    version2 = version_control.commit(updated_skill, "Second version", "test_user")
    
    assert version1 != version2

def test_rollback_to_same_version(version_control, skill):
    """Test rolling back to the same version."""
    version_control.version_manager.rollback.return_value = True
    version_control.version_manager.get_version.return_value = skill
    
    result = version_control.rollback(skill.id, "v1.0", "test_user")
    
    assert result is True

def test_get_version_current(version_control, skill):
    """Test getting the current version of a skill."""
    version_control.version_manager.get_version.return_value = skill
    
    current = version_control.get_version(skill.id, "v1.0")
    
    assert current.id == skill.id
    assert current.name == skill.name

def test_version_creation_empty_skill(version_control):
    """Test version creation with minimally initialized skill."""
    skill = Skill(id="minimal_skill", name="", description="", version="")
    version_control.version_manager.create_version.return_value = "v1.0"
    
    version = version_control.commit(skill, "Initial", "test_user")
    
    assert version is not None

def test_get_history_single_entry(version_control, skill):
    """Test getting history when only one version exists."""
    version_control.version_manager.get_history.return_value = ["v1.0"]
    
    history = version_control.get_history(skill.id)
    
    assert len(history) == 1
    assert "v1.0" in history