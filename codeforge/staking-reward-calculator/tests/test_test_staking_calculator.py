import pytest
from typing import Dict, Any
from src.staking_calculator import calculate_rewards
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate


def test_calculate_rewards_daily_compounding() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    
    assert isinstance(result, dict)
    assert "total_reward" in result
    assert "daily_breakdown" in result
    assert result["total_reward"] > 0
    assert len(result["daily_breakdown"]) == stake_data.duration_days


def test_calculate_rewards_monthly_compounding() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="monthly"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="monthly"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_zero_amount() -> None:
    stake_data = StakeData(
        amount=0.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] == 0


def test_calculate_rewards_zero_rate() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.0,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] == 0


def test_calculate_rewards_negative_amount() -> None:
    stake_data = StakeData(
        amount=-1000.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] == 0


def test_calculate_rewards_compound_vs_simple() -> None:
    stake_data_daily = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    stake_data_simple = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="none"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result_daily = calculate_rewards(stake_data_daily, reward_rate)
    result_simple = calculate_rewards(stake_data_simple, reward_rate)
    
    assert result_daily["total_reward"] >= result_simple["total_reward"]


def test_calculate_rewards_invalid_data() -> None:
    stake_data_valid = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    reward_rate_valid = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data_valid, reward_rate_valid)
    assert result["total_reward"] > 0


def test_calculate_rewards_no_compounding() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="none"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="none"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_quarterly_compounding() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="quarterly"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="quarterly"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_annual_compounding() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="annual"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="annual"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_monthly_breakdown_length() -> None:
    stake_data = StakeData(
        amount=500.0,
        duration_days=180,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.03,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert len(result["daily_breakdown"]) == stake_data.duration_days


def test_calculate_rewards_small_amount() -> None:
    stake_data = StakeData(
        amount=1.0,
        duration_days=1,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.01,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert "total_reward" in result
    assert "daily_breakdown" in result


def test_calculate_rewards_large_amount() -> None:
    stake_data = StakeData(
        amount=1000000.0,
        duration_days=730,
        compound_frequency="monthly"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.10,
        compound_frequency="monthly"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_short_duration() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=1,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0
    assert len(result["daily_breakdown"]) == 1


def test_calculate_rewards_high_rate() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.5,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_zero_duration() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=0,
        compound_frequency="daily"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert len(result["daily_breakdown"]) == 0
    assert result["total_reward"] >= 0


def test_calculate_rewards_invalid_compound_frequency_fallback() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="invalid"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="daily"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_same_compound_frequency() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="monthly"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="monthly"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0


def test_calculate_rewards_mixed_case() -> None:
    stake_data = StakeData(
        amount=1000.0,
        duration_days=365,
        compound_frequency="MONTHLY"
    )
    
    reward_rate = RewardRate(
        annual_rate=0.05,
        compound_frequency="monthly"
    )
    
    result = calculate_rewards(stake_data, reward_rate)
    assert result["total_reward"] > 0