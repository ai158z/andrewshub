import numpy as np
import pytest
from unittest.mock import Mock, patch
from qml_framework.quantum_processor import QuantumProcessor

class TestQuantumProcessor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.processor = QuantumProcessor()
        self.processor.initialize_framework()
        yield
        # Reset cache between tests
        self.processor._quantum_circuit_cache = {}
        self.processor._model_cache = {}

    def test_initialize_framework_success(self):
        processor = QuantumProcessor()
        result = processor.initialize_framework()
        assert result == True
        assert processor.framework_initialized == True

    def test_initialize_framework_already_initialized(self):
        processor = QuantumProcessor()
        processor.framework_initialized = True
        result = processor.initialize_framework()
        assert result == False

    def test_process_sensory_data_valid_input(self):
        processor = QuantumProcessor()
        processor.initialize_framework()
        data = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = processor.process_sensory_data(data)
        assert result['status'] == 'success'
        assert 'processed_data' in result
        assert 'data_shape' in result

    def test_process_sensory_data_empty_input(self):
        processor = QuantumProcessor()
        result = processor.process_sensory_data(np.array([]))
        assert result['status'] == 'error'

    def test_process_sensory_data_2d_array(self):
        processor = QuantumProcessor()
        data = [[1.0, 2.0], [3.0, 4.0]]
        result = processor.process_sensory_data(data)
        assert result['status'] == 'success'
        assert isinstance(result['processed_data'], np.ndarray)

    def test_process_sensory_data_list_input(self):
        processor = QuantumProcessor()
        data = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        result = processor.process_sensory_data(data)
        assert result['status'] == 'success'

    def test_train_quantum_model_valid_data(self):
        processor = QuantumProcessor()
        training_data = np.array([[1.0, 2.0], [3.0, 4.0]])
        labels = np.array([1, 0])
        result = processor.train_quantum_model(training_data, labels)
        assert result['status'] == 'trained'

    def test_train_quantum_model_empty_data(self):
        processor = QuantumProcessor()
        training_data = np.array([])
        labels = np.array([])
        result = processor.train_quantum_model(training_data, labels)
        assert result['status'] == 'error'

    def test_execute_quantum_computation(self):
        from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
        processor = QuantumProcessor()
        qr = QuantumRegister(2)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr)
        result = processor.execute_quantum_computation(qc)
        assert result['result'] == 'executed'

    def test_process_quantum_data(self):
        processor = QuantumProcessor()
        data = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = processor.process_quantum_data(data)
        assert isinstance(result, np.ndarray)

    def test_get_quantum_circuit_caching(self):
        processor = QuantumProcessor()
        circuit1 = processor.get_quantum_circuit(2)
        circuit2 = processor.get_quantum_circuit(2)
        assert circuit1 is circuit2

    def test_quantum_transform_circuit_creation(self):
        processor = QuantumProcessor()
        processor.initialize_framework()
        # Test that circuit creation works
        circuit = processor._create_feature_circuit(3)
        assert circuit is not None

    def test_process_quantum_data_empty_array(self):
        processor = QuantumProcessor()
        with pytest.raises(ValueError):
            processor.process_quantum_data(np.array([]))

    def test_process_quantum_data_valid_array(self):
        processor = QuantumProcessor()
        data = np.array([[1.0, 2.0]])
        result = processor.process_quantum_data(data)
        assert isinstance(result, np.ndarray)

    def test_process_quantum_data_single_feature(self):
        processor = QuantumProcessor()
        data = np.array([1.0, 2.0, 3.0])
        # Should not raise error for 1D array
        result = processor.process_quantum_data(data)
        assert isinstance(result, np.ndarray)

    def test_process_quantum_data_multiple_features(self):
        processor = QuantumProcessor()
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        result = processor.process_quantum_data(data)
        assert isinstance(result, np.ndarray)

    def test_get_processor_function(self):
        from qml_framework.quantum_processor import get_processor
        processor = get_processor()
        assert processor is not None

    @patch('qiskit_machine_learning.algorithms.QSVR')
    def test_train_model_with_mock(self, mock_qsvr):
        processor = QuantumProcessor()
        mock_qsvr.return_value.fit = Mock()
        training_data = np.array([[1, 2], [3, 4]])
        labels = np.array([0, 1])
        result = processor.train_quantum_model(training_data, labels)
        assert result['status'] == 'trained'

    def test_process_sensory_data_various_inputs(self):
        processor = QuantumProcessor()
        data1 = np.array([[1.0, 2.0]])
        data2 = [[1.0, 2.0]]
        result1 = processor.process_sensory_data(data1)
        result2 = processor.process_sensory_data(data2)
        assert result1['status'] == 'success'
        assert result2['status'] == 'success'