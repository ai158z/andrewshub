import pytest
from datetime import datetime, timedelta
from src.skill_proficiency import SkillProficiencyTracker

@pytest.fixture
def tracker():
    return SkillProficiencyTracker()

@pytest.fixture
def sample_timestamp():
    return datetime.now()

def test_update_proficiency_valid_data(tracker, sample_timestamp):
    skill_id = "skill_1"
    proficiency_data = {"accuracy": 0.85, "speed": 0.75}
    tracker.update_proficiency(skill_id, proficiency_data, sample_timestamp)
    
    history = tracker.get_proficiency_history(skill_id)
    assert len(history) == 1
    assert history[0]["timestamp"] == sample_timestamp
    assert history[0]["proficiency_data"] == proficiency_data

def test_update_proficiency_invalid_skill_id_type(tracker, sample_timestamp):
    with pytest.raises(ValueError):
        tracker.update_proficiency(123, {"accuracy": 0.8}, sample_timestamp)

def test_update_proficiency_invalid_proficiency_data_type(tracker, sample_timestamp):
    with pytest.raises(ValueError):
        tracker.update_proficiency("skill_1", "invalid_data", sample_timestamp)

def test_update_proficiency_invalid_timestamp_type(tracker):
    with pytest.raises(ValueError):
        tracker.update_proficiency("skill_1", {"accuracy": 0.8}, "invalid_timestamp")

def test_get_proficiency_history_invalid_skill_id(tracker):
    with pytest.raises(ValueError):
        tracker.get_proficiency_history(123)

def test_get_proficiency_history_nonexistent_skill(tracker):
    result = tracker.get_proficiency_history("nonexistent")
    assert result == []

def test_get_proficiency_history_valid(tracker, sample_timestamp):
    skill_id = "skill_1"
    proficiency_data = {"accuracy": 0.9}
    tracker.update_proficiency(skill_id, proficiency_data, sample_timestamp)
    
    history = tracker.get_proficiency_history(skill_id)
    assert len(history) == 1
    assert history[0]["timestamp"] == sample_timestamp
    assert history[0]["proficiency_data"] == proficiency_data

def test_get_skill_trend_invalid_skill_id(tracker):
    with pytest.raises(ValueError):
        tracker.get_skill_trend(123)

def test_get_skill_trend_no_history(tracker):
    result = tracker.get_skill_trend("nonexistent")
    assert result == {}

def test_get_skill_trend_with_history(tracker):
    skill_id = "skill_1"
    now = datetime.now()
    tracker.update_proficiency(skill_id, {"accuracy": 0.8}, now - timedelta(days=5))
    tracker.update_proficiency(skill_id, {"accuracy": 0.9}, now - timedelta(days=2))
    
    trend = tracker.get_skill_trend(skill_id, days=10)
    assert "accuracy" in trend
    assert trend["accuracy"] == 0.85

def test_get_skill_trend_outside_time_window(tracker, sample_timestamp):
    skill_id = "skill_1"
    old_date = datetime.now() - timedelta(days=45)
    tracker.update_proficiency(skill_id, {"accuracy": 0.5}, old_date)
    
    trend = tracker.get_skill_trend(skill_id, days=30)
    assert trend == {}

def test_get_skill_mastery_invalid_skill_id(tracker):
    with pytest.raises(ValueError):
        tracker.get_skill_mastery(123)

def test_get_skill_mastery_no_history(tracker):
    mastery = tracker.get_skill_mastery("nonexistent")
    assert mastery == 0.0

def test_get_skill_mastery_with_history(tracker):
    skill_id = "skill_1"
    tracker.update_proficiency(skill_id, {"accuracy": 0.8, "speed": 0.7}, datetime.now())
    mastery = tracker.get_skill_mastery(skill_id)
    expected = (0.8 + 0.7) / 2
    assert mastery == expected

def test_get_declining_skills_no_data(tracker):
    declining = tracker.get_declining_skills()
    assert declining == []

def test_get_declining_skills_with_decline(tracker):
    skill_id = "skill_1"
    now = datetime.now()
    tracker.update_proficiency("declining_skill", {"accuracy": 0.05}, now)
    tracker.update_proficiency("normal_skill", {"accuracy": 0.8}, now)
    
    declining = tracker.get_declining_skills(threshold=0.1, days=30)
    assert "declining_skill" in declining
    assert "normal_skill" not in declining

def test_get_declining_skills_multiple_metrics(tracker):
    skill_id = "skill_1"
    now = datetime.now()
    tracker.update_proficiency("multi_metric_skill", {"accuracy": 0.05, "speed": 0.8}, now)
    
    declining = tracker.get_declining_skills(threshold=0.1)
    # Should detect decline based on accuracy metric being below threshold
    assert "multi_metric_skill" in declining

def test_get_declining_skills_empty_with_no_data(tracker):
    declining = tracker.get_declining_skills()
    assert declining == []

def test_proficiency_data_structure(tracker, sample_timestamp):
    skill_id = "skill_1"
    proficiency_data = {"accuracy": 0.85}
    tracker.update_proficiency(skill_id, proficiency_data, sample_timestamp)
    
    history = tracker.get_proficiency_history(skill_id)
    assert len(history) == 1
    assert history[0]["timestamp"] == sample_timestamp
    assert "proficiency_data" in history[0]
    assert history[0]["proficiency_data"] == proficiency_data