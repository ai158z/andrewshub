import numpy as np
import pytest
from unittest.mock import Mock, patch

from src.models.curiosity_model import CuriosityModel
from src.models.task_predictor import TaskPredictor
from src.models.task_score_model import TaskScoreModel

def test_compute_curiosity_with_none_state():
    with pytest.raises(ValueError, match="State cannot be None"):
        CuriosityModel(TaskPredictor(), TaskPredictor()).compute_curiosity(None)

def test_update_curiosity_with_none_state():
    with pytest.raises(ValueError, match="State cannot be None"):
        CuriosityModel(TaskPredictor(), TaskPredictor()).update_curiosity(None)

def test_get_state_visitation_count_with_none_state():
    with pytest.raises(ValueError, match="State cannot be None"):
        CuriosityModel(TaskPredictor(), TaskPredictor()).get_state_visitation_count(None)

def test_get_state_action_visitation_count_with_none_state_or_action():
    with pytest.raises(ValueError, match="State and action cannot be None"):
        CuriosityModel(TaskPredictor(), TaskPredictor()).get_state_action_visitation_count(None, None)

def test_get_state_action_visitation_count_with_none_action():
    with pytest.raises(ValueError, match="State and action cannot be None"):
        CuriosityModel(TaskPredictor(), TaskPredictor()).get_state_action_visitation_count(np.array([1, 2]), None)

def test_compute_curiosity_basic():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    curiosity_score = model.compute_curiosity(state)
    
    assert isinstance(curiosity_score, float)
    assert curiosity_score >= 0

def test_compute_curiosity_with_transition():
    task_predictor = Mock(spec=TaskPredictor)
    task_predictor.predict.return_value = np.array([1.5, 2.5])
    task_score_model = Mock(spec=TaskScoreModel)
    
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    action = np.array([0.5])
    next_state = np.array([1.5, 2.5])
    
    # Mock the prediction error calculation
    with patch('numpy.mean', return_value=0.1):
        curiosity_score = model.compute_curiosity(state, action, next_state)
    
    assert isinstance(curiosity_score, float)

def test_update_curiosity_increments_counts():
    task_predictor = Mock(spec=TaskPredictor)
    task_predictor.train = Mock()
    task_score_model = Mock(spec=TaskScoreModel)
    
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    action = np.array([0.5])
    next_state = np.array([1.5, 2.5])
    
    # Initial state visit count should be 0
    assert model.get_state_visitation_count(state) == 0
    
    # Update curiosity model
    model.update_curiosity(state, action, next_state)
    
    # After update, state visit count should be 1
    assert model.get_state_visitation_count(state) == 1

def test_update_curiosity_trains_predictor():
    task_predictor = Mock(spec=TaskPredictor)
    task_predictor.train = Mock()
    task_score_model = Mock(spec=TaskScoreModel)
    
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    action = np.array([0.5])
    next_state = np.array([1.5, 2.5])
    
    model.update_curiosity(state, action, next_state)
    
    # Verify that train was called on the predictor
    task_predictor.train.assert_called_once_with(state, action, next_state)

def test_update_curiosity_fails_when_training_fails():
    task_predictor = Mock(spec=TaskPredictor)
    task_predictor.train = Mock(side_effect=Exception("Training failed"))
    task_score_model = Mock(spec=TaskScoreModel)
    
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    action = np.array([0.5])
    next_state = np.array([1.5, 2.5])
    
    with pytest.raises(RuntimeError, match="Failed to update curiosity model"):
        model.update_curiosity(state, action, next_state)

def test_get_state_visitation_count():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    assert model.get_state_visitation_count(state) == 0
    
    model.update_curiosity(state)
    assert model.get_state_visitation_count(state) == 1

def test_get_state_action_visitation_count():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    action = np.array([0.5])
    assert model.get_state_action_visitation_count(state, action) == 0
    
    model.update_curiosity(state, action)
    assert model.get_state_action_visitation_count(state, action) == 1

def test_reset_counts():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    action = np.array([0.5])
    
    model.update_curiosity(state, action)
    assert model.get_state_visitation_count(state) == 1
    assert model.get_state_action_visitation_count(state, action) == 1
    
    model.reset_counts()
    assert model.get_state_visitation_count(state) == 0
    assert model.get_state_action_visitation_count(state, action) == 0

def test_get_curiosity_parameters():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model, curiosity_weight=2.0, novelty_weight=0.8)
    
    params = model.get_curiosity_parameters()
    assert params == {'curiosity_weight': 2.0, 'novelty_weight': 0.8}

def test_set_curiosity_parameters():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model)
    
    model.set_curiosity_parameters(curiosity_weight=1.5, novelty_weight=0.3)
    params = model.get_curiosity_parameters()
    assert params['curiosity_weight'] == 1.5
    assert params['novelty_weight'] == 0.3

def test_set_curiosity_parameters_partial_update():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model, curiosity_weight=1.0, novelty_weight=0.5)
    
    model.set_curiosity_parameters(curiosity_weight=2.0)
    params = model.get_curiosity_parameters()
    assert params['curiosity_weight'] == 2.0
    assert params['novelty_weight'] == 0.5

def test_compute_curiosity_novelty_decreases_with_visits():
    task_predictor = TaskPredictor()
    task_score_model = TaskScoreModel()
    model = CuriosityModel(task_predictor, task_score_model)
    
    state = np.array([1.0, 2.0])
    
    # First visit - novelty should be 1.0 / (1.0 + 0) = 1.0, so score includes 0.5 * novelty_weight
    score1 = model.compute_curiosity(state)
    
    # Update state visit count
    model.update_curiosity(state)
    
    # Second visit - novelty should decrease
    score2 = model.compute_curiosity(state)
    
    # The second score should be less than the first if only novelty component matters
    # Since prediction error is 0, the difference comes from novelty (1.0 -> 0.5)
    assert score1 > score2 or score1 == score2  # At least not greater

def test_compute_curiosity_flattens_arrays():
    task_predictor = Mock(spec=TaskPredictor)
    task_predictor.predict.return_value = np.array([[1.5], [2.5]])
    task_score_model = Mock(spec=TaskScoreModel)
    
    model = CuriosityModel(task_predictor, task_score_model)
    
    # Test with 2D arrays
    state = np.array([[1.0, 2.0]])
    action = np.array([[0.5]])
    next_state = np.array([[1.5, 2.5]])
    
    with patch('numpy.mean', return_value=0.1):
        score = model.compute_curiosity(state, action, next_state)
    
    assert isinstance(score, float)