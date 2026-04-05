import numpy as np
import pytest
from unittest.mock import Mock, patch
from src.models.task_predictor import TaskPredictor

@pytest.fixture
def task_predictor():
    return TaskPredictor()

@pytest.fixture
def sample_data():
    X = np.random.random((100, 10))
    y = np.random.random((100, 1))
    return X, y

def test_init_task_predictor():
    predictor = TaskPredictor()
    assert predictor.model is None
    assert predictor.input_dim is None
    assert predictor.output_dim is None

def test_predict_before_training_raises_error(task_predictor):
    with pytest.raises(ValueError, match="Model has not been trained yet."):
        task_predictor.predict({'features': [1, 2, 3]})

def test_train_sets_input_output_dimensions(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    assert task_predictor.input_dim == X.shape[1]
    assert task_predictor.output_dim == 1

def test_train_creates_model(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    assert task_predictor.model is not None

def test_predict_returns_error_when_not_trained(task_predictor):
    result = task_predictor.predict({'features': [1, 2, 3]})
    assert result['status'] == 'error'
    assert 'Model has not been trained yet.' in result['error_message']

def test_predict_successful_prediction(task_predictor, sample_data):
    X, y = sample_data
    task_predict2or.train(X, y)
    
    with patch.object(task_predictor.model, 'predict', return_value=np.array([[0.5]])):
        result = task_predictor.predict({'features': [[1, 2, 3]]})
        assert result['status'] == 'success'

def test_evaluate_before_training_raises_error(task_predictor):
    X_test = np.array([[1, 2, 3]])
    y_test = np.array([1])
    
    with pytest.raises(ValueError, match="Model has not been trained yet."):
        task_predictor.evaluate(X_test, y_test)

def test_evaluate_returns_metrics(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    
    X_test = np.random.random((10, 10))
    y_test = np.random.random((10, 1))
    with patch.object(task_predictor.model, 'predict') as mock_predict:
        mock_predict.return_value = y_test
        result = task_predictor.evaluate(X_test, y_test)
        assert 'mse' in result
        assert 'mae' in result

def test_train_with_empty_data():
    predictor = TaskPredictor()
    X = np.array([])
    y = np.array([])
    with pytest.raises(ValueError):
        predictor.train(X, y)

def test_train_with_1d_data(task_predictor):
    X = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 1, 1, 1, 1])
    predictor = TaskPredictor()
    predictor.epochs = 1  # Reduce epochs for faster testing
    predictor.train(X, y)
    assert predictor.input_dim == 5
    assert predictor.output_dim == 1

def test_predict_with_invalid_input_data(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    result = task_predictor.predict({})
    assert result['status'] == 'error'

def test_predict_with_empty_features(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    result = task_predictor.predict({'features': []})
    assert result['status'] == 'error'

def test_evaluate_with_perfect_predictions(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    
    # Create test data that matches training data shape
    X_test = X[:10]
    y_test = y[:10]
    
    with patch.object(task_predictor.model, 'predict', return_value=y_test):
        result = task_predictor.evaluate(X_test, y_test)
        assert result['mse'] == 0.0
        assert result['mae'] == 0.0

def test_evaluate_with_imperfect_predictions(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    
    X_test = X[:10]
    y_test = y[:10]
    y_pred = y_test + 0.1  # Add some error
    
    with patch.object(task_predictor.model, 'predict', return_value=y_pred):
        result = task_predictor.evaluate(X_test, y_test)
        assert result['mse'] > 0
        assert result['mae'] > 0

def test_train_single_output_dim():
    predictor = TaskPredictor()
    X = np.random.random((100, 5))
    y = np.random.random((100,))  # 1D target
    predictor.train(X, y)
    assert predictor.output_dim == 1

def test_train_multi_output_dim():
    predictor = TaskPredictor()
    X = np.random.random((100, 5))
    y = np.random.random((100, 3))  # Multi-dimensional output
    predictor.train(X, y)
    assert predictor.output_dim == 3

def test_predict_with_exception_handling(task_predictor, sample_data):
    X, y = sample_data
    task_predictor.train(X, y)
    
    with patch.object(task_predictor.model, 'predict', side_effect=Exception('Prediction error')):
        result = task_predictor.predict({'features': [1, 2, 3]})
        assert result['status'] == 'error'
        assert result['error_message'] == 'Prediction error'

def test_train_parameters_set_correctly(task_predictor):
    assert task_predictor.epochs == 100
    assert task_predictor.batch_size == 32
    assert task_predictor.hidden_units == 64
    assert task_predictor.learning_rate == 0.001
    assert task_predictor.optimizer == 'adam'
    assert task_predictor.loss == 'mse'
    assert task_predictor.metrics == ['mae']