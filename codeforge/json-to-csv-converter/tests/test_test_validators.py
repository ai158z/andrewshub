import pytest
import json
import os
import tempfile
from src.validators import validate_json_schema, is_valid_json_file

@pytest.fixture
def sample_schema():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"}
        },
        "required": ["name", "age"]
    }

@pytest.fixture
def valid_data():
    return {
        "name": "John",
        "age": 30
    }

@pytest.fixture
def invalid_data():
    return {
        "name": 123,
        "age": "thirty"
    }

def test_validate_json_schema_with_valid_data(valid_data, sample_schema):
    assert validate_json_schema(valid_data, sample_schema) is True

def test_validate_json_schema_with_invalid_data(invalid_data, sample_schema):
    invalid_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "number"},
            "age": {"type": "string"}
        }
    }
    assert validate_json_schema(valid_data, invalid_schema) is False

def test_validate_json_schema_with_empty_data(sample_schema):
    empty_data = {}
    assert validate_json_schema(empty_data, sample_schema) is False

def test_is_valid_json_file_with_valid_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write('{"name": "John", "age": 30}')
        f.flush()
        assert is_valid_json_file(f.name) is True
        os.unlink(f.name)

def test_is_valid_json_file_with_invalid_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write('{"name": "John", "age": 30')  # Invalid JSON
        f.flush()
        assert is_valid_json_file(f.name) is False
        os.unlink(f.name)

def test_is_valid_json_file_with_nonexistent_file():
    assert is_valid_json_file("/non/existent/file.json") is False

def test_is_valid_json_file_with_non_json_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("This is not JSON content")
        f.flush()
        assert is_valid_json_file(f.name) is False
        os.unlink(f.name)

def test_is_valid_json_file_non_json_extension():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write('{"valid": "json"}')
        f.flush()
        assert is_valid_json_file(f.name) is False
        os.unlink(f.name)