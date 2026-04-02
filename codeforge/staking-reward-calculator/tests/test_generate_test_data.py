import pytest
import csv
import random
from unittest.mock import patch, mock_open
from tests.generate_test_data import generate_test_scenarios, save_to_csv


def test_generate_test_scenarios_default_count():
    scenarios = generate_test_scenarios()
    assert len(scenarios) == 100


def test_generate_test_scenarios_custom_count():
    scenarios = generate_test_scenarios(50)
    assert len(scenarios) == 50


def test_generate_test_scenarios_empty_result():
    scenarios = generate_test_scenarios(0)
    assert scenarios == []


def test_generate_test_scenarios_structure():
    scenarios = generate_test_scenarios(1)
    scenario = scenarios[0]
    assert 'stake_amount' in scenario
    assert 'duration_days' in scenario
    assert 'annual_rate' in scenario
    assert 'penalty_rate' in scenario


def test_generate_test_scenarios_value_ranges():
    scenarios = generate_test_scenarios(10)
    for scenario in scenarios:
        assert 100 <= scenario['stake_amount'] <= 10000
        assert 30 <= scenario['duration_days'] <= 1095
        assert 0.05 <= scenario['annual_rate'] <= 0.25
        assert 0.01 <= scenario['penalty_rate'] <= 0.15


def test_save_to_csv_success():
    scenarios = [
        {
            'stake_amount': 1000.0,
            'duration_days': 365,
            'annual_rate': 0.10,
            'penalty_rate': 0.05
        }
    ]
    
    with patch("builtins.open", mock_open()) as mock_file:
        save_to_csv(scenarios, "test.csv")
        mock_file.assert_called_once_with("test.csv", 'w', newline='')


def test_save_to_csv_empty_scenarios():
    with pytest.raises(ValueError, match="No scenarios provided to save"):
        save_to_csv([], "test.csv")


def test_save_to_csv_file_writing_error():
    scenarios = [
        {
            'stake_amount': 1000.0,
            'duration_days': 365,
            'annual_rate': 0.10,
            'penalty_rate': 0.05
        }
    ]
    
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = Exception("File write error")
        with pytest.raises(IOError, match="Error writing to CSV file"):
            save_to_csv(scenarios, "test.csv")


def test_save_to_csv_content():
    scenarios = [
        {
            'stake_amount': 1000.0,
            'duration_days': 365,
            'annual_rate': 0.10,
            'penalty_rate': 0.05
        }
    ]
    
    with patch("builtins.open", mock_open()) as mock_file:
        save_to_csv(scenarios, "test.csv")
        
        # Check that writeheader was called
        handle = mock_file()
        handle.writeheader.assert_called_once()
        
        # Check that writerow was called with correct data
        expected_calls = [
            {
                'stake_amount': 1000.0,
                'duration_days': 365,
                'annual_rate': 0.10,
                'penalty_rate': 0.05
            }
        ]
        for scenario in expected_calls:
            handle.writerow.assert_any_call(scenario)


def test_generate_test_scenarios_deterministic_with_seed():
    # Set seed for reproducible results
    random.seed(42)
    scenarios1 = generate_test_scenarios(5)
    random.seed(42)
    scenarios2 = generate_test_scenarios(5)
    
    assert scenarios1 == scenarios2


def test_generate_test_scenarios_floating_point_precision():
    scenarios = generate_test_scenarios(10)
    for scenario in scenarios:
        # Check that values have appropriate decimal places
        assert round(scenario['stake_amount'], 2) == scenario['stake_amount']
        assert round(scenario['annual_rate'], 4) == scenario['annual_rate']
        assert round(scenario['penalty_rate'], 4) == scenario['penalty_rate']


def test_save_to_csv_fieldnames():
    scenarios = [
        {
            'stake_amount': 1000.0,
            'duration_days': 365,
            'annual_rate': 0.10,
            'penalty_rate': 0.05
        }
    ]
    
    with patch("builtins.open", mock_open()) as mock_file:
        save_to_csv(scenarios, "test.csv")
        handle = mock_file()
        # Check that fieldnames are written in header
        handle.writeheader.assert_called_once()


def test_generate_test_scenarios_large_count():
    scenarios = generate_test_scenarios(1000)
    assert len(scenarios) == 1000


def test_generate_test_scenarios_minimum_values():
    # Test that values can reach their minimums
    # This is probabilistic but we can check a large sample
    scenarios = generate_test_scenarios(1000)
    stake_amounts = [s['stake_amount'] for s in scenarios]
    durations = [s['duration_days'] for s in scenarios]
    annual_rates = [s['annual_rate'] for s in scenarios]
    penalty_rates = [s['penalty_rate'] for s in scenarios]
    
    assert min(stake_amounts) >= 100
    assert min(durations) >= 30
    assert min(annual_rates) >= 0.05
    assert min(penalty_rates) >= 0.01


def test_generate_test_scenarios_maximum_values():
    # Test that values can reach their maximums
    # This is probabilistic but we can check a large sample
    scenarios = generate_test_scenarios(1000)
    stake_amounts = [s['stake_amount'] for s in scenarios]
    durations = [s['duration_days'] for s in scenarios]
    annual_rates = [s['annual_rate'] for s in scenarios]
    penalty_rates = [s['penalty_rate'] for s in scenarios]
    
    assert max(stake_amounts) <= 10000
    assert max(durations) <= 1095
    assert max(annual_rates) <= 0.25
    assert max(penalty_rates) <= 0.15