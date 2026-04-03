import pytest
import argparse
from unittest.mock import patch, MagicMock

# Import the functions to test
from src.validators import validate_percentage, validate_positive_int, validate_positive_float

def test_validate_percentage_valid_values():
    """Test that valid percentage strings convert correctly"""
    assert validate_percentage("0") == 0.0
    assert validate_percentage("50") == 50.0
    assert validate_percentage("100") == 100.0
    assert validate_percentage("25.5") == 25.5

def test_validate_percentage_invalid_range():
    """Test that percentages outside 0-100 raise ArgumentTypeError"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_percentage("101")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_percentage("-1")

def test_validate_percentage_invalid_format():
    """Test that invalid string formats raise ArgumentTypeError"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_percentage("not_a_number")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_percentage("")

@patch('src.utils.convert_to_float')
def test_validate_percentage_conversion_error(mock_convert):
    """Test that conversion errors are handled properly"""
    mock_convert.side_effect = ValueError("Conversion failed")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_percentage("invalid")

def test_validate_positive_int_valid_values():
    """Test that valid positive integers convert correctly"""
    assert validate_positive_int("0") == 0
    assert validate_positive_int("42") == 42
    assert validate_positive_int("1000") == 1000

def test_validate_positive_int_negative_value():
    """Test that negative integers raise ArgumentTypeError"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_int("-1")

def test_validate_positive_int_invalid_format():
    """Test that invalid string formats raise ArgumentTypeError"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_int("not_a_number")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_int("")

@patch('src.utils.convert_to_int')
def test_validate_positive_int_conversion_error(mock_convert):
    """Test that conversion errors are handled properly"""
    mock_convert.side_effect = ValueError("Conversion failed")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_int("invalid")

def test_validate_positive_float_valid_values():
    """Test that valid positive floats convert correctly"""
    assert validate_positive_float("0.0") == 0.0
    assert validate_positive_float("3.14") == 3.14
    assert validate_positive_float("100") == 100.0

def test_validate_positive_float_negative_value():
    """Test that negative floats raise ArgumentTypeError"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_float("-0.1")

def test_validate_positive_float_invalid_format():
    """Test that invalid string formats raise ArgumentTypeError"""
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_float("not_a_number")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_float("")

@patch('src.utils.convert_to_float')
def test_validate_positive_float_conversion_error(mock_convert):
    """Test that conversion errors are handled properly"""
    mock_convert.side_effect = ValueError("Conversion failed")
    
    with pytest.raises(argparse.ArgumentTypeError):
        validate_positive_float("invalid")