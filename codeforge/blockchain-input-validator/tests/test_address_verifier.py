import pytest
from unittest.mock import Mock, patch
from blockchain_validator.address_verifier import AddressVerifier


def test_verify_valid_ethereum_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Valid Ethereum address
    valid_address = "0x74e85519fd64d9a8e0350161e39351a4e41aa80e"
    result = verifier.verify(valid_address, 'ethereum')
    assert result is True


def test_verify_invalid_ethereum_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Invalid Ethereum address (wrong checksum)
    invalid_address = "0x74e85519fd64d9a8e0350161e39351a4e41aa80f"
    result = verifier.verify(invalid_address, 'ethereum')
    assert result is False


def test_verify_valid_bitcoin_legacy_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Valid Bitcoin legacy address
    valid_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    result = verifier.verify(valid_address, 'bitcoin')
    assert result is True


def test_verify_invalid_bitcoin_legacy_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Invalid Bitcoin legacy address (wrong checksum)
    invalid_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNb"
    result = verifier.verify(invalid_address, 'bitcoin')
    assert result is False


def test_verify_valid_bitcoin_bech32_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Valid Bech32 address
    valid_address = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"
    result = verifier.verify(valid_address, 'bitcoin')
    assert result is True


def test_verify_invalid_bitcoin_bech32_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Invalid Bech32 address
    invalid_address = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5"
    result = verifier.verify(invalid_address, 'bitcoin')
    assert result is False


def test_verify_suspicious_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=True)
    
    # Valid address but marked as suspicious
    address = "0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e"
    result = verifier.verify(address, 'ethereum')
    assert result is False


def test_verify_invalid_network_type():
    verifier = AddressVerifier()
    
    with pytest.raises(ValueError):
        verifier.verify("0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e", "invalid_network")


def test_verify_invalid_address_type():
    verifier = AddressVerifier()
    
    result = verifier.verify(None, 'ethereum')
    assert result is False


def test_verify_empty_address():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    result = verifier.verify("", 'ethereum')
    assert result is False


def test_verify_invalid_address_length():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    # Ethereum address with wrong length
    result = verifier.verify("0x123", 'ethereum')
    assert result is False


def test_is_valid_ethereum_address_invalid_hex():
    verifier = AddressVerifier()
    
    # Non-hex characters
    result = verifier.is_valid_ethereum_address("0x74e85519fd64d64d9a8e0350161e39351a4e41aa80g")
    assert result is False


def test_is_valid_bitcoin_address_invalid_prefix():
    verifier = AddressVerifier()
    
    # Invalid Bitcoin address prefix
    result = verifier.is_valid_bitcoin_address("4A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    assert result is False


def test_is_valid_generic_address_valid():
    verifier = AddressVerifier()
    
    # Valid generic address
    result = verifier.is_valid_generic_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    assert result is True


def test_is_valid_generic_address_invalid_length():
    verifier = AddressVerifier()
    
    # Generic address too short
    result = verifier.is_valid_generic_address("1A")
    assert result is False


def test_batch_verify_valid_addresses():
    verifier = AddressVerifier()
    verifier.threat_detector.is_suspicious_address = Mock(return_value=False)
    
    addresses = [
        {"address": "0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e", "network": "ethereum"},
        {"address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "network": "bitcoin"}
    ]
    
    results = verifier.batch_verify(addresses)
    assert results == [True, True]


def test_batch_verify_invalid_input():
    verifier = AddressVerifier()
    
    with pytest.raises(TypeError):
        verifier.batch_verify("not a list")


def test_batch_verify_invalid_address_dict():
    verifier = AddressVerifier()
    
    addresses = [
        {"address": "0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e", "network": "ethereum"},
        {"invalid": "format"}  # Missing required keys
    ]
    
    results = verifier.batch_verify(addresses)
    assert results == [True, False]


def test_validate_address_format_valid():
    verifier = AddressVerifier()
    
    result = verifier.validate_address_format("0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e", "ethereum")
    assert result is True


def test_validate_address_format_invalid_network():
    verifier = AddressVerifier()
    
    result = verifier.validate_address_format("0x74e85519fd64d64d9a8e0350161e39351a4e41aa80e", "invalid")
    assert result is False