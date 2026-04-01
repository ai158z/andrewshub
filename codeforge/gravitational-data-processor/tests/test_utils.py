import pytest
from src.gravitational_data.utils import validate_data, transform_coordinates
import math

def test_validate_data_valid_input():
    data = {
        'latitude': 45.0,
        'longitude': 90.0,
        'gravity_value': 9.81
    }
    assert validate_data(data) is True

def test_validate_data_invalid_type():
    data = "not a dict"
    assert validate_data(data) is False

def test_validate_data_missing_fields():
    data = {
        'latitude': 45.0,
        'gravity_value': 9.81
        # missing longitude
    }
    assert validate_data(data) is False

def test_validate_data_invalid_latitude_range():
    data = {
        'latitude': 95.0,  # Invalid latitude
        'longitude': 90.0,
        'gravity_value': 9.81
    }
    assert validate_data(data) is False

def test_validate_data_invalid_longitude_range():
    data = {
        'latitude': 45.0,
        'longitude': 190.0,  # Invalid longitude
        'gravity_value': 9.81
    }
    assert validate_data(data) is False

def test_validate_data_invalid_latitude_type():
    data = {
        'latitude': "invalid",
        'longitude': 90.0,
        'gravity_value': 9.81
    }
    assert validate_data(data) is False

def test_validate_data_invalid_longitude_type():
    data = {
        'latitude': 45.0,
        'longitude': "invalid",
        'gravity_value': 9.81
    }
    assert validate_data(data) is False

def test_validate_data_invalid_gravity_type():
    data = {
        'latitude': 45.0,
        'longitude': 90.0,
        'gravity_value': "invalid"  # Invalid type
    }
    assert validate_data(data) is False

def test_transform_coordinates_valid():
    lat, lon = transform_coordinates(45.0, 90.0)
    expected_lat = math.radians(45.0)
    expected_lon = math.radians(90.0)
    assert lat == expected_lat
    assert lon == expected_lon

def test_transform_coordinates_invalid_input_type():
    with pytest.raises(TypeError):
        transform_coordinates("invalid", 90.0)

def test_transform_coordinates_invalid_latitude_range():
    with pytest.raises(ValueError):
        transform_coordinates(95.0, 90.0)  # Latitude out of range

def test_transform_coordinates_invalid_longitude_range():
    with pytest.raises(ValueError):
        transform_coordinates(45.0, 190.0)  # Longitude out of range

def test_transform_coordinates_edge_cases():
    # Test edge cases for coordinates
    # 1. Minimum latitude and longitude
    lat_rad, lon_rad = transform_coordinates(-90.0, -180.0)
    assert lat_rad == math.radians(-90.0)
    assert lon_rad == math.radians(-180.0)
    
    # 2. Maximum latitude and longitude
    lat_rad, lon_rad = transform_coordinates(90.0, 180.0)
    assert lat_rad == math.radians(90.0)
    assert lon_rad == math.radians(180.0)

def test_transform_coordinates_valid_ranges():
    # Test that valid ranges work
    lat, lon = 0.0, 0.0
    result = transform_coordinates(lat, lon)
    assert result == (math.radians(lat), math.radians(lon))

def test_transform_coordinates_invalid_ranges():
    # Test invalid ranges raise errors
    with pytest.raises(ValueError):
        transform_coordinates(95.0, 0.0)  # Invalid latitude

def test_transform_coordinates_type_errors():
    # Test type errors raise exceptions
    with pytest.raises(TypeError):
        transform_coordinates("not a number", 0.0)

def test_validate_data_all_valid_fields():
    # All fields are valid
    data = {
        'latitude': 45.0,
        'longitude': 90.0,
        'gravity_value': 9.81
    }
    assert validate_data(data) is True

def test_validate_data_missing_field():
    # Missing gravity_value
    data = {
        'latitude': 45.0,
        'longitude': 90.0
        # missing gravity_value
    }
    assert validate_data(data) is False

def test_transform_coordinates_negative_values():
    # Test negative coordinate values work
    lat, lon = transform_coordinates(-45.0, -90.0)
    assert lat == math.radians(-45.0)
    assert lon == math.radians(-90.0)

def test_transform_coordinates_positive_values():
    # Test positive coordinate values work
    lat, lon = transform_coordinates(45.0, 90.0)
    assert (lat, lon) == (math.radians(45.0), math.radians(90.0))