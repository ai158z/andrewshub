import pytest
from ed25519_verifier.utils import encode_signature, decode_signature, normalize_key_format
from ed25519_verifier.exceptions import InvalidSignatureFormatError


def test_encode_signature_valid_bytes():
    signature = b"test_signature_data"
    result = encode_signature(signature)
    assert isinstance(result, str)
    assert len(result) > 0


def test_encode_signature_invalid_type():
    with pytest.raises(InvalidSignatureFormatError):
        encode_signature("not_bytes")


def test_encode_signature_returns_string():
    signature = b"test_data"
    result = encode_signature(signature)
    assert isinstance(result, str)


def test_decode_signature_valid_string():
    signature_str = "2XvX9oviH7fng6hNhm7N2H3p2DeM1sgstN4T3R3FvL2N"
    result = decode_signature(signature_str)
    assert isinstance(result, bytes)


def test_decode_signature_invalid_type():
    with pytest.raises(InvalidSignatureFormatError):
        decode_signature(12345)


def test_decode_signature_invalid_format():
    with pytest.raises(InvalidSignatureFormatError):
        decode_signature("invalid_base58_string!")


def test_decode_signature_returns_bytes():
    signature_str = "2XvX9oviH7fng6hNhm7N2H3p2DeM1sgstN4T3R3FvL2N"
    result = decode_signature(signature_str)
    assert isinstance(result, bytes)


def test_normalize_key_format_valid_bytes():
    key = b"test_key_data"
    result = normalize_key_format(key)
    assert isinstance(result, bytes)
    assert result == key


def test_normalize_key_format_invalid_type():
    with pytest.raises(InvalidSignatureFormatError):
        normalize_key_format("not_bytes")


def test_normalize_key_format_returns_bytes():
    key = b"test_key"
    result = normalize_key_format(key)
    assert isinstance(result, bytes)
    assert result == key


def test_encode_decode_roundtrip():
    original = b"test_data_for_roundtrip"
    encoded = encode_signature(original)
    decoded = decode_signature(encoded)
    assert decoded == original


def test_encode_signature_empty_bytes():
    signature = b""
    result = encode_signature(signature)
    assert isinstance(result, str)


def test_decode_signature_empty_string():
    with pytest.raises(InvalidSignatureFormatError):
        decode_signature("")


def test_decode_signature_valid_empty():
    signature_str = "2XvX9oviH7fng6hNhm7N2H3p2DeM1sgstN4T3R3FvL2N"
    result = decode_signature(signature_str)
    assert isinstance(result, bytes)


def test_encode_signature_type_check():
    with pytest.raises(InvalidSignatureFormatError):
        encode_signature(123)


def test_decode_signature_type_check():
    with pytest.raises(InvalidSignatureFormatError):
        decode_signature(123)


def test_normalize_key_format_type_check():
    with pytest.raises(InvalidSignatureFormatError):
        normalize_key_format(123)


def test_encode_decode_invalid_signature():
    invalid_sig = "invalid_signature!"
    with pytest.raises(InvalidSignatureFormatError):
        decode_signature(invalid_sig)


def test_normalize_key_format_edge_cases():
    # Test with empty bytes
    with pytest.raises(InvalidSignatureFormatError):
        normalize_key_format(b"")
    
    # Test with valid bytes
    key = b"valid_key_data"
    result = normalize_key_format(key)
    assert result == key


def test_encode_signature_consistency():
    signature = b"consistent_test_data"
    encoded1 = encode_signature(signature)
    encoded2 = encode_signature(signature)
    assert encoded1 == encoded2