import pytest
import decimal
from decimal import Decimal
from staking_calculator.utils import precise_division, precise_multiply, percentage_of

def test_precise_division_with_integers():
    result = precise_division(10, 3)
    expected = Decimal('3.33333333333333333333333333333333333333333333333333')
    assert result == expected

def test_precise_division_with_floats():
    result = precise_division(10.0, 3.0)
    expected = Decimal('3.33333333333333333333333333333333333333333333333333')
    assert result == expected

def test_precise_division_with_decimals():
    result = precise_division(Decimal('10'), Decimal('3'))
    expected = Decimal('3.33333333333333333333333333333333333333333333333333')
    assert result == expected

def test_precise_division_by_zero_raises_exception():
    with pytest.raises(decimal.DivisionByZero):
        precise_division(10, 0)

def test_precise_division_invalid_input_raises_type_error():
    with pytest.raises(TypeError):
        precise_division("invalid", 5)

def test_precise_multiply_with_integers():
    result = precise_multiply(15, 2)
    assert result == Decimal('30')

def test_precise_multiply_with_floats():
    result = precise_multiply(15.5, 2.0)
    assert result == Decimal('31.0')

def test_precise_multiply_with_decimals():
    result = precise_multiply(Decimal('15.5'), Decimal('2.5'))
    assert result == Decimal('38.75')

def test_precise_multiply_invalid_input_raises_type_error():
    with pytest.raises(TypeError):
        precise_multiply("invalid", 5)

def test_percentage_of_with_integers():
    result = percentage_of(1000, 15)
    expected = Decimal('150')
    assert result == expected

def test_percentage_of_with_floats():
    result = percentage_of(1000.0, 15.5)
    expected = Decimal('155.000000000000000000000000000000000000000000000000')
    assert result == expected

def test_percentage_of_with_decimals():
    result = percentage_of(Decimal('1000'), Decimal('15.5'))
    expected = Decimal('155.000000000000000000000000000000000000000000000000')
    assert result == expected

def test_percentage_of_invalid_input_raises_type_error():
    with pytest.raises(TypeError):
        percentage_of("invalid", 15)

def test_precise_division_negative_numbers():
    result = precise_division(-10, 2)
    assert result == Decimal('-5')

def test_precise_multiply_negative_numbers():
    result = precise_multiply(-15, 2)
    assert result == Decimal('-30')

def test_percentage_of_negative_amount():
    result = percentage_of(-1000, 15)
    assert result == Decimal('-150')

def test_precise_division_large_numbers():
    result = precise_division(1000000000000, 1000000)
    assert result == Decimal('1000000')

def test_precise_multiply_zero():
    result = precise_multiply(0, 100)
    assert result == Decimal('0')

def test_percentage_of_zero():
    result = percentage_of(0, 50)
    assert result == Decimal('0')