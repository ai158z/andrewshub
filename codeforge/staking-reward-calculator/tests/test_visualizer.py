import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.visualizer import plot_rewards_over_time
import matplotlib.figure
import matplotlib.pyplot as plt

@pytest.fixture
def sample_rewards_data():
    return {
        'dates': {
            'projections': {
                '2023-01-01': 100,
                '2023-02-01': 200,
                '2023-03-01': 150
            }
        }
    }

@pytest.fixture
def sample_direct_data():
    return {
        'dates': {
            '2023-01-01': 100,
            '2023-02-01': 200,
            '2023-03-01': 150
        }
    }

def test_plot_rewards_with_valid_projections_data(sample_rewards_data):
    fig = plot_rewards_over_time(sample_rewards_data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_direct_date_value_mapping(sample_direct_data):
    fig = plot_rewards_over_time(sample_direct_data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_empty_data():
    data = {'dates': {}}
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_invalid_date_format():
    data = {
        'dates': {
            'projections': {
                '2023/01/01': 100,
                'invalid-date': 200,
                '2023-03-01': 150
            }
        }
    }
    with patch('src.visualizer.logger') as mock_logger:
        fig = plot_rewards_over_time(data)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

def test_plot_rewards_with_malformed_data_structure():
    data = {'malformed': 'data'}
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_none_data():
    fig = plot_rewards_over_time(None)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_no_dates_key():
    data = {'other_key': {}}
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_empty_projections():
    data = {'dates': {'projections': {}}}
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_exception_handling(monkeypatch):
    def mock_plot(*args, **kwargs):
        raise Exception("Mocked exception")
    
    monkeypatch.setattr(plt, 'subplots', mock_plot)
    
    data = {
        'dates': {
            '2023-01-01': 100,
            '2023-02-01': 200
        }
    }
    
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_mixed_valid_invalid_dates():
    data = {
        'dates': {
            '2023-01-01': 100,
            'invalid-date': 200,
            '2023-03-01': 150
        }
    }
    with patch('src.visualizer.logger'):
        fig = plot_rewards_over_time(data)
        assert isinstance(fig, matplotlib.figure.Figure)
        plt.close(fig)

def test_plot_rewards_unsorted_dates():
    data = {
        'dates': {
            '2023-03-01': 150,
            '2023-01-01': 100,
            '2023-02-01': 200
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_single_data_point():
    data = {
        'dates': {
            '2023-01-01': 100
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_no_valid_dates():
    data = {
        'dates': {
            'invalid1': 100,
            'invalid2': 200,
            'also-invalid': 150
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_all_none_values():
    data = {
        'dates': {
            '2023-01-01': None,
            '2023-02-01': None
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_zero_values():
    data = {
        'dates': {
            '2023-01-01': 0,
            '2023-02-01': 0,
            '2023-03-01': 0
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_negative_values():
    data = {
        'dates': {
            '2023-01-01': -100,
            '2023-02-01': -200
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_large_dataset():
    # Create a larger dataset to test performance/robustness
    projections = {}
    for i in range(1, 101):
        day = f"2023-01-{i:02d}" if i <= 31 else f"2023-02-{i-31:02d}"
        if day.startswith("2023-02-0") and int(day.split("-")[2]) > 28:
            continue
        if i <= 100:
            projections[day] = i * 10
    
    data = {'dates': {'projections': projections}}
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)

def test_plot_rewards_with_float_values():
    data = {
        'dates': {
            '2023-01-01': 100.50,
            '2023-02-01': 200.75,
            '2023-03-01': 150.25
        }
    }
    fig = plot_rewards_over_time(data)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)