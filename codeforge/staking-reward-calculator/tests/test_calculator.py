import pytest
from decimal import Decimal
from src.calculator import calculate_rewards, calculate_apy, calculate_periodic_rewards

def test_calculate_rewards_valid_inputs():
    result = calculate_rewards(1000, 0.05, 365)
    assert result['principal'] == 1000.0
    assert result['rewards'] > 0
    assert result['total'] > result['principal']

def test_calculate_rewards_zero_duration():
    result = calculate_rewards(1000, 0.05, 0)
    assert result['rewards'] == 0
    assert result['principal'] == 1000.0
    assert result['total'] == 1000.0

def test_calculate_rewards_negative_principal():
    with pytest.raises(ValueError, match="Principal amount cannot be negative"):
        calculate_rewards(-1000, 0.05, 365)

def test_calculate_rewards_negative_apr():
    with pytest.raises(ValueError, match="APR cannot be negative"):
        calculate_rewards(1000, -0.05, 365)

def test_calculate_rewards_negative_duration():
    with pytest.raises(ValueError, match="Duration cannot be negative"):
        calculate_rewards(1000, 0.05, -365)

def test_calculate_rewards_none_inputs():
    with pytest.raises(ValueError, match="All parameters"):
        calculate_rewards(None, 0.05, 365)

def test_calculate_rewards_invalid_numeric_input():
    with pytest.raises(ValueError, match="Invalid numeric input"):
        calculate_rewards("invalid", 0.05, 365)

def test_calculate_rewards_string_inputs():
    result = calculate_rewards("1000", "0.05", "365")
    assert result['principal'] == 1000.0

def test_calculate_apy_default_compounding():
    apy = calculate_apy(0.05)
    assert apy > 0.05  # APY should be slightly higher than APR

def test_calculate_apy_custom_compounding():
    apy = calculate_apy(0.05, 12)  # Monthly compounding
    expected_apy = (1 + 0.05/12)**12 - 1
    assert abs(apy - expected_apy) < 0.0001

def test_calculate_apy_invalid_compounding():
    with pytest.raises(ValueError):
        calculate_apy("invalid")

def test_calculate_periodic_rewards_daily():
    result = calculate_periodic_rewards(1000, 0.05, 365, "daily")
    assert result['periods'] == 365
    assert result['principal'] == 1000.0
    assert result['rewards'] >= 0

def test_calculate_periodic_rewards_weekly():
    result = calculate_periodic_rewards(1000, 0.05, 52, "weekly")
    assert result['periods'] == 52

def test_calculate_periodic_rewards_monthly():
    result = calculate_periodic_rewards(1000, 0.05, 12, "monthly")
    assert result['periods'] == 12

def test_calculate_periodic_rewards_invalid_period_duration():
    with pytest.raises(ValueError, match="period_duration must be"):
        calculate_periodic_rewards(1000, 0.05, 12, "yearly")

def test_calculate_periodic_rewards_calculation_error():
    with pytest.raises(ValueError):
        calculate_periodic_rewards("invalid", 0.05, 12)

def test_calculate_rewards_precision():
    # Test that high precision calculations work correctly
    result = calculate_rewards(1000, "0.2", 365)  # 20% APR for a year
    # With daily compounding, should be significantly more than simple interest
    simple_interest = 1000 * 0.2
    assert result['rewards'] > simple_interest

def test_calculate_rewards_edge_case_zero_apr():
    result = calculate_rewards(1000, 0, 365)
    assert result['rewards'] == 0
    assert result['total'] == 1000.0

def test_calculate_rewards_edge_case_zero_principal():
    result = calculate_rewards(0, 0.05, 365)
    assert result['rewards'] == 0
    assert result['total'] == 0
    assert result['principal'] == 0