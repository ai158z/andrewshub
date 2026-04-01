import pytest
import requests
import json
from unittest.mock import patch, mock_open, MagicMock
from src.gravitational_data.data_source import DataSource

def test_fetch_real_time_data_success():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = ds.fetch_real_time_data(url)
        assert result == {"key": "value"}

def test_fetch_real_time_data_invalid_url():
    ds = DataSource()
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        ds.fetch_real_time_data("")

def test_fetch_real_time_data_non_string_url():
    ds = DataSource()
    with pytest.raises(ValueError, match="URL must be a non-empty string"):
        ds.fetch_real_time_data(123)

def test_fetch_real_time_data_connection_error():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get', side_effect=requests.exceptions.RequestException("Connection failed")):
        with pytest.raises(ConnectionError, match="Failed to fetch data"):
            ds.fetch_real_time_data(url)

def test_fetch_real_time_data_json_decode_error():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Failed to parse JSON response"):
            ds.fetch_real_time_data(url)

def test_load_static_dataset_json_success():
    ds = DataSource()
    file_path = "test.json"
    mock_data = {"name": "test", "value": 123}
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = ds.load_static_dataset(file_path)
        assert result == mock_data

def test_load_static_dataset_csv_success():
    ds = DataSource()
    file_path = "test.csv"
    csv_content = "name,value\nitem1,100\nitem2,200"
    expected_data = [{"name": "item1", "value": "100"}, {"name": "item2", "value": "200"}]
    
    with patch("pandas.read_csv") as mock_read_csv:
        mock_df = MagicMock()
        mock_df.to_dict.return_value = expected_data
        mock_read_csv.return_value = mock_df
        
        result = ds.load_static_dataset(file_path)
        assert result == expected_data

def test_load_static_dataset_invalid_path():
    ds = DataSource()
    with pytest.raises(ValueError, match="File path must be a non-empty string"):
        ds.load_static_dataset("")

def test_load_static_dataset_non_string_path():
    ds = DataSource()
    with pytest.raises(ValueError, match="File path must be a non-empty string"):
        ds.load_static_dataset(123)

def test_load_static_dataset_unsupported_format():
    ds = DataSource()
    with pytest.raises(ValueError, match="Unsupported file format"):
        ds.load_static_dataset("test.txt")

def test_load_static_dataset_file_not_found():
    ds = DataSource()
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        with pytest.raises(FileNotFoundError):
            ds.load_static_dataset("nonexistent.json")

def test_load_static_dataset_invalid_json():
    ds = DataSource()
    file_path = "test.json"
    
    with patch("builtins.open", mock_open(read_data="{invalid json}")):
        with pytest.raises(ValueError, match="Invalid JSON"):
            ds.load_static_dataset(file_path)

def test_load_static_dataset_generic_error():
    ds = DataSource()
    file_path = "test.json"
    
    with patch("builtins.open", side_effect=Exception("Generic error")):
        with pytest.raises(ValueError, match="Error loading file"):
            ds.load_static_dataset(file_path)

def test_fetch_real_time_data_unexpected_error():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get', side_effect=Exception("Unexpected error")):
        with pytest.raises(Exception, match="Unexpected error"):
            ds.fetch_real_time_data(url)

def test_fetch_real_time_data_timeout():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get', side_effect=requests.exceptions.Timeout()):
        with pytest.raises(ConnectionError):
            ds.fetch_real_time_data(url)

def test_fetch_real_time_data_http_error():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        mock_get.return_value = mock_response
        
        with pytest.raises(ConnectionError):
            ds.fetch_real_time_data(url)

def test_load_static_dataset_json_file_error():
    ds = DataSource()
    file_path = "test.json"
    
    with patch("builtins.open", mock_open(read_data="")):
        with patch("json.load", side_effect=Exception("JSON load error")):
            with pytest.raises(ValueError, match="Error loading file"):
                ds.load_static_dataset(file_path)

def test_load_static_dataset_csv_file_error():
    ds = DataSource()
    file_path = "test.csv"
    
    with patch("pandas.read_csv", side_effect=Exception("CSV read error")):
        with pytest.raises(ValueError, match="Error loading file"):
            ds.load_static_dataset(file_path)

def test_fetch_real_time_data_empty_response():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = ds.fetch_real_time_data(url)
        assert result == {}

def test_fetch_real_time_data_none_response():
    ds = DataSource()
    url = "http://api.test.com/data"
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = None
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = ds.fetch_real_time_data(url)
        assert result is None