import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from stop_skill_library.models import PerformanceMetrics
from stop_skill_library.reflection import ReflectionEngine


@pytest.fixture
def reflection_engine():
    return ReflectionEngine()


@pytest.fixture
def mock_performance_tracker():
    with patch('stop_skill_library.reflection.ReflectionEngine.performance_tracker') as mock:
        mock_tracker = Mock()
        mock.return_value = mock_tracker
        yield mock_tracker


@pytest.fixture
def mock_performance_analyzer():
    with patch('stop_skill_library.reflection.ReflectionEngine.performance_analyzer') as mock:
        mock_analyzer = Mock()
        mock.return_value = mock_analyzer
        yield mock_analyzer


def test_reflection_engine_initialization(reflection_engine):
    assert reflection_engine.performance_tracker is not None
    assert reflection_engine.performance_analyzer is not None
    assert reflection_engine.logger is not None


def test_track_performance_valid_input(reflection_engine, mock_performance_tracker):
    metrics_data = {
        'execution_time': 1.5,
        'memory_usage': 100,
        'accuracy': 0.95,
        'success_rate': 0.9,
        'error_count': 2,
        'call_count': 10,
        'metadata': {'test': 'data'}
    }
    
    result = reflection_engine.track_performance('skill_123', metrics_data)
    
    assert isinstance(result, PerformanceMetrics)
    assert result.skill_id == 'skill_123'
    assert result.execution_time == 1.5
    assert result.accuracy == 0.95
    mock_performance_tracker.track.assert_called_once_with(result)


def test_track_performance_invalid_skill_id(reflection, mock_performance_tracker):
    with pytest.raises(ValueError, match="skill_id must be a non-empty string"):
        reflection.track_performance('', {'execution_time': 1.0})


def test_track_performance_invalid_metrics_type(reflection_engine):
    with pytest.raises(ValueError, match="metrics must be a dictionary"):
        reflection_engine.track_performance('skill_123', 'invalid_metrics')


def test_track_performance_missing_metrics(reflection_engine, mock_performance_tracker):
    # Test with missing metrics - should use default values
    result = reflection_engine.track_performance('skill_123', {})
    
    assert result.skill_id == 'skill_123'
    assert result.execution_time == 0
    assert result.memory_usage == 0
    assert result.accuracy == 0.0
    mock_performance_tracker.track.assert_called_once()


def test_analyze_performance_valid_skill_id(reflection_engine, mock_performance_tracker, mock_performance_analyzer):
    mock_performance_tracker.get_metrics.return_value = [MagicMock()]
    mock_performance_analyzer.analyze.return_value = {'insight': 'test insight'}
    
    result = reflection_engine.analyze_performance('skill_123')
    
    assert result == {'insight': 'test insight'}
    mock_performance_tracker.get_metrics.assert_called_with('skill_123')
    mock_performance_analyzer.analyze.assert_called_once()


def test_analyze_performance_invalid_skill_id(reflection_engine):
    with pytest.raises(ValueError, match="skill_id must be a non-empty string"):
        reflection_engine.analyze_performance('')


def test_analyze_performance_no_metrics(reflection_engine, mock_performance_tracker):
    mock_performance_tracker.get_metrics.return_value = []
    
    result = reflection_engine.analyze_performance('skill_123')
    
    assert result == {"error": "No metrics found for analysis"}


def test_generate_report_for_specific_skill(reflection_engine, mock_performance_tracker):
    mock_metrics = Mock(skill_id='skill_123')
    mock_performance_tracker.get_metrics.return_value = mock_metrics
    mock_performance_tracker.generate_report.return_value = {'report': 'test report'}
    
    result = reflection_engine.generate_report('skill_123')
    
    assert 'skill_id' in result
    assert 'report' in result
    assert result['skill_id'] == 'skill_123'


def test_generate_report_for_all_skills(reflection_engine, mock_performance_tracker):
    mock_metrics = [Mock(skill_id='skill_123'), Mock(skill_id='skill_456')]
    mock_performance_tracker.get_all_metrics.return_value = mock_metrics
    mock_performance_tracker.get_metrics.return_value = mock_metrics[0]  # for first metric
    
    # Mock the generate_report and generate_insights methods
    with patch.object(reflection_engine.performance_tracker, 'generate_report') as mock_report:
        with patch.object(reflection_engine.performance_analyzer, 'generate_insights') as mock_insights:
            mock_report.return_value = {'report': 'test report'}
            mock_insights.return_value = {'insight': 'test insight'}
            
            result = reflection_engine.generate_report()
            
            assert 'summary' in result
            assert 'reports' in result
            assert len(result['reports']) == 2


