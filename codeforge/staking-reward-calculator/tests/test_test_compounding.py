import pytest
from decimal import Decimal
from staking_calculator import calculate_staking_rewards
from staking_calculator.calculator import calculate_rewards
from staking_calculator.models import StakingParameters
from staking_calculator.validators import validate_staking_parameters

@pytest.fixture
def base_params():
    return {
        "stake_amount": Decimal('1000'),
        "duration": 365,
        "apy": Decimal('0.05'),
        "penalty_rate": Decimal('0.00'),
        "compound_frequency": 365
    }

def test_daily_compounding(base_params):
    params = base_params.copy()
    params["compound_frequency"] = 365
    is_valid = validate_staking_parameters(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert is_valid
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    time_in_years = Decimal(params["duration"]) / Decimal('365')
    expected_amount = params["stake_amount"] * (Decimal('1') + params["apy"] / params["compound_frequency"]) ** (params["compound_frequency"] * time_in_years)
    assert round(float(result.total_reward), 2) == round(float(expected_amount - params["stake_amount"]), 2)

def test_weekly_compounding(base_params):
    params = base_params.copy()
    params["compound_frequency"] = 52
    is_valid = validate_staking_parameters(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert is_valid
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    time_in_years = Decimal(params["duration"]) / Decimal('365')
    expected_amount = params["stake_amount"] * (Decimal('1') + params["apy"] / params["compound_frequency"]) ** (params["compound_frequency"] * time_in_years)
    assert round(float(result.total_reward), 2) == round(float(expected_amount - params["stake_amount"]), 2)

def test_monthly_compounding(base_params):
    params = base_params.copy()
    params["compound_frequency"] = 12
    is_valid = validate_staking_parameters(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert is_valid
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    time_in_years = Decimal(params["duration"]) / Decimal('365')
    expected_amount = params["stake_amount"] * (Decimal('1') + params["apy"] / params["compound_frequency"]) ** (params["compound_frequency"] * time_in_years)
    assert round(float(result.total_reward), 2) == round(float(expected_amount - params["stake_amount"]), 2)

def test_annual_compounding(base_params):
    params = base_params.copy()
    params["compound_frequency"] = 1
    is_valid = validate_staking_parameters(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert is_valid
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    time_in_years = Decimal(params["duration"]) / Decimal('365')
    expected_amount = params["stake_amount"] * (Decimal('1') + params["apy"] / params["compound_frequency"]) ** (params["compound_frequency"] * time_in_years)
    assert round(float(result.total_reward), 2) == round(float(expected_amount - params["stake_amount"]), 2)

def test_validate_staking_parameters_valid(base_params):
    is_valid = validate_staking_parameters(
        base_params["stake_amount"],
        base_params["duration"],
        base_params["apy"],
        base_params["penalty_rate"],
        base_params["compound_frequency"]
    )
    assert is_valid

def test_validate_staking_parameters_invalid_amount():
    is_valid = validate_staking_parameters(
        Decimal('-1000'),
        365,
        Decimal('0.05'),
        Decimal('0.00'),
        365
    )
    assert not is_valid

def test_validate_staking_parameters_invalid_duration():
    is_valid = validate_staking_parameters(
        Decimal('1000'),
        -1,
        Decimal('0.05'),
        Decimal('0.00'),
        365
    )
    assert not is_valid

def test_validate_staking_parameters_invalid_apy():
    is_valid = validate_staking_parameters(
        Decimal('1000'),
        365,
        Decimal('-0.05'),
        Decimal('0.00'),
        365
    )
    assert not is_valid

def test_validate_staking_parameters_invalid_penalty():
    is_valid = validate_staking_parameters(
        Decimal('1000'),
        365,
        Decimal('0.05'),
        Decimal('-0.1'),
        365
    )
    assert not is_valid

def test_validate_staking_parameters_invalid_frequency():
    is_valid = validate_staking_parameters(
        Decimal('1000'),
        365,
        Decimal('0.05'),
        Decimal('0.00'),
        0
    )
    assert not is_valid

def test_calculate_rewards_with_penalty(base_params):
    params = base_params.copy()
    params["penalty_rate"] = Decimal('0.02')
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert result.total_reward >= 0

def test_calculate_rewards_zero_duration(base_params):
    params = base_params.copy()
    params["duration"] = 0
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert result.total_reward == 0

def test_calculate_rewards_zero_apy(base_params):
    params = base_params.copy()
    params["apy"] = Decimal('0')
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert result.total_reward == 0

def test_calculate_rewards_high_compound_frequency(base_params):
    params = base_params.copy()
    params["compound_frequency"] = 1000
    is_valid = validate_staking_parameters(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert is_valid
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    time_in_years = Decimal(params["duration"]) / Decimal('365')
    expected_amount = params["stake_amount"] * (Decimal('1') + params["apy"] / params["compound_frequency"]) ** (params["compound_frequency"] * time_in_years)
    assert round(float(result.total_reward), 2) == round(float(expected_amount - params["stake_amount"]), 2)

def test_calculate_rewards_low_compound_frequency(base_params):
    params = base_params.copy()
    params["compound_frequency"] = 2
    is_valid = validate_staking_parameters(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    assert is_valid
    result = calculate_rewards(
        params["stake_amount"],
        params["duration"],
        params["apy"],
        params["penalty_rate"],
        params["compound_frequency"]
    )
    time_in_years = Decimal(params["duration"]) / Decimal('365')
    expected_amount = params["stake_amount"] * (Decimal('1') + params["apy"] / params["compound_frequency"]) ** (params["compound_frequency"] * time_in_years)
    assert round(float(result.total_reward), 2) == round(float(expected_amount - params["stake_amount"]), 2)