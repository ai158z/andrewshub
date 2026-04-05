import pytest
from unittest.mock import Mock, patch, MagicMock
from blockchain_validator.transaction_validator import TransactionValidator
from blockchain_validator.rules.syntax import SyntaxValidator
from blockchain_validator.rules.security import SecurityValidator
from blockchain_validator.rules.semantics import SemanticValidator


@pytest.fixture
def validator():
    with patch.multiple("blockchain_validator.transaction_validator", 
                     EthereumFormat=Mock(), 
                     BitcoinFormat=Mock(), 
                     GenericFormat=Mock(),
                     ThreatDetector=Mock(),
                     AddressVerifier=Mock(),
                     SecurityValidator=Mock(),
                     SemanticValidator=Mock(),
                     SyntaxValidator=Mock()):
        validator = TransactionValidator()
        # Setup mocks
        validator.ethereum_validator.validate_transaction = Mock(return_value=True)
        validator.bitcoin_validator.validate_transaction = Mock(return_value=True)
        validator.generic_validator.validate_format = Mock(return_value=True)
        validator.generic_validator.validate_structure = Mock(return_value=True)
        validator.threat_detector.detect = Mock(return_value=False)
        validator.security_validator.check_signatures = Mock(return_value=True)
        validator.semantic_validator.validate_values = Mock(return_value=True)
        validator.semantic_validator.validate_context = Mock(return_value=True)
        validator.syntax_validator.validate_fields = Mock(return_value=True)
        validator.syntax_validator.validate_types = Mock(return_value=True)
        return validator


def test_validate_format_invalid_type(validator):
    with pytest.raises(ValueError, match="Transaction must be a dictionary"):
        validator.validate_format("not a dict")


def test_validate_format_empty_dict(validator):
    with pytest.raises(ValueError, match="Transaction cannot be empty"):
        validator.validate_format({})


def test_validate_format_missing_structure(validator):
    validator.generic_validator.validate_structure = Mock(return_value=False)
    result = validator.validate_format({"test": "data"})
    assert result is False


def test_validate_format_missing_fields(validator):
    validator.syntax_validator.validate_fields = Mock(return_value=False)
    result = validator.validate_format({"test": "data"})
    assert result is False


def test_validate_format_invalid_types(validator):
    validator.syntax_validator.validate_types = Mock(return_value=False)
    result = validator.validate_format({"test": "data"})
    assert result is False


def test_validate_format_ethereum(validator):
    transaction = {"blockchain": "ethereum", "data": "test"}
    result = validator.validate_format(transaction)
    assert result is True
    validator.ethereum_validator.validate_transaction.assert_called_once_with(transaction)


def test_validate_format_bitcoin(validator):
    transaction = {"blockchain": "bitcoin", "data": "test"}
    result = validator.validate_format(transaction)
    assert result is True
    validator.bitcoin_validator.validate_transaction.assert_called_once_with(transaction)


def test_validate_format_generic(validator):
    transaction = {"blockchain": "solana", "data": "test"}
    result = validator.validate_format(transaction)
    assert result is True
    validator.generic_validator.validate_format.assert_called_once_with(transaction)


def test_validate_format_no_blockchain(validator):
    transaction = {"data": "test"}
    result = validator.validate_format(transaction)
    assert result is True
    validator.generic_validator.validate_format.assert_called()


def test_validate_signature_invalid_type(validator):
    with pytest.raises(ValueError, match="Transaction must be a dictionary"):
        validator.validate_signature("not a dict")


def test_validate_signature_missing_signature(validator):
    with pytest.raises(ValueError, match="Transaction missing signature field"):
        validator.validate_signature({"amount": 100})


def test_validate_signature_missing_public_key(validator):
    with pytest.raises(ValueError, match="Transaction missing public key field"):
        validator.validate_signature({"signature": "sig"})


def test_validate_signature_missing_data_or_hash(validator):
    with pytest.raises(ValueError, match="Transaction missing data or hash field"):
        transaction = {"signature": "sig", "public_key": "key"}
        validator.validate_signature(transaction)


def test_validate_signature_success(validator):
    transaction = {"signature": "sig", "public_key": "key", "data": "test_data"}
    validator.security_validator.check_signatures = Mock(return_value=True)
    result = validator.validate_signature(transaction)
    assert result is True


def test_validate_amounts_invalid_type(validator):
    with pytest.raises(ValueError, match="Transaction must be a dictionary"):
        validator.validate_amounts("not a dict")


def test_validate_amounts_missing_amount(validator):
    with pytest.raises(ValueError, match="Transaction missing amount field"):
        validator.validate_amounts({"from": "addr1"})


def test_validate_amounts_missing_from_to(validator):
    with pytest.raises(ValueError, match="Transaction missing from/to fields"):
        validator.validate_amounts({"amount": 100})


def test_validate_amounts_non_numeric(validator):
    with pytest.raises(ValueError, match="Amount must be a number"):
        validator.validate_amounts({"amount": "not_a_number", "from": "addr1", "to": "addr2"})


def test_validate_amounts_negative_amount(validator):
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        validator.validate_amounts({"amount": -100, "from": "addr1", "to": "addr2"})


def test_validate_complete_pipeline(validator):
    transaction = {
        "blockchain": "generic",
        "signature": "sig",
        "public_key": "key",
        "data": "test_data",
        "amount": 100,
        "from": "addr1",
        "to": "addr2"
    }
    result = validator.validate(transaction)
    assert result is True


def test_validate_complete_pipeline_format_fails(validator):
    transaction = {
        "blockchain": "generic",
        "signature": "sig",
        "public_key": "key",
        "data": "test_data",
        "amount": 100,
        "from": "addr1",
        "to": "addr2"
    }
    validator.generic_validator.validate_format = Mock(return_value=False)
    result = validator.validate(transaction)
    assert result is False


def test_validate_complete_pipeline_signature_fails(validator):
    transaction = {
        "blockchain": "generic",
        "signature": "sig",
        "public_key": "key",
        "data": "test_data",
        "amount": 100,
        "from": "addr1",
        "to": "addr2"
    }
    validator.security_validator.check_signatures = Mock(return_value=False)
    result = validator.validate(transaction)
    assert result is False


def test_validate_complete_pipeline_amounts_fails(validator):
    transaction = {
        "blockchain": "generic",
        "signature": "sig",
        "public_key": "key",
        "data": "test_data",
        "amount": 100,
        "from": "addr1",
        "to": "addr2"
    }
    validator.semantic_validator.validate_values = Mock(return_value=False)
    result = validator.validate(transaction)
    assert result is False


def test_validate_complete_pipeline_threat_detected(validator):
    transaction = {
        "blockchain": "generic",
        "signature": "sig",
        "public_key": "key", 
        "data": "test_data",
        "amount": 100,
        "from": "addr1",
        "to": "addr2"
    }
    validator.threat_detector.detect = Mock(return_value=True)
    result = validator.validate(transaction)
    assert result is False


def test_validate_complete_pipeline_exception_handling(validator):
    transaction = "not a dict"
    result = validator.validate(transaction)
    assert result is False