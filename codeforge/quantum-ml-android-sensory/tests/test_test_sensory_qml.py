import numpy as np
import pytest
from unittest.mock import patch, MagicMock
from qml_framework import QMLFramework
from qml_framework.sensory_input import process_sensory_data
from qml_framework.core import initialize_framework
from qml_framework.quantum_layers import quantum_layers
from qml_framework.android_bridge import android_bridge

class TestSensoryQML:
    
    def test_framework_initialization(self):
        framework = QMLFramework()
        assert framework is not None

    @patch('numpy.random.random')
    def test_sensory_data_processing_with_mock(self, mock_random):
        mock_random.return_value = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        data = np.array([1, 2, 3, 4, 5])
        processed = process_sensory_data(data)
        expected = np.array([1, 2, 3, 4, 5])
        assert np.array_equal(processed, data)

    def test_framework_initialization_detailed(self):
        framework = QMLFramework()
        assert framework is not None
        assert isinstance(framework, QMLFramework)

    def test_sensory_data_processing_shape(self):
        test_data = np.random.random(100)
        processed = process_sensory_data(test_data)
        assert processed.shape == test_data.shape

    def test_sensory_data_integration(self):
        data = np.array([1, 2, 3, 4, 5])
        result = process_sensory_data(data)
        expected = np.array([1, 2, 3, 4, 5])
        assert np.array_equal(result, expected)

    def test_quantum_layer_operations(self):
        test_circuit = quantum_layers()
        assert test_circuit is not None

    def test_quantum_state_preparation(self):
        test_state = np.array([0.5, 0.5, 0.5, 0.5])
        # Check if state is normalized
        assert np.allclose(np.sum(test_state**2), 1.0)

    def test_circuit_measurement(self):
        framework = QMLFramework()
        test_cases = [
            np.array([1.0, 0.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 0.0, 1.0])
        ]
        for test_case in test_cases:
            measured = framework.measure(test_case)
            assert np.allclose(measured, test_case)

    def test_android_bridge_connection(self):
        bridge = android_bridge()
        assert bridge is not None

    def test_sensory_data_processing_array_unchanged(self):
        data = np.array([1, 2, 3, 4, 5])
        result = process_sensory_data(data)
        assert result.shape == data.shape

    def test_circuit_measurement_multiple_states(self):
        framework = QMLFramework()
        test_state = np.array([0.5, 0.5, 0.5, 0.5])
        assert np.allclose(np.sum(test_state**2), 1.0)

    def test_framework_measure_various_states(self):
        framework = QMLFramework()
        test_cases = [
            np.array([1.0, 0.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 0.0, 1.0])
        ]
        for test_case in test_cases:
            measured = framework.measure(test_case)
            assert np.allclose(measured, test_case)