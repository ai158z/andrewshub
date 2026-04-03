import pytest
import logging
from src.utils import convert_to_float, convert_to_int
from unittest.mock import patch

def test_convert_to_float_valid_string():
    assert convert_to_float("3.14") == 3.14

def test_convert_to_float_valid_integer_string():
    assert convert_to_float("42") == 42.0

def test_convert_to_float_negative_value():
    assert convert_to_float("-10.5") == -10.5

def test_convert_to_float_scientific_notation():
    assert convert_to_float("1e-3") == 0.001

def test_convert_to_float_zero_string():
    assert convert_to_float("0") == 0.0

def test_convert_to_float_invalid_type_raises_typeerror():
    with pytest.raises(TypeError):
        convert_to_float(3.14)

def test_convert_to_float_empty_string_raises_valueerror():
    with pytest.raises(ValueError):
        convert_to_float("")

def test_convert_to_float_invalid_string_raises_valueerror():
    with pytest.raises(ValueError):
        convert_to_float("not_a_number")

def test_convert_to_int_valid_string():
    assert convert_to_int("42") == 42

def test_convert_to_int_float_string():
    assert convert_to_int("42.0") == 42

def test_convert_to_int_negative_value():
    assert convert_to_int("-10") == -10

def test_convert_to_int_zero_string():
    assert convert_to_int("0") == 0

def test_convert_to_int_invalid_type_raises_typeerror():
    with pytest.raises(TypeError):
        convert_to_int(42)

def test_convert_to_int_empty_string_raises_valueerror():
    with pytest.raises(ValueError):
        convert_to_int("")

def test_convert_to_int_invalid_string_raises_valueerror():
    with pytest.raises(ValueError):
        convert_to_int("not_a_number")

def test_convert_to_int_float_with_decimal_raises_valueerror():
    with pytest.raises(ValueError):
        convert_to_int("42.5")

def test_convert_to_float_logs_error_on_invalid_type():
    with patch("src.utils.logger.error") as mock_logger:
        with pytest.raises(TypeError):
            convert_to_float(123)
        mock_logger.assert_called()

def test_convert_to_int_logs_error_on_invalid_type():
    with patch("src.utils.logger.error") as mock_logger:
        with pytest.raises(TypeError):
            convert_to_int(123)
        mock_logger.assert_called()

def test_convert_to_float_logs_error_on_empty_string():
    with patch("src.utils.logger.error") as mock_logger:
        with pytest.raises(ValueError):
            convert_to_float("")
        mock_logger.assert_called()

def test_convert_to_int_logs_error_on_empty_string():
    with patch("src.utils.logger.error") as mock_logger:
        with pytest.raises(ValueError):
            convert_to_int("")
        mock_logger.assert_called()