import pytest
from unittest.mock import Mock, patch, MagicMock
from src.skill_manager import SkillManager
from src.models.skill import Skill

@pytest.fixture
def skill_manager():
    with patch('src.skill_manager.SkillCatalog'), \
         patch('src.skill_manager.CuriosityAllocator'), \
         patch('src.skill_manager.TaskScorer'), \
         patch('src.skill_manager.SkillPlugin'):
        manager = SkillManager()
        manager.skill_catalog = Mock()
        manager.curiosity_allocator = Mock()
        manager.task_scorer = Mock()
        manager.skill_plugins = Mock()
        return manager

@pytest.fixture
def valid_skill():
    skill = Mock(spec=Skill)
    skill.validate.return_value = True
    return skill

def test_register_valid_skill(skill_manager, valid_skill):
    skill_manager.catalog = Mock()
    skill_manager.register_skill(valid_skill)
    skill_manager.catalog.add_skill.assert_called_once_with(valid_skill)

def test_register_invalid_skill_raises_error(skill_manager):
    invalid_skill = Mock()
    invalid_skill.validate.return_value = False
    with pytest.raises(ValueError, match="Invalid skill data"):
        skill_manager.register_skill(invalid_skill)

def test_execute_skill_success(skill_manager, valid_skill):
    skill_manager.task_scorer.predict_outcome.return_value = {"result": "success"}
    result = skill_manager.execute_skill(valid_skill)
    assert result == {"result": "success"}

def test_execute_skill_failure(skill_manager, valid_skill):
    skill_manager.task_scorer.predict_outcome.side_effect = Exception("Execution failed")
    result = skill_manager.execute_skill(valid_skill)
    assert result == {}

def test_update_skill_success(skill_manager, valid_skill):
    skill_manager.update_skill(valid_skill, "action", "observation")
    skill_manager.task_scorer.score_task.assert_called_once()

def test_update_skill_failure(skill_manager, valid_skill):
    skill_manager.task_scorer.score_task.side_effect = Exception("Update failed")
    skill_manager.update_skill(valid_skill, "action", "observation")
    skill_manager.task_scorer.update_task_score.assert_called_once()

def test_get_skill(skill_manager):
    skill_manager.skill_catalog.get_skill.return_value = "mock_skill"
    result = skill_manager.get_skill("test_skill")
    skill_manager.skill_catalog.get_skill.assert_called_with("test_skill")
    assert result == "mock_skill"

def test_add_skill(skill_manager, valid_skill):
    skill_manager.add_skill(valid_skill)
    skill_manager.skill_catalog.add_skill.assert_called_once_with(valid_skill)

def test_remove_skill(skill_manager):
    skill_manager.remove_skill("test_skill")
    skill_manager.skill_catalog.remove_skill.assert_called_once_with("test_skill")

def test_register_skill_plugin(skill_manager):
    skill_manager.register_skill_plugin("test_plugin")
    skill_manager.skill_plugins.register.assert_called_once_with("test_plugin")

def test_load_plugin_success(skill_manager):
    skill_manager.load_plugin("test_plugin")
    skill_manager.skill_plugins.load_plugin.assert_called_once_with("test_plugin")

def test_load_plugin_failure(skill_manager):
    skill_manager.skill_plugins.load_plugin.side_effect = Exception("Load failed")
    skill_manager.load_plugin("test_plugin")
    skill_manager.skill_plugins.unload_plugin.assert_called_once_with("test_plugin")