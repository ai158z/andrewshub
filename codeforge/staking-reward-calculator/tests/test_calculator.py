import pytest
from src.calculator import calculate_rewards

def test_calculate_rewards_positive_case():
    result = calculate_rewards(1000, 365, 0.05, 0.1)
    assert result['total_reward'] > 0
    assert result['stake_amount'] == 1000
    assert result['duration_days'] == 365
    assert result['apy'] == 0.05
    assert result['commission'] == 0.1

def test_calculate_rewards_zero_stake_amount():
    with pytest.raises(ValueError, match="Stake amount must be positive"):
        calculate_rewards(0, 365, 0.05, 0.1)

def test_calculate_rewards_negative_stake_amount():
    with pytest.raises(ValueError, match="Stake amount cannot be negative"):
        calculate_rewards(-100, 365, 0.05, 0.1)

def test_calculate_rewards_negative_duration():
    with pytest.raises(ValueError, match="Duration cannot be negative"):
        calculate_rewards(1000, -365, 0.05, 0.1)

def test_calculate_rewards_apy_out_of_range():
    with pytest.raises(ValueError, match="APY must be between 0 and 1"):
        calculate_rewards(1000, 365, 1.5, 0.1)

def test_calculate_rewards_commission_out_of_range():
    with pytest.raises(ValueError, match="Commission must be between 0 and 1"):
        calculate_rewards(1000, 365, 0.05, 1.5)

def test_calculate_rewards_zero_apy():
    result = calculate_rewards(1000, 365, 0, 0.1)
    assert result['total_reward'] == 0

def test_calculate_rewards_zero_commission():
    result = calculate_rewards(1000, 365, 0.05, 0)
    assert result['total_reward'] > 0

def test_calculate_rewards_high_commission():
    result = calculate_rewards(1000, 365, 0.05, 1)
    assert result['total_reward'] == 0

def test_calculate_rewards_various_durations():
    result = calculate_rewards(1000, 1, 0.05, 0.1)
    assert result['duration_days'] == 1

def test_calculate_rewards_various_apy_values():
    result = calculate_rewards(1000, 365, 0.1, 0.1)
    assert result['apy'] == 0.1

def test_calculate_rewards_various_commission_values():
    result = calculate_rewards(1000, 365, 0.05, 0.5)
    assert result['commission'] == 0.5

def test_calculate_rewards_various_stake_amounts():
    result = calculate_rewards(1, 365, 0.05, 0.1)
    assert result['stake_amount'] == 1

def test_calculate_rewards_negative_apy():
    with pytest.raises(ValueError, match="APY must be between 0 and 1"):
        calculate_rewards(1000, 365, -0.1, 0.1)

def test_calculate_rewards_negative_commission():
    with pytest.raises(ValueError, match="Commission cannot be negative"):
        calculate_rewards(1000, 365, 0.05, -0.1)

def test_calculate_rewards_commission_too_high():
    with pytest.raises(ValueError, match="Commission rate is too high"):
        calculate_rewards(1000, 365, 0.05, 1.1)

def test_calculate_rewards_zero_duration():
    with pytest.raises(ValueError) as exc_info:
        calculate_rewards(1000, 0, 0.05, 0.1)
    assert "Duration cannot be negative" in str(exc_info.value) or "APY must be positive" in str(exc_info.value)

def test_calculate_rewards_edge_case_small_values():
    result = calculate_rewards(0.01, 1, 0.01, 0.01)
    assert result['stake_amount'] == 0.01
    assert result['duration_days'] == 1
    assert result['apy'] == 0.01
    assert result['commission'] == 0.01

def test_calculate_rewards_edge_case_max_values():
    result = calculate_rewards(1000000, 365, 1, 1)
    assert result['total_reward'] == 0
    assert result['stake_amount'] == 1000000
    assert result['duration_days'] == 365
    assert result['apy'] == 1
    assert result['commission'] == 1

def test_calculate_rewards_edge_case_no_reward():
    result = calculate_rewards(1000, 365, 0.05, 1)
    assert result['total_reward'] == 0
    assert result['stake_amount'] == 1000
    assert result['duration_days'] == 365
    assert result['apy'] == 0.05
    assert result['commission'] == 1