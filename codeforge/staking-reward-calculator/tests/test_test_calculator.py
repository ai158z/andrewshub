import pytest
from decimal import Decimal
from staking_calculator import calculate_staking_rewards


def test_basic_reward_calculation():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    expected_reward = stake_amount * apy
    assert abs(float(result.total_reward) - float(expected_reward)) < 0.01
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_compound_interest_daily():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 365

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.compound_rewards > Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_zero_stake_amount():
    stake_amount = Decimal('0')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward == Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_zero_duration():
    stake_amount = Decimal('1000')
    duration = 0
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward == Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_zero_apr():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward == Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_high_compound_frequency():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 365

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.compound_rewards > Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_negative_values():
    stake_amount = Decimal('-1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    with pytest.raises(ValueError):
        calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)


def test_fractional_apr():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.035')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward > Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_large_stake_amount():
    stake_amount = Decimal('1000000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward > Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_small_apr():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.0001')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward > Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_high_penalty_rate():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.5')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward > Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions > Decimal('0')


def test_zero_compound_frequency():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 0

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward == Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions == Decimal('0')


def test_negative_duration():
    stake_amount = Decimal('1000')
    duration = -365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 1

    with pytest.raises(ValueError):
        calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)


def test_fractional_penalty():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.001')
    compound_frequency = 1

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward > Decimal('0')
    assert result.compound_rewards == Decimal('0')
    assert result.penalty_deductions > Decimal('0')


def test_maximum_values():
    stake_amount = Decimal('1000000')
    duration = 365000
    apy = Decimal('1.0')
    penalty_rate = Decimal('0')
    compound_frequency = 365

    result = calculate_staking_rewards(stake_amount, duration, apy, penalty_rate, compound_frequency)
    
    assert result.total_reward > Decimal('0')
    assert result.compound_rewards > Decimal('0')
    assert result.penalty_deductions == Decimal('0')