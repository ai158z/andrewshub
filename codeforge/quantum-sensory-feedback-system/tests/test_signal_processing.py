import pytest
import numpy as np
from src.utils.signal_processing import process_signal
from unittest.mock import patch, MagicMock

def test_process_signal_with_valid_input():
    signal = [1, 2, 3, 4, 5]
    result = process_signal(signal)
    assert isinstance(result, list)
    assert len(result) == len(signal)

def test_process_signal_empty_input():
    with pytest.raises(ValueError, match="Signal cannot be empty"):
        process_signal([])

def test_process_signal_with_single_value():
    signal = [5.0]
    result = process_signal(signal)
    assert result == [0.0]  # Single value normalized to 0

def test_process_signal_with_constant_values():
    signal = [3.0, 3.0, 3.0, 3.0]
    result = process_signal(signal)
    assert result == [0.0, 0.0, 0.0, 0.0]  # All values are the same, so normalized to 0

def test_process_signal_with_negative_values():
    signal = [-2, -1, 0, 1, 2]
    result = process_signal(signal)
    assert result == [0.0, 0.25, 0.5, 0.75, 1.0]

def test_process_signal_with_large_values():
    signal = [1000, 2000, 3000, 4000, 5000]
    result = process_signal(signal)
    assert result == [0.0, 0.25, 0.5, 0.75, 1.0]

def test_process_signal_with_float_values():
    signal = [1.5, 2.7, 3.14, 4.0, 5.25]
    result = process_signal(signal)
    assert len(result) == len(signal)
    assert all(isinstance(x, float) for x in result)

def test_process_signal_with_mixed_int_float():
    signal = [1, 2.5, 3, 4.7, 5]
    result = process_signal(signal)
    assert len(result) == len(signal)

def test_process_signal_noise_reduction_effect():
    # Test that the signal is actually being processed (not just returned as is)
    signal = [1, 5, 2, 8, 3, 9, 1]
    result = process_signal(signal)
    assert result != signal  # Should be different due to processing

def test_process_signal_normalization():
    # Test that output is properly normalized between 0 and 1
    signal = [10, 20, 30, 40, 50]
    result = process_signal(signal)
    assert min(result) == 0.0
    assert max(result) == 1.0

def test_process_signal_with_out_of_order_values():
    signal = [5, 1, 3, 2, 4]
    result = process_signal(signal)
    # Should be normalized to 0-1 range
    assert result[0] == 1.0  # max value in sorted order
    assert result[1] == 0.0  # min value in input

def test_process_signal_with_all_same_values():
    signal = [7, 7, 7, 7]
    result = process_signal(signal)
    # When all values are the same, they should all normalize to 0
    assert result == [0.0, 0.0, 0.0, 0.0]

def test_process_signal_with_two_values():
    signal = [1, 2]
    result = process_signal(signal)
    assert result == [0.0, 1.0]  # Should normalize to 0 and 1

def test_process_signal_with_string_input():
    # This should fail as input should be numerical
    with pytest.raises(TypeError):
        process_signal(["1", "2", "3"])

def test_process_signal_with_none_input():
    with pytest.raises(TypeError):
        process_signal(None)

def test_process_signal_with_inf_values():
    signal = [1, float('inf'), 3]
    result = process_signal(signal)
    # Should handle infinity properly
    assert len(result) == 3

def test_process_signal_with_nan_values():
    signal = [1, float('nan'), 3]
    result = process_signal(signal)
    assert len(result) == 3

def test_process_signal_logging_success():
    signal = [1, 2, 3]
    with patch('src.utils.signal_processing.logger') as mock_logger:
        process_signal(signal)
        mock_logger.info.assert_called_with("Signal processed successfully")

def test_process_signal_logging_error():
    with patch('src.utils.signal_processing.logger') as mock_logger:
        with pytest.raises(ValueError):
            process_signal([])
        mock_logger.error.assert_called()

def test_process_signal_with_window_size_adjustment():
    # Test that window size is properly adjusted for even numbers
    # and that the algorithm works with different signal lengths
    signal = [1, 2, 3, 4]  # Even length that should be adjusted
    result = process_signal(signal)
    assert isinstance(result, list)