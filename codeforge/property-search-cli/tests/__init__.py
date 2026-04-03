# tests/__init__.py
import os
import sys
import tempfile
import pytest
from typing import Generator


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "property_search: mark test to search properties"
    )
    config.addinivalue_line(
        "markers", "cli: mark CLI-related tests"
    )


@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_property_data():
    """Provide sample property data for testing."""
    return [
        {
            'id': 1,
            'address': '123 Main St',
            'price': 250000,
            'bedrooms': 3,
            'bathrooms': 2,
            'sqft': 1500,
            'neighborhood': 'Downtown',
            'year_built': 1995
        },
        {
            'id': 2,
            'address': '456 Oak Ave',
            'price': 320000,
            'bedrooms': 4,
            'bathrooms': 3,
            'sqft': 2200,
            'neighborhood': 'Westside',
            'year_built': 2005
        },
        {
            'id': 3,
            'address': '789 Pine Rd',
            'price': 480000,
            'bedrooms': 5,
            'bathrooms': 4,
            'sqft': 3200,
            'neighborhood': 'Eastside',
            'year_built': 2010
        }
    ]


@pytest.fixture
def mock_search_response():
    """Mock response for search properties."""
    return {
        "properties": [
            {"id": 1, "address": "123 Main St", "price": 250000},
            {"id": 2, "address": "456 Oak Ave", "price": 320000}
        ]
    }