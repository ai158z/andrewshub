import pytest
from unittest.mock import Mock, patch, MagicMock
from blockchain_validator.rules.security import SecurityValidator

def test_detect_malicious_patterns_found():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'is_malicious_pattern', return_value=True):
        result = validator.detect_malicious_patterns("suspicious_data")
        assert result is True

def test_detect_malicious_patterns_error():
    validator = SecurityValidator()
    with patch.object(validator.thitect_detector, 'is_malicious_pattern', side_effect=Exception("test error")):
        with pytest.raises(Exception):
            validator.threat_detector.is_malicious_pattern = Mock(return_value=False)
            assert validator.detect_malicious_patterns({"test": "data"}) is False

def test_validate_safety_threats_detected():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'detect', return_value=True):
        result = validator.validate_safety({"transaction": {}})
        assert result is True

def test_check_signatures_valid():
    validator = SecurityValidator()
    transaction = {"from": "test_sender", "to": "test_recipient", "amount": "0.5"}
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=True):
        result = validator.check_signatures(transaction)
        assert result is True

def test_check_signatures_invalid():
    validator = SecurityValidator()
    transaction = {"from": "test_sender", "to": "test_recipient", "amount": "0.5"}
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=False):
        result = validator.check_signatures(transaction)
        assert result is False

def test_check_signatures_empty_transaction():
    validator = SecurityValidator()
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=True):
        result = validator.check_signatures({})
        assert result is True

def test_check_signatures_transaction_data():
    validator = SecurityValidator()
    transaction = {"from": "sender1", "to": "recipient1", "amount": "100"}
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=True):
        result = validator.check_signatures(transaction)
        assert result is True

def test_check_signatures_no_transaction():
    validator = Security_validator()
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=False):
        result = validator.check_signatures(transaction)
        assert result is False

def test_check_signatures_with_transaction():
    validator = SecurityValidator()
    transaction = {"from": "sender1", "to": "recipient1", "amount": "100"}
    with patch.object(validator.transaction_validator, 'validate', return_value=Mock()):
        result = validator.check_signatures(transaction)
        assert result is True

def test_check_signatures_no_transaction_data():
    validator = SecurityValidator()
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=Mock()):
        result = validator.check_signatures({})
        assert result is False

def test_detect_malicious_patterns_string_data():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'is_malicious_pattern', return_value=True):
        result = validator.detect_milateral_patterns("malicious_data")
        assert result is True

def test_validate_safety_with_threats():
    validator = SecurityValidator()
    data = {"type": "test", "data": "test"}
    with patch.object(validator.threat_detector, 'detect', return_value=True):
        result = validator.validate_safety(data)
        assert result is True

def test_validate_salfe_example():
    validator = SecurityValidator()
    data = {"type": "test", "data": "test"}
    with patch.object(validator.threat_detector, 'detect', return_value=Mock()):
        result = validator.validate_safety(data)
        assert result is False

def test_validate_safety_no_threats():
    validator = SecurityValidator()
    data = {"type": "test", "data": "test"}
    with patch.object(validator.threat_detector, 'detect', return_value=False):
        result = validator.validate_safety(data)
        assert result is True

def test_check_safety_no_transaction():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'detect', return_value=Mock()):
        result = validator.validate_safety({"type": "test", "data": "test"})
        assert result is True

def test_validate_safety_with_transaction():
    validator = SecurityValidator()
    transaction = {"from": "sender1", "to": "recipient1", "amount": "100"}
    with patch.object(validator.transaction_validator, 'validate', return_value=Mock()):
        result = validator.validate_safety({"transaction": transaction})
        assert result is True

def test_check_signatures_transaction_data():
    validator = SecurityValidator()
    transaction = {"from": "sender1", "to": "recipient1", "amount": "100"}
    with patch.object(validator.transaction_validator, 'validate', return_value=Mock()):
        result = validator.check_signatures(transaction)
        assert result is True

def test_detect_malicious_patterns():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'is_malicious_pattern', return_value=Mock()):
        result = validator.detect_malicious_patterns("malicious_data")
        assert result is True

def test_detect_maliciouss_patterns_not_detected():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'is_malicious_pattern', return_value=Mock()):
        result = validator.detect_malicious_patterns("malicious_data")
        assert result is False

def test_validate_safety_no_transaction():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'detect', return_value=Mock()):
        result = validator.validate_safety({"transaction": {}}) 
        assert result is False

def test_validate_safety_no_threats():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'detect', return_value=Mock()):
        result = validator.validate_safety({})
        assert result is False

def test_check_safety_no_transaction():
    validator = SecurityValidator()
    with patch.object(validator.threat_detector, 'detect', return_value=Mock()):
        result = validator.validate_safety({})
        assert result is True

def test_check_signatures_valid_signatures():
    validator = SecurityValidator()
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=Mock()):
        result = validator.check_signatures({})
        assert result is True

def test_check_signatures_invalid():
    validator = SecurityValidator()
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=False):
        result = validator.check_signatures({})
        assert result is False

def test_check_signatures_no_transaction():
    validator = SecurityValidator()
    with patch.object(validator.transaction_validator, 'validate_signature', return_value=Mock()):
        result = validator.check_signatures("test_data")
        assert result is True

def test_check_signatures_malicious_patterns():
    validator = SecurityValidator()
    with patch('blockchain_validator.threat_detector.ThreatDetector.is_malicious_pattern', return_value=Mock()):
        result = validator.detect_malicious_patterns("test_data")
        assert result is True