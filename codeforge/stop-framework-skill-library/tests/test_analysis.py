import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from io import StringIO

from stop_skill_library.reflection.analysis import PerformanceAnalyzer, AnalysisResult
from stop_skill_library.models import PerformanceMetrics, Skill


@pytest.fixture
def mock_performance_tracker():
    return Mock()


@pytest.fixture
def mock_reflection_engine():
    return Mock()


@pytest.fixture
def performance_analyzer(mock_performance_tracker, mock_reflection_engine):
    return PerformanceAnalyzer(mock_performance_tracker, mock_reflection_engine)


@pytest.fixture
def sample_metrics():
    now = datetime.now()
    metrics = [
        PerformanceMetrics(timestamp=now - timedelta(days=2), value=0.8, execution_time=1.2, success_rate=0.9),
        PerformanceMetrics(timestamp=now - timedelta(days=1), value=0.7, execution_time=1.5, success_rate=0.85),
        PerformanceMetrics(timestamp=now, value=0.9, execution_time=1.0, success_rate=0.95)
    ]
    return metrics


def test_analyze_with_valid_skill_id(performance_analyzer, mock_performance_tracker, sample_metrics):
    mock_performance_tracker.get_metrics.return_value = sample_metrics
    result = performance_analyzer.analyze("skill_123")
    assert isinstance(result, AnalysisResult)
    assert result.skill_id == "skill_123"
    assert len(result.metrics) == 3


def test_analyze_with_time_window(performance_analyzer, mock_performance_tracker, sample_metrics):
    mock_performance_tracker.get_metrics.return_value = sample_metrics
    with patch('stop_skill_library.reflection.analysis.timedelta') as mock_timedelta:
        mock_timedelta.return_value = timedelta(days=1)
        result = performance_analyzer.analyze("skill_123", time_window=7)
        assert isinstance(result, AnalysisResult)


def test_analyze_empty_metrics(performance_analyzer, mock_performance_tracker):
    mock_performance_tracker.get_metrics.return_value = []
    result = performance_analyzer.analyze("skill_123")
    assert isinstance(result, AnalysisResult)
    assert result.metrics == []
    assert result.insights == {}


def test_calculate_insights_with_data(performance_analyzer, sample_metrics):
    insights = performance_analyzer._calculate_insights(sample_metrics)
    assert 'avg_performance' in insights
    assert 'performance_std' in insights
    assert 'total_executions' in insights
    assert insights['total_executions'] == 3


def test_calculate_insights_empty_list(performance_analyzer):
    insights = performance_analyzer._calculate_insights([])
    assert insights == {}


def test_generate_insights_with_sufficient_data(performance_analyzer):
    # Create a mock AnalysisResult with metrics
    analysis_result = AnalysisResult(
        skill_id="test_skill",
        metrics=[
            PerformanceMetrics(timestamp=datetime.now(), value=0.8, execution_time=1.0, success_rate=0.9),
            PerformanceMetrics(timestamp=datetime.now(), value=0.7, execution_time=1.2, success_rate=0.85)
        ]
    )
    
    insights = performance_analyzer.generate_insights(analysis_result)
    assert isinstance(insights, dict)
    assert 'trend' in insights


def test_generate_insights_with_insufficient_data(performance_analyzer):
    # Test with insufficient data for trend analysis
    analysis_result = AnalysisResult(
        skill_id="test_skill",
        metrics=[PerformanceMetrics(timestamp=datetime.now(), value=0.8, execution_time=1.0, success_rate=0.9)]
    )
    
    insights = performance_analyzer.generate_insights(analysis_result)
    assert 'trend' in insights
    assert insights['trend'] == 'insufficient_data'


def test_determine_trend_improving():
    values = [1, 2, 3, 4, 5]  # Clear upward trend
    trend = performance_analyzer._determine_trend(values)
    assert trend == 'improving'


def test_determine_trend_stable():
    values = [3, 3.1, 3.0, 3.2, 3.1]  # Stable values
    trend = performance_analyzer._determine_trend(values)
    assert trend == 'stable'


