import pytest
from unittest.mock import Mock, patch, MagicMock
from blockchain_validator.rules.semantics import SemanticValidator

@pytest.fixture
def semantic_validator():
    return SemanticValidator()

@pytest.fixture
def mock_dependencies():
    with patch('blockchain_validator.rules.semantics.TransactionValidator') as mock_tx_validator, \
         patch('blockchain_validator.rules.semantics.ThreatDetector') as mock_threat_detector, \
         patch('blockchain_validator.rules.semantics.AddressVerifier') as mock_address_verifier, \
         patch('blockchain_validator.rules.semantics.GenericFormat') as mock_generic_format, \
         patch('blockchain_validator.rules.semantics.EthereumFormat') as mock_ethereum_format, \
         patch('blockchain_validator.rules.semantics.BitcoinFormat') as mock_bitcoin_format:
        
        mock_tx_validator.return_value = Mock()
        mock_threat_detector.return_value = Mock()
        mock_address_verifier.return_value = Mock()
        mock_generic_format.return_value = Mock()
        mock_ethereum_format.return_value = Mock()
        mock_bitcoin_format.return_value = Mock()
        
        yield {
            'tx_validator': mock_tx_validator,
            'threat_detector': mock_threat_detector,
            'address_verifier': mock_address_verifier,
            'generic_format': mock_generic_format,
            'ethereum_format': mock_ethereum_format,
            'bitcoin_format': mock_bitcoin_format
        }

def test_validate_meaning_valid_transaction(semantic_validator):
    with patch.object(semantic_validator.generic_format, 'validate_structure', return_value=True), \
         patch.object(semantic_validator.transaction_validator, 'validate', return_value=True):
        result = semantic_validator.validate_meaning({'transaction': {}})
        assert result is True

def test_validate_meaning_invalid_structure(semantic_validator):
    with patch.object(semantic_validator.generic_format, 'validate_structure', return_value=False):
        result = semantic_validator.validate_meaning({})
        assert result is False

def test_validate_meaning_transaction_validation_fails(semantic_validator):
    with patch.object(semantic_validator.generic_format, 'validate_structure', return_value=True), \
         patch.object(semantic_validator.transaction_validator, 'validate', return_value=False):
        result = semantic_validator.validate_meaning({'transaction': {}})
        assert result is False

def test_validate_meaning_exception_handling(semantic_validator):
    with patch.object(semantic_validator.generic_format, 'validate_structure', side_effect=Exception("Test error")):
        result = semantic_validator.validate_meaning({})
        assert result is False

def test_validate_context_invalid_data_type(semantic_validator):
    result = semantic_validator.validate_context("invalid_string")
    assert result is False

def test_validate_context_ethereum_type(semantic_validator):
    with patch.object(semantic_validator.ethereum_format, 'validate_transaction', return_value=True):
        data = {'blockchain_type': 'ethereum'}
        result = semantic_validator.validate_context(data)
        assert result is True

def test_validate_context_bitcoin_type(semantic_validator):
    with patch.object(semantic_validator.bitcoin_format, 'validate_transaction', return_value=True):
        data = {'blockchain_type': 'bitcoin'}
        result = semantic_validator.validate_context(data)
        assert result is True

def test_validate_context_generic_transaction(semantic_validator):
    with patch.object(semantic_validator.transaction_validator, 'validate', return_value=True):
        data = {'transaction': {}}
        result = semantic_validator.validate_context(data)
        assert result is True

def test_validate_context_fallback(semantic_validator):
    with patch.object(semantic_validator.generic_format, 'validate_structure', return_value=True):
        result = semantic_validator.validate_context({})
        assert result is True

def test_validate_context_exception(semantic_validator):
    with patch.object(semantic_validator.generic_format, 'validate_structure', side_effect=Exception("Error")):
        result = semantic_validator.validate_context({})
        assert result is False

def test_validate_values_invalid_data_type(semantic_validator):
    result = semantic_validator.validate_values("invalid")
    assert result is False

def test_validate_values_address_verification_fails(semantic_validator):
    with patch.object(semantic_validator.address_verifier, 'verify', return_value=False):
        data = {'from_address': '0x123'}
        result = semantic_validator.validate_values(data)
        assert result is False

def test_validate_values_threat_detection_fails(semantic_validator):
    with patch.object(semantic_validator.address_verifier, 'verify', return_value=True), \
         patch.object(semantic_validator.threat_detector, 'is_suspicious_address', return_value=True), \
         patch.object(semantic_validator.threat_detector, 'is_malicious_pattern', return_value=True):
        data = {'to_address': '0x456'}
        result = semantic_validator.validate_values(data)
        assert result is False

def test_validate_values_malicious_pattern(semantic_validator):
    with patch.object(semantic_validator.address_verifier, 'verify', return_value=True), \
         patch.object(semantic_validator.threat_detector, 'is_suspicious_address', return_value=False), \
         patch.object(semantic_validator.threat_detector, 'is_malicious_pattern', return_value=False):
        result = semantic_validator.validate_values({})
        assert result is True

def test_validate_values_amount_validation_fails(semantic_validator):
    with patch.object(semantic_validator.threat_detector, 'is_malicious_pattern', return_value=False):
        data = {'amount': -5}
        result = semantic_validator.validate_values(data)
        assert result is False

def test_validate_values_missing_required_fields(semantic_validator):
    with patch.object(semantic_validator.threat_detector, 'is_malicious_pattern', return_value=False):
        data = {'from_address': '', 'to_address': '0x123', 'amount': 100}
        result = semantic_validator.validate_values(data)
        assert result is False

def test_validate_amount_positive_integer(semantic_validator):
    assert semantic_validator._validate_amount(100) is True

def test_validate_amount_negative_integer(semantic_validator):
    assert semantic_validator._validate_amount(-50) is False

def test_validate_amount_string_conversion(semantic_validator):
    assert semantic_validator._validate_amount("100.50") is True

def test_validate_amount_invalid_string(semantic_validator):
    assert semantic_validator._validate_amount("invalid") is False