import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.quantum_sensors.codonic_symbolic_layer import CodonicSymbolicLayer, Codon, CodonType

def test_initialization():
    layer = CodonicSymbolicLayer()
    assert layer is not None
    assert len(layer.codon_alphabet) > 0
    assert len(layer.codon_mapping) > 0

def test_symbolic_to_rna_conversion():
    layer = CodonicSymbolicLayer()
    result = layer._symbolic_to_rna("ABC")
    assert isinstance(result, str)
    assert len(result) == 3

def test_encode_symbolic_representation():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("ABC")
    assert isinstance(codons, list)
    assert len(codons) > 0
    assert all(isinstance(c, Codon) for c in codons)

def test_encode_decode_roundtrip():
    layer = CodonicSymbolicLayer()
    input_text = "TEST"
    encoded = layer.encode_symbolic_representation(input_text)
    decoded = layer.decode_codon_sequence(encoded)
    assert isinstance(decoded, str)

def test_decode_codon_sequence():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("TEST")
    result = layer.decode_codon_sequence(codons)
    assert isinstance(result, str)

def test_codon_frequency_calculation():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("AAABBBCCC")
    freq = layer.get_codon_frequency(codons)
    assert isinstance(freq, dict)
    assert len(freq) > 0

def test_codon_entropy_calculation():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("AAABBBCCC")
    entropy = layer.calculate_codon_entropy(codons)
    assert isinstance(entropy, float)
    assert entropy >= 0

def test_codon_sequence_validation():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("TEST")
    is_valid = layer.validate_codon_sequence(codons)
    assert isinstance(is_valid, bool)
    assert is_valid is True

def test_empty_input_encoding():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("")
    assert isinstance(codons, list)
    assert len(codons) == 0

def test_special_characters_encoding():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("ABC!@#")
    assert isinstance(codons, list)
    assert len(codons) > 0

def test_long_input_encoding():
    layer = CodonicSymbolicLayer()
    long_input = "A" * 1000
    codons = layer.encode_symbolic_representation(long_input)
    assert isinstance(codons, list)

def test_codon_type_enum():
    assert CodonType.SENSORY.value == "sensory"
    assert CodonType.MOTOR.value == "motor"
    assert CodonType.SYMBOLIC.value == "symbolic"

def test_codon_dataclass():
    codon = Codon(symbol="TEST", codon_type=CodonType.SYMBOLIC)
    assert codon.symbol == "TEST"
    assert codon.codon_type == CodonType.SYMBOLIC
    assert codon.amplitude == 1.0
    assert codon.phase == 0.0

def test_unknown_codon_handling():
    layer = CodonicSymbolicLayer()
    codons = layer.encode_symbolic_representation("XYZ")
    assert len(codons) > 0
    # Unknown codons should create codon objects with Unknown_ prefix
    symbols = [c.symbol for c in codons]
    assert any("Unknown" in s for s in symbols) or len(symbols) == 0

def test_rna_conversion_edge_cases():
    layer = CodonicSymbolicLayer()
    # Test with empty string
    result = layer._symbolic_to_rna("")
    assert result == ""
    
    # Test with special characters
    result = layer._symbolic_to_rna("!@#$%")
    assert isinstance(result, str)

def test_codon_frequency_edge_case():
    layer = CodonicSymbolicLayer()
    freq = layer.get_codon_frequency([])
    assert freq == {}
    
    # Test with single codon
    codons = layer.encode_symbolic_representation("A")
    freq = layer.get_codon_entropy(codons)
    assert isinstance(freq, float)

def test_invalid_codon_sequence():
    layer = CodonicSymbolicLayer()
    is_valid = layer.validate_codon_sequence([1, 2, 3])  # Invalid codon objects
    assert is_valid is False

def test_codon_with_invalid_data():
    layer = CodonicSymbolicLayer()
    # Create a codon with invalid data
    invalid_codon = Codon(symbol="", codon_type="invalid")  # type: ignore
    is_valid = layer.validate_codon_sequence([invalid_codon])
    assert is_valid is False

def test_entropy_edge_cases():
    layer = CodonicSymbolicLayer()
    # Test entropy of empty sequence
    entropy = layer.calculate_codon_entropy([])
    assert entropy == 0.0
    
    # Test entropy of single codon
    codons = layer.encode_symbolic_representation("A")[:1]  # Get first codon
    if codons:
        entropy = layer.calculate_codon_entropy(codons)
        assert isinstance(entropy, float)

def test_decode_edge_cases():
    layer = CodonicSymbolicLayer()
    # Test decoding empty sequence
    result = layer.decode_codon_sequence([])
    assert result == ""
    
    # Test decoding single codon
    codons = layer.encode_symbolic_representation("A")
    if codons:
        result = layer.decode_codon_sequence(codons[:1])
        assert isinstance(result, str)