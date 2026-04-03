import pytest
import decimal
from staking_calculator.validators import validate_staking_parameters
from staking_calculator.utils import precise_division, precise_multiply, percentage_of

def test_validate_staking_parameters_valid_inputs():
    assert validate_staking_parameters(1000, 365, 5.0, 2.0, 12) == True

def test_validate_staking_parameters_negative_stake_amount():
    with pytest.raises(ValueError, match="stake_amount must be non-negative"):
        validate_staking_parameters(-100, 365, 5.0, 2.0, 12)

def test_validate_staking_parameters_invalid_stake_amount_type():
    with pytest.raises(TypeError, match="stake_amount must be a number"):
        validate_staking_parameters("invalid", 365, 5.0, 2.0, 12)

def test_validate_staking_parameters_negative_duration():
    with pytest.raises(ValueError, match="duration must be non-negative"):
        validate_staking_parameters(1000, -30, 5.0, 2.0, 12)

def test_validate_staking_parameters_invalid_duration_type():
    with pytest.raises(TypeError, match="duration must be a number"):
        validate_staking_parameters(1000, "invalid", 5.0, 2.0, 12)

def test_validate_staking_parameters_negative_apy():
    with pytest.raises(ValueError, match="apy must be non-negative"):
        validate_staking_parameters(1000, 365, -5.0, 2.0, 12)

def test_validate_staking_parameters_invalid_apy_type():
    with pytest.raises(TypeError, match="apy must be a number"):
        validate_staking_parameters(1000, 365, "invalid", 2.0, 12)

def test_validate_staking_parameters_invalid_penalty_rate_type():
    with pytest.raises(TypeError, match="penalty_rate must be a number"):
        validate_staking_parameters(1000, 365, 5.0, "invalid", 12)

def test_validate_staking_parameters_penalty_rate_negative():
    with pytest.raises(ValueError, match="penalty_rate must be between 0 and 100"):
        validate_staking_parameters(1000, 365, 5.0, -5, 12)

def test_validate_staking_parameters_penalty_rate_over_100():
    with pytest.raises(ValueError, match="penalty_rate must be between 0 and 100"):
        validate_staking_parameters(1000, 365, 5.0, 105, 12)

def test_validate_staking_parameters_invalid_compound_frequency_type():
    with pytest.raises(TypeError, match="compound_frequency must be an integer"):
        validate_staking_parameters(1000, 365, 5.0, 2.0, "invalid")

def test_validate_staking_parameters_compound_frequency_zero():
    with pytest.raises(ValueError, match="compound_frequency must be positive"):
        validate_staking_parameters(1000, 365, 5.0, 2.0, 0)

def test_validate_staking_parameters_compound_frequency_negative():
    with pytest.raises(ValueError, match="compound_frequency must be positive"):
        validate_staking_parameters(1000, 365, 5.0, 2.0, -1)

def test_validate_staking_parameters_with_decimal_values():
    result = validate_staking_parameters(
        decimal.Decimal('1000.50'),
        decimal.Decimal('365.25'),
        decimal.Decimal('5.25'),
        decimal.Decimal('1.5'),
        365
    )
    assert result == True

def test_validate_staking_parameters_with_float_values():
    result = validate_staking_parameters(1000.5, 365.5, 5.5, 1.5, 12)
    assert result == True

def test_validate_staking_parameters_with_zero_values():
    result = validate_staking_parameters(0, 0, 0, 0, 1)
    assert result == True

def test_validate_staking_parameters_with_mixed_types():
    result = validate_staking_parameters(1000, 365, 5.0, 2, 12)
    assert result == True

def test_validate_staking_parameters_large_values():
    result = validate_staking_parameters(1000000, 10000, 50, 25, 365)
    assert result == True

def test_validate_staking_parameters_small_values():
    result = validate_staking_parameters(0.01, 0.5, 0.01, 0.01, 1)
    assert result == True