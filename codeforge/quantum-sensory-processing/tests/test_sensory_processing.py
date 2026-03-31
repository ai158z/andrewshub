```python
import pytest
import torch
from torch import Tensor
from unittest.mock import MagicMock
from src.sensory_processing import QuantumSensoryProcessor

def test_process_data_invalid_input_raises_value_error():
    processor = QuantumSensoryProcessor()
    invalid_input = [1, 2, 3]  # Not a Tensor
    with pytest.raises(ValueError):
        processor.process_data(invalid_input)

def test_process_data_successful_processing(mocker):
    processor = QuantumSensoryProcessor()
    mock_input = torch.tensor([1.0])
    
    mock_model_forward = mocker.patch.object(type(processor.model), 'forward', return_value=torch.tensor([2.0]))
    mock_metrics = mocker.patch('src.sensory_processing.calculate_magic_state_metrics', return_value={'metric1': 0.5})
    mock_test_ambiguous = mocker.patch('src.sensory_processing.test_ambiguous_input', return_value=False)
    mock_logger_error = mocker