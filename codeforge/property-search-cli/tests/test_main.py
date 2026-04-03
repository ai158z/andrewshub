import pytest
from unittest.mock import patch, MagicMock
from src.main import main, display_properties, setup_logging
import argparse
import logging
import sys

@pytest.fixture
def sample_properties():
    return [
        {
            'id': '1',
            'address': '123 Main St',
            'price': 250000,
            'bedrooms': 3,
            'bathrooms': 2,
            'sqft': 1500
        },
        {
            'id': '2',
            'address': '456 Oak Ave',
            'price': 300000,
            'bedrooms': 4,
            'bathrooms': 3,
            'sqft': 1800
        }
    ]

def test_display_properties_with_results(capfd, sample_properties):
    display_properties(sample_properties)
    out, err = capfd.readouterr()
    assert "Found 2 properties:" in out
    assert "ID: 1" in out
    assert "Address: 123 Main St" in out
    assert "Price: 250000" in out

def test_display_properties_empty(capfd):
    display_properties([])
    out, err = capfd.readouterr()
    assert "No properties found matching the specified criteria." in out

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_success(mock_setup_logging, mock_search_properties, mock_parse_args, sample_properties):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = sample_properties
    
    with patch.object(sys, 'argv', ['main.py']):
        result = main()
        assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_min_price_filter(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = "100000"
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    with patch('src.validators.validate_positive_float') as mock_validate:
        mock_validate.return_value = 100000.0
        result = main()
        assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_max_price_filter(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = "500000"
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    with patch('src.validators.validate_positive_float') as mock_validate:
        mock_validate.return_value = 500000.0
        result = main()
        assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_min_bedrooms_filter(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = "3"
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    with patch('src.validators.validate_positive_int') as mock_validate:
        mock_validate.return_value = 3
        result = main()
        assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_min_bathrooms_filter(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = "2"
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    with patch('src.validators.validate_positive_int') as mock_validate:
        mock_validate.return_value = 2
        result = main()
        assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_location_filter(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = "downtown"
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    result = main()
    assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_property_type_filter(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = "apartment"
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    result = main()
    assert result == 0

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_with_all_filters(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = "100000"
    mock_args.max_price = "500000"
    mock_args.min_bedrooms = "3"
    mock_args.min_bathrooms = "2"
    mock_args.location = "downtown"
    mock_args.property_type = "apartment"
    mock_parse_args.return_value = mock_args
    mock_search_properties.return_value = []
    
    with patch('src.validators.validate_positive_float') as mock_validate_float, \
         patch('src.validators.validate_positive_int') as mock_validate_int:
        mock_validate_float.return_value = 100000.0
        mock_validate_int.return_value = 3
        result = main()
        assert result == 0

@patch('src.main.parse_args')
def test_main_argparse_error(mock_parse_args):
    mock_parse_args.side_effect = SystemExit
    with patch.object(sys, 'argv', ['main.py', '--invalid-arg']):
        result = main()
        assert result == 1

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_search_exception_handling(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    mock_search_properties.side_effect = Exception("Database error")
    
    result = main()
    assert result == 1

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_invalid_min_price(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = "-100"
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    
    with patch('src.validators.validate_positive_float', side_effect=ValueError("Invalid value")):
        result = main()
        assert result == 1

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_invalid_max_price(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = "-100"
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    
    with patch('src.validators.validate_positive_float', side_effect=ValueError("Invalid value")):
        result = main()
        assert result == 1

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_invalid_min_bedrooms(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = "-1"
    mock_args.min_bathrooms = None
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    
    with patch('src.validators.validate_positive_int', side_effect=ValueError("Invalid value")):
        result = main()
        assert result == 1

@patch('src.main.parse_args')
@patch('src.main.search_properties')
@patch('src.main.setup_logging')
def test_main_invalid_min_bathrooms(mock_setup_logging, mock_search_properties, mock_parse_args):
    mock_args = MagicMock()
    mock_args.min_price = None
    mock_args.max_price = None
    mock_args.min_bedrooms = None
    mock_args.min_bathrooms = "-1"
    mock_args.location = None
    mock_args.property_type = None
    mock_parse_args.return_value = mock_args
    
    with patch('src.validators.validate_positive_int', side_effect=ValueError("Invalid value")):
        result = main()
        assert result == 1

def test_setup_logging():
    with patch('src.main.logging') as mock_logging:
        setup_logging()
        mock_logging.basicConfig.assert_called_once_with(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )