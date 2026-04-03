import pytest
from unittest.mock import patch, mock_open
import os
import tempfile
from tests import pytest_configure, temp_directory, sample_property_data, mock_search_response

def test_pytest_configure_adds_markers():
    mock_config = MockConfig()
    pytest_configure(mock_config)
    assert "property_search" in mock_config.markers
    assert "cli" in mock_config.markers
    assert len(mock_config.markers) == 2

def test_temp_directory_fixture():
    with patch('tests.tempfile') as mock_tempfile:
        mock_tempfile.TemporaryDirectory.return_value.__enter__.return_value = '/tmp/test'
        with tempfile.TemporaryDirectory() as temp_dir:
            result = temp_directory()
            assert result is not None

def test_sample_property_data_fixture():
    data = sample_property_data()
    assert len(data) == 3
    assert data[0]['id'] == 1
    assert data[1]['address'] == '456 Oak Ave'
    assert data[2]['price'] == 480000

def test_mock_search_response_fixture():
    response = mock_search_response()
    assert 'properties' in response
    assert len(response['properties']) == 2
    assert response['properties'][0]['id'] == 1

class MockConfig:
    def __init__(self):
        self.markers = []

    def addinivalue_line(self, line_type, marker):
        if line_type == "markers":
            self.markers.append(marker.split(':')[0])