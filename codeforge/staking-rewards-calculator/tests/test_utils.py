import pytest
from src.utils import calculate_compound_interest, calculate_penalty

def test_calculate_compound_interest_valid_inputs():
    result = calculate_compound_interest(1000, 0.05, 2, 4)
    assert result == pytest.approx(102.50, 0.01)

def test_calculate_compound_interest_zero_principal():
    result = calculate_compound_interest(0, 0.05, 2, 4)
    assert result == 0

def test_calculate_compound_interest_zero_rate():
    result = calculate_compound_interest(1000, 0, 2, 4)
    assert result == 0

def test_calculate_compound_interest_zero_time():
    result = calculate_compound_interest(1000, 0.05, 0, 4)
    assert result == 0

def test_calculate_compound_interest_negative_principal():
    with pytest.raises(ValueError, match="Principal cannot be negative"):
        calculate_compound_interest(-1000, 0.05, 2, 4)

def test_calculate_compound_interest_negative_rate():
    with pytest.raises(ValueError, match="Rate cannot be negative"):
        calculate_compound_interest(1000, -0.05, 2, 4)

def test_calculate_compound_interest_negative_time():
    with pytest.raises(ValueError, match="Time cannot be negative"):
        calculate_compound_interest(1000, 0.05, -2, 4)

def test_calculate_compound_interest_zero_frequency():
    with pytest.raises(ValueError, match="Frequency must be positive"):
        calculate_compound_interest(1000, 0.05, 2, 0)

def test_calculate_compound_interest_negative_frequency():
    with pytest.raises(ValueError, match="Frequency must be positive"):
        calculate_compound_interest(1000, 0.05, 2, -1)

def test_calculate_compound_interest_non_integer_frequency():
    with pytest.raises(ValueError, match="Frequency must be an integer"):
        calculate_compound_interest(1000, 0.05, 2, 4.5)

def test_calculate_penalty_valid_inputs():
    result = calculate_penalty(1000, 0.05)
    assert result == 50

def test_calculate_penalty_zero_amount():
    result = calculate_penalty(0, 0.05)
    assert result == 0

def test_calculate_penalty_zero_rate():
    result = calculate_penalty(1000, 0)
    assert result == 0

def test_calculate_penalty_negative_amount():
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        calculate_penalty(-1000, 0.05)

def test_calculate_penalty_negative_rate():
    with pytest.raises(ValueError, match="Penalty rate cannot be negative"):
        calculate_penalty(1000, -0.05)

def test_calculate_penalty_rate_over_100_percent():
    with pytest.raises(ValueError, match="Penalty rate cannot be greater than 1"):
        calculate_penalty(1000, 1.05)

def test_calculate_penalty_rate_100_percent():
    result = calculate_penalty(1000, 1)
    assert result == 1000

def test_calculate_compound_interest_large_numbers():
    result = calculate_compound_interest(1000000, 0.1, 10, 12)
    assert result == pytest.approx(1707041.77, 0.01)

def test_calculate_penalty_small_values():
    result = calculate_penalty(0.01, 0.01)
    assert result == 0.0001