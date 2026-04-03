import pytest
import math
from src.staking_calculator import calculate_apy, calculate_compound_interest, calculate_lockup_penalty

def test_calculate_apy_valid_input():
    rate = 0.05
    frequency = 12
    expected_apy = (1 + rate/frequency)**frequency - 1
    apy = calculate_apy(rate, frequency)
    assert math.isclose(apy, expected_apy, rel_tol=1e-9)

def test_calculate_apy_zero_rate():
    apy = calculate_apy(0.0, 12)
    assert apy == 0.0

def test_calculate_apy_invalid_rate_negative():
    with pytest.raises(ValueError):
        calculate_apy(-0.01, 12)

def test_calculate_apy_invalid_frequency_zero():
    with pytest.raises(ValueError):
        calculate_apy(0.05, 0)

def test_calculate_apy_compound_annually():
    apy = calculate_apy(0.05, 1)
    expected = (1 + 0.05/1)**1 - 1
    assert math.isclose(apy, expected, rel_tol=1e-9)

def test_calculate_compound_interest_valid():
    amount = calculate_compound_interest(1000, 0.05, 2, 12)
    expected = 1000 * (1 + 0.05/12)**(12*2)
    assert math.isclose(amount, expected, rel_tol=1e-9)

def test_calculate_compound_interest_zero_principal():
    with pytest.raises(ValueError):
        calculate_compound_interest(0, 0.05, 2, 12)

def test_calculate_compound_interest_negative_time():
    with pytest.raises(ValueError):
        calculate_compound_interest(1000, 0.05, -1, 12)

def test_calculate_compound_interest_zero_frequency():
    with pytest.raises(ValueError):
        calculate_compound_interest(1000, 0.05, 2, 0)

def test_calculate_lockup_penalty_valid():
    penalty = calculate_lockup_penalty(1000, 0.1)
    assert penalty == 100

def test_calculate_lockup_penalty_zero_amount():
    with pytest.raises(ValueError):
        calculate_lockup_penalty(0, 0.1)

def test_calculate_lockup_penalty_invalid_rate():
    with pytest.raises(ValueError):
        calculate_lockup_penalty(1000, 1.5)

def test_calculate_lockup_penalty_zero_penalty_rate():
    penalty = calculate_lockup_penalty(1000, 0)
    assert penalty == 0

def test_calculate_lockup_penalty_full_amount_penalty():
    penalty = calculate_lockup_penalty(1000, 1.0)
    assert penalty == 1000

def test_compound_interest_edge_case_zero_time():
    amount = calculate_compound_interest(1000, 0.05, 0, 12)
    assert amount == 1000

def test_compound_interest_edge_case_zero_rate():
    amount = calculate_compound_interest(1000, 0, 2, 12)
    assert amount == 1000

def test_compound_interest_negative_rate():
    with pytest.raises(ValueError):
        calculate_compound_interest(1000, -0.05, 2, 12)

def test_compound_interest_zero_time_valid():
    amount = calculate_compound_interest(1000, 0.05, 0, 12)
    assert amount == 1000

def test_compound_interest_zero_rate_valid():
    amount = calculate_compound_interest(1000, 0, 2, 12)
    assert amount == 1000