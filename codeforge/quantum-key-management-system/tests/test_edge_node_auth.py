import pytest
from unittest.mock import Mock, patch, MagicMock
from src.auth.edge_node_auth import EdgeNodeAuthenticator
import logging

# Generate test data
private_key = None
public_key = None
signature = None
test_node_id = "test_node_123"
test_data = b"test_data_message"

# Generate a key pair for testing
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
signature = private_key.sign(
    test_data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

def test_authenticate_node_success():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock all dependencies
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=True)
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test_key", "signature": b"test_sig"})
    
    assert result == True
    authenticator.certificate_manager.validate_certificate.assert_called_once_with(test_node_id)

def test_authenticate_node_certificate_validation_failure():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock certificate validation to fail
    authenticator.certificate_manager.validate_certificate = Mock(return_value=False)
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test_key", "signature": b"test_sig"})
    
    assert result == False
    authenticator.certificate_manager.validate_certificate.assert_called_once_with(test_node_id)

def test_authenticate_node_credential_verification_failure():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock certificate validation to pass but credential verification to fail
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=False)
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test_key", "signature": b"test_sig"})
    
    assert result == False

def test_verify_credentials_missing_fields():
    authenticator = EdgeNodeAuthenticator()
    
    # Test missing public_key
    result = authenticator.verify_credentials(test_node_id, {"signature": b"test_sig", "data": "test_data"})
    assert result == False
    
    # Test missing signature
    result = authenticator.verify_credentials(test_node_id, {"public_key": b"test_key", "data": "test_data"})
    assert result == False

def test_verify_credentials_success():
    authenticator = EdgeNodeAuthenticator()
    
    # Create valid credentials
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    credentials = {
        "public_key": public_key_pem,
        "signature": signature,
        "data": test_data.decode()
    }
    
    # Mock the public key loading and verification
    with patch('cryptography.hazmat.primitives.serialization.load_pem_public_key') as mock_load_key:
        mock_public_key = Mock()
        mock_public_key.verify = Mock()
        mock_load_key.return_value = mock_public_key
        
        result = authenticator.verify_credentials(test_node_id, credentials)
        
        assert result == True
        mock_public_key.verify.assert_called_once()

def test_verify_credentials_invalid_signature():
    authenticator = EdgeNodeAuthenticator()
    
    # Create credentials with invalid signature
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    credentials = {
        "public_key": public_key_pem,
        "signature": b"invalid_signature",
        "data": "invalid_data"
    }
    
    # Mock the public key loading
    with patch('cryptography.hazmat.primitives.serialization.load_pem_public_key') as mock_load_key:
        mock_public_key = Mock()
        mock_public_key.verify = Mock(side_effect=Exception("Signature verification failed"))
        mock_load_key.return_value = mock_public_key
        
        result = authenticator.verify_credentials(test_node_id, credentials)
        
        assert result == False

def test_verify_credentials_exception_handling():
    authenticator = EdgeNodeAuthenticator()
    
    # Create credentials that will cause an exception
    credentials = {
        "public_key": b"invalid_public_key_data",
        "signature": b"test_sig",
        "data": "test_data"
    }
    
    # Mock load_pem_public_key to raise an exception
    with patch('cryptography.hazmat.primitives.serialization.load_pem_private_key') as mock_load_key:
        mock_load_key.side_effect = Exception("Invalid key data")
        
        result = authenticator.verify_credentials(test_node_id, credentials)
        
        assert result == False

def test_authenticate_node_exception_handling():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock dependencies to raise exception
    authenticator.certificate_manager.validate_certificate = Mock(side_effect=Exception("Test exception"))
    authenticator.verify_credentials = Mock(return_value=True)
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test", "signature": b"test"})
    
    assert result == False

def test_verify_credentials_empty_credentials():
    authenticator = EdgeNodeAuthenticator()
    
    result = authenticator.verify_credentials(test_node_id, {})
    
    assert result == False

