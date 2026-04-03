import pytest
from unittest.mock import patch, MagicMock
from src.property_search import search_properties

@pytest.fixture
def sample_properties():
    return [
        {
            'id': 1,
            'address': '123 Main St',
            'city': 'Springfield',
            'state': 'IL',
            'zip_code': '62701',
            'price': 150000,
            'beds': 3,
            'baths': 2,
            'sqft': 1200,
            'property_type': 'Single Family',
            'listing_date': '2023-01-15'
        },
        {
            'id': 2,
            'address': '456 Oak Ave',
            'city': 'Springfield',
            'state': 'IL',
            'zip_code': '62702',
            'price': 275000,
            'beds': 4,
            'baths': 3,
            'sqft': 2100,
            'property_type': 'Townhouse',
            'listing_date': '2023-02-20'
        },
        {
            'id': 3,
            'address': '789 Pine Rd',
            'city': 'Riverside',
            'state': 'CA',
            'zip_code': '92501',
            'price': 89000,
            'beds': 2,
            'baths': 1,
            'sqft': 950,
            'property_type': 'Condo',
            'listing_date': '2023-03-10'
        }
    ]

@patch('src.property_search.get_properties')
def test_search_properties_no_filters(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({})
    assert len(result) == 3
    assert result == sample_properties

@patch('src.property_search.get_properties')
def test_search_properties_city_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'city': 'Springfield'})
    assert len(result) == 2
    assert all(prop['city'] == 'Springfield' for prop in result)

@patch('src.property_search.get_properties')
def test_search_properties_min_price_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'min_price': 100000})
    assert len(result) == 2
    assert all(prop['price'] >= 100000 for prop in result)

@patch('src.property_search.get_properties')
def test_search_properties_max_price_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'max_price': 200000})
    assert len(result) == 2
    assert all(prop['price'] <= 200000 for prop in result)
    
@patch('src.property_search.get_properties')
def test_search_properties_price_range_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'min_price': 100000, 'max_price': 200000})
    assert len(result) == 1
    assert result[0]['price'] == 150000

@patch('src.property_search.get_properties')
def test_search_properties_property_type_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'property_type': 'Condo'})
    assert len(result) == 1
    assert result[0]['property_type'] == 'Condo'

@patch('src.property_search.get_properties')
def test_search_properties_multiple_filters(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'city': 'Springfield', 'min_price': 100000})
    assert len(result) == 1
    assert result[0]['city'] == 'Springfield'
    assert result[0]['price'] == 150000

@patch('src.property_search.get_properties')
def test_search_properties_no_results(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'city': 'Nonexistent'})
    assert len(result) == 0

@patch('src.property_search.get_properties')
def test_search_properties_all_filters(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    filters = {
        'city': 'Springfield',
        'min_price': 100000,
        'max_price': 200000,
        'property_type': 'Single Family'
    }
    result = search_properties(filters)
    assert len(result) == 1
    assert result[0]['id'] == 1

def test_filter_by_price_range_lower_bound(sample_properties):
    properties = sample_properties
    filtered = [p for p in properties if p['price'] >= 100000]
    assert len(filtered) == 2
    assert all(p['id'] in [1, 2] for p in filtered)

def test_filter_by_price_range_upper_bound(sample_properties):
    properties = sample_properties
    filtered = [p for p in properties if p['price'] <= 200000]
    assert len(filtered) == 2
    assert all(p['id'] in [1, 3] for p in filtered)

def test_filter_by_price_range_no_match(sample_properties):
    properties = sample_properties
    filtered = [p for p in properties if 300000 <= p['price'] <= 400000]
    assert len(filtered) == 0

def test_search_properties_empty_filters(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({})
    assert len(result) == 3

def test_search_properties_case_sensitivity_property_type(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'property_type': 'condo'})
    assert len(result) == 0

@patch('src.property_search.get_properties')
def test_search_properties_invalid_filter_key(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'invalid_key': 'value'})
    assert len(result) == 3

@patch('src.property_search.get_properties')
def test_search_properties_beds_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'min_beds': 3})
    assert len(result) == 2
    assert all(prop['beds'] >= 3 for prop in result)

@patch('src.property_search.get_properties')
def test_search_properties_baths_filter(mock_get_properties, sample_properties):
    mock_get_properties.return_value = sample_properties
    result = search_properties({'min_baths': 2})
    assert len(result) == 2
    assert all(prop['baths'] >= 2 for prop in result)