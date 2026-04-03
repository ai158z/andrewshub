import pytest
from decimal import Decimal
from src.types import to_float, to_int


def test_to_float_with_float():
    assert to_float(3.14) == 3.14
    assert to_float(-2.5) == -2.5


def test_to_float_with_int():
    assert to_float(42) == 42.0
    assert to_float(-7) == -7.0


def test_to_float_with_string():
    assert to_float("3.14") == 3.14
    assert to_float("-42") == -42.0
    assert to_float("0") == 0.0
    assert to_float("1.23e-4") == 1.23e-4


def test_to_float_with_string_whitespace():
    assert to_float("  3.14  ") == 3.14
    assert to_float(" -42 ") == -42.0


def test_to_float_with_decimal():
    assert to_float(Decimal("3.14")) == 3.14
    assert to_float(Decimal("-42")) == -42.0


def test_to_float_invalid_string():
    with pytest.raises(ValueError, match="Invalid number format"):
        to_float("3.14.15")
    
    with pytest.raises(ValueError, match="Invalid number format"):
        to_float("abc")
    
    with pytest.raises(ValueError, match="Invalid number format"):
        to_float("3.14abc")


def test_to_float_invalid_type():
    with pytest.raises(TypeError):
        to_float([1, 2, 3])


def test_to_float_conversion_error():
    with pytest.raises(ValueError, match="Cannot convert"):
        to_float("not_a_number")


def test_to_int_with_int():
    assert to_int(42) == 42
    assert to_int(-7) == -7


def test_to_int_with_whole_float():
    assert to_int(42.0) == 42
    assert to_int(-7.0) == -7


def test_to_int_with_fractional_float():
    with pytest.raises(ValueError, match="Cannot convert fractional number"):
        to_int(3.14)
    
    with pytest.raises(ValueError, match="Cannot convert fractional number"):
        to_int(-2.5)


def test_to_int_with_string():
    assert to_int("42") == 42
    assert to_int("-7") == -7
    assert to_int("0") == 0


def test_to_int_with_whole_number_string():
    assert to_int("42.0") == 42
    assert to_int("-7.0") == -7


def test_to_int_with_fractional_string():
    with pytest.raises(ValueError, match="Cannot convert fractional number"):
        to_int("3.14")


def test_to_int_invalid_string():
    with pytest.raises(ValueError, match="Invalid integer format"):
        to_int("abc")
    
    with pytest.raises(ValueError, match="Invalid integer format"):
        to_int("42.5")


def test_to_int_with_decimal():
    assert to_int(Decimal("42")) == 42
    assert to_int(Decimal("-7")) == -7


def test_to_int_with_fractional_decimal():
    with pytest.raises(ValueError, match="Cannot convert fractional Decimal"):
        to_int(Decimal("3.14"))


def test_to_int_invalid_type():
    with pytest.raises(TypeError):
        to_int([1, 2, 3])