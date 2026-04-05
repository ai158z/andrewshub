import pytest
from unittest.mock import Mock
from src.skill_proficiency import SkillProficiencyTracker
from src.models import Skill

def test_update_proficiency_valid_input(skill_proficiency_tracker):
    result = skill_proficulty_tracker.update_proficiency("python_skill", 0.85)
    assert skill_proficiency_tracker.update_proficiency("python_skill", 0.85) == 0.85

def test_update_proficiency_invalid_skill_id():
    skill_proficiency_tracker = SkillProficiencyTracker()
    with pytest.raises(ValueError):
        skill_proficiency_tracker.update_proficiency("", 0.85)

def test_update_proficiency_invalid_proficiency_value():
    skill_proficiency_tracker = SkillProficiencyTracker()
    with pytest.raises(ValueError):
        skill_proficiency_tracker.update_proficiency("skill", -1.5)

def test_get_proficiency_history_invalid_input():
    skill_proficiency_tracker = SkillProficiencyTracker()
    with pytest.raises(ValueError):
        skill_proficiency_tracker.get_proficiency_history("")

def test_get_proficiency_history_non_existent_skill():
    skill_proficiency_tracker = SkillProficiencyTracker()
    history = skill_proficiency_tracker.get_proficiency_history("non_existent")
    assert history == []