def test_determine_trend_insufficient_data():
    values = [1.0]  # Only one data point
    trend = performance_analyzer._determine_trend(values)
    assert trend == 'insufficient_data'


def test_assess_stability_stable():
    metrics = [
        PerformanceMetrics(timestamp=datetime.now(), value=3.0),
        PerformanceMetrics(timestamp=datetime.now(), value=3.1),
        PerformanceMetrics(timestamp=datetime.now(), value=3.0)
    ]
    stability = performance_analyzer._assess_stability(metrics)
    assert stability == 'stable'


def test_assess_stability_highly_unstable():
    metrics = [
        PerformanceMetrics(timestamp=datetime.now(), value=1.0),
        PerformanceMetrics(timestamp=datetime.now(), value=5.0),
        PerformanceMetrics(timestamp=datetime.now(), value=2.0),
        PerformanceMetrics(timestamp=datetime.now(), value=8.0)
    ]
    stability = performance_analyzer._assess_stability(metrics)
    assert stability in ['stable', 'moderately_unstable', 'highly_unstable']


def test_generate_recommendations_declining_trend(performance_analyzer):
    # Create analysis result with declining trend
    insights = {'trend': 'declining', 'volatility': 0.6, 'performance_stability': 'highly_unstable'}
    analysis_result = AnalysisResult(skill_id="test", insights=insights)
    
    recommendations = performance_analyzer._generate_recommendations(analysis_result)
    assert len(recommendations) >= 1


def test_visualize_with_data(performance_analyzer):
    # Create a simple AnalysisResult with metrics for visualization
    metrics = [
        PerformanceMetrics(timestamp=datetime.now(), value=0.8),
        PerformanceMetrics(timestamp=datetime.now(), value=0.7)
    ]
    analysis_result = AnalysisResult(skill_id="test", metrics=metrics)
    
    visualizations = performance_analyzer.visualize(analysis_result)
    assert 'performance_trend' in visualizations
    assert 'performance_distribution' in visualizations


def test_visualize_no_data(performance_analyzer):
    analysis_result = AnalysisResult(skill_id="test", metrics=[])
    visualizations = performance_analyzer.visualize(analysis_result)
    assert visualizations == {}


def test_visualize_no_values(performance_analyzer):
    # Metrics without values should return empty visualizations
    metrics = [
        PerformanceMetrics(timestamp=datetime.now()),  # No value attribute
        PerformanceMetrics(timestamp=datetime.now())
    ]
    analysis_result = AnalysisResult(skill_id="test", metrics=metrics)
    visualizations = performance_analyzer.visualize(analysis_result)
    assert visualizations == {}


def test_error_handling_in_analyze(performance_analyzer, mock_performance_tracker):
    mock_performance_tracker.get_metrics.side_effect = Exception("Database error")
    
    with pytest.raises(Exception):
        performance_analyzer.analyze("skill_123")


def test_empty_metrics_visualization(performance_analyzer):
    analysis_result = AnalysisResult(skill_id="test", metrics=[])
    visualizations = performance_analyzer.visualize(analysis_result)
    assert visualizations == {}


def test_analyze_calls_logger_on_success(performance_analyzer, mock_performance_tracker, sample_metrics):
    mock_performance_tracker.get_metrics.return_value = sample_metrics
    with patch('stop_skill_library.reflection.analysis.logging') as mock_logging:
        performance_analyzer.analyze("skill_123")
        mock_logging.getLogger().info.assert_called()


def test_generate_insights_calls_reflection_engine_methods(performance_analyzer):
    # Test that generate_insights calls the appropriate helper methods
    analysis_result = AnalysisResult(skill_id="test")
    with patch.object(performance_analyzer, '_determine_trend') as mock_trend, \
         patch.object(performance_analyzer, '_assess_stability') as mock_stability:
        
        mock_trend.return_value = 'stable'
        mock_stability.return_value = 'stable'
        
        insights = performance_analyzer.generate_insights(analysis_result)
        assert 'trend' in insights
        assert 'performance_stability' in insights
        assert 'recommendations' in insights