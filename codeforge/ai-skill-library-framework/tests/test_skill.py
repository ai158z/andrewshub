import pytest
from src.models.skill import Skill, SkillModel
from unittest.mock import patch

def test_skill_initialization_with_valid_data():
    skill = Skill("test_skill", "A test skill", "2.0")
    assert skill.name == "test_skill"
    assert skill.description == "A test skill"

def test_skill_initialization_with_invalid_name():
    with pytest.raises(ValueError, match="Skill name must be a non-empty string"):
        Skill("test", "A test skill")

def test_skill_model_instantiation():
    model = SkillModel()

def test_skill_model_validation():
    with pytest.raises(ValueError):
        Skill("", "test", "1.0").validate()

def test_skill_model_to_dict():
    skill = Skill("test", "A test skill", "1.0")
    result = skill.to_dict()
    expected = {"name": "test", "description": "A test skill", "version": "1.0"}
    assert result == expected

def test_skill_instantiation():
    skill = Skill("test", "A test skill")
    assert skill.name == "test"
    assert skill.description == "A test skill"
    assert skill.version == "1.0"

def test_skill_validation():
    skill = Skill("test", "A test skill", "1.0")
    assert skill.validate()

def test_skill_to_dict():
    skill = Skill("test")
    result = skill.to_dict()
    expected = {"name": "test", "description": "A test skill", "version": "1.0"}
    assert result == expected

def test_skill_repr():
    skill = Skill("test")
    result = skill.__repr__()
    expected_json = '{"name": "test", "description": "A test skill", "version": "1.0"}'
    assert result == expected_json

def test_skill_validation():
    skill = Skill("test", "A test skill", "1.0")
    assert skill.validate()

def test_invalid_skill_name():
    with pytest.raises(ValueError):
        Skill("")  # This should raise a ValueError

def test_empty_description():
    skill = Skill("test", "", "1.0")
    assert skill.description == ""

def test_skill_version():
    skill = Skill("test", "A test skill", "1.0")
    assert skill.version == "1.0"

def test_skill_name_must_be_non_empty():
    assert Skill("test", "A test skill").name == "test"

def test_description_must_be_provided():
    skill = Skill("test", "A test skill")
    assert skill.description == "A test skill"

def test_version_must_be_valid():
    skill = Skill("test", "A test skill", "1.0")
    assert skill.version == "1.0"

def test_skill_with_empty_name_fails():
    with pytest.raises(ValueError):
        Skill("", "A test skill", "")

def test_skill_with_invalid_name():
    skill = Skill("", "A test skill")
    with pytest.raises(ValueError):
        skill.validate()

def test_skill_with_invalid_description():
    skill = Skill("", "A test skill")
    with pytest.raises(ValueError):
        skill.validate()

def test_skill_with_invalid_version():
    skill = Skill("test", "A test skill", "")
    with pytest.raises(ValueError):
        Skill("", "A test skill")

def test_skill_model_validation_fails_without_name():
    with pytest.raises(ValueError):
        SkillModel()

def test_skill_model_validation_with_empty_name():
    skill = Skill("", "A test skill")
    with pytest.raises(ValueError) as e:
        skill.validate()

def test_skill_model_validation_with_invalid_data():
    skill = Skill("test", "A test skill", "1.0")
    skill.name = "updated test"
    skill.description = "A test skill"
    skill._validate_inputs()
    assert skill.name == "test"
    assert skill.description == "A test skill"
    assert skill.version == "1.0"