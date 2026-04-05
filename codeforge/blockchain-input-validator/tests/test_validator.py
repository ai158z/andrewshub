import pytest
from unittest.mock import Mock, patch, MagicMock
from blockchain_validator.validator import TransactionValidator
from typing import Dict, Any

@pytest.fixture
def validator():
    return TransactionValidator()

@pytest.fixture
def valid_ethereum_transaction():
    return {
        'type': 'ethereum',
        'data': {
            'from': '0x1234567890123456789012345678901234567890',
            'to': '0x0987654321098765432109876543210987654321',
            'value': '1000000000000000000',
            'gas': 21000,
            'gasPrice': '20000000000',
            'nonce': 0
        }
    }

def test_validate_with_invalid_type(validator):
    with pytest.raises(TypeError):
        validator.validate("not a dict")

def test_validate_missing_type_field(validator):
    with pytest.raises(ValueError):
        validator.validate({'data': {}})

def test_validate_missing_data_field(validator):
    with pytest.raises(ValueError):
        validator.validate({'type': 'ethereum'})

@patch('blockchain_validator.validator.EthereumFormat')
@patch('blockchain_validator.validator.SyntaxValidator')
def test_ethereum_format_validation_success(mock_syntax_validator, mock_ethereum_format, validator):
    mock_ethereum_format.return_value.validate_transaction.return_value = {'is_valid': True, 'errors': []}
    mock_syntax_validator.return_value.validate_structure.return_value = {'is_valid': True, 'errors': []}
    
    data = {'type': 'ethereum', 'data': {}}
    result = validator.validate_format(data)
    assert result['is_valid'] is True
    assert len(result['errors']) == 0

def test_validate_format_invalid_data(validator):
    data = {'type': 'invalid', 'data': {}}
    result = validator.validate_format(data)
    assert 'errors' in result

@patch('blockchain_validator.validator.SyntaxValidator')
def test_validate_format_syntax_error(mock_syntax_validator, validator):
    mock_syntax_validator.return_value.validate_structure.return_value = {
        'is_valid': False, 
        'errors': ['Syntax error']
    }
    data = {'type': 'ethereum', 'data': {}}
    result = validator.validate_format(data)
    assert result['is_valid'] is False
    assert 'Syntax error' in result['errors']

def test_validate_semantics(validator):
    with patch('blockchain_validator.validator.SemanticValidator') as mock_semantic:
        mock_semantic.return_value.validate_meaning.return_value = {
            'is_valid': False,
            'errors': ['Invalid semantic meaning']
        }
        data = {}
        result = validator.validate_semantics(data)
        assert result['is_valid'] is False

def test_validate_security(validator):
    with patch('blockchain_validator.validator.SecurityValidator') as mock_security:
        mock_security.return_value.validate_safety.return_value = {
            'is_valid': False,
            'errors': ['Security violation detected']
        }
        data = {}
        result = validator.validate_security(data)
        assert result['is_valid'] is False
        assert 'Security violation detected' in result['errors']

def test_detect_threats_malicious(validator):
    with patch('blockchain_validator.validator.ThreatDetector') as mock_threat:
        mock_threat.return_value.is_malicious_pattern.return_value = True
        mock_threat.return_value.is_suspicious_address.return_value = False
        data = {'data': {'from': '0x123'}}
        result = validator.detect_threats(data)
        assert result['is_malicious'] is True

def test_detect_threats_suspicious_address(validator):
    with patch('blockchain_validator.validator.ThreatDetector') as mock_threat:
        mock_threat.return_value.is_malicious_pattern.return_value = False
        mock_threat.return_value.is_suspicious_address.return_value = True
        data = {'data': {'from': '0x123'}}
        result = validator.detect_threats(data)
        assert result['is_suspicious'] is True

def test_detect_threats_neither_malicious_nor_suspicious(validator):
    with patch('blockchain_validator.validator.ThreatDetector') as mock_threat:
        mock_threat.return_value.is_malicious_pattern.return_value = False
        mock_threat.return_value.is_suspicious_address.return_value = False
        data = {'data': {'from': '0x123'}}
        result = validator.detect_threats(data)
        assert result['is_malicious'] is False
        assert result['is_suspicious'] is False

