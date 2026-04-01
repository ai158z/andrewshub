import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.encoding.symbolic_encoder import SymbolicEncoder


def test_encode_string_data():
    encoder = SymbolicEncoder()
    data = "test"
    with patch.object(encoder.codonic_encoder, 'encode_symbolic') as mock_encode:
        mock_encode.return_value = b'encoded_result'
        result = encoder.encode(data)
        assert result == b'encoded_result'


def test_encode_bytes_data():
    encoder = SymbolicEncoder()
    data = b'test_bytes'
    result = encoder.encode(data)
    assert result == data


def test_encode_empty_list_raises_error():
    encoder = SymbolicEncoder()
    with pytest.raises(ValueError, match="Data cannot be empty"):
        encoder.encode([])


def test_encode_quantum_state_data():
    encoder = SymbolicEncoder()
    data = [1+1j, 2+2j, 3+3j]
    with patch.object(encoder.codonic_encoder, 'encode_symbolic'):
        result = encoder.encode(data)
        assert isinstance(result, bytes)


def test_encode_invalid_data_type():
    encoder = SymbolicEncoder()
    with pytest.raises(ValueError, match="Unsupported data type for encoding"):
        encoder.encode(123)


def test_encode_with_key():
    encoder = SymbolicEncoder()
    data = "test"
    key = b'secret_key'
    with patch.object(encoder.codonic_encoder, 'encode_symbolic') as mock_encode:
        mock_encode.return_value = "decoded_string"
        result = encoder.encode(data, key)
        assert result == "decoded_string"


def test_encode_quantum_states_normalization():
    encoder = SymbolicEncoder()
    data = [3+4j, 5+12j]
    normalized_result = encoder._encode_quantum_states(data)
    # Should return bytes of normalized complex numbers
    assert isinstance(normalized_result, bytes)


def test_decode_string_bytes():
    encoder = SymbolicEncoder()
    encoded_data = b'hello'
    result = encoder.decode(encoded_data)
    assert result == 'hello'


def test_decode_with_key():
    encoder = SymbolicEncoder()
    encoded_data = b'encoded'
    key = b'key'
    with patch.object(encoder.codonic_encoder, 'decode_symbolic') as mock_decode:
        mock_decode.return_value = "decoded"
        result = encoder.decode(encoded_data, key)
        assert result == "decoded"


def test_decode_without_key():
    encoder = SymbolicEncoder()
    encoded_data = b'test_data'
    result = encoder.decode(encoded_data)
    assert result == 'test_data'


def test_normalize_amplitude():
    encoder = SymbolicEncoder()
    amplitude = 3+4j
    normalized = encoder._normalize_amplitude(amplitude)
    assert abs(normalized) == pytest.approx(1.0)


def test_hadamard_transform():
    encoder = SymbolicEncoder()
    data = [1+0j, 0+1j]
    result = encoder._hadamard_transform(data)
    # Should return transformed data
    assert len(result) == len(data)


def test_encode_complex_data():
    encoder = SymbolicEncoder()
    data = [1+1j, 2+2j]
    result = encoder.encode(data)
    assert isinstance(result, bytes)


def test_encode_empty_data_raises():
    encoder = SymbolicEncoder()
    with pytest.raises(ValueError, match="Data cannot be empty"):
        encoder.encode([])


def test_encode_invalid_string_type():
    encoder = SymbolicEncoder()
    with pytest.raises(ValueError):
        encoder.encode(123)


def test_encode_quantum_state_list():
    encoder = SymbolicEncoder()
    data = [1+0j, 0+1j]
    result = encoder.encode(data)
    assert isinstance(result, bytes)


def test_encode_quantum_state_empty_list_error():
    encoder = SymbolicEncoder()
    with pytest.raises(ValueError):
        encoder.encode([])


def test_encode_quantum_state_with_key():
    encoder = SymbolicEncoder()
    data = [1+0j, 0+1j]
    key = b'test_key'
    with patch.object(encoder.codonic_encoder, 'encode_symbolic'):
        result = encoder.encode(data, key)
        assert isinstance(result, bytes)


def test_normalize_nonzero_amplitude():
    encoder = SymbolicEncoder()
    amplitude = 3+4j
    result = encoder._normalize_amplitude(amplitude)
    expected_magnitude = abs(amplitude)
    assert abs(result) == pytest.approx(1.0)