import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from stop_skill_library.models import Skill, SkillVersion
from stop_skill_library.storage.version_manager import VersionManager

@patch('stop_skill_library.storage.version_manager.HierarchicalStorage')
@patch('stop_skill_library.storage.version_manager.VersionControl')
def test_version_manager_init(mock_storage, mock_version_control):
    with pytest.raises(ValueError, match="Storage and version_control are required"):
        VersionManager(None, None, None)

def test_version_manager_initialization():
    storage = Mock()
    version_control = Mock()
    
    version_manager = VersionManager(storage, version_control)
    
    # Test valid initialization
    version_manager = VersionManager(storage, version_control)

def test_create_version_invalid_skill_id():
    storage = Mock()
    version_control = Mock()
    version_manager = VersionManager(storage, version_control)
    
    # Test invalid skill_id handling
    with pytest.raises(ValueError):
        version_manager.create_version("", {})

def test_create_version_success():
    storage = Mock()
    version_control = Mock()
    version_manager = VersionManager(storage, version_control)
    
    # Test valid creation
    with patch.object(version_manager.storage, 'get', return_value=Mock()) as mock_get:
        version_manager.create_version("skill123", {"test": "data"})

def test_get_version_success():
    storage = Mock()
    version_control = Mock()
    
    with patch.object(version_manager, 'get', return_value=Mock()) as mock_get:
        version_manager.get_history("skill123")

def test_rollback_to_version_success():
    storage = Mock()
    version_control = Mock()
    
    with patch.object(version_manager, 'get_history', return_value=Mock()) as mock_get:
        version_manager.get_version("skill123", "version456")

def test_get_history_success():
    storage = Mock()
    version_control = Mock()
    
    version_manager = VersionManager(storage, version_control)
    mock_get = Mock()
    version_manager = VersionManager(storage, version_control)
    
    # Test valid get_history
    with patch.object(version_manager, 'get_history', return_value=[]) as mock_get_history:
        version_manager.get_history("skill123")

def test_create_version_invalid_skill_id():
    version_control = Mock()
    version_manager = VersionManager(version_control, version_control)
    
    with pytest.raises(ValueError):
        version_manager.create_version(None, None)

def test_create_version_with_valid_skill():
    version_manager = VersionManager(version_control, version_control)
    version_control = Mock()
    
    # Test that skill_id is valid
    with patch.object(version_manager, 'create_version', return_value=Mock()) as mock_create:
        version_manager.create_version("skill123", {"test": "data"})

def test_rollback_to_version_with_valid_data():
    version_manager = VersionManager(version_control, version_control)
    
    # Test valid skill
    with patch.object(version_manager, 'get_version') as mock_get:
        version_manager.get_version("skill123", "version456")

def test_get_history_with_valid_data():
    version_manager = VersionManager(version_control, version_control)
    
    # Test valid get_history
    with patch.object(version_manager, 'get_history', return_value=[]) as mock_get:
        version_manager.get_history("skill123")

def test_rollback_to_version_with_invalid_data():
    version_manager = VersionManager(version_control, version_control)
    
    with pytest.raises(ValueError):
        version_manager.get_version("invalid123", 'version456')