import pytest
from staking_calculator import calculate_apy, calculate_compound_interest, calculate_penalty, calculate_staking_reward


def test_calculate_apy_normal():
    result = calculate_apy(0.05, 365)
    expected = 0.05
    assert pytest.approx(result, abs=1e-10) == expected


def test_calculate_apy_short_period():
    result = calculate_apy(0.10, 180)
    expected = (1 + 0.10) ** (365 / 180) - 1
    assert pytest.approx(result, abs=1e-10) == expected


def test_calculate_apy_higher_rate():
    result = calculate_apy(0.15, 365)
    expected = 0.15
    assert pytest.approx(result, abs=1e-10) == expected


def test_calculate_apy_zero_days():
    with pytest.raises(ValueError):
        calculate_apy(0.05, 0)


def test_calculate_apy_negative_rate():
    with pytest.raises(ValueError):
        calculate_apy(-0.05, 365)


def test_calculate_compound_interest_basic():
    result = calculate_compound_interest(1000, 0.05, 365)
    expected = 1000 * ((1 + 0.05) ** (365 / 365)) - 1000
    assert pytest.approx(result, abs=1e-10) == expected


def test_calculate_compound_interest_partial_year():
    result = calculate_compound_interest(5000, 0.08, 180)
    expected = 5000 * ((1 + 0.08) ** (180 / 365)) - 5000
    assert pytest.approx(result, abs=1e-10) == expected


def test_calculate_compound_interest_zero_principal():
    result = calculate_compound_interest(0, 0.05, 365)
    assert result == 0


def test_calculate_compound_interest_negative_principal():
    with pytest.raises(ValueError):
        calculate_compound_interest(-1000, 0.05, 365)


def test_calculate_compound_interest_negative_rate():
    with pytest.raises(ValueError):
        calculate_compound_interest(1000, -0.05, 365)


def test_calculate_penalty_normal():
    result = calculate_penalty(1000, 0.10)
    expected = 1000 * 0.10
    assert result == expected


def test_calculate_penalty_no_penalty():
    result = calculate_penalty(1000, 0)
    assert result == 0


def test_calculate_penalty_over_100_percent():
    with pytest.raises(ValueError):
        calculate_penalty(1000, 1.5)


def test_calculate_penalty_negative_amount():
    with pytest.raises(ValueError):
        calculate_penalty(-1000, 0.10)


def test_calculate_staking_reward_normal():
    stake_amount = 10000
    duration_days = 365
    annual_rate = 0.05
    penalty_rate = 0.10
    result = calculate_staking_reward(stake_amount, duration_days, annual_rate, penalty_rate)
    expected_interest = stake_amount * ((1 + annual_rate) ** (duration_days / 365)) - stake_amount
    assert pytest.approx(result, abs=1e-10) == expected_interest


def test_calculate_staking_reward_short_duration():
    stake_amount = 10000
    duration_days = 30
    annual_rate = 0.05
    penalty_rate = 0.10
    result = calculate_staking_reward(stake_amount, duration_days, annual_rate, penalty_rate)
    interest = stake_amount * ((1 + annual_rate) ** (duration_days / 365)) - stake_amount
    expected = interest * (1 - penalty_rate)
    assert pytest.approx(result, abs=1e-10) == expected


def test_calculate_staking_reward_negative_stake():
    with pytest.raises(ValueError):
        calculate_staking_reward(-10000, 365, 0.05, 0.10)


def test_calculate_staking_reward_negative_duration():
    with pytest.raises(ValueError):
        calculate_staking_reward(10000, -365, 0.05, 0.10)


def test_calculate_staking_reward_negative_rate():
    with pytest.raises(ValueError):
        calculate_staking_reward(10000, 365, -0.05, 0.10)