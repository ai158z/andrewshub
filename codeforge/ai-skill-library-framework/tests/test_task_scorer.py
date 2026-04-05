import pytest
from unittest.mock import Mock, patch
from src.task_scorer import TaskScorer
from src.models.task_predictor import TaskPredictor
from src.models.task_score_model import TaskScoreModel

class TestTaskScorer:
    @pytest.fixture
    def task_predictor_mock(self):
        return Mock(spec=TaskPredictor)

    @pytest.fixture
    def curiosity_model_mock(self):
        return Mock(spec=TaskScoreModel)

    @pytest.fixture
    def task_scorer(self, task_predictor_mock, curiosity_model_mock):
        return TaskScorer(task_predictor_mock, curiosity_model_mock)

    def test_init_with_defaults(self):
        scorer = TaskScorer()
        assert scorer.task_predictor is None
        assert scorer.curiosity_model is None

    def test_init_with_dependencies(self, task_predictor_mock, curiosity_model_mock):
        scorer = TaskScorer(task_predictor_mock, curiosity_model_mock)
        assert scorer.task_predictor == task_predictor_mock
        assert scorer.curiosity_model == curiosity_model_mock

    def test_predict_outcome_calls_predictor(self, task_scorer, task_predictor_mock):
        input_data = {"task": "test"}
        task_scorer.predict_outcome(input_data)
        task_predictor_mock.predict.assert_called_once_with(input_data)

    def test_predict_outcome_returns_dict(self, task_scorer):
        result = task_scorer.predict_outcome({"task": "test"})
        assert isinstance(result, dict)

    @patch('src.task_scorer.calculate_score')
    @patch('src.task_scorer.normalize_score')
    @patch('src.task_scorer.apply_weights')
    def test_score_task_calls_calculation_functions(self, mock_apply, mock_normalize, mock_calculate, task_scorer):
        mock_calculate.return_value = 0.8
        mock_normalize.return_value = 0.9
        mock_apply.return_value = 1.0
        
        task_description = {"description": "test task"}
        input_data = {"input": "test"}
        score = task_scorer.score_task(task_description, input_data)
        
        mock_calculate.assert_called()
        mock_normalize.assert_called()
        mock_apply.assert_called()
        assert score == 1.0

    def test_score_task_returns_number(self, task_scorer):
        with patch('src.task_scorer.calculate_score') as mock_calculate:
            mock_calculate.return_value = 0.75
            with patch('src.task_scorer.normalize_score') as mock_normalize:
                mock_normalize.return_value = 0.8
                with patch('src.task_scorer.apply_weights') as mock_apply:
                    mock_apply.return_value = 0.9
                    
                    result = task_scorer.score_task({"desc": "test"}, {"input": "data"})
                    assert isinstance(result, (int, float))

    def test_score_task_with_no_models(self):
        scorer = TaskScorer()
        with pytest.raises(AttributeError):
            scorer.score_task({"desc": "test"}, {"input": "data"})

    def test_predict_outcome_with_no_predictor(self):
        scorer = TaskScorer()
        with pytest.raises(AttributeError):
            scorer.predict_outcome({"input": "data"})

    @patch('src.task_scorer.calculate_score', return_value=0.5)
    @patch('src.task_scorer.normalize_score', return_value=0.6)
    @patch('src.task_scorer.apply_weights', return_value=0.7)
    def test_score_task_integration(self, mock_apply, mock_normalize, mock_calculate, task_scorer):
        result = task_scorer.score_task({"desc": "test"}, {"input": "data"})
        assert result == 0.7
        mock_calculate.assert_called_once()
        mock_normalize.assert_called_once()
        mock_apply.assert_called_once()

    def test_predict_outcome_with_none_predictor_raises_error(self):
        scorer = TaskScorer()
        with pytest.raises(AttributeError):
            scorer.predict_outcome({"input": "test"})

    def test_predict_outor_returns_dict(self, task_scorer):
        task_predictor_mock = Mock()
        task_predictor_mock.predict.return_value = {"prediction": "test_result"}
        scorer = TaskScorer(task_predictor_mock)
        result = scorer.predict_outcome({"input": "test"})
        assert result == {"prediction": "test_result"}

    @patch('src.task_scorer.calculate_score')
    def test_score_task_with_empty_input(self, mock_calculate, task_scorer):
        mock_calculate.return_value = 0.0
        with patch('src.task_scorer.normalize_score') as mock_normalize:
            mock_normalize.return_value = 0.0
            with patch('src.task_scorer.apply_weights') as mock_apply:
                mock_apply.return_value = 0.0
                result = task_scorer.score_task({}, {})
                assert result == 0.0

    def test_score_task_with_none_models_raises_error(self):
        scorer = TaskScorer()
        with pytest.raises(AttributeError):
            scorer.score_task({"desc": "test"}, {"input": "data"})

    @patch('src.task_scorer.calculate_score', return_value=1.0)
    @patch('src.task_scorer.normalize_score', return_value=1.0)
    @patch('src.task_scorer.apply_weights', return_value=1.0)
    def test_score_task_with_perfect_score(self, mock_apply, mock_normalize, mock_calculate, task_scorer):
        result = task_scorer.score_task({"desc": "test"}, {"input": "data"})
        assert result == 1.0

    @patch('src.task_scorer.calculate_score', return_value=-0.5)
    @patch('src.task_scorer.normalize_score', return_value=0.5)
    @patch('src.task_scorer.apply_weights', return_value=0.5)
    def test_score_task_with_negative_score(self, mock_apply, mock_normalize, mock_calculate, task_scorer):
        result = task_scorer.score_task({"desc": "test"}, {"input": "data"})
        assert result == 0.5

    def test_predict_outcome_empty_input(self, task_scorer):
        task_predictor_mock = Mock()
        task_predictor_mock.predict.return_value = {}
        scorer = TaskScorer(task_predictor_mock)
        result = scorer.predict_outcome({})
        assert result == {}

    def test_predict_outcome_none_input(self, task_scorer):
        with pytest.raises(TypeError):
            task_scorer.predict_outcome(None)

    def test_score_task_none_input(self, task_scorer):
        with pytest.raises(TypeError):
            task_scorer.score_task(None, {"input": "data"})

    def test_score_task_none_task_description(self, task_scorer):
        with pytest.raises(TypeError):
            task_scorer.score_task(None, None)

    @patch('src.task_scorer.calculate_score')
    def test_score_task_calculation_error(self, mock_calculate, task_scorer):
        mock_calculate.side_effect = Exception("Calculation failed")
        with pytest.raises(Exception):
            task_scorer.score_task({"desc": "test"}, {"input": "data"})

    def test_predict_outcome_model_error(self):
        task_predictor_mock = Mock()
        task_predictor_mock.predict.side_effect = Exception("Model error")
        scorer = TaskScorer(task_predictor_mock)
        with pytest.raises(Exception):
            scorer.predict_outcome({"input": "test"})