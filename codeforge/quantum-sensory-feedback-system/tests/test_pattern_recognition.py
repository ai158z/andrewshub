import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from src.perception.pattern_recognition import PatternRecognition

@pytest.fixture
def pattern_recognizer():
    return PatternRecognition()

@pytest.fixture
def sample_data():
    return [1.0, 2.0, 3.0, 4.0, 5.0]

def test_pattern_recognition_initialization():
    pr = PatternRecognition()
    assert len(pr.patterns) > 0
    assert pr.pattern_threshold == 0.8
    assert pr.min_cluster_size == 3

def test_empty_input_data(pattern_recognizer):
    result = pattern_recognizer.recognize_patterns([])
    assert result == []

def test_invalid_input_type(pattern_recognizer):
    with pytest.raises(ValueError, match="Input data must be a list"):
        pattern_recognizer.recognize_patterns("invalid")

@patch('src.perception.pattern_recognition.process_signal')
@patch('src.perception.pattern_recognition.quantum_fourier_transform')
def test_pattern_recognition_success(mock_qft, mock_process, pattern_recognizer, sample_data):
    mock_process.return_value = [1.0, 2.0, 3.0, 4.0, 5.0]
    mock_qft.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    result = pattern_recognizer.recognize_patterns(sample_data)
    assert isinstance(result, list)

@patch('src.perception.pattern_recognition.process_signal')
@patch('src.perception.pattern_recognition.quantum_fourier_transform')
def test_pattern_recognition_exception_handling(mock_qft, mock_process, pattern_recognizer, sample_data):
    mock_process.side_effect = Exception("Processing error")
    
    with pytest.raises(RuntimeError):
        pattern_recognizer.recognize_patterns(sample_data)

@patch('src.perception.pattern_recognition.linkage')
@patch('src.perception.pattern_recognition.fcluster')
def test_clustering_success(mock_fcluster, mock_linkage, pattern_recognizer):
    mock_linkage.return_value = np.array([[1, 2, 0.5, 1]])
    mock_fcluster.return_value = [1, 1, 2, 2, 3]
    
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = pattern_recognizer._cluster_data(data)
    assert isinstance(result, dict)
    assert len(result) > 0

def test_clustering_empty_data(pattern_recognizer):
    result = pattern_recognizer._cluster_data([])
    assert result == {}

@patch('src.perception.pattern_recognition.linkage')
def test_clustering_exception_handling(mock_linkage, pattern_recognizer):
    mock_linkage.side_effect = Exception("Clustering error")
    
    data = [1.0, 2.0, 3.0]
    result = pattern_recognizer._cluster_data(data)
    assert result == {}

def test_pattern_matching_with_matches(pattern_recognizer):
    data = [1.0, 0.5, 0.8, 0.2]
    clusters = {1: data}
    
    matches = pattern_recognizer._match_patterns(data, clusters)
    assert isinstance(matches, list)

def test_pattern_matching_no_matches(pattern_recognizer):
    data = [10.0, 10.0, 10.0, 10.0]  # Very different from templates
    clusters = {1: data}
    
    matches = pattern_recognizer._match_patterns(data, clusters)
    assert matches == []

def test_pattern_matching_exception_handling(pattern_recognizer):
    # Create a scenario where euclidean distance calculation fails
    data = [1.0]  # Different length than patterns
    clusters = {1: data}
    
    matches = pattern_recognizer._match_patterns(data, clusters)
    assert isinstance(matches, list)

def test_structure_results_with_matches_and_clusters(pattern_recognizer):
    pattern_matches = [{
        "pattern_id": 0,
        "cluster_id": 1,
        "confidence": 0.95,
        "pattern_data": [1.0, 0.5, 0.8, 0.2]
    }]
    clusters = {1: [1.0, 2.0, 3.0], 2: [4.0, 5.0, 6.0]}
    
    results = pattern_recognizer._structure_results(pattern_matches, clusters)
    assert isinstance(results, list)
    assert len(results) == 3  # 1 match result + 2 cluster summaries

def test_structure_results_no_matches(pattern_recognizer):
    pattern_matches = []
    clusters = {1: [1.0, 2.0, 3.0], 2: [4.0, 5.0, 6.0]}
    
    results = pattern_recognizer._structure_results(pattern_matches, clusters)
    assert len(results) == 2  # Only cluster summaries

def test_structure_results_missing_fields(pattern_recognizer):
    # Test with incomplete match data
    pattern_matches = [{}]
    clusters = {1: [1.0, 2.0, 3.0]}
    
    results = pattern_recognizer._structure_results(pattern_matches, clusters)
    assert len(results) == 1
    assert "cluster_id" in results[0]

@patch('src.perception.pattern_recognition.process_signal')
@patch('src.perception.pattern_recognition.quantum_fourier_transform')
@patch('src.perception.pattern_recognition.linkage')
@patch('src.perception.pattern_recognition.fcluster')
def test_full_pattern_recognition_pipeline(mock_fcluster, mock_linkage, mock_qft, mock_process, pattern_recognizer, sample_data):
    # Setup all mocks
    mock_process.return_value = sample_data
    mock_qft.return_value = sample_data
    mock_linkage.return_value = np.array([[1, 2, 0.5, 1]])
    mock_fcluster.return_value = [1, 1, 2, 2, 1]
    
    result = pattern_recognizer.recognize_patterns(sample_data)
    assert isinstance(result, list)

@patch('src.perception.pattern_recognition.process_signal')
def test_pattern_recognition_processing_failure(mock_process, pattern_recognizer, sample_data):
    mock_process.side_effect = Exception("Signal processing error")
    
    with pytest.raises(RuntimeError):
        pattern_recognizer.recognize_patterns(sample_data)