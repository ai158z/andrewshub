import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.task_scorer import TaskScorer
from src.models.task_predictor import TaskPredictor
from src.models.task_score_model import TaskScoreModel


@pytest.fixture
def mock_task_predictor():
    predictor = Mock(spec=TaskPredictor)
    predictor.predict.return_value = 0.8
    return predictor


@pytest.fixture
def mock_task_score_model():
    model = Mock(spec=TaskScoreModel)
    model.calculate_score.return_value = 0.9
    model.get_weights.return_value = {
        'novelty': 0.3,
        'feasibility': 0.5,
        'impact': 0.2
    }
    return model


@pytest.fixture
def task_data():
    return {
        'id': 'test_task_1',
        'description': 'Test task for unit testing',
        'complexity': 5,
        'required_skills': ['skill_a', 'skill_b']
    }


@pytest.fixture
def mock_curiosity_model():
    with patch('src.task_scorer.CuriosityModel') as mock:
        curiosity_instance = Mock()
        curiosity_instance.compute_curiosity.return_value = 0.7
        mock.return_value = curiosity_instance
        yield curiosity_instance


def test_score_task_returns_float(mock_task_predictor, mock_task_score_model, task_data, mock_curiosity_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    score = scorer.score_task(task_data)
    assert isinstance(score, float)
    assert 0 <= score <= 1


def test_score_task_calls_predictor_methods(mock_task_predictor, mock_task_score_model, task_data, mock_curiosity_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        scorer.score_task(task_data)
    
    mock_task_predictor.predict.assert_called()
    mock_task_score_model.calculate_score.assert_called()
    mock_task_score_model.get_weights.assert_called()
    mock_curiosity_model.compute_curiosity.assert_called()


def test_score_task_with_different_curiosity_score(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.6
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(task_data)
        assert isinstance(score, float)
        assert 0 <= score <= 1


def test_predict_outcome_returns_dict(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.6
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        prediction = scorer.predict_outcome(task_data)
        
    assert isinstance(prediction, dict)
    assert 'success_probability' in prediction
    assert 'expected_duration' in prediction
    assert 'resource_requirements' in prediction


def test_predict_outcome_calls_dependencies(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.6
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        scorer.predict_outcome(task_data)
        
    mock_task_predictor.predict.assert_called()
    mock_task_score_model.calculate_score.assert_called()


def test_score_task_with_zero_curiosity(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.0
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(task_data)
        assert isinstance(score, float)
        assert 0 <= score <= 1


def test_score_task_with_high_curiosity_score(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 1.0
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(task_data)
        assert isinstance(score, float)
        assert 0 <= score <= 1


def test_predict_outcome_with_different_task_structure(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    task = {
        'id': 'complex_task',
        'description': 'A complex task',
        'complexity': 10,
        'required_skills': ['skill_a', 'skill_b', 'skill_c', 'skill_d']
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.8
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        prediction = scorer.predict_outcome(task)
        
    assert 'success_probability' in prediction
    assert 'expected_duration' in prediction
    assert 'resource_requirements' in prediction


def test_score_task_with_varied_predictor_output(mock_task_predictor, mock_task_score_model, task_data):
    mock_task_predictor.predict.return_value = 0.95  # High confidence prediction
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.8
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(task_data)
        assert isinstance(score, float)


def test_predict_outcome_with_mocked_return_values(mock_task_predictor, mock_task_score_model, task_data):
    mock_task_predictor.predict.return_value = {
        'success_probability': 0.85,
        'expected_duration': 180,
        'resource_requirements': {'cpu': 4, 'memory': '8GB'}
    }
    
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.7
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        prediction = scorer.predict_outcome(task_data)
        
    assert prediction['success_probability'] == 0.85
    assert prediction['expected_duration'] == 180
    assert prediction['resource_requirements'] == {'cpu': 4, 'memory': '8GB'}


def test_score_task_with_edge_case_task(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    edge_task = {
        'id': '',
        'description': '',
        'complexity': 0,
        'required_skills': []
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.5
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(edge_task)
        assert isinstance(score, (int, float))


def test_predict_outcome_with_edge_case_task(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    edge_task = {
        'id': '',
        'description': '',
        'complexity': 0,
        'required_skills': []
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.3
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        prediction = scorer.predict_outcome(edge_task)
        
    assert isinstance(prediction, dict)
    assert 'success_probability' in prediction


def test_score_task_consistency(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.7
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score1 = scorer.score_task(task_data)
        score2 = scorer.score_task(task_data)
        assert score1 == score2  # Should be consistent with same inputs and mocks


def test_predict_outcome_consistency(mock_task_predictor, mock_task_score_model, task_data):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.7
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        pred1 = scorer.predict_outcome(task_data)
        pred2 = scorer.predict_outcome(task_data)
        assert pred1 == pred2  # Should be consistent with same inputs and mocks


def test_score_task_with_none_values(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    task_with_none = {
        'id': None,
        'description': None,
        'complexity': 0,
        'required_skills': []
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.0
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(task_with_none)
        assert isinstance(score, (int, float))


def test_predict_outcome_with_none_values(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    task_with_none = {
        'id': None,
        'description': None,
        'complexity': 0,
        'required_skills': []
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.0
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        prediction = scorer.predict_outcome(task_with_none)
        assert isinstance(prediction, dict)


def test_score_task_with_float_complexity(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    task = {
        'id': 'float_task',
        'description': 'Task with float complexity',
        'complexity': 3.5,  # Float complexity
        'required_skills': ['skill_a']
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.5
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        score = scorer.score_task(task)
        assert isinstance(score, (int, float))


def test_predict_outcome_with_float_complexity(mock_task_predictor, mock_task_score_model):
    scorer = TaskScorer(mock_task_predictor, mock_task_score_model)
    task = {
        'id': 'float_task',
        'description': 'Task with float complexity',
        'complexity': 3.5,
        'required_skills': ['skill_a']
    }
    
    mock_curiosity_model = Mock()
    mock_curiosity_model.compute_curiosity.return_value = 0.5
    
    with patch('src.task_scorer.CuriosityModel', return_value=mock_curiosity_model):
        prediction = scorer.predict_outcome(task)
        assert isinstance(prediction, dict)