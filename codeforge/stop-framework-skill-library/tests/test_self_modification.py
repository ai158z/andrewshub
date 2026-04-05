import pytest
from unittest.mock import Mock, MagicMock
from stop_skill_library.improvement.self_modification import SelfModificationEngine
from stop_skill_library.models import Skill

@pytest.fixture
def mock_storage():
    return Mock()

@pytest.fixture
def mock_security_manager():
    return Mock()

@pytest.fixture
def mock_skill():
    skill = Mock(spec=Skill)
    skill.parent = None
    skill.children = []
    return skill

@pytest.fixture
def self_modification_engine(mock_storage, mock_security_manager):
    engine = SelfModificationEngine(mock_storage, mock_security_manager)
    engine.safety_constraints = Mock()
    engine.version_control = Mock()
    engine.modification_validator = Mock()
    return engine

def test_modify_success(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.modification_validator.validate.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = True
    mock_storage.add.return_value = True
    self_modification_engine.security_manager.check_access.return_value = True
    self_modification_engine.version_control.create_version.return_value = Mock()
    
    result = self_modification_engine.modify("test_skill", {"key": "value"}, {})
    assert result is True

def test_modify_skill_not_found(self_modification_engine, mock_storage):
    mock_storage.get.return_value = None
    
    result = self_modification_engine.modify("nonexistent", {"key": "value"}, {})
    assert result is False

def test_modify_validation_fails(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.modification_validator.validate.return_value = False
    
    result = self_modification_engine.modify("test_skill", {"key": "value"}, {})
    assert result is False

def test_modify_access_denied(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.security_manager.check_access.return_value = False
    
    result = self_modification_engine.modify("test_skill", {"key": "value"}, {})
    assert result is False

def test_modify_safety_validation_fails(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.security_manager.check_access.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = False
    
    result = self_modification_engine.modify("test_skill", {"key": "value"}, {})
    assert result is False

def test_validate_modification_access_denied(self_modification_engine):
    self_modification_engine.security_manager.check_access.return_value = False
    
    result = self_modification_engine.validate_modification("test_skill", {"key": "value"})
    assert result is False

def test_validate_modification_safety_fails(self_modification_engine):
    self_modification_engine.security_manager.check_access.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = False
    
    result = self_modification_engine.validate_modification("test_skill", {"key": "value"})
    assert result is False

def test_validate_modification_signature_fails(self_modification_engine):
    self_modification_engine.security_manager.check_access.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = True
    self_modification_engine.modification_validator.validate.return_value = False
    
    result = self_modification_engine.validate_modification("test_skill", {"key": "value"})
    assert result is False

def test_validate_modification_success(self_modification_engine):
    self_modification_engine.security_manager.check_access.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = True
    self_modification_engine.modification_validator.validate.return_value = True
    
    result = self_modification_engine.validate_modification("test_skill", {"key": "value"})
    assert result is True

def test_apply_modification_skill_not_found(self_modification_engine, mock_storage):
    mock_storage.get.return_value = None
    
    result = self_modification_engine.apply_modification("nonexistent", {"key": "value"}, {})
    assert result is False

def test_apply_modification_create_version_fails(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.version_control.create_version.return_value = None
    
    result = self_modification_engine.apply_modification("test_skill", {"key": "value"}, {})
    assert result is False

def test_apply_modification_storage_fails(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.version_control.create_version.return_value = Mock()
    mock_storage.add.return_value = False
    
    result = self_modification_engine.apply_modification("test_skill", {"key": "value"}, {})
    assert result is False

def test_apply_modification_success_with_parent_update(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    mock_storage.get_parent.return_value = mock_skill
    mock_skill.parent = "parent_skill"
    self_modification_engine.version_control.create_version.return_value = Mock()
    mock_storage.add.return_value = True
    
    result = self_modification_engine.apply_modification("test_skill", {"key": "value"}, {})
    assert result is True

def test_modify_exception_handling(self_modification_engine, mock_storage):
    mock_storage.get.side_effect = Exception("Storage error")
    
    result = self_modification_engine.modify("test_skill", {"key": "value"}, {})
    assert result is False

def test_validate_modification_exception_handling(self_modification_engine):
    self_modification_engine.security_manager.check_access.side_effect = Exception("Security error")
    
    result = self_modification_engine.validate_modification("test_skill", {"key": "value"})
    assert result is False

def test_apply_modification_exception_handling(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.version_control.create_version.side_effect = Exception("Version control error")
    
    result = self_modification_engine.apply_modification("test_skill", {"key": "value"}, {})
    assert result is False

def test_modify_empty_skill_data(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.modification_validator.validate.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = True
    mock_storage.add.return_value = True
    self_modification_engine.security_manager.check_access.return_value = True
    
    result = self_modification_engine.modify("test_skill", {}, {})
    assert result is True

def test_modify_none_skill_data(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.modification_validator.validate.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = True
    self_modification_engine.security_manager.check_access.return_value = True
    mock_storage.add.return_value = True
    
    result = self_modification_engine.modify("test_skill", None, {})
    assert result is True

def test_validate_modification_empty_changes(self_modification_engine):
    self_modification_engine.security_manager.check_access.return_value = True
    self_modification_engine.safety_constraints.validate.return_value = True
    self_modification_engine.modification_validator.validate.return_value = True
    
    result = self_modification_engine.validate_modification("test_skill", {})
    assert result is True

def test_apply_modification_storage_returns_false(self_modification_engine, mock_storage, mock_skill):
    mock_storage.get.return_value = mock_skill
    self_modification_engine.version_control.create_version.return_value = Mock()
    mock_storage.add.return_value = False
    
    result = self_modification_engine.apply_modification("test_skill", {"key": "value"}, {})
    assert result is False