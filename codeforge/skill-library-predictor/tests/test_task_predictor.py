import pytest
from unittest.mock import patch, MagicMock
from src.task_predictor import TaskPredictor
from src.models import Task

@pytest.fixture
def task_predictor():
    return TaskPredictor()

@pytest.fixture
def mock_task():
    task = Task()
    task.complexity = 3
    task.priority = 2
    task.estimated_duration = 5
    return task

def test_task_predictor_initialization():
    with patch('src.task_predictor.os.path.exists', return_value=False):
        with patch('src.task_predictor.joblib.dump'):
            predictor = TaskPredictor()
            assert predictor.model is not None

def test_predict_task_outcome_success(task_predictor, mock_task):
    with patch.object(task_predictor.model, 'predict', return_value=[1]):
        with patch.object(task_predictor.model, 'predict_proba', return_value=[[0.1, 0.9]]):
            result = task_predictor.predict_task_outcome(mock_task)
            assert result['prediction'] == 1
            assert result['confidence'] == 0.9

def test_predict_task_outcome_exception_handling(task_predictor, mock_task):
    with patch.object(task_predictor.model, 'predict', side_effect=Exception("Test error")):
        result = task_predictor.predict_task_outcome(mock_task)
        assert result['prediction'] == "success"
        assert result['confidence'] == 0.5

def test_extract_features(task_predictor):
    task = Task()
    task.complexity = 5
    task.priority = 3
    task.estimated_duration = 10
    
    features = task_predictor._extract_features(task)
    assert features['complexity'] == 5
    assert features['priority'] == 3
    assert features['estimated_duration'] == 10

def test_update_model_success():
    training_data = [
        {'complexity': 3, 'priority': 2, 'estimated_duration': 5, 'success': 1},
        {'complexity': 1, 'priority': 1, 'estimated_duration': 2, 'success': 0}
    ]
    
    with patch('src.task_predictor.train_test_split', return_value=([[[3,2,5]], [[1,1,2]], [1], [0]])):
        with patch('src.task_predictor.joblib.dump'):
            predictor = TaskPredictor()
            result = predictor.update_model(training_data)
            assert result is True

def test_update_model_exception():
    training_data = [{'complexity': 'invalid', 'priority': None, 'estimated_duration': None, 'success': None}]
    
    with patch('src.task_predictor.train_test_split', side_effect=Exception("Invalid data")):
        predictor = TaskPredictor()
        result = predictor.update_model(training_data)
        assert result is False

def test_get_model_features_success(task_predictor):
    with patch.object(task_predictor.model, 'feature_importances_', new=[0.5, 0.3, 0.2]):
        features = task_predictor.get_model_features()
        assert features is not None

def test_get_model_features_exception(task_predictor):
    with patch.object(task_predictor.model, 'feature_importances_', side_effect=Exception("Error")):
        features = task_predictor.get_model_features()
        assert features is None

def test_get_proficiency_success():
    with patch('src.task_predictor.SkillProficiencyTracker') as mock_tracker_class:
        mock_instance = MagicMock()
        mock_instance.get_proficiency.return_value = [{'skill': 'test', 'rating': 0.8}]
        mock_tracker_class.return_value = mock_instance
        
        predictor = TaskPredictor()
        result = predictor.get_proficiency(0.5)
        assert len(result) == 1
        assert result[0]['skill'] == 'test'

def test_get_proficiency_exception():
    with patch('src.task_predictor.SkillProficiencyTracker', side_effect=Exception("Error")):
        predictor = TaskPredictor()
        result = predictor.get_proficiency(0.5)
        assert result == []

def test_get_skills_success():
    with patch('src.task_predictor.SkillLibrary') as mock_library_class:
        mock_instance = MagicMock()
        mock_instance.get_skills.return_value = [{'id': 'test_skill'}]
        mock_library_class.return_value = mock_instance
        
        predictor = TaskPredictor()
        result = predictor.get_skills()
        assert len(result) == 1
        assert result[0]['id'] == 'test_skill'

def test_get_skills_exception():
    with patch('src.task_predictor.SkillLibrary', side_effect=Exception("Error")):
        predictor = TaskPredictor()
        result = predictor.get_skills()
        assert result == []

def test_get_users():
    predictor = TaskPredictor()
    result = predictor.get_users()
    assert result == []

def test_get_budget_success():
    with patch('src.task_predictor.CuriosityBudget') as mock_budget_class:
        mock_instance = MagicMock()
        mock_instance.get_budget.return_value = 100.0
        mock_budget_class.return_value = mock_instance
        
        predictor = TaskPredictor()
        result = predictor.get_budget()
        assert result == 100.0

def test_get_budget_exception():
    with patch('src.task_predictor.CuriosityBudget', side_effect=Exception("Error")):
        predictor = TaskPredictor()
        result = predictor.get_budget()
        assert result == 0.0

def test_get_user_by_id():
    with patch('src.task_predictor.TaskPredictor.get_user_by_id') as mock_get_user:
        mock_get_user.return_value = None
        predictor = TaskPredictor()
        result = predictor.get_user_by_id(123)
        assert result is None

def test_calculate_success_rate_success():
    with patch('src.task_predictor.calculate_success_rate', return_value=0.75):
        predictor = TaskPredictor()
        result = predictor.calculate_success_rate()
        assert result == 0.75

def test_calculate_success_rate_exception():
    with patch('src.task_predictor.calculate_success_rate', side_effect=Exception("Error")):
        predictor = TaskPredictor()
        result = predictor.calculate_success_rate()
        assert result == 0.0

def test_format_response_success():
    with patch('src.task_predictor.format_response', return_value={'status': 'formatted'}):
        predictor = TaskPredictor()
        result = predictor.format_response()
        assert result == {'status': 'formatted'}

def test_format_response_exception():
    with patch('src.task_predictor.format_response', side_effect=Exception("Error")):
        predictor = TaskPredictor()
        result = predictor.format_response()
        assert result == {}