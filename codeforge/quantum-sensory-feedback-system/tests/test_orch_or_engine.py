import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.sensory.orch_or_engine import (
    OrchOREngine, 
    SensoryInputHandler, 
    QuantumProcessor, 
    PatternRecognition,
    ActuatorController,
    ResponseGenerator
)

def test_orch_or_engine_initialization():
    engine = OrchOREngine()
    assert engine.sensory_handler is not None
    assert engine.quantum_processor is not None
    assert engine.pattern_recognizer is not None
    assert engine.actuator_controller is not None
    assert engine.response_generator is not None

def test_sensory_input_handler_process_input():
    handler = SensoryInputHandler()
    test_data = {"temp": 1.5, "humidity": 0.8, "pressure": 1013.2}
    result = handler.process_input(test_data)
    
    # Check that values are normalized
    assert result["temp"] == 1.0  # Should be clipped to 1.0
    assert result["humidity"] == 0.8
    assert result["pressure"] == 0.8

def test_sensory_input_handler_with_extreme_values():
    handler = SensoryInputHandler()
    test_data = {"value1": 2.0, "value2": -2.0, "value3": 0.5}
    result = handler.process_input(test_data)
    
    # Check that extreme values are clipped
    assert result["value1"] == 1.0  # Should be clipped to 1.0
    assert result["value2"] == -1.0  # Should be clipped to -1.0
    assert result["value3"] == 0.5    # Should remain unchanged

def test_quantum_processor_process_quantum_state():
    processor = QuantumProcessor()
    test_data = {"sensor1": 0.5, "sensor2": 0.8}
    result = processor.process_quantum_state(test_data)
    
    assert "quantum_processed" in result
    assert "data" in result
    assert "frequencies" in result
    assert "processed_signal" in result

def test_pattern_recognition_recognize_patterns():
    recognizer = PatternRecognition()
    test_data = [1, 2, 3, 4, 5]
    patterns = recognizer.recognize_patterns(test_data)
    
    assert len(patterns) > 0
    assert "frequency" in patterns[0]
    assert "amplitude" in patterns[0]
    assert "phase" in patterns[0]

def test_actuator_controller_control_response():
    controller = ActuatorController()
    input_data = {"motor1": 0.7, "motor2": -0.3}
    result = controller.control_response(input_data)
    
    # Control logic: value * 0.5
    assert result["motor1"] == 0.35
    assert result["motor2"] == -0.15

def test_response_generator_generate_feedback():
    generator = ResponseGenerator()
    processed_data = {"input1": 0.5, "input2": 0.8}
    feedback = generator.generate_feedback(processed_data)
    
    # Feedback logic: value * 2.0
    assert feedback["input1"] == 1.0
    assert feedback["input2"] == 1.6

def test_quantum_fourier_transform():
    data = [1, 2, 3, 4, 5]
    result = quantum_fourier_transform(data)
    
    assert isinstance(result, list)
    assert len(result) == len(data)

def test_process_signal():
    signal = [1, 2, 3, 4, 5]
    processed = process_signal(signal)
    
    assert isinstance(processed, list)
    assert len(processed) == len(signal)

def test_orch_or_engine_compute_orch_or_state():
    engine = OrchOREngine()
    quantum_data = {"sensor1": [1, 2, 3], "sensor2": [0.5, 0.8, 0.2]}
    result = engine.compute_orch_or_state(quantum_data)
    
    assert "sensory_input" in result
    assert "quantum_state" in result
    assert "patterns_detected" in result
    assert "adapted_perception" in result
    assert "feedback_response" in result

def test_orch_or_engine_compute_orch_or_state_error():
    engine = OrchOREngine()
    # Force an error by passing invalid data
    with patch.object(engine.sensory_handler, 'process_input', 
                     side_effect=Exception("Test error")):
        result = engine.compute_orch_or_state({"invalid": "data"})
        assert "error" in result

def test_sensory_input_handler_edge_cases():
    handler = SensoryInputHandler()
    
    # Test with empty dict
    result = handler.process_input({})
    assert result == {}
    
    # Test with None values
    result = handler.process_input({"null": None, "empty": []})
    assert result["null"] is None
    assert result["empty"] == []

def test_pattern_recognition_with_empty_data():
    recognizer = PatternRecognition()
    patterns = recognizer.recognize_patterns([])
    assert patterns == []

def test_pattern_recognition_with_single_value():
    recognizer = PatternRecognition()
    patterns = recognizer.recognize_patterns([1.0])
    
    # Single value should produce one pattern with frequency 0
    assert len(patterns) == 1
    assert patterns[0]["frequency"] == 0

def test_actuator_controller_edge_cases():
    controller = ActuatorController()
    
    # Test with empty input
    result = controller.control_response({})
    assert result == {}
    
    # Test with None values
    result = controller.control_response({"actuator": None})
    assert result["actuator"] is None

def test_response_generator_edge_cases():
    generator = ResponseGenerator()
    
    # Test with empty dict
    result = generator.generate_feedback({})
    assert result == {}

def test_quantum_processor_process_with_various_inputs():
    processor = QuantumProcessor()
    
    # Test with normal values
    result = processor.process_quantum_state({
        "input1": 1.0, 
        "input2": 0.5,
        "input3": -0.5
    })
    
    assert "quantum_processed" in result

def test_orch_or_engine_error_handling():
    engine = OrchOREngine()
    
    # Force error in processing
    with patch('src.sensory.orch_or_engine.SensoryInputHandler.process_input', 
               side_effect=Exception("Forced error")):
        result = engine.compute_orch_or_state({"test": "data"})
        assert "error" in result

def test_orch_or_engine_normal_flow():
    # Test normal flow without errors
    engine = OrchOREngine()
    result = engine.compute_orch_or_state({
        "sensor1": 0.5,
        "sensor2": 0.8
    })
    
    # Should not have error in result
    assert "error" not in result

def test_orch_or_engine_component_initialization():
    # Test that all components are properly initialized
    engine = OrchOREngine()
    assert hasattr(engine, 'sensory_handler')
    assert hasattr(engine, 'quantum_processor')
    assert hasattr(engine, 'pattern_recognizer')
    assert hasattr(engine, 'actuator_controller')
    assert hasattr(engine, 'response_generator')
    assert hasattr(engine, 'adaptation_engine')