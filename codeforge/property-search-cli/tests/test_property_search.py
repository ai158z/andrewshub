import pytest
from src.property_search import search_properties, _filter_by_price_range, _filter_by_bedrooms, _filter_by_bathrooms, _filter_by_property_type, _filter_by_city, _filter_by_zip_code

def test_search_properties_no_filters():
    results = search_properties({})
    assert len(results) == 4

def test_search_properties_price_filter_min_only():
    filters = {'min_price': 800000}
    results = search_properties(filters)
    assert len(results) == 2
    assert results[0]['id'] == 2
    assert results[1]['id'] == 4

def test_search_properties_price_filter_max_only():
    filters = {'max_price': 900000}
    results = search_properties(filters)
    assert len(results) == 3
    assert results[0]['id'] == 1
    assert results[1]['id'] == 3
    assert results[2]['id'] == 4

def test_search_properties_price_filter_range():
    filters = {'min_price': 800000, 'max_price': 1000000}
    results = search_properties(filters)
    assert len(results) == 1
    assert results[0]['id'] == 3

def test_search_properties_bedroom_filter():
    filters = {'min_bedrooms': 3}
    results = search_properties(filters)
    assert len(results) == 2
    assert results[0]['id'] == 1
    assert results[1]['id'] == 4

def test_search_properties_bathroom_filter():
    filters = {'min_bathrooms': 3}
    results = search_properties(filters)
    assert len(results) == 1
    assert results[0]['id'] == 2

def test_search_properties_property_type_filter():
    filters = {'property_type': 'Single Family Home'}
    results = search_properties(filters)
    assert len(results) == 2
    assert results[0]['id'] == 1
    assert results[1]['id'] == 4

def test_search_properties_city_filter():
    filters = {'city': 'Anytown'}
    results = search_properties(filters)
    assert len(results) == 2
    assert results[0]['id'] == 1
    assert results[1]['id'] == 4

def test_search_properties_zip_code_filter():
    filters = {'zip_code': '90210'}
    results = search_properties(filters)
    assert len(results) == 2
    assert results[0]['id'] == 1
    assert results[1]['id'] == 4

def test_search_properties_multiple_filters():
    filters = {
        'min_price': 800000,
        'max_price': 1000000,
        'min_bedrooms': 2,
        'city': 'Anytown'
    }
    results = search_properties(filters)
    assert len(results) == 1
    assert results[0]['id'] == 4

def test_search_properties_no_matches():
    filters = {'min_price': 2000000}
    results = search_properties(filters)
    assert len(results) == 0

def test_filter_by_price_range_no_filter():
    properties = [{'price': 500000}, {'price': 1000000}]
    result = _filter_by_price_range(properties, 0, 0)
    assert result == properties

def test_filter_by_bedrooms_no_filter():
    properties = [{'bedrooms': 2}, {'bedrooms': 3}]
    result = _filter_by_bedrooms(properties, 0)
    assert result == properties

def test_filter_by_bathrooms_no_filter():
    properties = [{'bathrooms': 2}, {'bathrooms': 3}]
    result = _filter_by_bathrooms(properties, 0)
    assert result == properties

def test_filter_by_property_type_no_filter():
    properties = [{'property_type': 'Condo'}, {'property_type': 'Townhouse'}]
    result = _filter_by_property_type(properties, '')
    assert result == properties

def test_filter_by_city_no_filter():
    properties = [{'city': 'Anytown'}, {'city': 'Sometown'}]
    result = _filter_by_city(properties, '')
    assert result == properties

def test_filter_by_zip_code_no_filter():
    properties = [{'zip_code': '90210'}, {'zip_code': '90211'}]
    result = _filter_by_zip_code(properties, '')
    assert result == properties

def test_filter_by_property_type_case_insensitive():
    properties = [{'property_type': 'Condo'}, {'property_type': 'Townhouse'}]
    result = _filter_by_property_type(properties, 'condo')
    assert len(result) == 1
    assert result[0]['property_type'] == 'Condo'

def test_filter_by_city_case_insensitive():
    properties = [{'city': 'Anytown'}, {'city': 'Sometown'}]
    result = _filter_by_city(properties, 'anytown')
    assert len(result) == 1
    assert result[0]['city'] == 'Anytown'