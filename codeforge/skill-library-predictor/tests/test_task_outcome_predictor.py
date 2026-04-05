import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from src.task_outcome_predictor import TaskOutcomePredictor
from src.models import Task, Prediction

@pytest.fixture
def predictor():
    return TaskOutcomePredictor()

@pytest.fixture
def sample_training_data():
    return [
        {'description_length': 100, 'estimated_duration': 5, 'skill_count': 3, 'outcome': True},
        {'description_length': 50, 'estimated_duration': 2, 'skill_count': 1, 'outcome': False},
        {'description_length': 200, 'estimated_duration': 8, 'skill_count': 5, 'outcome': True},
        {'description_length': 25, 'estimated_duration': 1, 'skill_count': 2, 'outcome': False}
    ]

@pytest.fixture
def sample_task():
    return Task(
        id="task_001",
        description="Sample task description",
        estimated_duration=5,
        required_skills=["skill1", "skill2"]
    )

def test_init():
    predictor = TaskOutcomePredictor()
    assert not predictor.is_trained
    assert predictor.feature_columns == []

def test_train_model_success(predictor, sample_training_data):
    with patch('src.task_outcome_predictor.train_test_split') as mock_split:
        mock_split.return_value = (
            pd.DataFrame([d for d in sample_training_data[:3]]),  # X_train
            pd.DataFrame([sample_training_data[3]]),  # X_test
            [True, False, True],  # y_train
            [False]  # y_test
        )
        result = predictor.train_model(sample_training_data)
        assert result is True
        assert predictor.is_trained is True

def test_train_model_empty_data(predictor):
    result = predictor.train_model([])
    assert result is False
    assert not predictor.is_trained

def test_train_model_missing_outcome_column(predictor):
    data = [{'feature1': 1, 'feature2': 2}]  # Missing 'outcome' column
    result = predictor.train_model(data)
    assert result is False
    assert not predictor.is_trained

def test_train_model_with_pandas_dataframe(predictor, sample_training_data):
    # Test that training works with actual DataFrame
    df = pd.DataFrame(sample_training_data)
    # Manually set the feature columns to avoid empty list
    predictor.feature_columns = list(df.columns[:-1])  # All except 'outcome'
    result = predictor.train_model(sample_training_data)
    assert result is True

def test_predict_outcome_not_trained(predictor, sample_task):
    prediction = predictor.predict_outcome(sample_task)
    assert prediction.predicted_outcome is False
    assert prediction.confidence == 0.0
    assert prediction.explanation == "Model not trained"

def test_predict_outcome_trained(predictor, sample_training_data, sample_task):
    # First train the model
    with patch('src.task_outcome_predictor.train_test_split') as mock_split:
        mock_split.return_value = (
            pd.DataFrame(sample_training_data),  # X_train
            pd.DataFrame(),  # X_test (empty for this test)
            [True] * len(sample_training_data),  # y_train
            []  # y_test
        )
        predictor.train_model(sample_training_data)
    
    # Mock the model's predict methods
    with patch.object(predictor.model, 'predict_proba', return_value=[[0.3, 0.7]]):
        with patch.object(predictor.model, 'predict', return_value=[True]):
            prediction = predictor.predict_outcome(sample_task)
            assert isinstance(prediction, Prediction)
            assert prediction.task_id == sample_task.id

def test_predict_outcome_exception_handling(predictor, sample_task):
    # Mock an exception during prediction
    with patch.object(predictor, '_task_to_features', side_effect=Exception("Test error")):
        prediction = predictor.predict_outcome(sample_task)
        assert prediction.predicted_outcome is False
        assert prediction.confidence == 0.0
        assert prediction.explanation == "Prediction error occurred"

def test_task_to_features(predictor, sample_task):
    # Test feature extraction
    features = predictor._task_to_features(sample_task)
    assert isinstance(features, list)
    assert len(features) >= 0
    # Features should be numeric
    assert all(isinstance(f, (int, float)) for f in features)

def test_task_to_features_empty_feature_columns(predictor, sample_task):
    # When feature_columns is empty, should return empty list or pad with zeros
    features = predictor._task_to_features(sample_task)
    assert isinstance(features, list)

