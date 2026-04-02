import pytest
from unittest.mock import patch, MagicMock
from src.staking_calculator import StakingCalculator
from src.models import StakingResult

def test_init_staking_calculator():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12, penalty_rate=0.1)
    assert calculator.config.apy == 0.05
    assert calculator.config.compound_frequency == 12
    assert calculator.config.penalty_rate == 0.1

def test_init_staking_calculator_defaults():
    calculator = StakingCalculator(apy=0.08)
    assert calculator.config.apy == 0.08
    assert calculator.config.compound_frequency == 1
    assert calculator.config.penalty_rate == 0.0

def test_calculate_rewards_valid_inputs():
    calculator = StakingCalculator(apy=0.05, compound_frequency=12)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365)
    assert "gross_reward" in result
    assert "net_reward" in result
    assert "penalty" in result
    assert "duration" in result
    assert result["duration"] == 365

def test_calculate_rewards_with_penalty():
    calculator = StakingCalculator(apy=0.05, compound_frequency=1, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=180, lockup_days=365)
    assert result["penalty"] > 0

def test_calculate_rewards_no_penalty_when_lockup_exceeds_duration():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365, lockup_days=180)
    assert result["penalty"] == 0

def test_calculate_rewards_no_penalty_when_no_lockup():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365)
    assert result["penalty"] == 0

def test_calculate_rewards_zero_stake_amount():
    calculator = StakingCalculator(apy=0.05)
    result = calculator.calculate_rewards(stake_amount=0, duration_days=365)
    assert result["gross_reward"] == 0
    assert result["net_reward"] == 0
    assert result["penalty"] == 0

def test_calculate_rewards_zero_duration():
    calculator = StakingCalculator(apy=0.05)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=0)
    assert result["gross_reward"] == 0
    assert result["net_reward"] == 0
    assert result["penalty"] == 0

def test_calculate_rewards_negative_stake_amount_raises_error():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=-1000, duration_days=365)

def test_calculate_rewards_negative_duration_raises_error():
    calculator = StakingCalculator(apy=0.05)
    with pytest.raises(ValueError):
        calculator.calculate_rewards(stake_amount=1000, duration_days=-365)

def test_calculate_rewards_zero_lockup_days():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365, lockup_days=0)
    assert result["penalty"] == 0

def test_calculate_rewards_lockup_equal_to_duration():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365, lockup_days=365)
    assert result["penalty"] == 0

def test_calculate_rewards_lockup_greater_than_duration():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=180, lockup_days=365)
    assert result["penalty"] == 0

def test_calculate_rewards_invalid_inputs_raises_error():
    calculator = StakingCalculator(apy=0.05)
    with patch('src.staking_calculator.validate_inputs', return_value=False):
        with pytest.raises(ValueError):
            calculator.calculate_rewards(stake_amount=1000, duration_days=365)

def test_calculate_rewards_runtime_error_on_calculation_failure():
    calculator = StakingCalculator(apy=0.05)
    with patch('src.staking_calculator.calculate_compound_interest', side_effect=Exception("Calculation error")):
        with pytest.raises(RuntimeError):
            calculator.calculate_rewards(stake_amount=1000, duration_days=365)

def test_calculate_rewards_high_apy():
    calculator = StakingCalculator(apy=0.5, compound_frequency=365)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365)
    assert result["gross_reward"] > 0
    assert result["net_reward"] == result["gross_reward"]

def test_calculate_rewards_compound_frequency_greater_than_duration():
    calculator = StakingCalculator(apy=0.05, compound_frequency=730)  # More than daily compounding for 1 year
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365)
    assert result["gross_reward"] >= 0

def test_calculate_rewards_zero_apy():
    calculator = StakingCalculator(apy=0.0)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365)
    assert result["gross_reward"] == 0
    assert result["net_reward"] == 0

def test_calculate_rewards_zero_penalty_rate():
    calculator = StakingCalculator(apy=0.05, penalty_rate=0.0)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=180, lockup_days=365)
    assert result["penalty"] == 0
    assert result["net_reward"] == result["gross_reward"]

def test_calculate_rewards_full_result_object():
    calculator = StakingCalculator(apy=0.05, compound_frequency=4, penalty_rate=0.1)
    result = calculator.calculate_rewards(stake_amount=1000, duration_days=365, lockup_days=180)
    staking_result = StakingResult(**result)
    assert isinstance(staking_result, StakingResult)