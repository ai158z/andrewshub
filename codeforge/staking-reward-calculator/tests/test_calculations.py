import pytest
import math
from backend.src.utils.calculations import calculate_rewards, project_rewards

def test_calculate_rewards_positive_case():
    result = calculate_rewards(1000, 0.05, 365)
    expected = 1000 * (math.exp(0.05 * 1) - 1)
    assert math.isclose(result, expected, rel_tol=1e-10)

def test_calculate_rewards_zero_values():
    result = calculate_rewards(0, 0, 1)
    assert result == 0

def test_calculate_rewards_negative_stake_raises_error():
    with pytest.raises(ValueError):
        calculate_rewards(-1000, 0.05, 365)

def test_calculate_rewards_negative_apr_raises_error():
    with pytest.raises(ValueError):
        calculate_rewards(1000, -0.05, 365)

def test_calculate_rewards_zero_duration_raises_error():
    with pytest.raises(ValueError):
        calculate_rewards(1000, 0.05, 0)

def test_project_rewards_valid_params():
    params = {
        'initial_stake': 1000,
        'apr': 0.05,
        'duration_days': 365,
        'compounding_frequency': 'daily'
    }
    result = project_rewards(params)
    assert 'total_rewards' in result
    assert 'projected_values' in result
    assert 'final_amount' in result

def test_project_rewards_invalid_initial_stake_raises_error():
    params = {
        'initial_stake': -1000,
        'apr': 0.05,
        'duration_days': 365,
        'compounding_frequency': 'daily'
    }
    with pytest.raises(ValueError):
        project_rewards(params)

def test_project_rewards_invalid_apr_raises_error():
    params = {
        'initial_stake': 1000,
        'apr': -0.05,
        'duration_days': 365,
        'compounding_frequency': 'daily'
    }
    with pytest.raises(ValueError):
        project_rewards(params)

def test_project_rewards_zero_duration_raises_error():
    params = {
        'initial_stake': 1000,
        'apr': 0.05,
        'duration_days': 0,
        'compounding_frequency': 'daily'
    }
    with pytest.raises(ValueError):
        project_rewards(params)

def test_calculate_rewards_large_values():
    result = calculate_rewards(1000000, 0.2, 1000)
    expected = 1000000 * (math.exp(0.2 * (1000/365)) - 1)
    assert math.isclose(result, expected, rel_tol=1e-10)

def test_calculate_rewards_small_values():
    result = calculate_rewards(0.01, 0.001, 1)
    expected = 0.01 * (math.exp(0.001 * (1/365)) - 1)
    assert math.isclose(result, expected, rel_tol=1e-10)

def test_project_rewards_small_values():
    params = {
        'initial_stake': 0.01,
        'apr': 0.001,
        'duration_days': 1,
        'compounding_frequency': 'daily'
    }
    result = project_rewards(params)
    assert result['final_amount'] > 0

def test_project_rewards_missing_params_raises_error():
    params = {
        'initial_stake': 1000,
        'apr': 0.05
    }
    with pytest.raises(ValueError):
        project_rewards(params)

def test_project_rewards_extra_duration_key_ignored():
    params = {
        'initial_stake': 1000,
        'apr': 0.05,
        'duration_days': 365,
        'compounding_frequency': 'daily',
        'extra_key': 'ignored'
    }
    result = project_rewards(params)
    assert 'total_rewards' in result

def test_calculate_rewards_fractional_days():
    result = calculate_rewards(1000, 0.05, 182.5)
    expected = 1000 * (math.exp(0.05 * (182.5/365)) - 1)
    assert math.isclose(result, expected, rel_tol=1e-10)

def test_calculate_rewards_zero_apr():
    result = calculate_rewards(1000, 0, 365)
    assert result == 0

def test_project_rewards_zero_apr():
    params = {
        'initial_stake': 1000,
        'apr': 0,
        'duration_days': 365,
        'compounding_frequency': 'daily'
    }
    result = project_rewards(params)
    assert result['total_rewards'] == 0

def test_project_rewards_various_frequencies():
    params = {
        'initial_stake': 1000,
        'apr': 0.05,
        'duration_days': 365,
        'compounding_frequency': 'monthly'
    }
    result = project_rewards(params)
    # Should handle different compounding frequencies without error
    assert 'total_rewards' in result

def test_calculate_rewards_precision():
    result = calculate_rewards(123.456, 0.0123, 456)
    expected = 123.456 * (math.exp(0.0123 * (456/365)) - 1)
    assert math.isclose(result, expected, abs_tol=0.0000001)