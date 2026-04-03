import pytest
from decimal import Decimal
from staking_calculator.calculator import calculate_rewards
from staking_calculator.validators import validate_staking_parameters


def test_penalty_calculation_valid_parameters():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    is_valid = validate_staking_parameters(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )
    assert is_valid is True


def test_penalty_deductions_exist():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions is not None
    assert result.penalty_deductions > Decimal('0')
    assert isinstance(result.penalty_deductions, Decimal)


def test_penalty_deductions_zero_rate():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions == Decimal('0')


def test_penalty_deductions_calculation():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    expected_penalty = result.compound_rewards * penalty_rate
    assert result.penalty_deductions == expected_penalty


def test_high_penalty_rate_deduction():
    stake_amount = Decimal('5000')
    duration = 180
    apy = Decimal('0.08')
    high_penalty_rate = Decimal('0.25')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        high_penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions is not None
    assert result.penalty_deductions > Decimal('0')


def test_negative_penalty_rate_raises_error():
    stake_amount = Decimal('5000')
    duration = 180
    apy = Decimal('0.08')
    negative_penalty_rate = Decimal('-0.1')
    compound_frequency = 365

    with pytest.raises(ValueError):
        calculate_rewards(
            stake_amount,
            duration,
            apy,
            negative_penalty_rate,
            compound_frequency
        )


def test_total_reward_positive_with_penalty():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.total_reward > Decimal('0')


def test_penalty_deduction_proportional_to_rewards():
    stake_amount = Decimal('5000')
    duration = 180
    apy = Decimal('0.08')
    penalty_rate = Decimal('0.25')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    expected_gross_reward = stake_amount * (1 + apy * duration / 365)
    expected_penalty = expected_gross_reward * penalty_rate

    assert abs(result.penalty_deductions - expected_penalty) < Decimal('0.01')


def test_zero_stake_amount_no_penalty():
    stake_amount = Decimal('0')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions == Decimal('0')
    assert result.total_reward == Decimal('0')


def test_zero_duration_no_penalty():
    stake_amount = Decimal('1000')
    duration = 0
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions == Decimal('0')
    assert result.total_reward == Decimal('0')


def test_zero_apy_no_penalty():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0')
    penalty_rate = Decimal('0.10')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions == Decimal('0')
    assert result.total_reward == stake_amount


def test_very_high_penalty_rate():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.99')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions > Decimal('0')
    assert result.total_reward > Decimal('0')


def test_very_low_penalty_rate():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.001')
    compound_frequency = 365

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions > Decimal('0')
    assert result.total_reward > Decimal('0')


def test_penalty_with_monthly_compounding():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 12

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions is not None
    assert result.penalty_deductions > Decimal('0')


def test_penalty_with_no_compounding():
    stake_amount = Decimal('1000')
    duration = 365
    apy = Decimal('0.05')
    penalty_rate = Decimal('0.10')
    compound_frequency = 1

    result = calculate_rewards(
        stake_amount,
        duration,
        apy,
        penalty_rate,
        compound_frequency
    )

    assert result.penalty_deductions is not None
    assert result.penalty_deductions > Decimal('0')