def test_generate_report_no_metrics_found(reflection_engine, mock_performance_tracker):
    mock_performance_tracker.get_metrics.return_value = None
    
    result = reflection_engine.generate_report('nonexistent_skill')
    
    assert result == {"error": "No metrics found for skill nonexistent_skill"}


def test_track_performance_exception_handling(reflection_engine, mock_performance_tracker):
    mock_performance_tracker.track.side_effect = Exception("Tracking failed")
    
    with pytest.raises(Exception, match="Tracking failed"):
        reflection_engine.track_performance('skill_123', {
            'execution_time': 1.0,
            'accuracy': 0.95
        })


def test_analyze_performance_exception_handling(reflection_engine, mock_performance_tracker):
    mock_performance_tracker.get_metrics.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        reflection_engine.analyze_performance('skill_123')


def test_generate_report_exception_handling(reflection_engine):
    with patch.object(reflection_engine.performance_tracker, 'get_metrics') as mock_get:
        mock_get.side_effect = Exception("Report generation failed")
        
        with pytest.raises(ValueError, match="Failed to generate report"):
            reflection_engine.generate_report('skill_123')


def test_track_performance_with_default_values(reflection_engine, mock_performance_tracker):
    metrics_data = {
        'execution_time': 2.0,
        'accuracy': 0.85
        # Other fields will use defaults
    }
    
    result = reflection_engine.track_performance('skill_123', metrics_data)
    
    assert result.execution_time == 2.0
    assert result.accuracy == 0.85
    assert result.memory_usage == 0  # Default value
    assert result.error_count == 0  # Default value
    mock_performance_tracker.track.assert_called_once()


def test_performance_metrics_creation_with_defaults(reflection_engine, mock_performance_tracker):
    # Test when no metrics are provided
    result = reflection_engine.track_performance('skill_123', {})
    
    assert isinstance(result, PerformanceMetrics)
    assert result.skill_id == 'skill_123'
    assert result.execution_time == 0
    assert result.accuracy == 0.0


def test_generate_report_with_analysis_insights(reflection_engine, mock_performance_tracker):
    mock_metrics = Mock()
    mock_performance_tracker.get_metrics.return_value = mock_metrics
    
    with patch.object(reflection_engine.performance_analyzer, 'generate_insights') as mock_insights:
        mock_insights.return_value = {'recommendation': 'optimize memory usage'}
        
        result = reflection_engine.generate_report('skill_123')
        
        assert 'analysis' in result
        assert result['analysis'] == {'recommendation': 'optimize memory usage'}


def test_generate_report_all_skills_summary(reflection_engine, mock_performance_tracker):
    mock_metrics = [Mock(skill_id=f'skill_{i}') for i in range(2)]
    mock_performance_tracker.get_all_metrics.return_value = mock_metrics
    
    with patch.object(reflection_engine.performance_tracker, 'generate_report') as mock_report:
        with patch.object(reflection_engine.performance_analyzer, 'generate_insights') as mock_insights:
            mock_report.return_value = {'summary': 'test summary'}
            mock_insights.return_value = {'insight': 'test insight'}
            
            result = reflection_engine.generate_report()
            
            assert 'summary' in result
            assert len(result['reports']) == 2


def test_performance_metrics_dataclass_creation(reflection_engine, mock_performance_tracker):
    metrics_data = {
        'execution_time': 1.5,
        'memory_usage': 1024,
        'accuracy': 0.92,
        'success_rate': 0.95,
        'error_count': 3,
        'call_count': 15,
        'metadata': {'version': '1.0'}
    }
    
    result = reflection_engine.track_performance('test_skill', metrics_data)
    
    assert result.execution_time == 1.5
    assert result.memory_usage == 1024
    assert result.accuracy == 0.92
    assert result.success_rate == 0.95
    assert result.error_count == 3
    assert result.call_count == 15
    assert result.metadata == {'version': '1.0'}


def test_track_performance_datetime_timestamp(reflection_engine, mock_performance_tracker):
    result = reflection_engine.track_performance('skill_123', {'execution_time': 1.0})
    
    # Check that timestamp is set to current time
    assert isinstance(result.timestamp, datetime)
    assert result.timestamp <= datetime.now()