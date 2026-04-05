import pytest
from unittest.mock import patch, MagicMock
from src.task_outcome_predictor import TaskOutcomePredictor
from src.models import Task, Skill

class TestTaskOutcomePredictor:
    @pytest.fixture
    def predictor(self):
        return TaskOutcomePredictor()

    @pytest.fixture
    def mock_task(self):
        task = MagicMock()
        task.skills = [MagicMock()]
        task.complexity = 5
        return task

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_returns_expected_dict(self, mock_predict, predictor, mock_task):
        # Setup
        mock_predict.return_value = {'success_probability': 0.85, 'confidence': 0.95}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert isinstance(result, dict)
        assert 'success_probability' in result
        assert 'confidence' in result
        mock_predict.assert_called_once_with(mock_task)

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_with_no_skills(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.skills = []
        mock_task.complexity = 3
        mock_predict.return_value = {'success_probability': 0.5, 'confidence': 0.7}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert isinstance(result, dict)
        mock_predict.assert_called_once_with(mock_task)

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_with_high_complexity(self, mock_predict, predictor, mock_task):
        # Setup
        mock_task.complexity = 10
        mock_predict.return_value = {'success_probability': 0.3, 'confidence': 0.8}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert isinstance(result, dict)
        assert result['success_probability'] == 0.3
        assert result['confidence'] == 0.8

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_returns_true(self, mock_train, predictor):
        # Setup
        mock_train.return_value = True
        tasks = [MagicMock(), MagicMock()]
        for task in tasks:
            task.skills = [MagicMock()]
            task.complexity = 5
            task.success = True
        
        # Act
        result = predictor.train_model(tasks)
        
        # Assert
        assert result is True
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_with_empty_tasks(self, mock_train, predictor):
        # Setup
        mock_train.return_value = False
        
        # Act
        result = predictor.train_model([])
        
        # Assert
        assert result is False
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_with_none_tasks(self, mock_train, predictor):
        # Setup
        mock_train.return_value = False
        
        # Act
        result = predictor.train_model(None)
        
        # Assert
        assert result is False
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_with_zero_complexity(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.skills = [MagicMock()]
        mock_task.complexity = 0
        mock_predict.return_value = {'success_probability': 0.95, 'confidence': 0.9}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert result['success_probability'] == 0.95
        mock_predict.assert_called_once_with(mock_task)

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_various_skill_levels(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.skills = [MagicMock(), MagicMock(), MagicMock()]
        mock_task.complexity = 7
        mock_predict.return_value = {'success_probability': 0.6, 'confidence': 0.85}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert isinstance(result, dict)
        mock_predict.assert_called_once_with(mock_task)

    def test_task_initialization(self, predictor):
        # Act
        task = Task()
        
        # Assert
        assert hasattr(task, 'skills')
        assert hasattr(task, 'complexity')
        assert hasattr(task, 'success')

    def test_skill_initialization(self):
        # Act
        skill = Skill("Python", 80)
        
        # Assert
        assert skill.name == "Python"
        assert skill.level == 80

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_consistent_results(self, mock_predict, predictor, mock_task):
        # Setup
        mock_predict.return_value = {'success_probability': 0.75, 'confidence': 0.9}
        mock_predict.side_effect = [
            {'success_probability': 0.75, 'confidence': 0.9},
            {'success_probability': 0.75, 'confidence': 0.9}
        ]
        
        # Act
        result1 = predictor.predict_outcome(mock_task)
        result2 = predictor.predict_outcome(mock_task)
        
        # Assert
        assert result1 == result2
        assert mock_predict.call_count == 2

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_invalid_input(self, mock_predict, predictor):
        # Setup
        mock_predict.return_value = {'success_probability': 0.0, 'confidence': 0.0}
        
        # Act & Assert
        with pytest.raises((TypeError, AttributeError)):
            predictor.predict_outcome(None)

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_multiple_calls(self, mock_train, predictor):
        # Setup
        mock_train.return_value = True
        tasks = [MagicMock()]
        task = tasks[0]
        task.skills = [MagicMock()]
        task.complexity = 5
        task.success = True
        
        # Act
        result1 = predictor.train_model(tasks)
        result2 = predictor.train_model(tasks)
        
        # Assert
        assert result1 is True
        assert result2 is True
        assert mock_train.call_count == 2

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_boundary_values(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.skills = [MagicMock()]
        mock_task.complexity = 1
        mock_predict.return_value = {'success_probability': 0.99, 'confidence': 0.99}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert result['success_probability'] == 0.99
        assert result['confidence'] == 0.99

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_extreme_complexity(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.complexity = 100
        mock_task.skills = [MagicMock()]
        mock_predict.return_value = {'success_probability': 0.01, 'confidence': 0.1}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert result['success_probability'] <= 1.0
        assert result['confidence'] <= 1.0

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_with_mixed_task_success(self, mock_train, predictor):
        # Setup
        mock_train.return_value = True
        tasks = [MagicMock(), MagicMock()]
        tasks[0].success = True
        tasks[1].success = False
        for task in tasks:
            task.skills = [MagicMock()]
            task.complexity = 5
        
        # Act
        result = predictor.train_model(tasks)
        
        # Assert
        assert result is True
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_single_task(self, mock_train, predictor):
        # Setup
        mock_train.return_value = True
        task = MagicMock()
        task.skills = [MagicMock()]
        task.complexity = 5
        task.success = True
        
        # Act
        result = predictor.train_model([task])
        
        # Assert
        assert result is True
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_no_tasks(self, mock_train, predictor):
        # Setup
        mock_train.return_value = False
        
        # Act
        result = predictor.train_model([])
        
        # Assert
        assert result is False
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_missing_attributes(self, mock_predict, predictor):
        # Setup
        mock_predict.return_value = {'success_probability': 0.0, 'confidence': 0.0}
        
        # Act & Assert
        with pytest.raises((KeyError, AttributeError)):
            task = MagicMock()
            del task.complexity
            predictor.predict_outcome(task)

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_with_none_skills(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.skills = None
        mock_task.complexity = 5
        mock_predict.return_value = {'success_probability': 0.0, 'confidence': 0.0}
        
        # Act & Assert
        with pytest.raises((TypeError, AttributeError)):
            predictor.predict_outcome(mock_task)
            
    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_with_empty_result(self, mock_predict, predictor):
        # Setup
        mock_predict.return_value = {}
        
        # Act
        result = predictor.predict_outcome(MagicMock())
        
        # Assert
        assert result == {}
        assert len(result) == 0

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_invalid_task_data(self, mock_train, predictor):
        # Setup
        mock_train.return_value = False
        
        # Act
        result = predictor.train_model("invalid")
        
        # Assert
        assert result is False
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.train_model')
    def test_train_model_with_none_success(self, mock_train, predictor):
        # Setup
        mock_train.return_value = True
        task = MagicMock()
        task.skills = [MagicMock()]
        task.complexity = 5
        task.success = None
        
        # Act
        result = predictor.train_model([task])
        
        # Assert
        assert result is True
        mock_train.assert_called_once()

    @patch('src.task_outcome_predictor.TaskOutcomePredictor.predict_outcome')
    def test_predict_outcome_with_varied_skill_count(self, mock_predict, predictor):
        # Setup
        mock_task = MagicMock()
        mock_task.skills = [MagicMock() for _ in range(5)]
        mock_task.complexity = 5
        mock_predict.return_value = {'success_probability': 0.7, 'confidence': 0.8}
        
        # Act
        result = predictor.predict_outcome(mock_task)
        
        # Assert
        assert isinstance(result, dict)
        assert 0 <= result['success_probability'] <= 1
        assert 0 <= result['confidence'] <= 1
        mock_predict.assert_called_once_with(mock_task)