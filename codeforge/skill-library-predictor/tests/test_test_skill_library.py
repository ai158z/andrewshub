import pytest
from unittest.mock import Mock
from src.skill_library import SkillLibrary
from src.models import Skill


@pytest.fixture
def skill_library():
    return SkillLibrary()


@pytest.fixture
def test_skill_data():
    return {
        "name": "Python Programming",
        "category": "Programming",
        "description": "Ability to write Python code",
        "proficiency": 80
    }


def test_add_skill_success(skill_library, test_skill_data):
    result = skill_library.add_skill(**test_skill_data)
    assert isinstance(result, Skill)
    assert result.name == test_skill_data["name"]
    assert result.category == test_skill_data["category"]
    assert result.description == test_skill_data["description"]
    assert result.proficiency == test_skill_data["proficiency"]


def test_add_skill_missing_required_field(skill_library):
    with pytest.raises(ValueError):
        skill_library.add_skill(name="Test Skill", category="Test")


def test_get_skills_all(skill_library, test_skill_data):
    skill1 = skill_library.add_skill(**test_skill_data)
    skill2 = skill_library.add_skill(
        name="JavaScript Programming",
        category="Programming",
        description="Ability to write JavaScript code",
        proficiency=75
    )
    
    skills = skill_library.get_skills()
    assert len(skills) >= 2
    assert skill1 in skills
    assert skill2 in skills


def test_get_skills_by_category(skill_library, test_skill_data):
    skill_library.add_skill(**test_skill_data)
    skill_library.add_skill(
        name="JavaScript Programming",
        category="Programming",
        description="Ability to write JavaScript code",
        proficiency=75
    )
    
    programming_skills = skill_library.get_skills(category="Programming")
    assert len(programming_skills) > 0
    for skill in programming_skills:
        assert skill.category == "Programming"


def test_update_skill_success(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    
    updated_skill = skill_library.update_skill(
        skill_id=skill.id,
        name="Advanced Python Programming",
        description="Expert ability to write Python code",
        proficiency=90
    )
    
    assert updated_skill.name == "Advanced Python Programming"
    assert updated_skill.description == "Expert ability to write Python code"
    assert updated_skill.proficiency == 90


def test_update_nonexistent_skill(skill_library):
    with pytest.raises(ValueError):
        skill_library.update_skill(
            skill_id=99999,
            name="Non-existent skill",
            description="This skill doesn't exist",
            proficiency=50
        )


def test_remove_skill_success(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    result = skill_library.remove_skill(skill.id)
    assert result is True


def test_remove_already_removed_skill(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    skill_library.remove_skill(skill.id)
    result = skill_library.remove_skill(skill.id)
    assert result is False


def test_remove_nonexistent_skill(skill_library):
    with pytest.raises(ValueError):
        skill_library.remove_skill(99999)


def test_add_skill_returns_skill_object(skill_library, test_skill_data):
    result = skill_library.add_skill(**test_skill_data)
    assert isinstance(result, Skill)
    skills = skill_library.get_skills()
    assert result in skills


def test_get_skills_returns_list(skill_library, test_skill_data):
    skill_library.add_skill(**test_skill_data)
    skills = skill_library.get_skills()
    assert isinstance(skills, list)


def test_update_skill_fields(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    
    updated_skill = skill_library.update_skill(
        skill_id=skill.id,
        name="Updated Skill",
        description="Updated description",
        proficiency=95
    )
    
    assert updated_skill.name == "Updated Skill"
    assert updated_skill.description == "Updated description"
    assert updated_skill.proficiency == 95


def test_add_multiple_skills(skill_library, test_skill_data):
    skill1 = skill_library.add_skill(**test_skill_data)
    skill2 = skill_library.add_skill(
        name="JavaScript",
        category="Programming",
        description="JS skills",
        proficiency=70
    )
    
    skills = skill_library.get_skills()
    assert len(skills) >= 2
    assert skill1 in skills
    assert skill2 in skills


def test_get_skills_empty_library(skill_library):
    skills = skill_library.get_skills()
    assert isinstance(skills, list)
    assert len(skills) == 0


def test_get_skills_filter_by_category_empty(skill_library):
    skills = skill_library.get_skills(category="NonExistent")
    assert isinstance(skills, list)
    assert len(skills) == 0


def test_update_skill_partial_fields(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    
    # Only update name and description
    updated_skill = skill_library.update_skill(
        skill_id=skill.id,
        name="New Name"
    )
    
    assert updated_skill.name == "New Name"
    assert updated_skill.description == test_skill_data["description"]


def test_add_skill_with_invalid_proficiency(skill_library, test_skill_data):
    # Test with proficiency > 100
    with pytest.raises(ValueError):
        skill_library.add_skill(
            name="Test Skill",
            category="Test",
            description="Test description",
            proficiency=150
        )


def test_skill_uniqueness_by_id(skill_library, test_skill_data):
    skill1 = skill_library.add_skill(**test_skill_data)
    skill2 = skill_library.add_skill(**test_skill_data)
    
    assert skill1.id != skill2.id


def test_remove_skill_updates_collection(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    skills_before = skill_library.get_skills()
    assert skill in skills_before
    
    skill_library.remove_skill(skill.id)
    skills_after = skill_library.get_skills()
    assert skill not in skills_after


def test_update_skill_preserves_id(skill_library, test_skill_data):
    skill = skill_library.add_skill(**test_skill_data)
    original_id = skill.id
    
    updated_skill = skill_library.update_skill(
        skill_id=skill.id,
        name="Updated Name"
    )
    
    assert updated_skill.id == original_id
    assert updated_skill.name == "Updated Name"