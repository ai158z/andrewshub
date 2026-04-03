import pytest
from unittest.mock import patch
from staking_calculator import calculate_apy, calculate_compound_interest

def test_calculate_apy_basic():
    result = calculate_apy(0.05, 12)
    expected = (1 + 0.05/12) ** 12 - 1
    assert round(result, 10) == round(expected, 10)

def test_calculate_apy_zero_rate():
    result = calculate_apy(0.0, 12)
    assert result == 0.0

def test_calculate_apy_high_frequency():
    result = calculate_apy(0.1, 365)
    expected = (1 + 0.1/365) ** 365 - 1
    assert round(result, 10) == round(expected, 10)

def test_calculate_compound_interest_basic():
    result = calculate_compound_interest(1000, 0.05, 1, 1)
    expected = 1000 * (1 + 0.05) - 1000
    assert round(result, 10) == round(expected, 10)

def test_calculate_compound_interest_large_principal():
    result = calculate_compound_interest(10000, 0.05, 1, 1)
    expected = 10000 * (1 + 0.05) - 10000
    assert round(result, 10) == round(expected, 10)

def test_calculate_compound_interest_zero_principal():
    result = calculate_compound_interest(0, 0.05, 1, 1)
    assert result == 0

def test_calculate_compound_interest_high_precision():
    result = calculate_compound_interest(5000.50, 0.025, 2, 4)
    expected = 5000.50 * (1 + 0.025 / 4) ** (4 * 2) - 5000.50
    assert round(result, 2) == round(expected, 2)

@pytest.mark.parametrize("principal,rate,time_periods,compound_frequency,expected", [
    (1000, 0.05, 1, 1, 1000 * (1 + 0.05) - 1000),
    (0, 0.05, 1, 1, 0),
])
def test_calculate_compound_interest_parametrized(principal, rate, time_periods, compound_frequency, expected):
    result = calculate_compound_interest(principal, rate, time_periods, compound_frequency)
    assert round(result, 10) == round(expected, 10)

def test_calculate_apy_edge_cases():
    # Test zero rate
    result = calculate_apy(0.0, 12)
    assert result == 0.0
    
    # Test high frequency case
    result = calculate_apy(0.1, 365)
    expected = (1 + 0.1/365) ** 365 - 1
    assert round(result, 10) == round(expected, 10)

def test_compound_interest_edge_cases():
    # Test zero principal
    result = calculate_compound_interest(0, 0.05, 1, 1)
    assert result == 0

    # Test high precision
    result = calculate_compound_interest(5000.50, 0.025, 2, 4)
    expected = 5000.50 * (1 + 0.025 / 4) ** (4 * 2) - 5000.50
    assert round(result, 2) == round(expected, 2)

def test_invalid_input_apy():
    with pytest.raises(TypeError):
        calculate_apy("invalid", 12)

def test_invalid_input_compound_interest():
    with pytest.raises(TypeError):
        calculate_compound_interest("invalid", 0.05, 1, 1)

def test_calculate_apy_negative_rate():
    result = calculate_apy(-0.05, 12)
    expected = (1 + (-0.05)/12) ** 12 - 1
    assert round(result, 10) == round(expected, 10)

def test_calculate_compound_interest_negative_principal():
    result = calculate_compound_interest(-1000, 0.05, 1, 1)
    expected = -1000 * (1 + 0.05) - (-1000)
    assert round(result, 10) == round(expected, 10)