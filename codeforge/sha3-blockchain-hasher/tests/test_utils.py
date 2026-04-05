import os
import pytest
from unittest.mock import mock_open, patch
from sha3_hasher.utils import (
    sha3_512_hash, 
    sha3_512_hash_hex, 
    validate_environment_variables, 
    format_hash_for_display,
    validate_data_integrity,
    get_file_hash
)

def test_sha3_512_hash_valid_bytes():
    data = b"test data"
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_invalid_type():
    with pytest.raises(TypeError):
        sha3_512_hash("string data")

def test_sha3_512_hash_empty_bytes():
    with pytest.raises(ValueError):
        sha3_512_hash(b"")

def test_sha3_512_hash_hex():
    data = b"test data"
    result = sha3_512_hash_hex(data)
    assert isinstance(result, str)
    assert len(result) == 128
    assert all(c in '0123456789abcdef' for c in result)

def test_sha3_512_hash_hex_invalid_type():
    with pytest.raises(TypeError):
        sha3_512_hash_hex("string data")

def test_sha3_512_hash_hex_empty_bytes():
    with pytest.raises(ValueError):
        sha3_512_hash_hex(b"")

def test_validate_environment_variables_all_set():
    with patch.dict(os.environ, {'TEST_VAR1': 'value1', 'TEST_VAR2': 'value2'}):
        result = validate_environment_variables('TEST_VAR1', 'TEST_VAR2')
        assert result == {'TEST_VAR1': 'value1', 'TEST_VAR2': 'value2'}

def test_validate_environment_variables_missing():
    with patch.dict(os.environ, {'TEST_VAR1': 'value1'}):
        with pytest.raises(EnvironmentError) as excinfo:
            validate_environment_variables('TEST_VAR1', 'MISSING_VAR')
        assert 'MISSING_VAR' in str(excinfo.value)

def test_format_hash_for_display():
    hash_bytes = bytes.fromhex('a' * 128)
    result = format_hash_for_display(hash_bytes, 4)
    assert isinstance(result, str)
    assert ' ' in result
    assert result == result.upper()

def test_format_hash_for_display_default_chunk():
    hash_bytes = bytes.fromhex('a' * 128)
    result = format_hash_for_display(hash_bytes)
    assert len(result.split(' ')[0]) == 4

def test_validate_data_integrity_valid():
    data = b"test data"
    hash_string = sha3_512_hash_hex(data)
    result = validate_data_integrity(data, hash_string)
    assert result is True

def test_validate_data_integrity_invalid():
    data = b"test data"
    wrong_hash = "0" * 128
    result = validate_data_integrity(data, wrong_hash)
    assert result is False

def test_validate_data_integrity_unsupported_algorithm():
    with pytest.raises(ValueError):
        validate_data_integrity(b"test", "abc123", "md5")

def test_get_file_hash_valid():
    file_content = b"test file content"
    with patch("builtins.open", mock_open(read_data=file_content)):
        with patch("os.path.exists", return_value=True):
            result = get_file_hash("dummy_path")
            assert isinstance(result, bytes)
            assert len(result) == 64

def test_get_file_hash_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            get_file_hash("nonexistent_file")

def test_sha3_512_hash_consistent():
    data = b"consistent test data"
    hash1 = sha3_512_hash(data)
    hash2 = sha3_512_hash(data)
    assert hash1 == hash2

def test_sha3_512_hash_different_input():
    data1 = b"data1"
    data2 = b"data2"
    assert sha3_512_hash(data1) != sha3_512_hash(data2)

def test_sha3_512_hash_hex_consistent():
    data = b"consistent test data"
    hex_hash = sha3_512_hash_hex(data)
    manual_hex = sha3_512_hash(data).hex()
    assert hex_hash == manual_hex

def test_validate_environment_variables_case_sensitive():
    with patch.dict(os.environ, {'test_var': 'value'}):
        result = validate_environment_variables('test_var')
        assert result['test_var'] == 'value'
        with pytest.raises(EnvironmentError):
            validate_environment_variables('TEST_VAR')

def test_format_hash_for_display_empty():
    hash_bytes = bytes()
    result = format_hash_for_display(hash_bytes)
    assert result == ""