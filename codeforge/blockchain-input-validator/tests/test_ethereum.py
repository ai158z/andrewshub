import pytest
from unittest.mock import patch, MagicMock
from blockchain_validator.formats.ethereum import EthereumFormat

def test_validate_transaction_valid():
    transaction = {
        'from': '0x1234567890123456789012345678901234567890',
        'to': '0x0987654321098765432109876543210987654321',
        'value': 1000000000000000000,
        'gas': 21000,
        'gasPrice': 20000000000,
        'nonce': 0,
        'chainId': 1,
        'r': 12345,
        's': 67890,
        'v': 27
    }
    assert EthereumFormat.validate_transaction(transaction) is True

def test_validate_transaction_missing_field():
    transaction = {
        'from': '0x1234567890123456789012345678901234567890',
        'to': '0x0987654321098765432109876543210987654321',
        'value': 1000000000000000000,
        'gas': 21000,
        'gasPrice': 20000000000,
        'nonce': 0,
        'r': 12345,
        's': 67890
        # Missing chainId
    }
    assert EthereumFormat.validate_transaction(transaction) is False

def test_validate_transaction_invalid_address():
    transaction = {
        'from': 'invalid_address',
        'to': '0x0987654321098765432109876543210987654321',
        'value': 1000000000000000000,
        'gas': 21000,
        'gasPrice': 20000000000,
        'nonce': 0,
        'chainId': 1,
        'r': 12345,
        's': 67890,
        'v': 27
    }
    assert EthereumFormat.validate_transaction(transaction) is False

def test_validate_transaction_invalid_value():
    transaction = {
        'from': '0x1234567890123456789012345678901234567890',
        'to': '0x0987654321098765432109876543210987654321',
        'value': -1000000000000000000,  # Negative value
        'gas': 21000,
        'gasPrice': 20000000000,
        'nonce': 0,
        'chainId': 1,
        'r': 12345,
        's': 67890,
        'v': 27
    }
    assert EthereumFormat.validate_transaction(transaction) is False

def test_validate_address_valid():
    address = '0x1234567890123456789012345678901234567890'
    assert EthereumFormat.validate_address(address) is True

def test_validate_address_invalid_format():
    address = 'invalid_address_format'
    assert EthereumFormat.validate_address(address) is False

def test_validate_address_invalid_type():
    address = 12345
    assert EthereumFormat.validate_address(address) is False

def test_validate_address_checksum_valid():
    address = '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed'  # Valid checksum address
    assert EthereumFormat.validate_address(address) is True

def test_validate_address_checksum_invalid():
    address = '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed'  # Invalid checksum
    assert EthereumFormat.validate_address(address) is False

def test_parse_transaction_hex_string():
    raw_tx = '0xf86d80843b9aca0082520894f0109fc8df283027b6285cc889f5aa624eac28d78801158e460913d00000180a00000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000'
    with patch('blockchain_validator.formats.ethereum.decode') as mock_decode:
        mock_decode.return_value = [0, 1000000000, 21000, b'\xf0\x10\x9f\xc8\xdf(\x30\'\xb6(y\\\xc8\x89\xf5\xaad\xe2\x8d', 50000000000000000, b'', 27, 0, 0]
        result = EthereumFormat.parse_transaction(raw_tx)
        assert 'nonce' in result
        assert 'gasPrice' in result
        assert 'gas' in result
        assert 'to' in result
        assert 'value' in result

def test_parse_transaction_bytes():
    raw_tx = bytes.fromhex('f86d80843b9aca0082520894f0109fc8df283027b6285cc889f5aa624eac28d78801158e460913d00000180a00000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000')
    with patch('blockchain_validator.formats.ethereum.decode') as mock_decode:
        mock_decode.return_value = [0, 1000000000, 21000, b'\xf0\x10\x9f\xc8\xdf(\x30\'\xb6(y\\\xc8\x89\xf5\xaad\xe2\x8d', 50000000000000000, b'', 27, 0, 0]
        result = EthereumFormat.parse_transaction(raw_tx)
        assert 'nonce' in result

def test_parse_transaction_invalid_hex():
    raw_tx = 'invalid_hex_string'
    with pytest.raises(ValueError, match="Failed to parse transaction"):
        EthereumFormat.parse_transaction(raw_tx)

def test_parse_transaction_invalid_type():
    raw_tx = 12345
    with pytest.raises(TypeError, match="Raw transaction must be string or bytes"):
        EthereumFormat.parse_transaction(raw_tx)

def test_parse_transaction_non_hex_string():
    raw_tx = 'zzzz'
    with pytest.raises(ValueError, match="Raw transaction is not valid hex"):
        EthereumFormat.parse_transaction(raw_tx)