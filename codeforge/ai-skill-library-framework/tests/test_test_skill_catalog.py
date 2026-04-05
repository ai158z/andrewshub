import pytest
import tempfile
import os
import json
from src.skill_catalog import SkillCatalog

@pytest.fixture
def temp_skill_file():
    # Create a temporary skill file for testing
    skill_data = {
        "test_skill_1": {
            "name": "test_skill_1",
            "type": "function",
            "description": "A test skill for testing purposes",
            "parameters": {
                "param1": "value1"
            }
        },
        "test_skill_2": {
            "name": "test_skill_2",
            "type": "function", 
            "description": "Another test skill",
            "parameters": {
                "param1": "value2"
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(skill_data, f, indent=2)
        temp_file_path = f.name
    
    yield temp_file_path
    os.unlink(temp_file_path)

@pytest.fixture
def skill_catalog():
    return SkillCatalog()

def test_load_skills_from_file(skill_catalog, temp_skill_file):
    skill_catalog.load_skills(temp_skill_file)
    assert "test_skill_1" in skill_catalog.skills
    assert "test_skill_2" in skill_catalog.skills

def test_load_skills_file_not_found(skill_catalog):
    with pytest.raises(FileNotFoundError):
        skill_catalog.load_skills("non_existent_file.json")

def test_add_skill(skill_catalog):
    skill_data = {
        "name": "new_skill",
        "type": "function",
        "description": "A new skill",
        "parameters": {"test": "value"}
    }
    
    skill_catalog.add_skill("new_skill", skill_data)
    assert "new_skill" in skill_catalog.skills

def test_remove_existing_skill(skill_catalog):
    skill_data = {
        "name": "removable_skill", 
        "type": "function",
        "description": "A skill to remove",
        "parameters": {"test": "value"}
    }
    
    skill_catalog.add_skill("removable_skill", skill_data)
    assert "removable_skill" in skill_catalog.skills
    
    skill_catalog.remove_skill("removable_skill")
    assert "removable_skill" not in skill_catalog.skills

def test_remove_nonexistent_skill(skill_catalog):
    # Removing a skill that doesn't exist should not raise an error
    skill_catalog.remove_skill("nonexistent_skill")

def test_get_skill_names(skill_catalog):
    skill_data = {
        "sample_skill": {
            "name": "sample_skill",
            "type": "function", 
            "description": "A sample skill",
            "parameters": {"param": "value"}
        }
    }
    
    skill_catalog.add_skill("sample_skill", skill_data)
    skill_names = skill_catalog.get_skill_names()
    assert "sample_skill" in skill_names

def test_get_skill_names_empty_catalog(skill_catalog):
    # Test with empty catalog
    skill_names = skill_catalog.get_skill_names()
    assert skill_names == []

def test_get_skill_details(skill_catalog):
    skill_data = {
        "name": "detailed_skill",
        "type": "function",
        "description": "Skill with details",
        "parameters": {"param": "test_value"}
    }
    
    skill_catalog.add_skill("detailed_skill", skill_data)
    details = skill_catalog.get_skill_details("detailed_skill")
    assert details["name"] == "detailed_skill"
    assert details["parameters"]["param"] == "test_value"

def test_get_skill_details_nonexistent(skill_catalog):
    details = skill_catalog.get_skill_details("nonexistent")
    assert details is None

def test_update_skill_existing(skill_catalog):
    original_data = {
        "name": "update_skill",
        "type": "function",
        "description": "Original description",
        "parameters": {"original": "value"}
    }
    
    skill_catalog.add_skill("update_skill", original_data)
    
    updated_data = {
        "name": "update_skill", 
        "type": "function",
        "description": "Updated description",
        "parameters": {"updated": "value"}
    }
    
    skill_catalog.add_skill("update_skill", updated_data)
    details = skill_catalog.get_skill_details("update_skill")
    assert details["description"] == "Updated description"

def test_clear_catalog(skill_catalog):
    skill_data = {
        "name": "clear_skill",
        "type": "function", 
        "description": "To be cleared",
        "parameters": {"test": "value"}
    }
    skill_catalog.add_skill("clear_skill", skill_data)
    
    skill_catalog.clear()
    assert len(skill_catalog.get_skill_names()) == 0

def test_load_skills_invalid_json(skill_catalog):
    # Create invalid JSON file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_file.write("invalid json content")
        temp_file_path = temp_file.name
    
    try:
        with pytest.raises(json.JSONDecodeError):
            skill_catalog.load_skills(temp_file_path)
    finally:
        os.unlink(temp_file_path)

def test_load_skills_invalid_structure(skill_catalog):
    # Create valid JSON but invalid structure
    invalid_skill_data = {"invalid": "structure"}
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        json.dump(invalid_skill_data, temp_file)
        temp_file_path = temp_file.name
    
    try:
        # Should handle invalid structure gracefully
        skill_catalog.load_skills(temp_file_path)
    finally:
        os.unlink(temp_file_path)

def test_add_skill_none_data(skill_catalog):
    with pytest.raises(TypeError):
        skill_catalog.add_skill("none_data_skill", None)

def test_add_skill_invalid_name(skill_catalog):
    # Test with empty skill name
    skill_data = {
        "name": "",
        "type": "function",
        "description": "Invalid name", 
        "parameters": {"test": "value"}
    }
    
    with pytest.raises(ValueError):
        skill_catalog.add_skill("", skill_data)

def test_skill_with_no_parameters(skill_catalog):
    skill_data = {
        "name": "no_params_skill",
        "type": "function", 
        "description": "Skill without parameters"
        # No parameters key
    }
    
    skill_catalog.add_skill("no_params_skill", skill_data)
    assert "no_params_skill" in skill_catalog.skills

def test_get_skill_details_missing_fields(skill_catalog):
    skill_data = {
        "name": "partial_skill",
        "type": "function"
        # Missing description and parameters
    }
    
    skill_catalog.add_skill("partial_skill", skill_data)
    details = skill_catalog.get_skill_details("partial_skill")
    assert details is not None
    assert "type" in details

def test_load_multiple_skills_same_name(skill_catalog, temp_skill_file):
    # Load skills from file
    skill_catalog.load_skills(temp_skill_file)
    
    # Try to load same file again - should overwrite
    skill_catalog.load_skills(temp_skill_file)
    
    skill_names = skill_catalog.get_skill_names()
    assert len(skill_names) >= 2

def test_add_and_remove_same_skill(skill_catalog):
    skill_data = {
        "name": "temp_skill",
        "type": "function",
        "description": "Temporary",
        "parameters": {"temp": "value"}
    }
    
    skill_catalog.add_skill("temp_skill", skill_data)
    assert "temp_skill" in skill_catalog.skills
    
    skill_catalog.remove_skill("temp_skill")
    assert "temp_skill" not in skill_catalog.skills