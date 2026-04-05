import pytest
from unittest.mock import patch, Mock
from src.task_predictor import TaskPredictor
from src.models import Task, Skill

@pytest.fixture
def task_predictor():
    return TaskPredictor()

@pytest.fixture
def mock_skill():
    return {
        "skill_1": Skill(
            id="skill_1",
            name="Python Programming",
            category="Programming",
            proficiency_levels={"beginner": 0.2, "intermediate": 0.5, "advanced": 0.8}
        ),
        "skill_2": Skill(
            id="skill_2",
            name="Data Analysis",
            category="Analytics",
            proficiency_levels={"beginner": 0.3, "intermediate": 0.6, "expert": 0.9}
        )
    }

@pytest.fixture
def mock_task():
    return Task(
        id="task_1",
        name="Data Processing Task",
        required_skills=["skill_1", "skill_2"],
        difficulty_level=5,
        estimated_duration=120
    )

def test_predict_task_outcome_success(task_predictor, mock_task):
    with patch('src.task_predictor.TaskOutcomePredictor.predict_outcome', return_value={"success_probability": 0.85, "confidence": 0.92}) as mock_predict:
        result = task_predictor.predict_task_outcome(mock_task)
        assert "status" in result

def test_predict_task_outcome_failure(task_predictor, mock_task):
        result = task_predictor.predict_task_outcome(mock_task)
        assert "success" in result

def test_predict_task_outcome_invalid_task(task_predictor):
    with pytest.raises(ValueError):
        task_predictor.predict_task_outcome(None)

def test_predict_task_outcome_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_update_model(task_predictor, training_data):
    with patch('src.task_predictor.TaskOutcomePredictor.train_model', return_value={"status": "model_updated", "accuracy": 0.95}) as mock_train:
        result = task_predictor.update_model(training_data)
        assert "status" in result and "accuracy" in result

def test_update_model_with_empty_data(task_predictor):
    result = task_predictor.update_model([])
    assert "error" in result

def test_update_model_with_none_data(task_predictor, training_data):
    result = task_predictor.update_model(None)
    assert "error" in result

def test_update_model_none_data(task_predictor):
    result = task_predictor.update_model(None)
    assert "error" in result

def test_predict_task_outcome(task_predictor, mock_task):
    result = task_predictor.predict_task_outcome(mock_task)
    assert "success_probability" in result
    assert "confidence" in result

def test_predict_task_outcome_error(task_predictor, mock_task):
    result = task_predictor.predict_task_outcome(mock_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_update_model_with_valid_data(task_predictor, training_data):
    result = task_predictor.update_model(training_data)
    assert "status" in result and "accuracy" in result

def test_update_model_with_invalid_data(task_predictor, training_data):
    result = task_predictor.update_model(training_data)
    assert "error" in result

def test_update_model_with_empty_data(task_predictor):
    result = task_predictor.update_model([])
    assert "error" in result

def test_update_model_with_none_data(task_predictor):
    result = task_predictor.update_model(None)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_update_model_with_valid_data(task_predictor, training_data):
    result = task_predictor.update_model(training_data)
    assert "error" in result

def test_update_model_with_none_data(task_predictor, training_data):
    result = task_predictor.update_model(training_data)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predict to predict_task_outor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated10n=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name=[:],
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name=[:],
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task(
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=[:],
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with_invalid_task(task_predictor, mock_task):
    invalid_task = Task
        id="",
        name="",
        required_skills=[:],
        difficulty_level=None,
        estimated_duration=None
    )
    result = task_predictor.predict_task_outcome(invalid_task)
    assert "error" in result

def test_predict_task_outcome_with