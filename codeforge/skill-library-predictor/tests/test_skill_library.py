import pytest
from unittest.mock import Mock, patch
from src.models import Skill
from src.skill_library import SkillLibrary

def test_init_skill_library():
    library = SkillLibrary()
    assert library.skills == {}
    assert len(library.get_skills()) == 0

def test_add_valid_skill():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    result = library.add_skill(skill)
    assert result is True
    assert len(library.skills) == 1
    assert "test_skill" in library.skills

def test_add_invalid_skill_type():
    library = SkillLibrary()
    with pytest.raises(ValueError, match="Invalid skill object"):
        library.add_skill("not a skill")

def test_add_duplicate_skill():
    library = SkillLibrary()
    skill1 = Mock(spec=Skill)
    skill1.id = "test_skill"
    skill2 = Mock(spec=Skill)
    skill2.id = "test_skill"
    library.add_skill(skill1)
    with pytest.raises(ValueError, match="Skill with id test_skill already exists"):
        library.add_skill(skill2)

def test_get_skills_empty():
    library = SkillLibrary()
    skills = library.get_skills()
    assert skills == []

def test_get_skills_with_items():
    library = SkillLibrary()
    skill1 = Mock(spec=Skill)
    skill1.id = "skill1"
    skill2 = Mock(spec=Skill)
    skill2.id = "skill2"
    library.add_skill(skill1)
    library.add_skill(skill2)
    skills = library.get_skills()
    assert len(skills) == 2
    assert skill1 in skills
    assert skill2 in skills

def test_update_skill_exists():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    result = library.update_skill("test_skill", {"name": "Updated Name"})
    assert result is True

def test_update_skill_not_exists():
    library = SkillLibrary()
    result = library.update_skill("nonexistent", {"name": "Updated Name"})
    assert result is False

def test_update_skill_invalid_field():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    with patch('src.skill_library.logging.warning') as mock_warning:
        library.update_skill("test_skill", {"invalid_field": "value"})
        mock_warning.assert_called()

def test_remove_skill_exists():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    result = library.remove_skill("test_skill")
    assert result is True
    assert "test_skill" not in library.skills

def test_remove_skill_not_exists():
    library = SkillLibrary()
    result = library.remove_skill("nonexistent")
    assert result is False

def test_get_skill_exists():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    result = library.get_skill("test_skill")
    assert result == skill

def test_get_skill_not_exists():
    library = SkillLibrary()
    result = library.get_skill("nonexistent")
    assert result is None

def test_add_skill_logs_info():
    with patch('src.skill_library.logging.info') as mock_info:
        library = SkillLibrary()
        skill = Mock(spec=Skill)
        skill.id = "test_skill"
        library.add_skill(skill)
        mock_info.assert_called_with("Added skill: test_skill")

def test_add_skill_logs_error():
    with patch('src.skill_library.logging.error') as mock_error:
        library = SkillLibrary()
        library.add_skill("not a skill")
        mock_error.assert_called_with("Invalid skill object provided")

def test_add_skill_logs_warning():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    
    with patch('src.skill_library.logging.warning') as mock_warning:
        bad_skill = Mock(spec=Skill)
        bad_skill.id = "test_skill"
        with pytest.raises(ValueError):
            library.add_skill(bad_skill)
        mock_warning.assert_called_with("Skill with id test_skill already exists")

def test_update_skill_logs_info():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    
    with patch('src.skill_library.logging.info') as mock_info:
        library.update_skill("test_skill", {"name": "Updated"})
        mock_info.assert_called_with("Updated skill: test_skill")

def test_remove_skill_logs_info():
    library = SkillLibrary()
    skill = Mock(spec=Skill)
    skill.id = "test_skill"
    library.add_skill(skill)
    
    with patch('src.skill_library.logging.info') as mock_info:
        library.remove_skill("test_skill")
        mock_info.assert_called_with("Removed skill: test_skill")

def test_remove_skill_logs_warning():
    library = SkillLibrary()
    with patch('src.skill_library.logging.warning') as mock_warning:
        library.remove_skill("nonexistent")
        mock_warning.assert_called_with("Skill with id nonexistent not found for removal")