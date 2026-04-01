import pytest
from unittest.mock import patch, MagicMock
from src.core.crypto_utils import hash_key, generate_random_bytes, encrypt_data
import hashlib
import secrets

def test_hash_key_valid_bytes():
    key = b"test_key"
    result = hash_key(key)
    expected = hashlib.sha256(key).hexdigest()
    assert result == expected

def test_hash_key_invalid_input_type():
    with pytest.raises(TypeError):
        hash_key("not_bytes")

def test_hash_key_logs_error_on_invalid_input(caplog):
    with pytest.raises(TypeError):
        hash_key("invalid")
    assert "Invalid input: key must be bytes" in caplog.text

def test_generate_random_bytes_valid():
    with patch('secrets.token_bytes') as mock_token:
        mock_token.return_value = b'random_data'
        result = generate_random_bytes(16)
        assert result == b'random_data'
        mock_token.assert_called_once_with(16)

def test_generate_random_bytes_invalid_length():
    with pytest.raises(ValueError):
        generate_random_bytes(-1)

def test_generate_random_bytes_invalid_type():
    with pytest.raises(ValueError):
        generate_random_bytes("not_an_integer")

def test_generate_random_bytes_logs_error_on_invalid_input(caplog):
    with pytest.raises(ValueError):
        generate_random_bytes("invalid")
    assert "Invalid input: length must be a positive integer" in caplog.text

def test_encrypt_data_valid_inputs():
    data = b"secret_data"
    key = b"encryption_key"
    
    with patch('src.core.crypto_utils.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'0' * 16
        iv, encrypted = encrypt_data(data, key)
        assert iv == b'0' * 16
        assert isinstance(encrypted, bytes)

def test_encrypt_data_invalid_data_type():
    key = b"key"
    with pytest.raises(TypeError):
        encrypt_data("not_bytes", key)

def test_encrypt_data_invalid_key_type():
    data = b"data"
    with pytest.raises(TypeError):
        encrypt_data(data, "not_bytes")

def test_encrypt_data_invalid_both_types():
    with pytest.raises(TypeError):
        encrypt_data("not_bytes", "not_bytes_either")

def test_encrypt_data_logs_error_on_invalid_input(caplog):
    with pytest.raises(TypeError):
        encrypt_data("invalid", "also_invalid")
    assert "Invalid input: data and key must be bytes" in caplog.text

def test_hash_key_logs_success(caplog):
    key = b"test_key"
    hash_key(key)
    assert "Key hashed successfully" in caplog.text

def test_generate_random_bytes_logs_success(caplog):
    with patch('secrets.token_bytes'):
        generate_random_bytes(16)
        assert "Generated 16 random bytes" in caplog.text

def test_encrypt_data_logs_success(caplog):
    with patch('src.core.crypto_utils.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'0' * 16
        data = b"data"
        key = b"key"
        encrypt_data(data, key)
        assert "Data encrypted successfully" in caplog.text

def test_hash_key_empty_bytes():
    key = b""
    result = hash_key(key)
    expected = hashlib.sha256(key).hexdigest()
    assert result == expected

def test_generate_random_bytes_zero_length():
    with pytest.raises(ValueError):
        generate_random_bytes(0)

def test_encrypt_data_empty_data():
    data = b""
    key = b"key"
    with patch('src.core.crypto_utils.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'0' * 16
        iv, encrypted = encrypt_data(data, key)
        assert iv == b'0' * 16
        assert isinstance(encrypted, bytes)

def test_encrypt_data_key_padding():
    data = b"test_data"
    short_key = b"k"
    long_key = b"k" * 50
    
    with patch('src.core.crypto_utils.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'0' * 16
        # Test with short key (should be padded)
        encrypt_data(data, short_key)
        # Test with long key (should be truncated)
        encrypt_data(data, long_key)