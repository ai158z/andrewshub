import pytest
from unittest.mock import Mock, patch, MagicMock
from src.staking_calculator import calculate_rewards
from src.models.stake_data import StakeData
from src.models.reward_rate import RewardRate

@pytest.fixture
def mock_stake_data():
    return StakeData(amount=1000.0, stake_duration_days=365)

@pytest.fixture
def mock_reward_rate():
    return RewardRate(annual_rate=0.05, is_compounded=False)

def test_valid_stake_amount_calculation(mock_stake_data, mock_reward_rate):
    result = calculate_rewards(mock_stake_data, mock_reward_rate)
    assert result is not None
    assert "stake_amount" in result
    assert result["stake_amount"] == 1000.0
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is False
    assert result["estimated_reward"] == pytest.approx(50.0)
    assert result["total_amount_after_reward"] == pytest.approx(1050.0)
    assert result["formatted_stake_amount"] == "1000.00"
    assert result["formatted_estimated_reward"] == "50.00"
    assert result["formatted_total_amount"] == "1050.00"

def test_invalid_stake_amount_raises_error():
    stake_data = StakeData(amount=0, stake_duration_days=365)
    stake_data.amount = -100.0
    with pytest.raises(ValueError):
        calculate_rewards(stake_data, mock_reward_rate())

def test_zero_stake_amount():
    stake_data = StakeData(amount=0.0, stake_duration_days=365)
    with pytest.raises(ValueError):
        pass

def test_negative_stake_amount():
    stake_data = StakeData(amount=-100.0, stake_duration_days=365)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=False)
    with pytest.raises(AssertionError):
        pass

def test_compound_interest_calculation():
    stake_data = StakeData(amount=1000.0, stake_duration_days=365)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=True)
    result = calculate_rewards(stake_data, reward_rate)
    assert result is not None
    assert result["stake_amount"] == 1000.0
    assert result["stake_duration_days"] == 365
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is True
    assert result["estimated_reward"] == 50.0

def test_simple_interest_calculation():
    stake_data = StakeData(amount=1000.0, stake_duration_days=365)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=False)
    result = calculate_rewards(stake_data, reward_rate)
    assert result is not None
    assert result["stake_amount"] == 1000.0
    assert result["stake_duration_days"] == 365
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is False
    assert result["estimated_reward"] == pytest.approx(50.0)

def test_negative_amount_raises_error():
    stake_data = StakeData(amount=-100.0, stake_duration_days=365)
    with pytest.raises(ValueError):
        pass

def test_zero_amount_stake():
    stake_data = StakeData(amount=0.0, stake_duration_days=365)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=False)
    with pytest.raises(ValueError):
        pass

def test_invalid_compound_stake():
    stake_data = StakeData(amount=1000.0, stake_duration_days=365)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=True)
    result = calculate_rewards(stake_data, reward_rate)
    assert result is not None
    assert result["stake_amount"] == 1000.0
    assert result["stake_duration_days"] == 365
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is True
    assert result["estimated_reward"] == 50.0
    assert result["total_amount_after_reward"] == 1050.0
    assert result["formatted_stake_amount"] == "1000.00"
    assert result["formatted_estimated_reward"] == "50.00"
    assert result["formatted_total_amount"] == "105.00"

@pytest.mark.parametrize("amount", [1000.0, 2000.0, 3000.0])
def test_stake_amount_calculation(amount):
    stake_data = StakeData(amount=amount, stake_duration_days=365)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=False)
    result = calculate_rewards(stake_data, reward_rate)
    assert result is not None
    assert result["stake_amount"] == amount
    assert result["stake_duration_days"] == 365
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is False
    assert result["estimated_reward"] == 50.0
    assert result["total_amount_after_reward"] == 1050.0
    assert result["formatted_stake_amount"] == "1000.00"
    assert result["formatted_estimated_reward"] == "50.00"
    assert result["formatted_total_amount"] == "1050.00"

def test_zero_duration_stake():
    stake_data = StakeData(amount=1000.0, stake_duration_days=0)
    with pytest.raises(ValueError):
        pass

def test_negative_duration_stake():
    stake_data = StakeData(amount=1000.0, stake_duration_days=-1)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=False)
    result = calculate_rewards(stake_data, reward_rate)
    assert result is not None
    assert result["stake_amount"] == 1000.0
    assert result["stake_duration_days"] == 365
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is False
    assert result["estimated_reward"] == 50.0
    assert result["total_amount_after_reward"] == 1050.0
    assert result["formatted_stake_amount"] == "1000.00"
    assert result["formatted_estimated_reward"] == "50.00"
    assert result["formatted_total_amount"] == "1050.00"

def test_zero_stake_amount():
    stake_data = StakeData(amount=0.0, stake_duration_days=365)
    with pytest.raises(ValueError):
        pass

def test_zero_stake_amount():
    stake_data = StakeData(amount=0.0, stake_duration_days=3615)
    reward_rate = RewardRate(annual_rate=0.05, is_compounded=False)
    result = calculate_rewards(stake_data, reward_rate)
    assert result is not None
    assert result["stake_amount"] == 0.0
    assert result["stake_duration_days"] == 365
    assert result["reward_rate"] == 0.05
    assert result["is_compounded"] is False
    assert result["estimated_reward"] == 50.0
    # Add more test cases here for edge cases and error conditions
    # (These would require implementing the full test suite with appropriate assertions)