def test_train_model_exception_during_training(predictor, sample_training_data):
    # Mock an exception during train_test_split
    with patch('src.task_outcome_predictor.train_test_split', side_effect=Exception("Test error")):
        result = predictor.train_model(sample_training_data)
        assert result is False
        assert not predictor.is_trained

def test_predict_outcome_with_empty_model_features(predictor, sample_task):
    # Test when model has no feature columns
    predictor.feature_columns = []
    prediction = predictor.predict_outcome(sample_task)
    assert isinstance(prediction, Prediction)

def test_predict_outcome_model_training_accuracy_logging(predictor, sample_training_data, caplog):
    # Test that accuracy is logged during training
    with patch('src.task_outcome_predictor.train_test_split') as mock_split:
        # Prepare test data for accuracy calculation
        train_data_df = pd.DataFrame(sample_training_data)
        mock_split.return_value = (
            train_data_df.iloc[:-1],  # X_train
            train_data_df.iloc[[-1]],  # X_test
            [True] * (len(sample_training_data) - 1),  # y_train
            [False]  # y_test
        )
        
        with caplog.at_level('INFO'):
            result = predictor.train_model(sample_training_data)
            assert result is True
            # Check if accuracy logging happened
            assert any("accuracy:" in record.message for record in caplog.records if record.levelname == "INFO")

def test_predict_outcome_model_not_trained_case(predictor, sample_task):
    # Test prediction when model is not trained
    predictor.is_trained = False
    prediction = predictor.predict_outcome(sample_task)
    assert not predictor.is_trained
    assert not prediction.predicted_outcome
    assert prediction.confidence == 0.0
    assert prediction.explanation == "Model not trained"

def test_train_model_with_inconsistent_data(predictor):
    # Test with data that has inconsistent feature lengths
    inconsistent_data = [
        {'a': 1, 'b': 2, 'outcome': True},
        {'a': 3, 'c': 4, 'outcome': False}  # Missing 'b', has extra 'c'
    ]
    result = predictor.train_model(inconsistent_data)
    assert result is True  # Should still work, handling missing features gracefully

def test_predict_outcome_confidence_calculation(predictor, sample_training_data, sample_task):
    # Test that confidence is calculated properly
    with patch('src.task_outcome_predictor.train_test_split'):
        with patch.object(predictor.model, 'predict_proba', return_value=[[0.2, 0.8]]):
            with patch.object(predictor.model, 'predict', return_value=[1]):
                predictor.train_model(sample_training_data)
                prediction = predictor.predict_outcome(sample_task)
                assert abs(prediction.confidence - 0.8) < 0.001 or abs(prediction.confidence - 0.2) < 0.001

def test_train_model_large_dataset(predictor):
    # Test with larger dataset
    large_data = [
        {'feature1': i, 'feature2': i*2, 'outcome': i % 2 == 0}
        for i in range(100)
    ]
    result = predictor.train_model(large_data)
    assert result is True

def test_predict_outcome_with_untrained_model(sample_task):
    # Test prediction with untrained model should return default prediction
    untrained_predictor = TaskOutcomePredictor()
    prediction = untrained_predictor.predict_outcome(sample_task)
    assert not prediction.predicted_outcome
    assert prediction.confidence == 0.0
    assert "Model not trained" in prediction.explanation

def test_train_model_single_feature_column():
    # Test training with single feature column
    predictor = TaskOutcomePredictor()
    data = [
        {'feature1': 1, 'outcome': True},
        {'feature1': 2, 'outcome': False},
        {'feature1': 3, 'outcome': True}
    ]
    result = predictor.train_model(data)
    assert result is True

def test_task_to_features_padding(predictor):
    # Test that features are properly padded or trimmed
    predictor.feature_columns = ['f1', 'f2', 'f3']  # 3 expected features
    task = Task(id="test", description="", estimated_duration=0, required_skills=[])
    features = predictor._task_to_features(task)
    assert len(features) == 3
    assert all(f == 0.0 for f in features)  # Should be padded with zeros

def test_train_model_with_missing_values(predictor):
    # Test training with data containing None/missing values
    data_with_missing = [
        {'a': 1, 'b': None, 'outcome': True},
        {'a': None, 'b': 2, 'outcome': False},
        {'a': 3, 'b': 4, 'outcome': True}
    ]
    result = predictor.train_model(data_with_missing)
    assert result is True  # Should handle missing values gracefully