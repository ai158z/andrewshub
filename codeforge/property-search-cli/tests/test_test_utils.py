import pytest
from src.utils import convert_to_float, convert_to_int


def test_convert_to_float_valid_positive():
    result = convert_to_float("3.14")
    assert result == 3.14


def test_convert_to_float_valid_negative():
    result = convert_to_float("-3.14")
    assert result == -3.14


def test_convert_to_float_valid_zero():
    result = convert_to_float("0")
    assert result == 0.0


def test_convert_to_float_valid_integer_string():
    result = convert_to_float("42")
    assert result == 42.0


def test_convert_to_float_invalid_empty_string():
    with pytest.raises(ValueError):
        convert_to_float("")


def test_convert_to_float_invalid_non_numeric():
    with pytest.raises(ValueError):
        convert_to_float("not_a_number")


def test_convert_to_float_invalid_multiple_dots():
    with pytest.raises(ValueError):
        convert_to_float("12.34.56")


def test_convert_to_int_valid_positive():
    result = convert_to_int("42")
    assert result == 42


def test_convert_to_int_valid_negative():
    result = convert_to_int("-42")
    assert result == -42


def test_convert_to_int_valid_zero():
    result = convert_to_int("0")
    assert result == 0


def test_convert_to_int_invalid_empty_string():
    with pytest.raises(ValueError):
        convert_to_int("")


def test_convert_to_int_invalid_non_numeric():
    with pytest.raises(ValueError):
        convert_to_int("not_a_number")


def test_convert_to_int_invalid_float_string():
    with pytest.raises(ValueError):
        convert_to_int("12.34")


def test_convert_to_int_invalid_float_value():
    with pytest.raises(ValueError):
        convert_to_int("12.34")


def test_convert_to_float_edge_large_number():
    result = convert_to_float("1e10")
    assert result == 1e10


def test_convert_to_int_edge_large_number():
    result = convert_to_int("1000000")
    assert result == 1000000


def test_convert_to_float_edge_negative_zero():
    result = convert_to_float("-0.0")
    assert result == -0.0


def test_convert_to_int_edge_negative_zero():
    result = convert_to_int("-0")
    assert result == 0


def test_convert_to_float_edge_positive_zero():
    result = convert_to_float("+0.0")
    assert result == 0.0


def test_convert_to_int_edge_positive_zero():
    result = convert_to_int("+0")
    assert result == 0