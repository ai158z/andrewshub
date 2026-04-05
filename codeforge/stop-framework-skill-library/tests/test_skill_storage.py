import pytest
from unittest.mock import Mock, patch, MagicMock
from uuid import UUID, uuid4
from stop_skill_library.models import Skill

@pytest.fixture
def skill_storage():
    with patch.multiple("stop_skill_library.skill_storage", 
                      HierarchicalStorage=Mock(),
                      VersionManager=Mock(),
                      AccessController=Mock(),
                      ModificationValidator=Mock()):
        from stop_skill_library.skill_storage import SkillStorage
        storage = SkillStorage()
        storage.storage = Mock()
        storage.version_manager = Mock()
        storage.access_controller = Mock()
        storage.validator = Mock()
        yield storage

@pytest.fixture
def sample_skill():
    return Skill(id=uuid4(), name="Test Skill", description="A test skill")

def test_add_skill_validates_skill_type(skill_storage, sample_skill):
    with pytest.raises(ValueError, match="Provided object is not a valid Skill instance"):
        skill_storage.add_skill("not a skill")

def test_add_skill_success(skill_storage, sample_skill):
    skill_storage.storage.add.return_value = sample_skill.id
    skill_storage.version_manager.create_version = Mock()
    
    result = skill_storage.add_skill(sample_skill)
    assert isinstance(result, UUID)
    skill_storage.storage.add.assert_called_once_with(sample_skill.id, sample_skill, None)
    skill_storage.version_manager.create_version.assert_called_once_with(sample_skill.id, sample_skill)

def test_add_skill_with_parent(skill_storage, sample_skill):
    parent_id = uuid4()
    skill_storage.storage.add.return_value = sample_skill.id
    skill_storage.version_manager.create_version = Mock()
    
    result = skill_storage.add_skill(sample_skill, parent_id)
    assert isinstance(result, UUID)
    skill_storage.storage.add.assert_called_with(sample_skill.id, sample_skill, parent_id)

def test_get_skill_invalid_uuid(skill_storage):
    with pytest.raises(TypeError):
        skill_storage.get_skill("invalid-uuid")

def test_get_skill_success(skill_storage):
    skill_id = uuid4()
    mock_skill = Mock()
    skill_storage.storage.get.return_value = mock_skill
    
    result = skill_storage.get_skill(skill_id)
    assert result == mock_skill

def test_get_skill_not_found(skill_storage):
    skill_id = uuid4()
    skill_storage.storage.get.return_value = None
    
    result = skill_storage.get_skill(skill_id)
    assert result is None

def test_remove_skill_invalid_uuid(skill_storage):
    with pytest.raises(TypeError):
        skill_storage.remove_skill("invalid-uuid")

def test_remove_skill_success(skill_storage):
    skill_id = uuid4()
    skill_storage.storage.remove.return_value = True
    
    result = skill_storage.remove_skill(skill_id)
    assert result is True

def test_remove_skill_not_found(skill_storage):
    skill_id = uuid4()
    skill_storage.storage.remove.return_value = False
    
    result = skill_storage.remove_skill(skill_id)
    assert result is False

def test_list_skills_success(skill_storage):
    skill_storage.storage.list_all.return_value = [uuid4(), uuid4()]
    
    result = skill_storage.list_skills()
    assert len(result) == 2
    assert all(isinstance(id, UUID) for id in result)

def test_get_children_invalid_uuid(skill_storage):
    with pytest.raises(TypeError):
        skill_storage.get_children("invalid-uuid")

def test_get_children_success(skill_storage):
    parent_id = uuid4()
    skill_storage.storage.list_children.return_value = [uuid4(), uuid4()]
    
    result = skill_storage.get_children(parent_id)
    assert len(result) == 2
    skill_storage.storage.list_children.assert_called_with(parent_id)

def test_get_parent_invalid_uuid(skill_storage):
    with pytest.raises(TypeError):
        skill_storage.get_parent("invalid-uuid")

def test_get_parent_success(skill_storage):
    skill_id = uuid4()
    parent_id = uuid4()
    skill_storage.storage.get_parent.return_value = parent_id
    
    result = skill_storage.get_parent(skill_id)
    assert result == parent_id

def test_get_parent_none(skill_storage):
    skill_id = uuid4()
    skill_storage.storage.get_parent.return_value = None
    
    result = skill_storage.get_parent(skill_id)
    assert result is None

def test_get_skill_history_invalid_uuid(skill_storage):
    with pytest.raises(TypeError):
        skill_storage.get_skill_history("invalid-uuid")

def test_get_skill_history_success(skill_storage):
    skill_id = uuid4()
    history_data = [{"version": "1", "data": "test"}]
    skill_storage.version_manager.get_history.return_value = history_data
    
    result = skill_storage.get_skill_history(skill_id)
    assert result == history_data

def test_rollback_skill_invalid_uuid(skill_storage):
    with pytest.raises(TypeError):
        skill_storage.rollback_skill("invalid-uuid", "v1")

def test_rollback_skill_success(skill_storage):
    skill_id = uuid4()
    version_id = "v1"
    mock_skill = Mock()
    skill_storage.version_manager.get_version.return_value = mock_skill
    skill_storage.storage.update.return_value = None
    
    result = skill_storage.rollback_skill(skill_id, version_id)
    assert result is True
    skill_storage.storage.update.assert_called_once_with(skill_id, mock_skill)

def test_rollback_skill_version_not_found(skill_storage):
    skill_id = uuid4()
    version_id = "nonexistent"
    skill_storage.version_manager.get_version.return_value = None
    
    result = skill_storage.rollback_skill(skill_id, version_id)
    assert result is False