import pytest
from datetime import datetime
from src.skill_library.core.skill import Skill
from unittest.mock import patch, MagicMock

@pytest.fixture
def skill():
    return Skill(name="test_skill", domain="test_domain")

def test_skill_initialization():
    skill = Skill(name="test_skill", domain="test_domain")
    assert skill.name == "test_skill"
    assert skill.domain == "test_domain"
    assert skill.version == "1.0"
    assert skill.metadata == {}
    assert isinstance(skill.created_at, datetime)
    assert isinstance(skill.updated_at, datetime)
    assert skill.performance_history == []
    assert skill.efficiency_metrics == {}

def test_skill_initialization_with_version():
    skill = Skill(name="test_skill", domain="test_domain", version="2.0")
    assert skill.version == "2.0"

def test_skill_initialization_with_metadata():
    metadata = {"key": "value"}
    skill = Skill(name="test_skill", domain="test_domain", metadata=metadata)
    assert skill.metadata == metadata

def test_skill_evaluate(skill):
    result = skill.evaluate()
    assert result["name"] == "test_skill"
    assert result["domain"] == "test_domain"
    assert result["version"] == "1.0"

def test_skill_update():
    skill = Skill(name="test_skill", domain="test_domain")
    new_metadata = {"accuracy": 0.95}
    result = skill.update(new_metadata)
    assert "accuracy" in result["metadata"]
    assert skill.updated_at != skill.created_at

def test_skill_update_empty_metadata(skill):
    result = skill.update({})
    assert result["metadata"] == {}

def test_skill_update_performance_history():
    skill = Skill(name="test_skill", domain="test_domain")
    new_metadata = {"accuracy": 0.8}
    skill.update(new_metadata)
    assert skill.performance_history[-1] == new_metadata

def test_skill_update_multiple_times():
    skill = Skill(name="test_skill", domain="test_domain")
    update1 = {"accuracy": 0.7}
    update2 = {"accuracy": 0.9}
    skill.update(update1)
    skill.update(update2)
    assert skill.performance_history[-1] == update2
    assert len(skill.performance_history) == 2

def test_skill_evaluate_after_update(skill):
    skill.update({"accuracy": 0.85})
    result = skill.evaluate()
    assert result["metadata"]["accuracy"] == 0.85

def test_skill_default_version():
    skill = Skill(name="test_skill", domain="test_domain")
    assert skill.version == "1.0"

def test_skill_custom_version():
    skill = Skill(name="test_skill", domain="test_domain", version="2.1")
    assert skill.version == "2.1"

def test_skill_metadata_none():
    skill = Skill(name="test_skill", domain="test_domain", metadata=None)
    assert skill.metadata == {}

def test_skill_metadata_empty():
    skill = Skill(name="test_skill", domain="test_domain", metadata={})
    assert skill.metadata == {}

def test_skill_metadata_update():
    skill = Skill(name="test_skill", domain="test_domain", metadata={"initial": "value"})
    skill.update({"updated": "value"})
    assert skill.metadata["initial"] == "value"
    assert skill.metadata["updated"] == "value"

def test_skill_created_updated_timestamps():
    skill = Skill(name="test_skill", domain="test_domain")
    assert skill.created_at <= skill.updated_at

def test_skill_update_modifies_updated_at():
    skill = Skill(name="test_skill", domain="test_domain")
    original_updated = skill.updated_at
    skill.update({"test": "data"})
    assert skill.updated_at > original_updated

def test_skill_performance_history_tracks_updates():
    skill = Skill(name="test_skill", domain="test_domain")
    skill.update({"update1": "data1"})
    skill.update({"update2": "data2"})
    assert len(skill.performance_history) == 2
    assert skill.performance_history == [{"update1": "data1"}, {"update2": "data2"}]

def test_evaluate_returns_correct_structure(skill):
    result = skill.evaluate()
    assert "name" in result
    assert "domain" in result
    assert "version" in result
    assert "metadata" in result
    assert isinstance(result, dict)