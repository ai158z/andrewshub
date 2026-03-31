import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.sensory.quantum_processor import QuantumProcessor

@pytest.fixture
def quantum_processor():
    return QuantumProcessor()

@pytest.fixture
def sample_input_data():
    return {
        "data": [1.0, 2.0, 3.0, 4.0],
        "timestamp": "2023-01-01T00:00:00Z"
    }

def test_quantum_processor_initialization():
    processor = QuantumProcessor()
    assert processor.quantum_enabled is True
    assert processor.processed_states == []

def test_process_quantum_state_success(quantum_processor, sample_input_data):
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = [0.5, 1.0, 1.5, 2.0]
        
        result = quantum_processor.process_quantum_state(sample_input_data)
        
        assert result["status"] == "processed"
        assert "metadata" in result
        assert result["metadata"]["processor"] == "quantum_state_processor"

def test_process_quantum_state_invalid_input_type(quantum_processor):
    with pytest.raises(RuntimeError):
        quantum_processor.process_quantum_state("invalid_input")

def test_process_quantum_state_empty_data(quantum_processor):
    input_data = {"data": []}
    result = quantum_processor.process_quantum_state(input_data)
    assert result["status"] == "processed"
    assert result["data"]["processed"] is False

def test_process_quantum_state_processing_error(quantum_processor):
    with patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        mock_qft.side_effect = Exception("Processing failed")
        with pytest.raises(RuntimeError):
            quantum_processor.process_quantum_state({"data": [1, 2, 3]})

def test_apply_quantum_transformations_empty_signal(quantum_processor):
    data = {"data": []}
    result = quantum_processor._apply_quantum_transformations(data)
    assert result["processed"] is False
    assert result["result"] is None

def test_apply_quantum_transformations_with_signal(quantum_processor):
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        data = {"data": [1, 2, 3, 4]}
        result = quantum_processor._apply_quantum_transformations(data)
        
        assert result["processed"] is True
        assert "signal" in result
        assert "qft_result" in result
        assert "amplitude" in result
        assert "phase" in result

def test_process_quantum_state_with_valid_signal(quantum_processor, sample_input_data):
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        result = quantum_processor.process_quantum_state(sample_input_data)
        
        assert result["status"] == "processed"
        assert result["data"]["processed"] is True

def test_process_quantum_state_with_exception(quantum_processor, sample_input_data):
    with patch('src.sensory.quantum_processor.process_signal', side_effect=Exception("Test error")):
        with pytest.raises(RuntimeError) as exc_info:
            quantum_processor.process_quantum_state(sample_input_data)
        assert "Quantum processing error" in str(exc_info.value)

def test_process_quantum_state_with_logging_error(quantum_processor, sample_input_data):
    with patch('src.sensory.quantum_processor.logger') as mock_logger:
        with patch('src.sensory.quantum_processor.process_signal', side_effect=Exception("Test error")):
            with pytest.raises(RuntimeError):
                quantum_processor.process_quantum_state(sample_input_data)
        mock_logger.error.assert_called()

def test_process_quantum_state_none_timestamp(quantum_processor):
    input_data = {"data": [1, 2, 3]}
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        result = quantum_processor.process_quantum_state(input_data)
        assert result["metadata"]["timestamp"] is None

def test_process_quantum_state_with_timestamp(quantum_processor):
    input_data = {
        "data": [1, 2, 3, 4],
        "timestamp": "2023-01-01T00:00:00Z"
    }
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        result = quantum_processor.process_quantum_state(input_data)
        assert result["metadata"]["timestamp"] == "2023-01-01T00:00:00Z"

def test_process_quantum_state_missing_data(quantum_processor):
    input_data = {}
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        result = quantum_processor.process_quantum_state(input_data)
        assert result["data"]["processed"] is True

def test_apply_quantum_transformations_missing_data(quantum_processor):
    data = {}
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        result = quantum_processor._apply_quantum_transformations(data)
        assert result["processed"] is True

def test_apply_quantum_transformations_with_signal_mocked(quantum_processor):
    data = {"data": [1, 2, 3]}
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        
        result = quantum_processor._apply_quantum_transformations(data)
        assert result["processed"] is True

def test_apply_quantum_transformations_no_signal_data(quantum_processor):
    data = {"data": []}
    result = quantum_processor._apply_quantum_transformations(data)
    assert result["processed"] is False

def test_apply_quantum_transformations_with_signal_processing(quantum_processor):
    data = {"data": [1, 2, 3, 4]}
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5, 1.0, 1.5, 2.0])
        result = quantum_processor._apply_quantum_transformations(data)
        
        assert result["processed"] is True
        assert "signal" in result
        assert "qft_result" in result
        assert "amplitude" in result
        assert "phase" in result

def test_process_quantum_state_full_integration(quantum_processor, sample_input_data):
    with patch('src.sensory.quantum_processor.process_signal') as mock_process_signal, \
         patch('src.sensory.quantum_processor.quantum_fourier_transform') as mock_qft:
        
        mock_process_signal.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_qft.return_value = np.array([0.5+0.5j, 1.0+1.0j, 1.5+1.5j, 2.0+2.0j])
        
        result = quantum_processor.process_quantum_state(sample_input_data)
        
        assert result["status"] == "processed"
        assert result["data"]["processed"] is True
        assert "amplitude" in result["data"]
        assert "phase" in result["data"]

def test_process_quantum_state_error_handling(quantum_processor):
    with pytest.raises(RuntimeError):
        quantum_processor.process_quantum_state(None)