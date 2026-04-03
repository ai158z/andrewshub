import pytest
from unittest.mock import patch
from src.validators import validate_percentage, validate_positive_int, validate_positive_float


def test_validate_percentage_valid_values():
    assert validate_percentage("0") == 0.0
    assert validate_percentage("50") == 50.0
    assert validate_percentage("100") == 100.0


def test_validate_percentage_invalid_range():
    with pytest.raises(ValueError):
        validate_percentage("150")
    with pytest.raises(ValueError):
        validate_percentage("-10")


def test_validate_percentage_invalid_format():
    with pytest.raises(ValueError):
        validate_percentage("invalid")


def test_validate_positive_int_valid_values():
    assert validate_positive_int("10") == 10
    assert validate_positive_int("0") == 0


def test_validate_positive_int_invalid_negative():
    with pytest.raises(ValueError):
        validate_positive_int("-5")


def test_validate_positive_int_invalid_format():
    with pytest.raises(ValueError):
        validate_positive_int("not_a_number")


def test_validate_positive_float_valid_values():
    assert validate_positive_float("10.5") == 10.5
    assert validate_positive_float("0") == 0.0


def test_validate_positive_float_invalid_negative():
    with pytest.raises(ValueError):
        validate_positive_float("-5.5")


def test_validate_positive_float_invalid_format():
    with pytest.raises(ValueError):
        validate_positive_float("not_a_number")