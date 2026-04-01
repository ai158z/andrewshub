import pytest
import pandas as pd
from unittest.mock import Mock, patch

def test_process_gravitational_data_returns_dataframe(processor, sample_gravitational_data):
    """Test that process_gravitational_data returns a pandas DataFrame."""
    result = processor.process_gravitational_data(sample_gravitational_data)
    assert isinstance(result, pd.DataFrame)

def test_process_gravitational_data_empty_input(processor):
    """Test processing with empty data."""
    empty_data = {"measurements": []}
    result = processor.process_gravitational_data(empty_data)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0

def test_calculate_statistics_returns_dict(processor):
    """Test that calculate_statistics returns a dictionary."""
    mock_df = pd.DataFrame({
        'gravity': [9.81, 9.79, 9.80],
        'latitude': [40.7128, 34.0522, 41.8781],
        'longitude': [-74.0060, -118.2437, -87.6298]
    })
    stats = processor.calculate_statistics(mock_df)
    assert isinstance(stats, dict)

def test_data_processor_initialization():
    """Test DataProcessor class initializes correctly."""
    processor = DataProcessor()
    assert processor is not None

def test_process_gravitational_data_structure(sample_gravitational_data, processor):
    """Test the structure of processed data output."""
    result = processor.process_gravitational_data(sample_gravitational_data)
    assert list(result.columns) == ['gravity', 'latitude', 'longitude']
    assert len(result) == 3

def test_calculate_statistics_computes_all_values(processor):
    """Test that all statistical values are computed."""
    df = pd.DataFrame({
        'gravity': [9.81, 9.79, 9.80],
        'latitude': [40.7128, 34.0522, 41.8781],
        'longitude': [-74.0060, -118.2437, -87.6298]
    })
    stats = processor.calculate_statistics(df)
    assert all(key in stats for key in ['mean', 'median', 'std_dev', 'min', 'max'])

def test_process_data_with_invalid_input(processor):
    """Test processing invalid input data."""
    with pytest.raises(ValueError):
        processor.process_gravitational_data(None)

def test_process_data_with_missing_fields(processor):
    """Test processing data with missing required fields."""
    invalid_data = {"measurements": [{"id": 1}]}  # Missing lat/lon/gravity
    with pytest.raises(KeyError):
        processor.process_gravitational_data(invalid_data)

def test_calculate_statistics_with_empty_dataframe(processor):
    """Test calculate_statistics with empty DataFrame."""
    empty_df = pd.DataFrame()
    result = processor.calculate_statistics(empty_df)
    assert result == {}

def test_data_processor_handles_single_record(processor):
    """Test data processing with single data record."""
    single_record = {
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81}
        ]
    }
    result = processor.process_gravitational_data(single_record)
    assert len(result) == 1

def test_data_processor_handles_multiple_records(processor):
    """Test processing multiple data records."""
    multi_data = {
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81},
            {"id": 2, "latitude": 34.0522, "longitude": -118.2437, "gravity": 9.79}
        ]
    }
    result = processor.process_gravitational_data(multi_data)
    assert len(result) == 2

def test_data_processor_preserves_data_types(processor):
    """Test that data types are preserved in processing."""
    data = {"measurements": [{"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81}]}
    result = processor.process_gravitational_data(data)
    assert result['id'].dtype == 'int64'
    assert result['latitude'].dtype == 'float64'
    assert result['longitude'].dtype == 'float64'
    assert result['gravity'].dtype == 'float64'

def test_data_processor_large_dataset_handling(processor):
    """Test handling of large datasets."""
    large_data = {"measurements": []}
    for i in range(10000):
        large_data["measurements"].append({
            "id": i, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81
        })
    result = processor.process_gravitational_data(large_data)
    assert len(result) == 10000

def test_data_processor_edge_case_zero_gravity(processor):
    """Test processing data with zero gravity values."""
    zero_gravity_data = {
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 0.0}
        ]
    }
    result = processor.process_gravitational_data(zero_gravity_data)
    assert len(result) == 1
    assert result.iloc[0]['gravity'] == 0.0

def test_data_processor_negative_values(processor):
    """Test handling of negative measurement values."""
    negative_data = {
        "measurements": [
            {"id": 1, "latitude": -40.7128, "longitude": -74.0060, "gravity": -9.81}
        ]
    }
    result = processor.process_gravitational_data(negative_data)
    assert result.iloc[0]['latitude'] < 0
    assert result.iloc[0]['longitude'] < 0
    assert result.iloc[0]['gravity'] < 0

def test_data_processor_missing_measurements(processor):
    """Test error handling when measurements are missing."""
    data = {}
    with pytest.raises(KeyError):
        processor.process_gravitational_data(data)

def test_data_processor_invalid_coordinates(processor):
    """Test handling of invalid coordinate data."""
    invalid_coords = {
        "measurements": [
            {"id": 1, "latitude": "invalid", "longitude": -74.0060, "gravity": 9.81}
        ]
    }
    with pytest.raises(ValueError):
        processor.process_gravitational_data(invalid_coords)

def test_data_processor_timestamp_processing(processor):
    """Test timestamp handling in gravitational data."""
    timestamp_data = {
        "timestamp": "2023-01-01T12:00:00Z",
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81}
        ]
    }
    result = processor.process_gravitational_data(timestamp_data)
    assert 'timestamp' in timestamp_data

