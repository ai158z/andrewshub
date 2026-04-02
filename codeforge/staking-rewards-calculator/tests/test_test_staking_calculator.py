import pytest
from src.staking_calculator import StakingCalculator


def test_calculate_rewards_compound():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=365)
    
    assert isinstance(result, dict)
    assert "gross_reward" in result
    assert "net_reward" in result
    assert "penalty" in result
    assert "duration" in result
    assert result["gross_reward"] > 0
    assert result["net_reward"] >= 0
    assert result["penalty"] >= 0
    assert result["duration"] == 365


def test_calculate_rewards_simple():
    calculator = StakingCalculator(apy=0.03, compound_frequency=1)
    result = calculator.calculate_rewards(stake_amount=5000.0, duration_days=180)
    
    assert isinstance(result, dict)
    assert "gross_reward" in result
    assert result["penalty"] == 0
    assert result["duration"] == 180


def test_calculate_with_penalty():
    calculator = StakingCalculator(apy=0.08, compound_frequency=4, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=2000.0, duration_days=90, lockup_days=180)
    
    assert isinstance(result, dict)
    assert result["penalty"] > 0
    assert result["net_reward"] < result["gross_reward"]
    assert result["duration"] == 90


def test_invalid_stake_amount_negative():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=-100.0, duration_days=365)


def test_invalid_stake_amount_zero():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=0.0, duration_days=365)


def test_invalid_duration_negative():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=1000.0, duration_days=-30)


def test_invalid_duration_zero():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=1000.0, duration_days=0)


def test_invalid_lockup_days_negative():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=1000.0, duration_days=365, lockup_days=-30)


def test_no_penalty_when_duration_exceeds_lockup():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=365, lockup_days=180)
    
    assert result["penalty"] == 0
    assert result["net_reward"] == result["gross_reward"]


def test_high_compound_frequency():
    calculator = StakingCalculator(apy=0.05, compound_frequency=365)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=365)
    
    assert result["gross_reward"] > 0


def test_zero_apy():
    calculator = StakingCalculator(apy=0.0, compound_frequency=12)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=365)
    
    assert result["gross_reward"] == 0
    assert result["net_reward"] == 0
    assert result["penalty"] == 0


def test_high_penalty_rate():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12, penalty_rate=0.5)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=90, lockup_days=180)
    
    assert result["penalty"] > 0
    assert result["net_reward"] < result["gross_reward"]


def test_same_lockup_and_duration():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=180, lockup_days=180)
    
    assert result["penalty"] == 0
    assert result["net_reward"] == result["gross_reward"]


def test_very_short_duration():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=1)
    
    assert result["gross_reward"] > 0
    assert result["penalty"] == 0


def test_large_stake_amount():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12)
    result = calculator.calculate_rewards(stake_amount=100000.0, duration_days=365)
    
    assert result["gross_reward"] > 0
    assert result["net_reward"] > 0


def test_no_compounding():
    calculator = StakingCalculator(apy=0.05, compound_frequency=0)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=365)
    
    assert result["gross_reward"] >= 0


def test_lockup_greater_than_duration():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=90, lockup_days=365)
    
    assert result["penalty"] > 0
    assert result["net_reward"] < result["gross_reward"]


def test_zero_penalty_rate():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12, penalty_rate=0.0)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=90, lockup_days=180)
    
    assert result["penalty"] == 0
    assert result["net_reward"] == result["gross_reward"]


def test_fractional_apy():
    calculator = StakingCalculator(apy=0.045, compound_frequency=12)
    result = calculator.calculate_rewards(stake_amount=1000.0, duration_days=365)
    
    assert result["gross_reward"] > 0


def test_minimum_valid_inputs():
    calculator = StakingCalculator(apy=0.0001, compound_frequency=1, penalty_rate=0.99)
    result = calculator.calculate_rewards(stake_amount=1.0, duration_days=1)
    
    assert isinstance(result, dict)
    assert result["duration"] == 1