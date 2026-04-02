import pytest
from decimal import Decimal
from src.staking_calculator import calculate_apy, calculate_compound_interest, calculate_penalty, calculate_staking_reward

def test_calculate_apy_positive():
    result = calculate_apy(0.05, 365)
    assert isinstance(result, Decimal)
    assert result > 0

def test_calculate_apy_zero_days_raises():
    with pytest.raises(ValueError, match="Days must be a positive integer"):
        calculate_apy(0.05, 0)

def test_calculate_apy_negative_rate_raises():
    with pytest.raises(ValueError, match="Rate cannot be negative"):
        calculate_apy(-0.05, 365)

def test_calculate_compound_interest_basic():
    result = calculate_compound_interest(1000, 0.05, 365)
    assert isinstance(result, Decimal)
    assert result > 1000

def test_calculate_compound_interest_zero_principal():
    result = calculate_compound_interest(0, 0.05, 365)
    assert result == 0

def test_calculate_compound_interest_negative_principal_raises():
    with pytest.raises(ValueError, match="Principal cannot be negative"):
        calculate_compound_interest(-1000, 0.05, 365)

def test_calculate_compound_interest_negative_time_raises():
    with pytest.raises(ValueError, match="Time cannot be negative"):
        calculate_compound_interest(1000, 0.05, -10)

def test_calculate_penalty_basic():
    result = calculate_penalty(1000, 0.05)
    assert isinstance(result, Decimal)
    assert result == Decimal('50')

def test_calculate_penalty_negative_rate_raises():
    with pytest.raises(ValueError, match="Penalty rate cannot be negative"):
        calculate_penalty(1000, -0.05)

def test_calculate_penalty_zero_amount():
    result = calculate_penalty(0, 0.05)
    assert result == 0

def test_calculate_staking_reward_basic():
    result = calculate_staking_reward(1000, 365, 0.05, 0.02)
    assert 'reward' in result
    assert 'penalty' in result
    assert 'apy' in result
    assert result['reward'] > 1000

def test_calculate_staking_reward_zero_amount_raises():
    with pytest.raises(ValueError, match="Stake amount must be positive"):
        calculate_staking_reward(0, 365, 0.05, 0.02)

def test_calculate_staking_reward_negative_duration_raises():
    with pytest.raises(ValueError, match="Duration must be positive"):
        calculate_staking_reward(1000, 0, 0.05, 0.02)

def test_calculate_staking_reward_negative_amount_raises():
    with pytest.raises(ValueError, match="Stake amount must be positive"):
        calculate_staking_reward(-1000, 365, 0.05, 0.02)

def test_calculate_staking_reward_zero_duration_raises():
    with pytest.raises(ValueError, match="Duration must be positive"):
        calculate_staking_reward(1000, 0, 0.05, 0.02)

def test_calculate_staking_reward_negative_rate():
    result = calculate_staking_reward(1000, 365, -0.05, 0.02)
    assert 'reward' in result
    assert 'penalty' in result
    assert 'apy' in result

def test_calculate_apy_edge_cases():
    # Test with very small rate
    result = calculate_apy(0.0001, 365)
    assert isinstance(result, Decimal)
    
    # Test with 0 rate
    result = calculate_apy(0, 365)
    assert result == 0

def test_calculate_compound_interest_edge_cases():
    # Test with 0 rate
    result = calculate_compound_interest(1000, 0, 365)
    assert result == 1000

def test_calculate_penalty_edge_cases():
    # Test with 0 penalty rate
    result = calculate_penalty(1000, 0)
    assert result == 0
    
    # Test with 100% penalty rate
    result = calculate_penalty(1000, 1)
    assert result == 1000

def test_calculate_staking_reward_edge_cases():
    # Test with 0 rates
    result = calculate_staking_reward(1000, 365, 0, 0)
    assert result['reward'] == 1000
    assert result['penalty'] == 0
    assert result['apy'] == 0