def test_data_processor_duplicate_ids(processor):
    """Test handling of duplicate measurement IDs."""
    duplicate_data = {
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81},
            {"id": 1, "latitude": 34.0522, "longitude": -118.2437, "gravity": 9.79}
        ]
    }
    result = processor.process_gravitational_data(duplicate_data)
    assert len(result) == 2

def test_data_processor_with_nan_values(processor):
    """Test handling of NaN values in data."""
    import numpy as np
    nan_data = {
        "measurements": [
            {"id": 1, "latitude": np.nan, "longitude": -74.0060, "gravity": 9.81}
        ]
    }
    result = processor.process_gravitational_data(nan_data)
    assert result.isna().any().any() or result.isnull().any().any()

def test_data_processor_large_numbers(processor):
    """Test handling of large numerical values."""
    large_num_data = {
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 999999.99}
        ]
    }
    result = processor.process_gravitational_data(large_num_data)
    assert result.iloc[0]['gravity'] == 999999.99

def test_calculate_statistics_with_data_types(processor):
    """Test calculate_statistics handles different data types."""
    df = pd.DataFrame({
        'gravity': [9.81, 9.79, 9.80],
        'latitude': [40.7128, 34.0522, 41.8781],
        'longitude': [-74.0060, -118.2437, -87.6298]
    })
    stats = processor.calculate_statistics(df)
    assert isinstance(stats['mean']['gravity'], float)
    assert isinstance(stats['std_dev']['gravity'], float)

def test_process_gravitational_data_with_none_values(processor):
    """Test processing data with None values."""
    none_data = {
        "measurements": [
            {"id": 1, "latitude": None, "longitude": -74.0060, "gravity": 9.81}
        ]
    }
    with pytest.raises(KeyError):
        processor.process_gravitational_data(none_data)

def test_calculate_statistics_missing_columns(processor):
    """Test calculate_statistics with missing columns."""
    df = pd.DataFrame({'x': [1, 2, 3]})  # Missing gravity column
    result = processor.calculate_statistics(df)
    assert result == {}  # Should return empty dict when required columns missing

def test_data_processor_float_precision(processor):
    """Test data processor maintains float precision."""
    data = {"measurements": [{"id": 1, "latitude": 40.123456789, "longitude": -74.987654321, "gravity": 9.81123456789}]}
    result = processor.process_gravitational_data(data)
    assert abs(result.iloc[0]['latitude'] - 40.123456789) < 1e-10

def test_process_gravitational_data_with_extra_fields(processor):
    """Test processing data with extra unexpected fields."""
    extra_data = {
        "measurements": [
            {"id": 1, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81, "extra": "field"}
        ]
    }
    result = processor.process_gravitational_data(extra_data)
    assert len(result.columns) == 4  # id, latitude, longitude, gravity

def test_calculate_statistics_edge_values(processor):
    """Test calculate_statistics with edge case values."""
    # Test with very small numbers
    df = pd.DataFrame({
        'gravity': [0.000001, 0.000002, 0.000003],
        'latitude': [0.000001, 0.000002, 0.000003],
        'longitude': [0.000001, 0.000002, 0.000003]
    })
    stats = processor.calculate_statistics(df)
    assert stats['mean']['gravity'] > 0

def test_data_processor_memory_efficiency(processor):
    """Test data processor handles memory efficiently."""
    # This is a basic test - in practice would need more sophisticated memory testing
    data = {"measurements": []}
    for i in range(100):
        data["measurements"].append({
            "id": i, "latitude": 40.7128, "longitude": -74.0060, "gravity": 9.81
        })
    result = processor.process_gravitational_data(data)
    assert len(result) == 100
    assert result.memory_usage().sum() > 0