import pytest
import numpy as np
from src.encoding.codonic_layer import CodonicEncoder, encode_symbolic, decode_symbolic

def test_codonic_encoder_initialization():
    encoder = CodonicEncoder()
    assert encoder.codewords is not None
    assert encoder.basis_states is not None

def test_encode_valid_string():
    encoder = CodonicEncoder()
    result = encoder.encode("01")
    assert result == "00001111"

def test_encode_invalid_input_type():
    encoder = CodonicEncoder()
    with pytest.raises(TypeError):
        encoder.encode(123)

def test_encode_with_unknown_characters():
    encoder = CodonicEncoder()
    result = encoder.encode("0x1")  # 'x' is not in codewords
    assert result == "000000001111"  # 'x' defaults to '0' codeword

def test_decode_valid_codeword():
    encoder = CodonicEncoder()
    result = encoder.decode("00001111")
    assert result == "01"

def test_decode_invalid_input_type():
    encoder = CodonicEncoder()
    with pytest.raises(TypeError):
        encoder.decode(123)

def test_decode_incomplete_codeword():
    encoder = CodonicEncoder()
    result = encoder.decode("000011")  # Incomplete codeword
    assert result == "0"  # Should decode only complete codewords

def test_find_symbol_for_codeword():
    encoder = CodonicEncoder()
    assert encoder._find_symbol_for_codeword("0000") == "0"
    assert encoder._find_symbol_for_codeword("1111") == "1"
    assert encoder._find_symbol_for_codeword("0011") == "+"
    assert encoder._find_symbol_for_codeword("1100") == "-"
    assert encoder._find_symbol_for_codeword("0101") == "i"
    assert encoder._find_symbol_for_codeword("1010") == "-i"

def test_find_symbol_for_unknown_codeword():
    encoder = CodonicEncoder()
    result = encoder._find_symbol_for_codeword("9999")  # Unknown codeword
    assert result == "0"  # Default fallback

def test_encode_symbolic_function():
    result = encode_symbolic("01")
    assert result == "00001111"

def test_encode_symbolic_invalid_type():
    with pytest.raises(TypeError):
        encode_symbolic(123)

def test_decode_symbolic_function():
    result = decode_symbolic("00001111")
    assert result == "01"

def test_decode_symbolic_invalid_type():
    with pytest.raises(TypeError):
        decode_symbolic(123)

def test_codonic_encoder_basis_states():
    encoder = CodonicEncoder()
    expected_states = ['0', '1', '+', '-', 'i', '-i']
    assert encoder.basis_states == expected_states

def test_codonic_encoder_codewords():
    encoder = CodonicEncoder()
    expected_codewords = {
        '0': '0000',
        '1': '1111',
        '+': '0011',
        '-': '1100',
        'i': '0101',
        '-i': '1010'
    }
    assert encoder.codewords == expected_codewords

def test_encode_empty_string():
    encoder = CodonicEncoder()
    result = encoder.encode("")
    assert result == ""

def test_decode_empty_string():
    encoder = CodonicEncoder()
    result = encoder.decode("")
    assert result == ""

def test_encode_symbolic_empty_string():
    result = encode_symbolic("")
    assert result == ""

def test_decode_symbolic_empty_string():
    result = decode_symbolic("")
    assert result == ""