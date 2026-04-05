import pytest
from sha3_hasher.core import sha3_512_hash

def test_sha3_512_hash_with_bytes():
    data = b"hello world"
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_with_string():
    data = "hello world"
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_consistent_results():
    data = "test data"
    hash1 = sha3_512_hash(data)
    hash2 = sha3_512_hash(data)
    assert hash1 == hash2

def test_sha3_512_hash_different_inputs_different_outputs():
    data1 = "data1"
    data2 = "data2"
    hash1 = sha3_512_hash(data1)
    hash2 = sha3_512_hash(data2)
    assert hash1 != hash2

def test_sha3_512_hash_empty_string_error():
    with pytest.raises(ValueError, match="Data cannot be empty"):
        sha3_512_hash("")

def test_sha3_512_hash_empty_bytes_error():
    with pytest.raises(ValueError, match="Data cannot be empty"):
        sha3_512_hash(b"")

def test_sha3_512_hash_invalid_type_error():
    with pytest.raises(TypeError, match="Data must be bytes or string"):
        sha3_512_hash(123)

def test_sha3_512_hash_none_data_error():
    with pytest.raises(ValueError, match="Data cannot be empty"):
        sha3_512_hash(None)

def test_sha3_512_hash_none_bytes_error():
    with pytest.raises(TypeError, match="Data must be bytes or string"):
        sha3_512_hash(None)

def test_sha3_512_hash_unicode_string():
    data = "Hello 世界 🌍"
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_long_string():
    data = "a" * 10000
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_special_characters():
    data = "!@#$%^&*()_+-=[]{}|;':,./<>?"
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_binary_data():
    data = b"\x00\x01\x02\x03\xff\xfe\xfd"
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_same_input_same_output():
    data = "consistent input"
    hash1 = sha3_512_hash(data)
    hash2 = sha3_512_hash(data)
    assert hash1 == hash2

def test_sha3_512_hash_empty_string_vs_bytes():
    with pytest.raises(ValueError):
        sha3_512_hash("")
    with pytest.raises(ValueError):
        sha3_512_hash(b"")

def test_sha3_512_hash_bytes_vs_string_same_result():
    data_str = "hello"
    data_bytes = b"hello"
    assert sha3_512_hash(data_str) == sha3_512_hash(data_bytes)

def test_sha3_512_hash_hex_output():
    data = "test"
    result = sha3_512_hash(data)
    hex_result = result.hex()
    assert isinstance(hex_result, str)
    assert len(hex_result) == 128

def test_sha3_512_hash_large_data():
    data = "A" * 10**6  # 1MB of data
    result = sha3_512_hash(data)
    assert isinstance(result, bytes)
    assert len(result) == 64

def test_sha3_512_hash_zero_length_validation():
    with pytest.raises(ValueError):
        sha3_512_hash("")
    with pytest.raises(ValueError):
        sha3_512_hash(b"")

def test_sha3_512_hash_type_preservation():
    str_result = sha3_512_hash("test")
    bytes_result = sha3_512_hash(b"test")
    assert str_result == bytes_result
    assert isinstance(str_result, bytes)