def test_run_validation_pipeline_format_error(validator):
    with patch.object(validator, 'validate_format') as mock_format:
        mock_format.return_value = {
            'is_valid': False,
            'errors': ['Format error']
        }
        data = {}
        result = validator.run_validation_pipeline(data)
        assert result['is_valid'] is False
        assert 'Format error' in result['errors']

def test_run_validation_pipeline_semantic_error(validator):
    with patch.object(validator, 'validate_format') as mock_format:
        mock_format.return_value = {'is_valid': True, 'errors': []}
        
        with patch.object(validator, 'validate_semantics') as mock_semantic:
            mock_semantic.return_value = {
                'is_valid': False,
                'errors': ['Semantic error']
            }
            data = {}
            result = validator.run_validation_pipeline(data)
            assert result['is_valid'] is False
            assert 'Semantic error' in result['errors']

def test_run_validation_pipeline_security_error(validator):
    with patch.object(validator, 'validate_format') as mock_format:
        mock_format.return_value = {'is_valid': True, 'errors': []}
        
        with patch.object(validator, 'validate_semantics') as mock_semantic:
            mock_semantic.return_value = {'is_valid': True, 'errors': []}
            
            with patch.object(validator, 'validate_security') as mock_security:
                mock_security.return_value = {
                    'is_valid': False,
                    'errors': ['Security error']
                }
                data = {}
                result = validator.run_validation_pipeline(data)
                assert result['is_valid'] is False
                assert 'Security error' in result['errors']

def test_run_validation_pipeline_threat_detected(validator):
    with patch.object(validator, 'validate_format') as mock_format:
        mock_format.return_value = {'is_valid': True, 'errors': []}
        
        with patch.object(validator, 'validate_semantics') as mock_semantic:
            mock_semantic.return_value = {'is_valid': True, 'errors': []}
            
            with patch.object(validator, 'validate_security') as mock_security:
                mock_security.return_value = {'is_valid': True, 'errors': []}
                
                with patch.object(validator, 'detect_threats') as mock_threat:
                    mock_threat.return_value = {
                        'is_malicious': True,
                        'is_suspicious': False,
                        'details': []
                    }
                    data = {}
                    result = validator.run_validation_pipeline(data)
                    assert result['is_valid'] is False
                    assert 'Threat detected in transaction' in result['errors']

def test_run_validation_pipeline_all_valid(validator):
    with patch.object(validator, 'validate_format') as mock_format:
        mock_format.return_value = {'is_valid': True, 'errors': []}
        
        with patch.object(validator, 'validate_semantics') as mock_semantic:
            mock_semantic.return_value = {'is_valid': True, 'errors': []}
            
            with patch.object(validator, 'validate_security') as mock_security:
                mock_security.return_value = {'is_valid': True, 'errors': []}
                
                with patch.object(validator, 'detect_threats') as mock_threat:
                    mock_threat.return_value = {
                        'is_malicious': False,
                        'is_suspicious': False,
                        'details': []
                    }
                    data = {}
                    result = validator.run_validation_pipeline(data)
                    assert result['is_valid'] is True

def test_verify_address_success(validator):
    with patch('blockchain_validator.validator.AddressVerifier') as mock_verifier:
        mock_verifier.return_value.verify.return_value = True
        result = validator.verify_address('0x123', 'ethereum')
        assert result is True

def test_verify_address_failure(validator):
    with patch('blockchain_validator.validator.AddressVerifier') as mock_verifier:
        mock_verifier.return_value.verify.return_value = False
        result = validator.verify_address('0x123', 'ethereum')
        assert result is False

def test_verify_address_exception(validator):
    with patch('blockchain_validator.validator.AddressVerifier') as mock_verifier:
        mock_verifier.return_value.verify.side_effect = Exception("Verification failed")
        result = validator.verify_address('0x123', 'ethereum')
        assert result is False

def test_validate_blockchain_input(validator):
    with patch('blockchain_validator.validator.BlockchainValidator') as mock_blockchain:
        mock_blockchain.return_value.validate.return_value = {'status': 'valid'}
        result = validator.validate_blockchain_input({})
        assert result['status'] == 'valid'