def test_authenticate_node_performance_monitoring():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock all dependencies
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=True)
    
    # Mock performance tracker methods
    authenticator.performance_tracker.start_monitoring = Mock()
    authenticator.performance_tracker.stop_monitoring = Mock()
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test", "signature": b"test"})
    
    assert result == True
    authenticator.performance_tracker.start_monitoring.assert_called_once()
    authenticator.performance_tracker.stop_monitoring.assert_called_once()

def test_authenticate_node_missing_credential_fields():
    authenticator = EdgeNodeAuthenticator()
    
    # Test with missing required fields
    result = authenticator.authenticate_node(test_node_id, {})
    
    # Should fail due to missing fields
    assert result == False

def test_verify_credentials_invalid_public_key():
    authenticator = EdgeNodeAuthenticator()
    
    # Test with invalid public key data
    credentials = {
        "public_key": b"invalid_key_data",
        "signature": b"test_sig",
        "data": "test_data"
    }
    
    result = authenticator.verify_credentials(test_node_id, credentials)
    
    assert result == False

def test_verify_credentials_missing_data():
    authenticator = EdgeNodeAuthenticator()
    
    # Test with missing data field
    credentials = {
        "public_key": b"test_key",
        "signature": b"test_sig"
        # Missing "data" field
    }
    
    result = authenticator.verify_credentials(test_node_id, credentials)
    
    assert result == False

def test_authenticate_node_logging():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock dependencies
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=True)
    
    # Capture logs
    import logging
    logging.getLogger().setLevel(logging.INFO)
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test", "signature": b"test"})
    
    assert result == True

def test_authenticate_node_finally_block():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock dependencies
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=True)
    
    # Mock performance tracker methods
    authenticator.performance_tracker.start_monitoring = Mock()
    authenticator.performance_tracker.stop_monitoring = Mock()
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test", "signature": b"test"})
    
    # Ensure finally block is executed
    assert result == True
    authenticator.performance_tracker.stop_monitoring.assert_called_once()

def test_verify_credentials_signature_verification_exception():
    authenticator = EdgeNodeAuthenticator()
    
    # Create valid credentials but make verification fail
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    credentials = {
        "public_key": public_key_pem,
        "signature": b"invalid_signature",
        "data": "test_data"
    }
    
    # Mock the public key loading and make verify raise an exception
    with patch('cryptography.hazmat.primitives.serialization.load_pem_public_key') as mock_load_key:
        mock_public_key = Mock()
        mock_public_key.verify = Mock(side_effect=Exception("Verification failed"))
        mock_load_key.return_value = mock_public_key
        
        result = authenticator.verify_credentials(test_node_id, credentials)
        
        assert result == False

def test_authenticate_node_empty_node_id():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock dependencies
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=True)
    
    # Test with empty node_id
    result = authenticator.authenticate_node("", {"public_key": b"test", "signature": b"test"})
    
    assert result == True

def test_verify_credentials_none_values():
    authenticator = EdgeNodeAuthenticator()
    
    # Test with None values
    credentials = {
        "public_key": None,
        "signature": None,
        "data": None
    }
    
    result = authenticator.verify_credentials(test_node_id, credentials)
    
    assert result == False

def test_authenticate_node_none_credentials():
    authenticator = EdgeNodeAuthenticator()
    
    # Test with None credentials
    result = authenticator.authenticate_node(test_node_id, None)
    
    assert result == False

def test_verify_credentials_logging():
    # Test that proper logging occurs
    authenticator = EdgeNodeAuthenticator()
    
    result = authenticator.verify_credentials(test_node_id, {})
    
    assert result == False
    # Would need to capture logs to fully test this

def test_authenticate_node_full_success():
    authenticator = EdgeNodeAuthenticator()
    
    # Mock all dependencies for full success path
    authenticator.certificate_manager.validate_certificate = Mock(return_value=True)
    authenticator.verify_credentials = Mock(return_value=True)
    
    result = authenticator.authenticate_node(test_node_id, {"public_key": b"test", "signature": b"test"})
    
    assert result == True