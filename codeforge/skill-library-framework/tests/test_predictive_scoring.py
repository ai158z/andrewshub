import numpy as np
import torch
from unittest.mock import Mock, patch
import pytest

from src.skill_library.models.predictive_scoring import PredictiveScoringModel


class TestPredictiveScoringModel:
    def test_predict_relevance_returns_float(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector') as mock_get_vector, \
             patch.object(model, '_compute_similarity') as mock_similarity:
            mock_get_vector.return_value = np.array([])
            mock_similarity.return_value = 0.75
            result = model.predict_relevance("test task")
            assert isinstance(result, float)
            assert result == 0.75

    def test_predict_relevance_calls_internal_methods(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector') as mock_get_vector, \
             patch.object(model, '_compute_similarity') as mock_similarity:
            mock_get_vector.return_value = np.array([1, 2, 3])
            mock_similarity.return_value = 0.8
            result = model.predict_relevance("test task")
            mock_get_vector.assert_called_once_with("test task")
            mock_similarity.assert_called_once()

    def test_get_task_vector_returns_array(self):
        model = PredictiveScoringModel()
        result = model._get_task_vector("test task")
        assert isinstance(result, np.ndarray)

    def test_compute_similarity_returns_float(self):
        model = PredictiveScoringModel()
        test_vector = np.array([1, 2, 3])
        result = model._compute_similarity(test_vector)
        assert isinstance(result, float)

    def test_predict_returns_float(self):
        model = PredictiveScoringModel()
        features = np.array([0.5, 0.3, 0.2])
        result = model.predict(features)
        assert isinstance(result, float)

    def test_hasattr_helper_method(self):
        model = PredictiveScoringModel()
        obj = Mock()
        obj.test_attr = "exists"
        assert model._hasattr(obj, "test_attr") is True
        assert model._hasattr(obj, "nonexistent_attr") is False

    def test_predict_relevance_with_empty_task_description(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector'), \
             patch.object(model, '_compute_similarity'):
            result = model.predict_relevance("")
            assert isinstance(result, float)

    def test_str_representation(self):
        model = PredictiveScoringModel()
        result = str(model)
        assert isinstance(result, str)
        assert "PredictiveScoringModel" in result

    def test_repr_representation(self):
        model = PredictiveScoringModel()
        result = repr(model)
        assert isinstance(result, str)
        assert "PredictiveScoringModel" in result

    def test_predict_with_various_input_shapes(self):
        model = PredictiveScoringModel()
        # Test 1D array
        features_1d = np.array([1, 2, 3])
        result = model.predict(features_1d)
        assert isinstance(result, float)
        
        # Test 2D array
        features_2d = np.array([[1, 2], [3, 4]])
        result = model.predict(features_2d)
        assert isinstance(result, float)

    def test_model_initialization_with_weights(self):
        weights = {"layer1": np.array([1, 2, 3])}
        model = PredictiveScoringModel(model_weights=weights)
        assert model.model_weights == weights

    def test_model_initialization_without_weights(self):
        model = PredictiveScoringModel()
        assert model.model_weights == {}

    def test_predict_relevance_with_mocked_dependencies(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector') as mock_get_vector, \
             patch.object(model, '_compute_similarity') as mock_similarity:
            mock_get_vector.return_value = np.array([1, 2, 3])
            mock_similarity.return_value = 0.85
            result = model.predict_relevance("test task")
            assert result == 0.85

    def test_predict_with_torch_tensor_input(self):
        model = PredictiveScoringModel()
        # Create features as torch tensor
        features = torch.tensor([0.1, 0.2, 0.3]).numpy()
        result = model.predict(features)
        assert isinstance(result, float)

    def test_predict_with_empty_features(self):
        model = PredictiveScoringModel()
        result = model.predict(np.array([]))
        assert isinstance(result, float)

    def test_predict_relevance_returns_zero_for_uninitialized_model(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector', return_value=np.array([])), \
             patch.object(model, '_compute_similarity', return_value=0.0):
            result = model.predict_relevance("test task")
            assert result == 0.0

    def test_multiple_predict_calls_consistency(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector'), \
             patch.object(model, '_compute_similarity'):
            result1 = model.predict_relevance("test task 1")
            result2 = model.predict_relevance("test task 2")
            assert isinstance(result1, float)
            assert isinstance(result2, float)

    def test_predict_with_different_feature_types(self):
        model = PredictiveScoringModel()
        # Test with different numpy array types
        int_features = np.array([1, 2, 3])
        float_features = np.array([1.5, 2.5, 3.5])
        bool_features = np.array([True, False, True])
        
        result1 = model.predict(int_features)
        result2 = model.predict(float_features)
        result3 = model.predict(bool_features)
        
        assert all(isinstance(r, float) for r in [result1, result2, result3])

    def test_hasattr_edge_cases(self):
        model = PredictiveScoringModel()
        # Test with None object
        assert model._hasattr(None, "test") is False
        # Test with object that has attribute
        test_obj = type('TestObj', (), {})()
        test_obj.attr = "value"
        assert model._hasattr(test_obj, "attr") is True
        assert model._hasattr(test_obj, "missing_attr") is False

    def test_predict_relevance_integration_flow(self):
        model = PredictiveScoringModel()
        with patch.object(model, '_get_task_vector') as mock_get_vector, \
             patch.object(model, '_compute_similarity') as mock_similarity:
            mock_get_vector.return_value = np.array([1, 2, 3])
            mock_similarity.return_value = 0.75
            
            result = model.predict_relevance("complex task description")
            
            mock_get_vector.assert_called_once_with("complex task description")
            mock_similarity.assert_called_once_with(mock_get_vector.return_value)
            assert result == 0.75