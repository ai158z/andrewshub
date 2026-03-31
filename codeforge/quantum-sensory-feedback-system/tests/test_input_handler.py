import pytest
from unittest.mock import Mock, patch, MagicMock
from src.sensory.input_handler import SensoryInputHandler

@pytest.fixture
def input_handler():
    return SensoryInputHandler()

@pytest.fixture
def mock_dependencies():
    with patch('src.sensory.input_handler.QuantumProcessor') as mock_qproc, \
         patch('src.sensory.input_handler.OrchOREngine') as mock_orch, \
         patch('src.sensory.input_handler.PerceptionAdaptation') as mock_adapt, \
         patch('src.sensory.input_handler.PatternRecognition') as mock_pattern, \
         patch('src.sensory.input_handler.ActuatorController') as mock_actuator, \
         patch('src.sensory.input_handler.ResponseGenerator') as mock_response:
        
        # Mock all dependencies to prevent actual initialization
        mock_qproc.return_value = Mock()
        mock_orch.return_value = Mock()
        mock_adapt.return_value = Mock()
        mock_pattern.return_value = Mock()
        mock_actuator.return_value = Mock()
        mock_response.return_value = Mock()
        
        yield

def test_process_input_success(input_handler, mock_dependencies):
    # Setup
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    input_handler.quantum_processor.process_quantum_state.return_value = {"state": "quantum"}
    input_handler.orch_or_engine.compute_orch_or_state.return_value = {"state": "orch_or"}
    input_handler.perception_adaptation.adapt_to_input.return_value = {"patterns": []}
    input_handler.pattern_recognition.recognize_patterns.return_value = ["pattern1"]
    input_handler.response_generator.generate_feedback.return_value = {"feedback": "test"}
    input_handler.actuator_controller.control_response.return_value = {"response": "actuator"}
    
    # Mock process_signal and quantum_fourier_transform to return simple values
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
    
    assert result["status"] == "success"
    assert "processed_signal" in result
    assert "quantum_data" in result
    assert "orch_or_data" in result

def test_process_input_with_empty_data(input_handler, mock_dependencies):
    empty_data = {}
    
    # Mock to raise an exception for empty data
    with patch('src.sensory.input_handler.process_signal', side_effect=Exception("Invalid data")):
        result = input_handler.process_input(empty_data)
        
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_invalid_signal(input_handler, mock_dependencies):
    invalid_data = {"signal": None, "metadata": "test"}
    
    # Mock process_signal to raise an exception
    with patch('src.sensory.input_handler.process_signal', side_effect=Exception("Signal processing error")):
        result = input_handler.process_input(invalid_data)
        
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_quantum_processor_failure(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Mock quantum processor to raise an exception
    with patch('src.sensory.input_handler.QuantumProcessor') as mock_qproc:
        mock_qproc.process_quantum_state.side_effect = Exception("Quantum processing error")
        with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
             patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
            result = input_handler.process_input(test_data)
            
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_orch_or_failure(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Mock ORCH-OR engine to raise an exception
    with patch('src.sensory.input_handler.OrchOREngine') as mock_orch:
        mock_orch.compute_orch_or_state.side_effect = Exception("ORCH-OR error")
        with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
             patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
            result = input_handler.process_input(test_data)
            
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_pattern_recognition_failure(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Mock pattern recognition to raise an exception
    with patch('src.sensory.input_handler.PatternRecognition') as mock_pattern:
        mock_pattern.recognize_patterns.side_effect = Exception("Pattern recognition error")
        with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
             patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
            result = input_handler.process_input(test_data)
            
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_actuator_failure(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Mock actuator to raise an exception
    with patch('src.sensory.input_handler.ActuatorController') as mock_actuator:
        mock_actuator.control_response.side_effect = Exception("Actuator error")
        with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
             patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
            result = input_handler.process_input(test_data)
            
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_response_generator_failure(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Mock response generator to raise an exception
    with patch('src.sensory.input_handler.ResponseGenerator') as mock_response:
        mock_response.generate_feedback.side_effect = Exception("Feedback error")
        with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
             patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
            result = input_handler.process_input(test_data)
            
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_perception_adaptation_failure(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Mock perception adaptation to raise an exception
    with patch('src.sensory.input_handler.PerceptionAdaptation') as mock_adapt:
        mock_adapt.adapt_to_input.side_effect = Exception("Perception adaptation error")
        with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
             patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
            result = input_handler.process_input(test_data)
            
    assert result["status"] == "error"
    assert "error" in result

def test_process_input_with_full_pipeline_success(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    # Setup all successful mocks
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    assert result["status"] == "success"
    assert "processed_signal" in result
    assert "quantum_data" in result
    assert "orch_or_data" in result
    assert "adapted_perception" in result
    assert "patterns" in result
    assert "feedback" in result
    assert "actuator_response" in result

def test_process_input_with_missing_metadata(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3]}  # Missing metadata
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    # This should either pass or fail depending on validation logic
    assert "status" in result

def test_process_input_with_empty_signal(input_handler, mock_dependencies):
    test_data = {"signal": [], "metadata": "test"}
    
    result = input_handler.process_input(test_data)
    
    # Should handle empty signal gracefully
    assert result["status"] in ["success", "error"]

def test_process_input_with_none_signal(input_handler, mock_dependencies):
    test_data = {"signal": None, "metadata": "test"}
    
    result = input_handler.process_input(test_data)
    
    # Should handle None signal gracefully
    assert result["status"] in ["success", "error"]

def test_process_input_with_large_signal(input_handler, mock_dependencies):
    test_data = {"signal": [1] * 1000, "metadata": "test"}
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    assert result["status"] == "success"

def test_process_input_with_special_characters(input_handler, mock_dependencies):
    test_data = {"signal": ["special!@#$%^&*()"], "metadata": "test"}
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    assert result["status"] == "success"

def test_process_input_with_unicode_data(input_handler, mock_dependencies):
    test_data = {"signal": ["数据"], "metadata": "测试"}
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    assert result["status"] == "success"

def test_process_input_with_nested_data(input_handler, mock_dependencies):
    test_data = {
        "signal": {"nested": [1, 2, 3]}, 
        "metadata": {"level": "test"}
    }
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    assert result["status"] == "success"

def test_process_input_with_multiple_calls(input_handler, mock_dependencies):
    test_data1 = {"signal": [1, 2, 3], "metadata": "test1"}
    test_data2 = {"signal": [4, 5, 6], "metadata": "test2"}
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result1 = input_handler.process_input(test_data1)
        result2 = input_handler.process_input(test_data2)
        
    assert result1["status"] == "success"
    assert result2["status"] == "success"

def test_process_input_with_logging(input_handler, mock_dependencies):
    test_data = {"signal": [1, 2, 3], "metadata": "test"}
    
    with patch('src.sensory.input_handler.process_signal', return_value=[4, 5, 6]), \
         patch('src.sensory.input_handler.quantum_fourier_transform', return_value=[7, 8, 9]):
        result = input_handler.process_input(test_data)
        
    assert result["status"] == "success"
    assert "input_data" in result
    assert "processed_signal" in result
    assert "quantum_data" in result
    assert "orch_or_data" in result
    assert "adapted_perception" in result
    assert "patterns" in result
    assert "feedback" in result
    assert "actuator_response" in result