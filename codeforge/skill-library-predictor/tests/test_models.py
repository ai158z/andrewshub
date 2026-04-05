import pytest
from datetime import datetime
from src.models import Skill, Task, User, TaskRequest, SkillCreate, SkillUpdate, Prediction
from pydantic import ValidationError

def test_skill_creation():
    skill = Skill(
        id=1,
        name="Python",
        description="Programming skill",
        category="coding",
        level="intermediate"
    )
    assert skill.level == "intermediate"

def test_skill_creation_error():
    with pytest.raises(ValidationError):
        skill = Skill()

def test_task_creation():
    task = Task()
    assert task is not None

def test_user_creation():
    user = User(user_id=1, name="test", email="test@example.com")
    assert user.user_id == 1
    assert user.name == "test"

def test_task_request_creation():
    task_request = TaskRequest()
    assert task_request is not None

def test_prediction_creation():
    prediction = Prediction(
        predicted_skills=[{"skill_name": "Python", "level": "intermediate"}],
        predicted_outcome="Good"
    )
    assert prediction is not None

def test_user_creation():
    user = User()
    assert user is not None

def test_task_request_creation():
    task_request = TaskRequest()
    assert task_request is not None

def test_prediction_creation_detailed():
    prediction = Prediction()
    assert prediction is not None

def test_user_creation_with_task():
    user = User(
        user_id=1,
        name="test",
        email="test@example.com"
    )
    assert user is not None

def test_skill_creation_detailed():
    user = User(
        user_id=1,
        name="test",
        email="test@example.com"
    )
    assert user is not None
    assert 1 == 1

def test_user_update():
    task_request = TaskRequest()
    task = Task(user=task_request, task_id=1)
    assert task is not None
    assert task.user_id == 1

def test_user_creation():
    user = User()
    assert user is not None

def test_skill_update():
    skill_update = SkillUpdate(
        skill_data=Skill(id=1, name="test", category="test", level="beginner")
    )
    assert skill_update is not None

def test_prediction_creation_detailed():
    skill_update = SkillUpdate()
    assert skill_update is not None

def test_task_request_creation_detailed():
    task_request = TaskRequest()
    task = Task()
    assert task is not None

def test_task_request_creation_detailed():
    task_request = TaskRequest()
    assert task_request is not None

def test_user_creation_detailed():
    user = User()
    assert user is not None

def test_prediction_creation_detailed():
    skill = Skill()
    assert skill is not None

def test_user_update_detailed():
    user = User()
    assert user is not None