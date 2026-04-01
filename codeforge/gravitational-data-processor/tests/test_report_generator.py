import pandas as pd
import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from src.gravitational_data.report_generator import ReportGenerator

class TestReportGenerator:
    def test_generate_report_with_valid_dataframe(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        
        # Execute
        result = rg.generate_report(df)
        
        # Verify
        assert isinstance(result, str)
        report_data = json.loads(result)
        assert 'Shape:' in report_data or 'shape' in report_data
        
    def test_generate_report_with_empty_dataframe(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame()
        
        # Execute
        result = rg.generate_report(df)
        
        # Verify
        assert isinstance(result, str)
        report_data = json.loads(result)
        assert 'Shape:' in report_data or 'shape' in report_data

    def test_generate_report_with_invalid_input(self):
        # Setup
        rg = ReportGenerator()
        
        # Execute & Verify
        with pytest.raises(ValueError) as e:
            rg.generate_report("not a dataframe")
        assert "Invalid data type" in str(e.value) or "must be a pandas" in str(e.value)

    def test_generate_report_with_none_input(self):
        # Setup
        rg = ReportGenerator()
        
        # Execute & Verify
        with pytest.raises(ValueError):
            rg.generate_report(None)

    @patch('pandas.DataFrame.to_csv')
    def test_export_to_csv_success(self, mock_to_csv):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        
        # Execute
        rg.export_to_csv(df, "test.csv")
        
        # Verify
        mock_to_csv.assert_called_once_with("test.csv", index=False)

    def test_export_to_csv_invalid_data_type(self):
        # Setup
        rg = ReportGenerator()
        
        # Execute & Verify
        with pytest.raises(ValueError) as e:
            rg.export_to_csv("not a dataframe", "test.csv")
        assert "Invalid data type" in str(e.value) or "must be a pandas" in str(e.value)

    def test_export_to_csv_invalid_filename(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        
        # Execute & Verify
        with pytest.raises(ValueError):
            rg.export_to_csv(df, "test.txt")

    @patch('pandas.DataFrame.to_csv')
    def test_export_to_csv_calls_pandas_to_csv(self, mock_to_csv):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame()
        
        # Execute
        rg.export_to_csv(df, "output.csv")
        
        # Verify
        mock_to_csv.assert_called_once()

    def test_export_to_csv_with_valid_inputs(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        
        # Execute & Verify
        try:
            rg.export_to_csv(df, "test.csv")
        except Exception:
            pytest.fail("export_to_csv raised an exception unexpectedly")

    def test_export_to_csv_none_data(self):
        # Setup
        rg = ReportGenerator()
        
        # Execute & Verify
        with pytest.raises(ValueError):
            rg.export_to_csv(None, "test.csv")

    def test_export_to_csv_empty_dataframe(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame()
        
        # Execute
        result = rg.export_to_csv(df, "test.csv")
        
        # Verify
        assert result is None

    def test_export_to_csv_invalid_data(self):
        # Setup
        rg = ReportGenerator()
        
        # Execute & Verify
        with pytest.raises(ValueError):
            rg.export_to_csv("invalid", "test.csv")

    def test_generate_report_structure(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        
        # Execute
        result = rg.generate_report(df)
        
        # Verify
        assert isinstance(result, str)
        # If it's valid JSON, we can load it
        try:
            json.loads(result)
            is_json = True
        except:
            is_json = False
        
        if is_json:
            assert 'shape' in result
        else:
            assert 'Data Report:' in result
            assert 'Shape:' in result

    def test_generate_report_with_mixed_data_types(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({
            'numeric': [1, 2, 3],
            'text': ['a', 'b', 'c'],
            'floats': [1.1, 2.2, 3.3]
        })
        
        # Execute
        result = rg.generate_report(df)
        
        # Verify
        assert isinstance(result, str)

    def test_generate_report_with_no_data(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame()
        
        # Execute
        result = rg.generate_report(df)
        
        # Verify
        assert isinstance(result, str)

    def test_generate_report_single_column(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'single': [1]})
        
        # Execute
        result = rg.generate_report(df)
        
        # Verify
        assert isinstance(result, str)

    def test_generate_report_special_characters(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'col@#$': [1], 'data*': ['test']})
        
        # Execute & Verify
        try:
            result = rg.generate_report(df)
            assert isinstance(result, str)
        except Exception as e:
            pytest.fail(f"generate_report failed with: {e}")

    def test_export_to_csv_with_actual_file(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        
        # Execute & Verify
        try:
            rg.export_to_csv(df, "output.csv")
        except Exception as e:
            pytest.fail(f"export_to_csv failed: {e}")

    def test_generate_report_exception_handling(self):
        # Setup
        rg = ReportGenerator()
        df = "invalid_data"
        
        # Execute & Verify
        with pytest.raises(ValueError):
            rg.generate_report(df)

    def test_export_to_csv_filename_validation(self):
        # Setup
        rg = ReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        
        # Execute & Verify
        with pytest.raises(ValueError):
            rg.export_to_csv(df, "not_a_csv.txt")