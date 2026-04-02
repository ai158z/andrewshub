import pytest
from decimal import Decimal
from src.staking_calculator import calculate_apy, calculate_compound_interest, calculate_lockup_penalty, validate_inputs

def test_calculate_apy_basic():
    result = calculate_apy(0.05, 365)
    assert round(float(result), 10) == 0.05

def test_calculate_apy_partial_year():
    result = calculate_apy(0.10, 180)
    expected = (1 + 0.10) ** (180/365) - 1
    assert round(float(result), 10) == expected

def test_calculate_apy_zero_rate():
    result = calculate_apy(0.0, 365)
    assert float(result) == 0.0

def test_calculate_compound_interest_basic():
    result = calculate_compound_interest(1000, 0.05, 1, 12)
    expected = 1000 * ((1 + 0.05/12) ** 12) - 1000
    assert round(float(result), 10) == round(expected, 10)

def test_calculate_compound_interest_zero_rate():
    result = calculate_compound_interest(1000, 0.0, 1, 12)
    assert float(result) == 0.0

def test_calculate_lockup_penalty_basic():
    result = calculate_lockup_penalty(1000, 0.10)
    assert float(result) == 100.0

def test_calculate_lockup_penalty_zero():
    result = calculate_lockup_penalty(1000, 0.0)
    assert float(result) == 0.0

def test_validate_inputs_valid():
    assert validate_inputs(1000, 0.05, 365) is True

def test_validate_inputs_decimal():
    assert validate_inputs(Decimal('1000'), Decimal('0.05'), 365) is True

def test_validate_inputs_negative_principal():
    with pytest.raises(ValueError):
        validate_inputs(-1000, 0.05, 365)

def test_validate_inputs_negative_rate():
    with pytest.raises(ValueError):
        validate_inputs(1000, -0.05, 365)

def test_validate_inputs_zero_principal():
    with pytest.raises(ValueError):
        validate_inputs(0, 0.05, 365)

def test_validate_inputs_invalid_rate():
    with pytest.raises(ValueError):
        validate_inputs(1000, 1.5, 365)

def test_validate_inputs_non_numeric():
    with pytest.raises(ValueError):
        validate_inputs("invalid", 0.05, 365)

def test_validate_inputs_none():
    with pytest.raises(ValueError):
        validate_inputs(None, 0.05, 365)

def test_compound_interest_quarterly():
    principal = 5000
    rate = 0.03
    time = 2
    n = 4
    result = calculate_compound_interest(principal, rate, time, n)
    expected = principal * ((1 + rate/n) ** (n * time)) - principal
    assert round(float(result), 10) == round(expected, 10)

def test_calculate_lockup_penalty_edge_cases():
    result = calculate_lockup_penalty(100, 1.0)
    assert float(result) == 100.0

def test_calculate_apy_edge_cases():
    result = calculate_apy(0.0, 365)
    assert float(result) == 0.0

def test_compound_interest_edge_cases():
    result = calculate_compound_interest(1000, 0.0, 1, 12)
    assert float(result) == 0.0

def test_validate_inputs_edge_cases():
    with pytest.raises(ValueError):
        validate_inputs(1000, -0.05, 365)

def test_compound_interest_zero_rate():
    result = calculate_compound_interest(1000, 0.0, 1, 12)
    assert float(result) == 0.0