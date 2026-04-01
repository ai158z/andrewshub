import pandas as pd
import pytest
from unittest.mock import Mock, mock_open, patch
from src.gravitational_data.report_generator import ReportGenerator

def test_generate_report_success():
    mock_data = pd.DataFrame({
        'timestamp': pd.Timestamp('2023-01-01 12:00:00'),
        'sensor_id': ['G1', 'G2'],
        'values': [1.23, 4.56]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    
    assert isinstance(result, str)
    assert "gravitational analysis" in result
    assert "Report generated successfully" in result

def test_generate_report_empty_dataframe():
    mock_data = pd.DataFrame()
    with pytest.raises(ValueError, match="No data to generate report for"):
        report = ReportGenerator()
        report.generate_report(mock_data)

def test_generate_report_empty_dict():
    mock_data = {}
    with pytest.raises(ValueError, match="No data to generate report for"):
        report = ReportGenerator()
        report.generate_report(mock_data)

def test_export_to_csv_success():
    mock_data = pd.DataFrame({
        'values': [1.23, 4.51, 3.34]
    })
    
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        report = ReportGenerator()
        report.export_to_csv(mock_data, 'test.csv')
        mock_to_csv.assert_called_once_with('test.csv', index=False)

def test_export_to_csv_empty_data():
    mock_data = pd.DataFrame()
    with pytest.raises(ValueError, match="No data to export"):
        report = ReportGenerator()
        report.export_to_csv(mock_data, 'test.csv')

def test_export_to_csv_invalid_data():
    mock_data = []
    with pytest.raises(ValueError, match="No data to export"):
        report = ReportGenerator()
        report.export_to_csv(mock_data, 'test.csv')

def test_generate_report_and_export_integration():
    mock_data = pd.DataFrame({
        'values': [1.23, 4.51, 3.34]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    
    assert "Report generated successfully" in result

def test_export_to_csv_called_with_correct_args():
    mock_data = pd.DataFrame({
        'values': [1.23, 4.51, 3.34]
    })
    
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        report = ReportGenerator()
        report.export_to_csv(mock_data, 'output.csv')
        mock_to_csv.assert_called_once_with('output.csv', index=False)

def test_generate_report_with_minimal_data():
    mock_data = pd.DataFrame({
        'values': [1.0]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    assert isinstance(result, str)
    assert "gravitational analysis" in result

def test_generate_report_with_no_values_column():
    mock_data = pd.DataFrame({
        'sensor_id': ['G1', 'G2']
    })
    
    with pytest.raises(ValueError, match="No data to generate report for"):
        report = ReportGenerator()
        report.generate_report(mock_data)

def test_generate_report_with_none_values():
    mock_data = pd.DataFrame({
        'values': [None, None]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    assert isinstance(result, str)

def test_export_to_csv_default_filename():
    mock_data = pd.DataFrame({
        'values': [1.23, 4.56]
    })
    
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        report = ReportGenerator()
        report.export_to_csv(mock_data)
        mock_to_csv.assert_called_once()

def test_generate_report_single_row():
    mock_data = pd.DataFrame({
        'timestamp': [pd.Timestamp('2023-01-01 12:00:00')],
        'sensor_id': ['G1'],
        'values': [1.23]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    assert isinstance(result, str)
    assert "gravitational analysis" in result

def test_generate_report_mixed_valid_invalid():
    mock_data = pd.DataFrame({
        'values': [1.23, None, 4.56]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    assert isinstance(result, str)

def test_export_to_csv_with_various_data_types():
    mock_data = pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=3),
        'sensor_id': ['S1', 'S2', 'S3'],
        'values': [1.0, 2.5, 3.0]
    })
    
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        report = ReportGenerator()
        report.export_to_csv(mock_data, 'test_output.csv')
        mock_to_csv.assert_called_once_with('test_output.csv', index=False)

def test_generate_report_with_nan_values():
    mock_data = pd.DataFrame({
        'values': [1.23, float('nan'), 3.45]
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    assert isinstance(result, str)

def test_export_to_csv_with_empty_dataframe():
    mock_data = pd.DataFrame()
    with pytest.raises(ValueError, match="No data to export"):
        report = ReportGenerator()
        report.export_to_csv(mock_data, 'empty.csv')

def test_generate_report_large_dataset():
    large_data = pd.DataFrame({
        'values': list(range(1000))
    })
    
    report = ReportGenerator()
    result = report.generate_report(large_data)
    assert isinstance(result, str)

def test_export_to_csv_large_dataset():
    large_data = pd.DataFrame({
        'values': list(range(1000))
    })
    
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        report = ReportGenerator()
        report.export_to_csv(large_data, 'large.csv')
        mock_to_csv.assert_called_once_with('large.csv', index=False)

def test_generate_report_special_characters():
    mock_data = pd.DataFrame({
        'values': ['value with spaces', 'value-with-dashes', 'value_with_underscores']
    })
    
    report = ReportGenerator()
    result = report.generate_report(mock_data)
    assert isinstance(result, str)