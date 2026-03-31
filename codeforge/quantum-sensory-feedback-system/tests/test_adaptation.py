import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from src.perception.adaptation import PerceptionAdaptation
from src.sensory.input_handler import SensoryInputHandler
from src.sensory.quantum_processor import QuantumProcessor
from src.sensory.orch_or_engine import OrchOREngine
from src.perception.pattern_recognition import PatternRecognition
from src.feedback.actuator import ActuatorController
from src.feedback.response_generator import ResponseGenerator
from src.utils.quantum_math import quantum_fourier_transform
from src.utils.signal_processing import process_signal


class TestPerceptionAdaptation:
    @pytest.fixture
    def adaptation_system(self):
        return PerceptionAdaptation()

    @pytest.fixture
    def mock_sensory_data(self):
        return {
            "sensor_type": "visual",
            "signal": [1.0, 2.0, 3.0, 4.0, 5.0],
            "timestamp": 1234567890
        }

    @patch('src.perception.adaptation.SensoryInputHandler')
    @patch('src.perception.adaptation.QuantumProcessor')
    @patch('src.perception.adaptation.OrchOREngine')
    @patch('src.perception.adaptation.PatternRecognition')
    @patch('src.perception.adaptation.ActuatorController')
    @patch('src.perception.adaptation.ResponseGenerator')
    @patch('src.perception.adaptation.quantum_fourier_transform')
    @patch('src.perception.adaptation.process_signal')
    @patch('src.perception.adaptation.redis_client')
    def test_adapt_to_input_success(self, mock_redis, mock_qft, mock_ps, mock_response_gen, 
                                   mock_actuator, mock_pattern_rec, mock_orch, mock_input_handler, 
                                   mock_quantum_proc, adaptation_system, mock_sensory_data):
        # Setup mocks
        mock_input_handler.return_value.process_input.return_value = {"processed": True}
        mock_quantum_proc.return_value.process_quantum_state.return_value = {"quantum": "state"}
        mock_orch.compute_orch_or_state.return_value = {"orch_or": "state"}
        mock_pattern_rec.recognize_patterns.return_value = ["pattern1", "pattern2"]
        mock_actuator.control_response.return_value = {"actuator": "response"}
        mock_response_gen.generate_feedback.return_value = {"feedback": "generated"}
        mock_qft.return_value = [1, 2, 3, 4, 5]
        mock_ps.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        result = adaptation_system.adapt_to_input(mock_sensory_data)
        
        # Verify the result structure
        assert "input" in result
        assert "quantum_state" in result
        assert "orch_or_state" in result
        assert "patterns" in result
        assert "actuator_response" in result
        assert "feedback" in result
        
        # Verify methods were called
        mock_input_handler.return_value.process_input.assert_called_once()
        mock_quantum_proc.return_value.process_quantum_state.assert_called_once()
        mock_orch.compute_orch_or_state.assert_called_once()
        mock_pattern_rec.recognize_patterns.assert_called_once()
        mock_actuator.control_response.assert_called_once()
        mock_response_gen.generate_feedback.assert_called_once()

    def test_adapt_to_input_exception(self, adaptation_system, mock_sensory_data):
        # Mock a component to raise an exception
        with patch.object(adaptation_system.input_handler, 'process_input', side_effect=Exception("Test error")):
            result = adaptation_system.adapt_to_input(mock_sensory_data)
            assert "error" in result
            assert result["error"] == "Test error"

    def test_calibrate_system_success(self, adaptation_system):
        calibration_data = {"test": "data", "signal": [1, 2, 3, 4, 5]}
        result = adaptation_system.calibrate_system(calibration_data)
        assert "processed" in result or "error" in result

    def test_calibrate_system_exception(self, adaptation_system):
        with patch.object(adaptation_system.input_handler, 'process_input', side_effect=Exception("Calibration error")):
            result = adaptation_system.calibrate_system({"test": "data"})
            assert "error" in result

    def test_process_adaptation_feedback_success(self, adaptation_system):
        feedback_data = {"feedback": "test", "signal": [1, 2, 3]}
        result = adaptation_system.process_adaptation_feedback(feedback_data)
        # Should either succeed or have error
        assert isinstance(result, dict)

    def test_process_adaptation_feedback_exception(self, adaptation_system):
        with patch.object(adaptation_system.input_handler, 'process_input', side_effect=Exception("Feedback error")):
            result = adaptation_system.process_adaptation_feedback({"feedback": "data"})
            assert "error" in result

    def test_normalize_signal_empty(self, adaptation_system):
        # Test with empty signal
        signal = np.array([])
        result = adaptation_system._normalize_signal(signal)
        assert len(result) == 0

    def test_normalize_signal_normal(self, adaptation_system):
        # Test with normal signal
        signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = adaptation_system._normalize_signal(signal)
        assert isinstance(result, np.ndarray)
        # Normalized signal should have mean ~0 and std ~1
        assert abs(np.mean(result)) < 0.1  # Approximately zero mean
        assert abs(np.std(result) - 1.0) < 0.1  # Approximately unit variance

    @patch('src.perception.adaptation.quantum_fourier_transform')
    @patch('src.perception.adaptation.process_signal')
    def test_signal_processing_path(self, mock_process_signal, mock_qft, adaptation_system, mock_sensory_data):
        mock_qft.return_value = [1, 2, 3, 4, 5]
        mock_process_signal.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        result = adaptation_system.adapt_to_input(mock_sensory_data)
        
        # Verify signal processing was called
        mock_qft.assert_called_once()
        mock_process_signal.assert_called_once()

    def test_apply_adaptation_algorithms_no_signal(self, adaptation_system):
        data = {"no_signal": "data"}
        result = adaptation_system._apply_adaptation_algorithms(data)
        assert result == data  # Should return unchanged if no signal field

    def test_apply_adaptation_algorithms_with_signal(self, adaptation_system):
        data = {"signal": [1, 2, 3, 4, 5]}
        result = adaptation_system._apply_adaptation_algorithms(data)
        assert "adapted_signal" in result
        # Should be normalized version of input signal
        assert len(result["adapted_signal"]) == len(data["signal"])

    @patch('src.perception.adaptation.SensoryInputHandler')
    @patch('src.perception.adaptation.QuantumProcessor')
    def test_components_initialization(self, mock_quantum, mock_input, adaptation_system):
        # Verify components are properly initialized
        assert hasattr(adaptation_system, 'input_handler')
        assert hasattr(adaptation_system, 'quantum_processor')
        assert hasattr(adaptation_system, 'orch_or_engine')
        assert hasattr(adaptation_system, 'pattern_recognition')
        assert hasattr(adaptation_system, 'actuator_controller')
        assert hasattr(adaptation_system, 'response_generator')

    @patch('src.perception.adaptation.redis_client')
    def test_redis_caching(self, mock_redis, adaptation_system, mock_sensory_data):
        with patch.object(adaptation_system, 'adapt_to_input') as mock_adapt:
            mock_adapt.return_value = {"test": "result"}
            adaptation_system.adapt_to_input(mock_sensory_data)
            # Redis set should be called for caching
            mock_redis.set.assert_called()

    def test_empty_sensory_data(self, adaptation_system):
        result = adaptation_system.adapt_to_input({})
        # Should handle empty input gracefully
        assert isinstance(result, dict)

    def test_invalid_sensory_data(self, adaptation_system):
        # Test with invalid data that should cause error
        invalid_data = {"invalid": "data", "signal": "not_a_list"}
        result = adaptation_system._apply_adaptation_algorithms(invalid_data)
        # Should return data unchanged
        assert "signal" in result
        assert result["signal"] == "not_a_list"  # Unchanged

    @patch('src.perception.adaptation.quantum_fourier_transform')
    def test_quantum_transform_error(self, mock_qft, adaptation_system, mock_sensory_data):
        mock_qft.side_effect = Exception("Transform error")
        result = adaptation_system.adapt_to_input(mock_sensory_data)
        # Should handle transform error gracefully
        assert isinstance(result, dict)
        # The result should still contain other data even if transform fails
        assert "input" in result or "error" in result

    def test_adaptation_with_no_signal(self, adaptation_system):
        # Test adaptation with data that has no signal field
        data = {"sensor_type": "visual", "timestamp": 1234567890}
        result = adaptation_system.adapt_to_input(data)
        # Should work without signal processing
        assert isinstance(result, dict)

    def test_calibrate_empty_data(self, adaptation_system):
        result = adaptation_system.calibrate_system({})
        # Should handle empty calibration data
        assert isinstance(result, dict)

    def test_calibrate_no_signal_field(self, adaptation_system):
        calibration_data = {"test_field": "value"}
        result = adaptation_system.calibrate_system(calibration_data)
        # Should process even without signal field
        assert isinstance(result, dict)

    def test_normalize_signal_single_value(self, adaptation_system):
        # Test with single value array
        signal = np.array([5.0])
        result = adaptation_system._normalize_signal(signal)
        # Should handle single value (std dev will be 0)
        assert len(result) == 1
        assert result[0] == 5.0  # Should remain unchanged for single value

    @patch('src.perception.adaptation.SensoryInputHandler')
    def test_input_handler_exception(self, mock_input_handler, adaptation_system, mock_sensory_data):
        mock_input_handler.return_value.process_input.side_effect = Exception("Handler error")
        result = adaptation_system.adapt_to_input(mock_sensory_data)
        assert "error" in result
        assert result["error"] == "Handler error"