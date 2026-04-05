import json
import os
from unittest.mock import patch, mock_open, MagicMock
import pytest
from src.skill_catalog import SkillCatalog
from src.models.skill import Skill

def test_init_with_existing_catalog_file():
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='{"skill1": {"id": "skill1", "name": "test", "description": "test skill", "parameters": {}, "metadata": {}}}')):
            catalog = SkillCatalog("test_catalog.json")
            assert "skill1" in catalog.skills

def test_init_with_nonexistent_catalog_file():
    with patch('os.path.exists', return_value=False):
        catalog = SkillCatalog("nonexistent.json")
        assert len(catalog.skills) == 0

def test_init_with_none_catalog_file():
    catalog = SkillCatalog(None)
    assert catalog.catalog_file is None
    assert len(catalog.skills) == 0

def test_load_skills_file_not_found(caplog):
    with patch('os.path.exists', return_value=False):
        catalog = SkillCatalog("missing.json")
        assert len(catalog.skills) == 0

def test_load_skills_invalid_json(caplog):
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='invalid json')):
            with pytest.raises(json.JSONDecodeError):
                SkillCatalog("test.json")

def test_get_skill_exists():
    catalog = SkillCatalog()
    skill = Skill("skill1", "Test Skill", "A test skill")
    catalog.add_skill(skill)
    retrieved = catalog.get_skill("skill1")
    assert retrieved is not None
    assert retrieved.name == "Test Skill"

def test_get_skill_not_exists():
    catalog = SkillCatalog()
    skill = catalog.get_skill("nonexistent")
    assert skill is None

def test_get_skill_invalid_id():
    catalog = SkillCatalog()
    with pytest.raises(ValueError, match="Skill ID must be a non-empty string"):
        catalog.get_skill("")

def test_get_skill_none_id():
    catalog = SkillCatalog()
    with pytest.raises(ValueError, match="Skill ID must be a non-empty string"):
        catalog.get_skill(None)

def test_add_skill_valid():
    catalog = SkillCatalog()
    skill = Skill("skill1", "Test Skill", "A test skill")
    result = catalog.add_skill(skill)
    assert result is True
    assert "skill1" in catalog.skills

def test_add_skill_invalid_type():
    catalog = SkillCatalog()
    with pytest.raises(TypeError):
        catalog.add_skill("not a skill")

def test_add_skill_no_id():
    catalog = SkillCatalog()
    skill = Skill("", "Test Skill", "A test skill")
    with pytest.raises(ValueError, match="Skill must have a valid skill_id"):
        catalog.add_skill(skill)

def test_remove_skill_exists():
    catalog = SkillCatalog()
    skill = Skill("skill1", "Test Skill", "A test skill")
    catalog.add_skill(skill)
    result = catalog.remove_skill("skill1")
    assert result is True
    assert "skill1" not in catalog.skills

def test_remove_skill_not_exists():
    catalog = SkillCatalog()
    result = catalog.remove_skill("nonexistent")
    assert result is False

def test_remove_skill_invalid_id():
    catalog = SkillCatalog()
    with pytest.raises(ValueError, match="Skill ID must be a non-empty string"):
        catalog.remove_skill("")

def test_list_skills():
    catalog = SkillCatalog()
    skill1 = Skill("skill1", "Skill 1", "First test skill")
    skill2 = Skill("skill2", "Skill 2", "Second test skill")
    catalog.add_skill(skill1)
    catalog.add_skill(skill2)
    skill_ids = catalog.list_skills()
    assert "skill1" in skill_ids
    assert "skill2" in skill_ids
    assert len(skill_ids) == 2

def test_save_catalog_no_file_path():
    catalog = SkillCatalog()
    with pytest.raises(ValueError, match="Catalog file path not set"):
        catalog.save_catalog()

def test_save_catalog_success():
    catalog = SkillCatalog("test.json")
    skill = Skill("skill1", "Test Skill", "A test skill")
    catalog.add_skill(skill)
    
    with patch('builtins.open', mock_open()) as mock_file:
        with patch('json.dump') as mock_json:
            catalog.save_catalog()
            mock_file.assert_called()
            mock_json.assert_called()

def test_save_catalog_exception():
    catalog = SkillCatalog("test.json")
    skill = Skill("skill1", "Test Skill", "A test skill")
    catalog.add_skill(skill)
    
    with patch('builtins.open', side_effect=Exception("File error")):
        with pytest.raises(Exception, match="File error"):
            catalog.save_catalog()