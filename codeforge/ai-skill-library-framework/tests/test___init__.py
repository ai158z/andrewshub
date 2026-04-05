import numpy as np
import pytest
from src.models import Skill, TaskPredictor, CuriosityModel, TaskScoreModel

def test_skill_initialization():
    skill = Skill("test_skill", "A test skill", {"test": "value"})
    assert skill.name == "test_skill"
    assert skill.description == "A test skill"
    assert skill.parameters == {"test": "value"}
    assert skill.validate() == True

def test_skill_validation_error():
    with pytest.raises(ValueError):
        Skill("", "test", {})

def test_skill_validation_success():
    skill = Skill("test_skill")
    assert skill.validate() == True

def test_task_predictor_initialization():
    # Test simple features prediction
    predictor = TaskPredictor()
    assert predictor is not None

def test_task_predictor_prediction():
    pred = predictor.predict(np.array([1, 2, 3]))
    assert isinstance(pred, float)

def test_task_predictor_train():
    X = np.random.random((10, 5))
    y = np.random.random(10)
    pred = TaskPredictor()
    metrics = pred.train(X, y)
    assert 'samples' in metrics

def test_curiosity_model():
    model = CuriosityModel()
    state = {"position": [1, 2], "velocity": 0.5}
    curiosity = model.compute_curiosity(state)
    assert isinstance(curiosity, float)

def test_task_score_model_weights():
    weights = {
        'complexity': 0.3,
        'priority': 0.4,
        'resource_cost': 0.2,
        'skill_match': 0.1
    }
    model = TaskScoreModel(weights)
    score = model.calculate_score({
        'complexity': 50,
        'priority': 75,
        'resource_cost': 25,
        'skill_match': 90
    })
    assert score > 0, "Task score should be positive"

def test_task_predictor_evaluate(mocker, mock_data):
    # Mock the data
    mocker.patch('my_module.get_data', return_value=mock_data)
    # Your test logic here
    pass

def test_task_score_model():
    pass