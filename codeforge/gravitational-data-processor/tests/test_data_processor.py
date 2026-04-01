import pytest
import pandas as pd
import numpy as np
from src.gravitational_data.data_processor import DataProcessor

class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    def test_process_gravitational_data_valid_input(self):
        """Test processing valid gravitational data."""
        processor = DataProcessor()
        data = {'gravity_measurements': [9.8, 9.7, 9.9], 'time': [1, 2, 3]}
        result = processor.process_gravitational_data(data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['gravity_measurements', 'time']
    
    def test_process_gravitational_data_invalid_type(self):
        """Test processing with invalid data type."""
        processor = DataProcessor()
        with pytest.raises(TypeError):
            processor.process_gravitational_data("invalid_data")
    
    def test_process_gravitational_data_empty_dict(self):
        """Test processing empty data dictionary."""
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process_gravitational_data({})
    
    def test_calculate_statistics_valid_dataframe(self):
        """Test calculating statistics with valid DataFrame."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'gravity_measurements': [9.8, 9.7, 9.9, np.nan],
            'time': [1, 2, 3, 4]
        })
        stats = processor.calculate_statistics(df)
        assert 'gravity_measurements' in stats
        assert 'time' in stats
        assert stats['data_info']['total_rows'] == 4
        assert stats['gravity_measurements']['mean'] == 9.8
        assert stats['gravity_measurements']['std'] == 0.1
    
    def test_calculate_statistics_empty_dataframe(self):
        """Test calculating statistics with empty DataFrame."""
        processor = DataProcessor()
        df = pd.DataFrame()
        result = processor.calculate_statistics(df)
        assert result == {}
    
    def test_calculate_statistics_invalid_type(self):
        """Test calculating statistics with invalid data type."""
        processor = DataProcessor()
        with pytest.raises(TypeError):
            processor.calculate_statistics("invalid_data")
    
    def test_calculate_statistics_with_missing_values(self):
        """Test statistics calculation handles missing values correctly."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'gravity_measurements': [9.8, np.nan, 9.9],
            'time': [1, 2, np.nan]
        })
        stats = processor.calculate_statistics(df)
        assert stats['gravity_measurements']['missing_values'] == 1
        assert stats['time']['missing_values'] == 1
    
    def test_calculate_statistics_non_numeric_data(self):
        """Test statistics with non-numeric data."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'gravity_measurements': [9.8, 9.7, 9.9]
        })
        stats = processor.calculate_statistics(df)
        # Non-numeric columns should not appear in stats
        assert 'category' not in stats
        assert 'gravity_measurements' in stats
    
    def test_process_gravitational_data_large_dataset(self):
        """Test processing large gravitational data set."""
        processor = DataProcessor()
        large_data = {
            'gravity_measurements': list(range(10000)),
            'time': list(range(10000))
        }
        result = processor.process_gravitational_data(large_data)
        assert len(result) == 10000
    
    def test_calculate_statistics_single_value(self):
        """Test statistics with single value."""
        processor = DataProcessor()
        df = pd.DataFrame({'gravity_measurements': [9.8]})
        stats = processor.calculate_statistics(df)
        assert stats['gravity_measurements']['mean'] == 9.8
        assert stats['gravity_measurements']['std'] == 0.0
    
    def test_calculate_statistics_all_nan_values(self):
        """Test statistics with all NaN values."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'gravity_measurements': [np.nan, np.nan, np.nan],
            'time': [np.nan, np.nan, np.nan]
        })
        stats = processor.calculate_statistics(df)
        assert stats['data_info']['missing_data'] == 6
    
    def test_process_gravitational_data_with_none_values(self):
        """Test processing data with None values."""
        processor = DataProcessor()
        data = {'gravity_measurements': [9.8, None, 9.9], 'time': [1, 2, None]}
        result = processor.process_gravitational_data(data)
        assert len(result) == 3
        assert result['gravity_measurements'].isna().sum() == 1
    
    def test_calculate_statistics_mixed_data_types(self):
        """Test statistics with mixed data types."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'numeric_col': [1, 2, 3],
            'string_col': ['a', 'b', 'c'],
            'gravity_measurements': [9.8, 9.7, 9.9]
        })
        stats = processor.calculate_statistics(df)
        # Only numeric columns should be in stats
        assert 'numeric_col' in stats
        assert 'gravity_measurements' in stats
        assert 'string_col' not in stats
    
    def test_process_gravitational_data_consistent_results(self):
        """Test that processing returns consistent results."""
        processor = DataProcessor()
        data = {'gravity_measurements': [1, 2, 3, 4, 5]}
        result1 = processor.process_gravitational_data(data)
        result2 = processor.process_gravitational_data(data)
        pd.testing.assert_frame_equal(result1, result2)
    
    def test_calculate_statistics_consistent_results(self):
        """Test that statistics calculation is consistent."""
        processor = DataProcessor()
        df = pd.DataFrame({'gravity_measurements': [1, 2, 3, 4, 5]})
        stats1 = processor.calculate_statistics(df)
        stats2 = processor.calculate_statistics(df)
        assert stats1 == stats2
    
    def test_process_gravitational_data_duplicate_keys(self):
        """Test processing data with duplicate column names."""
        processor = DataProcessor()
        data = {
            'gravity_measurements': [1, 2, 3],
            'gravity_measurements': [4, 5, 6]  # This will overwrite the previous
        }
        result = processor.process_gravitational_data(data)
        assert len(result.columns) == 1
    
    def test_calculate_statistics_edge_case_values(self):
        """Test statistics with edge case values."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'gravity_measurements': [0, -9.8, 999.99, np.inf, -np.inf],
            'time': [1, 2, 3, 4, 5]
        })
        stats = processor.calculate_statistics(df)
        assert 'gravity_measurements' in stats
        assert stats['data_info']['total_rows'] == 5
    
    def test_process_gravitational_data_empty_values(self):
        """Test processing data with empty values."""
        processor = DataProcessor()
        data = {'gravity_measurements': [], 'time': []}
        result = processor.process_gravitational_data(data)
        assert len(result) == 0
        assert list(result.columns) == ['gravity_measurements', 'time']
    
    def test_calculate_statistics_no_numeric_data(self):
        """Test statistics with no numeric data."""
        processor = DataProcessor()
        df = pd.DataFrame({
            'name': ['A', 'B', 'C'],
            'description': ['test1', 'test2', 'test3']
        })
        stats = processor.calculate_statistics(df)
        # Should only contain data_info, no column stats since no numeric data
        assert 'data_info' in stats
        assert len(stats) == 1
    
    def test_process_gravitational_data_type_error(self):
        """Test processing with type error in data."""
        processor = DataProcessor()
        with pytest.raises(TypeError):
            processor.process_gravitational_data(None)