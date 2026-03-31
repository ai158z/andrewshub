import pytest
import numpy as np
from unittest.mock import Mock, patch
from codonic_layer.interference_tracker import InterferenceTracker

@pytest.fixture
def tracker():
    return InterferenceTracker()

@pytest.fixture
def sample_amplitude_data():
    return np.array([1.0, 2.0, 3.0, 4.0])

@pytest.fixture
def sample_phase_data():
    return np.array([0.1, 0.2, 0.3, 0.4])

def test_init(tracker):
    assert tracker.patterns == []
    assert tracker.current_analysis is None

def test_track_pattern_valid_input(tracker, sample_amplitude_data, sample_phase_data):
    result = tracker.track_pattern(sample_amplitude_data, sample_phase_data, 50.0)
    assert 'amplitude' in result
    assert 'phase' in result
    assert 'timestamp' in result
    assert 'frequency' in result
    assert len(tracker.patterns) == 1

def test_track_pattern_invalid_amplitude(tracker):
    with pytest.raises(ValueError):
        tracker.track_pattern(np.array([]), np.array([1, 2, 3]))

def test_track_pattern_invalid_phase(tracker):
    with pytest.raises(ValueError):
        tracker.track_pattern(np.array([1, 2, 3]), np.array([]))

def test_analyze_interference_valid_input(tracker):
    reference = np.array([1.0, 2.0, 3.0])
    test = np.array([1.1, 2.1, 2.9])
    result = tracker.analyze_interference(reference, test)
    assert 'coherence' in result
    assert 'correlation' in result
    assert 'intensity_ratio' in result

def test_analyze_interference_invalid_reference(tracker):
    with pytest.raises(ValueError):
        tracker.analyze_interference(np.array([]), np.array([1, 2, 3]))

def test_analyze_interference_invalid_test(tracker):
    with pytest.raises(ValueError):
        tracker.analyze_interference(np.array([1, 2, 3]), np.array([]))

def test_predict_interference_valid_input(tracker):
    pattern_history = [
        {'amplitude': [1.0, 2.0], 'phase': [0.1, 0.2]},
        {'amplitude': [1.5, 2.5], 'phase': [0.15, 0.25]}
    ]
    with patch.object(tracker.quantum_states, 'evolve_state', return_value=np.array([1.0])):
        result = tracker.predict_interference(pattern_history)
        assert isinstance(result, np.ndarray)

def test_predict_interference_empty_history(tracker):
    with pytest.raises(ValueError):
        tracker.predict_interference([])

def test_visualize_pattern_valid_input(tracker):
    with patch('matplotlib.pyplot.figure') as mock_fig:
        with patch('matplotlib.pyplot.plot') as mock_plot:
            with patch('matplotlib.pyplot.show') as mock_show:
                tracker.visualize_pattern(np.array([1, 2, 3]))
                mock_plot.assert_called()

def test_visualize_pattern_invalid_input(tracker):
    with pytest.raises(TypeError):
        tracker.visualize_pattern([1, 2, 3])  # Not a numpy array

@patch('matplotlib.pyplot.show')
def test_visualize_pattern_execution(mock_show, tracker):
    pattern = np.array([1.0, 2.0, 3.0])
    tracker.visualize_pattern(pattern, "Test Pattern")
    mock_show.assert_called_once()

def test_track_pattern_stores_data(tracker, sample_amplitude_data, sample_phase_data):
    tracker.track_pattern(sample_amplitude_data, sample_phase_data)
    assert len(tracker.patterns) == 1
    pattern = tracker.patterns[0]
    assert pattern['amplitude'] == sample_amplitude_data.tolist()
    assert pattern['phase'] == sample_phase_data.tolist()
    assert 'timestamp' in pattern

def test_analyze_interference_returns_dict(tracker):
    reference = np.array([1.0, 2.0, 3.0])
    test = np.array([1.1, 2.1, 2.9])
    result = tracker.analyze_interference(reference, test)
    assert isinstance(result, dict)
    assert all(key in result for key in ['coherence', 'correlation', 'intensity_ratio', 'frequency'])

def test_predict_interference_returns_array(tracker):
    pattern_history = [
        {'amplitude': [1.0, 2.0], 'phase': [0.1, 0.2]}
    ]
    with patch.object(tracker.quantum_states, 'evolve_state', return_value=np.array([1.0])):
        result = tracker.predict_interference(pattern_history)
        assert isinstance(result, np.ndarray)

def test_analyze_with_nan_coherence(tracker):
    reference = np.array([np.nan, np.nan])
    test = np.array([np.nan, np.nan])
    result = tracker.analyze_interference(reference, test)
    assert result['coherence'] == 0.0  # Should handle NaN case

def test_analyze_with_zero_division(tracker):
    reference = np.array([0.0, 0.0])
    test = np.array([0.0, 0.0])
    result = tracker.analyze_interference(reference, test)
    assert 'intensity_ratio' in result
    # Should not cause division by zero error

def test_track_pattern_appends_to_patterns(tracker, sample_amplitude_data, sample_phase_data):
    initial_length = len(tracker.patterns)
    tracker.track_pattern(sample_amplitude_data, sample_phase_data)
    assert len(tracker.patterns) == initial_length + 1

def test_analyze_interference_stores_result(tracker):
    reference = np.array([1.0, 2.0, 3.0])
    test = np.array([1.1, 2.1, 2.9])
    tracker.analyze_interference(reference, test)
    assert tracker.current_analysis is not None
    assert isinstance(tracker.current_analysis, dict)