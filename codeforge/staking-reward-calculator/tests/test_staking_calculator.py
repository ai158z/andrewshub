import pytest
from decimal import Decimal
from src.staking_calculator import StakingCalculator

@pytest.fixture
def calculator():
    return StakingCalculator()

def test_calculate_apy_valid_inputs(calculator):
    result = calculator.calculate_apy(1000, 1, 5)
    assert result == Decimal('50')

def test_calculate_apy_zero_duration(calculator):
    result = calculator.calculate_apy(1000, 0, 5)
    assert result == Decimal('0')

def test_calculate_apy_negative_apy_rate_raises_error(calculator):
    with pytest.raises(ValueError, match="APY rate cannot be negative"):
        calculator.calculate_apy(1000, 1, -5)

def test_calculate_apy_negative_stake_amount_raises_error(calculator):
    with pytest.raises(ValueError, match="Stake amount cannot be negative"):
        calculator.calculate_apy(-1000, 1, 5)

def test_calculate_apy_negative_duration_raises_error(calculator):
    with pytest.raises(ValueError, match="Duration cannot be negative"):
        calculator.calculate_apy(1000, -1, 5)

def test_calculate_apy_invalid_input_type_raises_error(calculator):
    with pytest.raises(ValueError):
        calculator.calculate_apy("invalid", 1, 5)

def test_calculate_compound_interest_valid_inputs(calculator):
    result = calculator.calculate_compound_interest(1000, 5, 1, 1)
    assert result > Decimal('1000')

def test_calculate_compound_interest_zero_time(calculator):
    result = calculator.calculate_compound_interest(1000, 5, 0, 1)
    assert result == Decimal('1000')

def test_calculate_compound_interest_negative_time_raises_error(calculator):
    with pytest.raises(ValueError, match="Time cannot be negative"):
        calculator.calculate_compound_interest(1000, 5, -1, 1)

def test_calculate_compound_interest_invalid_frequency_raises_error(calculator):
    with pytest.raises(ValueError, match="Compound frequency must be positive"):
        calculator.calculate_compound_interest(1000, 5, 1, 0)

def test_calculate_compound_interest_negative_principal_raises_error(calculator):
    with pytest.raises(ValueError, match="Principal cannot be negative"):
        calculator.calculate_compound_interest(-1000, 5, 1, 1)

def test_apply_lockup_penalty_valid_inputs(calculator):
    result = calculator.apply_lockup_penalty(100, 10)
    assert result == Decimal('90')

def test_apply_lockup_penalty_zero_penalty(calculator):
    result = calculator.apply_lockup_penalty(100, 0)
    assert result == Decimal('100')

def test_apply_lockup_penalty_full_penalty(calculator):
    result = calculator.apply_lockup_penalty(100, 100)
    assert result == Decimal('0')

def test_apply_lockup_penalty_invalid_rate_raises_error(calculator):
    with pytest.raises(ValueError, match="Penalty rate must be between 0 and 100"):
        calculator.apply_lockup_penalty(100, 150)

def test_apply_lockup_penalty_negative_reward_raises_error(calculator):
    with pytest.raises(ValueError, match="Reward amount cannot be negative"):
        calculator.apply_lockup_penalty(-100, 10)

def test_validate_input_none_raises_error(calculator):
    with pytest.raises(ValueError, match="Value cannot be None"):
        calculator.validate_input(None)

def test_validate_input_invalid_string_raises_error(calculator):
    with pytest.raises(ValueError):
        calculator.validate_input("invalid")

def test_validate_input_invalid_type_raises_error(calculator):
    with pytest.raises(ValueError):
        calculator.validate_input([1, 2, 3])