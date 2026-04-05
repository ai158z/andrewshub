import pytest
from unittest.mock import Mock, patch, MagicMock
from stop_skill_library.core import SkillLibrary
from stop_skill_library.models import Skill, SkillVersion, PerformanceMetrics

@pytest.fixture
def skill_library():
    with patch.multiple("stop_skill_library.core", 
                     SkillStorage=MagicMock(),
                     SelfImprovementEngine=MagicMock(),
                     ReflectionEngine=MagicMock(),
                     VersionControl=MagicMock(),
                     SecurityManager=MagicMock()):
        return SkillLibrary()

@pytest.fixture
def mock_skill():
    return Skill(id="test-skill-123", name="Test Skill", description="A test skill")

def test_add_skill_success(skill_library, mock_skill):
    skill_library.security_manager.validate_modification.return_value = True
    skill_library.storage.add_skill.return_value = "test-skill-123"
    result = skill_library.add_skill(mock_skill)
    assert result == "test-skill-123"

def test_add_skill_missing_id_or_name(skill_library, mock_skill):
    mock_skill.id = ""
    mock_skill.name = ""
    with pytest.raises(ValueError, match="Skill must have an ID and name"):
        skill_library.add_skill(mock_skill)

def test_add_skill_permission_denied(skill_library, mock_skill):
    skill_library.security_manager.validate_modification.return_value = False
    with pytest.raises(PermissionError):
        skill_library.add_skill(mock_skill)

def test_add_skill_storage_failure(skill_library, mock_skill):
    skill_library.security_manager.validate_modification.return_value = True
    skill_library.storage.add_skill.side_effect = Exception("Storage error")
    with pytest.raises(Exception, match="Storage error"):
        skill_library.add_skill(mock_skill)

def test_improve_skill_success(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.improvement_engine.validate_improvement.return_value = True
    skill_library.security_manager.validate_modification.return_value = True
    result = skill_library.improve_skill("test-skill-123", {"enhancement": "new_feature"})
    assert isinstance(result, Skill)

def test_improve_skill_not_found(skill_library):
    skill_library.storage.get_skill.return_value = None
    with pytest.raises(ValueError, match="Skill with ID test-skill-123 not found"):
        skill_library.improve_skill("test-skill-123", {})

def test_improve_skill_validation_failure(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.improvement_engine.validate_improvement.return_value = False
    with pytest.raises(ValueError, match="Improvement validation failed"):
        skill_library.improve_skill("test-skill-123", {})

def test_improve_skill_permission_denied(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.improvement_engine.validate_improvement.return_value = True
    skill_library.security_manager.validate_modification.return_value = False
    with pytest.raises(PermissionError):
        skill_library.improve_skill("test-skill-123", {})

def test_reflect_success(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    metrics = PerformanceMetrics(accuracy=0.95, latency=100)
    skill_library.reflection_engine.track_performance.return_value = metrics
    skill_library.reflection_engine.generate_report.return_value = metrics
    result = skill_library.reflect("test-skill-123")
    assert result == metrics

def test_reflect_skill_not_found(skill_library):
    skill_library.storage.get_skill.return_value = None
    with pytest.raises(ValueError, match="Skill with ID test-skill-123 not found"):
        skill_library.reflect("test-skill-123")

def test_get_skill_success(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    result = skill_library.get_skill("test-skill-123")
    assert result == mock_skill

def test_get_skill_not_found(skill_library):
    skill_library.storage.get_skill.return_value = None
    result = skill_library.get_skill("non-existent")
    assert result is None

def test_list_skills(skill_library):
    skills = [MagicMock(), MagicMock()]
    skill_library.storage.list_skills.return_value = skills
    result = skill_library.list_skills()
    assert result == skills

def test_list_skills_exception(skill_library):
    skill_library.storage.list_skills.side_effect = Exception("Database error")
    with pytest.raises(Exception, match="Database error"):
        skill_library.list_skills()

def test_improve_skill_apply_failure(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.improvement_engine.apply_improvement.side_effect = Exception("Apply error")
    skill_library.improvement_engine.validate_improvement.return_value = True
    with pytest.raises(Exception, match="Apply error"):
        skill_library.improve_skill("test-skill-123", {})

def test_add_skill_version_control_failure(skill_library, mock_skill):
    skill_library.security_manager.validate_modification.return_value = True
    skill_library.version_control.commit.side_effect = Exception("Version control error")
    skill_library.storage.add_skill.return_value = "test-skill-123"
    with pytest.raises(Exception, match="Version control error"):
        skill_library.add_skill(mock_skill)

def test_improve_skill_version_control_failure(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.improvement_engine.validate_improvement.return_value = True
    skill_library.security_manager.validate_modification.return_value = True
    skill_library.version_control.commit.side_effect = Exception("Version control error")
    with pytest.raises(Exception, match="Version control error"):
        skill_library.improve_skill("test-skill-123", {})

def test_reflect_tracking_failure(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.reflection_engine.track_performance.side_effect = Exception("Tracking error")
    with pytest.raises(Exception, match="Tracking error"):
        skill_library.reflect("test-skill-123")

def test_reflect_report_failure(skill_library, mock_skill):
    skill_library.storage.get_skill.return_value = mock_skill
    skill_library.reflection_engine.track_performance.return_value = PerformanceMetrics(accuracy=0.95, latency=100)
    skill_library.reflection_engine.generate_report.side_effect = Exception("Report generation error")
    with pytest.raises(Exception, match="Report generation error"):
        skill_library.reflect("test-skill-123")