import pytest
from decimal import Decimal
from src.staking_calculator import validate_inputs, calculate_apy, calculate_compound_interest, calculate_lockup_penalty

def test_validate_inputs_valid_numbers():
    assert validate_inputs(100, 5.5, Decimal('3.14')) is True

def test_validate_inputs_negative_number_raises():
    with pytest.raises(ValueError):
        validate_inputs(-5)

def test_validate_inputs_non_numeric_raises():
    with pytest.raises(TypeError):
        validate_inputs("not_a_number")

def test_calculate_apy_valid_inputs():
    result = calculate_apy(0.05, 365)
    assert isinstance(result, Decimal)

def test_calculate_apy_negative_days_raises():
    with pytest.raises(ValueError):
        calculate_apy(0.05, -5)

def test_calculate_apy_zero_days_raises():
    with pytest.raises(ValueError):
        calculate_apy(0.05, 0)

def test_calculate_compound_interest_valid():
    result = calculate_compound_interest(1000, 0.05, 2, 4)
    assert isinstance(result, Decimal)
    assert result > 0

def test_calculate_compound_interest_invalid_n_raises():
    with pytest.raises(ValueError):
        calculate_compound_interest(1000, 0.05, 2, 0)

def test_calculate_lockup_penalty_valid():
    result = calculate_lockup_penalty(1000, 0.05)
    assert isinstance(result, Decimal)
    assert result > 0

def test_calculate_lockup_penalty_negative_amount():
    result = calculate_lockup_penalty(1000, -0.05)
    assert result < 0  # Penalty can be negative as per logic

def test_calculate_compound_interest_precision():
    result = calculate_compound_interest(Decimal('1000.5'), 0.05, 1, 1)
    assert isinstance(result, Decimal)

def test_calculate_apy_precision():
    result = calculate_apy(0.05, 365)
    assert isinstance(result, Decimal)

def test_validate_inputs_decimal_conversion():
    result = validate_inputs(100, 0.05, Decimal('3.14'))
    assert result is True

def test_validate_inputs_invalid_type():
    with pytest.raises(TypeError):
        validate_inputs("string", 5, 10)

def test_calculate_apy_with_zero_rate():
    result = calculate_apy(0, 365)
    assert result == Decimal('0')

def test_calculate_apy_with_zero_days():
    with pytest.raises(ValueError):
        calculate_apy(0.05, 0)

def test_calculate_compound_interest_with_zero_values():
    result = calculate_compound_interest(0, 0, 0, 1)
    assert result == Decimal('0')

def test_calculate_lockup_penalty_with_zero_values():
    result = calculate_lockup_penalty(0, 0)
    assert result == Decimal('0')

def test_calculate_apy_edge_case_large_days():
    result = calculate_apy(0.01, 10000)
    assert isinstance(result, Decimal)