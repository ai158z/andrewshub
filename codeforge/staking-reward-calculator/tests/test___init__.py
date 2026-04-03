import pytest
from decimal import Decimal
from staking_calculator import calculate_staking_rewards, calculate_compound_interest, apply_compound_interest
from staking_calculator.models import RewardBreakdown

def test_calculate_staking_rewards_valid_input():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.05'),
        compounding_frequency=12
    )
    assert isinstance(result, RewardBreakdown)
    assert result.total_reward > Decimal('1000')
    assert result.compound_rewards > Decimal('0')

def test_calculate_staking_rewards_with_penalty():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.05'),
        compounding_frequency=12,
        penalty_rate=Decimal('0.1')
    )
    assert result.penalty_deductions > Decimal('0')

def test_calculate_staking_rewards_zero_apy():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0'),
        compounding_frequency=12
    )
    assert result.total_reward == Decimal('1000')
    assert result.compound_rewards == Decimal('0')

def test_calculate_staking_rewards_zero_duration():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=0,
        apy=Decimal('0.05'),
        compounding_frequency=12
    )
    assert result.total_reward == Decimal('1000')
    assert result.compound_rewards == Decimal('0')

def test_calculate_staking_rewards_invalid_stake_amount():
    with pytest.raises(ValueError):
        calculate_staking_rewards(
            stake_amount=Decimal('-1000'),
            duration=365,
            apy=Decimal('0.05'),
            compounding_frequency=12
        )

def test_calculate_staking_rewards_invalid_apy():
    with pytest.raises(ValueError):
        calculate_staking_rewards(
            stake_amount=Decimal('1000'),
            duration=365,
            apy=Decimal('-0.05'),
            compounding_frequency=12
        )

def test_calculate_staking_rewards_invalid_duration():
    with pytest.raises(ValueError):
        calculate_staking_rewards(
            stake_amount=Decimal('1000'),
            duration=-1,
            apy=Decimal('0.05'),
            compounding_frequency=12
        )

def test_calculate_staking_rewards_invalid_compounding_frequency():
    with pytest.raises(ValueError):
        calculate_staking_rewards(
            stake_amount=Decimal('1000'),
            duration=365,
            apy=Decimal('0.05'),
            compounding_frequency=0
        )

def test_calculate_compound_interest_basic():
    principal = 1000.0
    rate = 0.05
    time = 1.0
    frequency = 1
    result = calculate_compound_interest(principal, rate, time, frequency)
    assert result == 1050.0

def test_apply_compound_interest():
    principal = 1000.0
    rate = 0.05
    time = 1.0
    frequency = 12
    result = apply_compound_interest(principal, rate, time, frequency)
    assert result > principal

def test_calculate_staking_rewards_high_compounding_frequency():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.05'),
        compounding_frequency=365
    )
    assert isinstance(result, RewardBreakdown)
    assert result.total_reward > Decimal('1000')

def test_calculate_staking_rewards_no_compounding():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.05'),
        compounding_frequency=1
    )
    # Simple interest calculation for comparison
    simple_interest = Decimal('1000') * Decimal('0.05')
    assert result.compound_rewards >= simple_interest

def test_calculate_staking_rewards_large_numbers():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000000'),
        duration=365,
        apy=Decimal('0.1'),
        compounding_frequency=12
    )
    assert isinstance(result, RewardBreakdown)
    assert result.total_reward > Decimal('1000000')

def test_calculate_staking_rewards_small_apy():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.0001'),
        compounding_frequency=12
    )
    assert result.total_reward > Decimal('1000')
    assert result.compound_rewards > Decimal('0')

def test_calculate_staking_rewards_fractional_duration():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=182,  # Half a year
        apy=Decimal('0.05'),
        compounding_frequency=12
    )
    assert isinstance(result, RewardBreakdown)

def test_calculate_staking_rewards_max_penalty():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.05'),
        compounding_frequency=12,
        penalty_rate=Decimal('1')  # 100% penalty
    )
    assert result.penalty_deductions > Decimal('0')

def test_calculate_staking_rewards_edge_case_zero_penalty():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('0.05'),
        compounding_frequency=12,
        penalty_rate=Decimal('0')
    )
    assert result.penalty_deductions == Decimal('0')

def test_calculate_staking_rewards_edge_case_maximum_apy():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=365,
        apy=Decimal('1'),  # 100% APY
        compounding_frequency=12
    )
    assert result.total_reward == Decimal('2000')  # Simple interest would be 2000

def test_calculate_staking_rewards_edge_case_single_day():
    result = calculate_staking_rewards(
        stake_amount=Decimal('1000'),
        duration=1,
        apy=Decimal('0.05'),
        compounding_frequency=365
    )
    assert result.total_reward > Decimal('1000')