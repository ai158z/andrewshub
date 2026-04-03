import pytest
import argparse
from src.validator import validate_principal, validate_apr, convert_input

def test_validate_principal_positive_float():
    result = validate_principal(1000.0)
    assert result == 1000.0

def test_validate_principal_positive_int():
    result = validate_principal(1000)
    assert result == 1000.0

def test_validate_principal_positive_string():
    result = validate_principal("1000")
    assert result == 1000.0

def test_validate_principal_zero():
    with pytest.raises(argparse.ArgumentTypeError, match="Principal amount must be positive"):
        validate_principal(0)

def test_validate_principal_negative():
    with pytest.raises(argparse.ArgumentTypeError, match="Principal amount must be positive"):
        validate_principal(-100)

def test_validate_principal_invalid_string():
    with pytest.raises(argparse.ArgumentTypeError, match="Invalid principal amount"):
        validate_principal("invalid")

def test_validate_apr_valid():
    result = validate_apr(0.05)
    assert result == 0.05

def test_validate_apr_string():
    result = validate_apr("0.075")
    assert result == 0.075

def test_validate_apr_negative():
    with pytest.raises(argparse.ArgumentTypeError, match="APR rate must be between 0 and 1"):
        validate_apr(-0.1)

def test_validate_apr_over_100_percent():
    with pytest.raises(argparse.ArgumentTypeError, match="APR rate must be between 0 and 1"):
        validate_apr(1.5)

def test_validate_apr_invalid_string():
    with pytest.raises(argparse.ArgumentTypeError, match="Invalid APR rate"):
        validate_apr("invalid")

def test_convert_input_int():
    result = convert_input("123")
    assert result == 123
    assert isinstance(result, int)

def test_convert_input_float():
    result = convert_input("123.45")
    assert result == 123.45
    assert isinstance(result, float)

def test_convert_input_string():
    result = convert_input("hello")
    assert result == "hello"
    assert isinstance(result, str)

def test_convert_input_invalid_int():
    result = convert_input("abc")
    assert result == "abc"

def test_convert_input_mixed():
    result = convert_input("123.0")
    assert result == 123.0
    assert isinstance(result, float)

def test_convert_input_zero():
    result = convert_input("0")
    assert result == 0
    assert isinstance(result, int)

def test_convert_input_negative():
    result = convert_input("-123.45")
    assert result == -123.45
    assert isinstance(result, float)

def test_convert_input_scientific():
    result = convert_input("1e5")
    assert result == 100000.0
    assert isinstance(result, float)