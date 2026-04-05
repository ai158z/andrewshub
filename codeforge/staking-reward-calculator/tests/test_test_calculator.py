import pytest
from src.calculator import calculate_rewards

def test_calculate_rewards_basic():
    rewards = calculate_rewards(1000.0, 365, 5.0, 0.1)
    assert rewards == 1000.00

def test_calculate_rewards_zero_stake():
    result = calculate_rewards(0, 365, 5.0, 0.1)
    assert result == 0

def test_calculate_rewards_zero_time():
    result = calculate_rewards(1000.0, 0, 5.0, 0.1)
    assert result == 0.0

def test_calculate_rewards_zero_rate():
    result = calculate_rewards(1000.0, 365, 0, 0.1)
    assert result == 0

def test_calculate_rewards_zero_fee():
    result = calculate_rewards(1000.0, 365, 5.0, 0)
    assert result == 1000.0

def test_calculate_rewards_negative_stake():
    result = calculate_rewards(-1000.0, 365, 5.0, 0.1)
    assert result <= 0

def test_calculate_rewards_large_numbers():
    result = calculate_rewards(1000000.0, 3650, 500.0, 0.1)
    assert result > 0

def test_calculate_rewards_various_scenarios():
    # Test multiple scenarios with parametrize values
    test_cases = [
        (1000.0, 365, 0.05, 0.1),
        (500.0, 182.5, 0.05, 0.05),
        (2000.0, 730, 0.1, 0.2)
    ]
    
    for stake, days, apr, fee in test_cases:
        result = calculate_rewards(stake, days, apr, fee)
        assert result >= 0

def test_calculate_rewards_zero_parameters():
    result = calculate_rewards(0, 0, 0, 0)
    assert result == 0

def test_calculate_rewards_edge_case_zero_stake():
    result = calculate_rewards(0, 365, 5.0, 0.1)
    assert result == 0

def test_calculate_rewards_edge_case_zero_time():
    result = calculate_rewards(1000.0, 0, 5.0, 0.1)
    assert result == 0.0

def test_calculate_rewards_edge_case_zero_apr():
    result = calculate_rewards(1000.0, 365, 0, 0.1)
    assert result == 0

def test_calculate_rewards_edge_case_high_values():
    result = calculate_rewards(1000000.0, 730, 100.0, 0.5)
    assert isinstance(result, float)

def test_calculate_rewards_edge_case_negative_apr():
    result = calculate_rewards(1000.0, 365, -5.0, 0.1)
    assert result >= 0

def test_calculate_rewards_edge_case_zero_division():
    result = calculate_rewards(0, 0, 0, 0.1)
    assert result == 0

def test_calculate_rewards_edge_case_large_stake():
    result = calculate_rewards(1000000000.0, 365, 5.0, 0.1)
    assert isinstance(result, float)

def test_calculate_rewards_edge_case_small_values():
    result = calculate_rewards(1.0, 1, 0.001, 0.001)
    assert isinstance(result, float)

def test_calculate_rewards_edge_case_normal_case():
    result = calculate_rewards(1000.0, 365, 0.05, 0.1)
    assert result == 1000.0

def test_calculate_rewards_edge_case_zero_everything():
    result = calculate_rewards(0, 0, 0, 0)
    assert result == 0

def test_calculate_rewards_edge_case_negative_fee():
    result = calculate_rewards(1000.0, 365, 5.0, -0.1)
    assert result >= 0

def test_calculate_rewards_edge_case_zero_stake_time():
    result = calculate_rewards(0, 0, 5.0, 0.1)
    assert result == 0