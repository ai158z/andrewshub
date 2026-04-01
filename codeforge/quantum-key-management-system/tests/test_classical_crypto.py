import pytest
from unittest.mock import Mock, patch, MagicMock
from src.fallback.classical_crypto import ClassicalCryptoFallback
import os
import sys

# Add src to path for imports
sys.path.insert(0, 'src')

@pytest.fixture
def crypto_fallback():
    """Fixture to create ClassicalCryptoFallback instance with mocked dependencies"""
    with patch.multiple('src.fallback.classical_crypto', 
                      KeyDistributor=Mock(),
                      QKDProtocol=Mock(),
                      KeyStorage=Mock(),
                      EdgeNodeAuthenticator=Mock(),
                      CertificateManager=Mock(),
                      CodonicEncoder=Mock(),
                      SymbolicEncoder=Mock(),
                      BackupChannel=Mock(),
                      PerformanceTracker=Mock(),
                      LatencyMetrics=Mock()):
        return ClassicalCryptoFallback()

def test_initialization_with_default_key_size():
    """Test that ClassicalCryptoFallback initializes with default key size"""
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 32
        fallback = ClassicalCryptoFallback()
        assert fallback.key_size == 256
        mock_gen.assert_called_with(32)

def test_initialization_with_custom_key_size():
    """Test that ClassicalCryptoFallback initializes with custom key size"""
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 16
        fallback = ClassicalCryptoFallback(key_size=128)
        assert fallback.key_size == 128
        mock_gen.assert_called_with(16)

def test_cipher_initialization_failure():
    """Test that initialization fails when cipher key generation fails"""
    with patch('src.fallback.classical_crypto.generate_random_bytes', side_effect=Exception("Key generation failed")):
        with pytest.raises(Exception, match="Key generation failed"):
            ClassicalCryptoFallback()

def test_encrypt_success():
    """Test successful encryption"""
    fallback = ClassicalCryptoFallback()
    fallback.cipher_key = b'test_key_1234567890123456789012'
    
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 16
        result = fallback.encrypt(b"test data")
        assert result is not None
        assert isinstance(result, bytes)

def test_encrypt_with_empty_data():
    """Test encryption with empty data"""
    fallback = ClassicalCryptoFallback()
    fallback.cipher_key = b'test_key_1234567890123456789012'
    
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 16
        result = fallback.encrypt(b"")
        assert result is not None

def test_encrypt_with_none_data():
    """Test encryption with None data should raise exception"""
    fallback = ClassicalCryptoFallback()
    fallback.cipher_key = b'test_key_1234567890123456789012'
    
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 16
        with pytest.raises(Exception):
            fallback.encrypt(None)

def test_decrypt_success():
    """Test successful decryption"""
    fallback = ClassicalCryptoFallback()
    fallback.cipher_key = b'test_key_1234567890123456789012'
    
    # Mock the decryption process
    with patch('src.fallback.classical_crypto.Cipher') as mock_cipher:
        mock_cipher_instance = Mock()
        mock_cipher.return_value = mock_cipher_instance
        mock_cipher_instance.decryptor.return_value = Mock()
        
        result = fallback.decrypt(b"test", b"iv")
        assert result is not None

def test_decrypt_with_empty_data():
    """Test decryption with empty data"""
    fallback = ClassicalCryptoFallback()
    fallback.cipher_key = b'test_key_1234567890123456789012'
    
    with patch('src.fallback.classical_crypto.Cipher') as mock_cipher:
        mock_cipher_instance = Mock()
        mock_cipher.return_value = mock_cipher_instance
        mock_cipher_instance.decryptor.return_value = Mock()
        
        result = fallback.decrypt(b"", b"iv")
        assert result is not None

def test_authenticate_and_authorize_success():
    """Test successful node authentication and authorization"""
    fallback = ClassicalCryptoFallback()
    fallback.authenticator.authenticate_node.return_value = True
    fallback.certificate_manager.validate_certificate.return_value = True
    
    result = fallback._authenticate_and_authorize("node1", {"cred": "test"})
    assert result is True

def test_authenticate_and_authorize_node_auth_failure():
    """Test authentication failure when node authentication fails"""
    fallback = ClassicalCryptoFallback()
    fallback.authenticator.authenticate_node.return_value = False
    fallback.certificate_manager.validate_certificate.return_value = True
    
    result = fallback._authenticate_and_authorize("node1", {"cred": "test"})
    assert result is False

def test_authenticate_and_authorize_cert_validation_failure():
    """Test authentication failure when certificate validation fails"""
    fallback = ClassicalCryptoFallback()
    fallback.authenticator.authenticate_node.return_value = True
    fallback.certificate_manager.validate_certificate.return_value = False
    
    result = fallback._authenticate_and_authorize("node1", {"cred": "test"})
    assert result is False

def test_authenticate_and_authorize_exception_handling():
    """Test authentication handles exceptions gracefully"""
    fallback = ClassicalCryptoFallback()
    fallback.authenticator.authenticate_node.side_effect = Exception("Auth failed")
    
    result = fallback._authenticate_and_authorize("node1", {"cred": "test"})
    assert result is False

def test_encode_data_codonic_success():
    """Test successful codonic encoding"""
    fallback = ClassicalCryptoFallback()
    fallback.codonic_encoder.encode_symbolic.return_value = b"encoded"
    
    result = fallback._encode_data(b"test", "codonic")
    assert result == b"encoded"

def test_encode_data_symbolic_success():
    """Test successful symbolic encoding"""
    fallback = ClassicalCryptoFallback()
    fallback.symbolic_encoder.encode.return_value = b"encoded"
    
    result = fallback._encode_data(b"test", "symbolic")
    assert result == b"encoded"

def test_encode_data_exception():
    """Test encoding handles exceptions"""
    fallback = ClassicalCryptoFallback()
    fallback.codonic_encoder.encode_symbolic.side_effect = Exception("Encoding failed")
    
    with pytest.raises(Exception, match="Encoding failed"):
        fallback._encode_data(b"test", "codonic")

def test_decode_data_codonic_success():
    """Test successful codonic decoding"""
    fallback = ClassicalCryptoFallback()
    fallback.codonic_encoder.decode_symbolic.return_value = b"decoded"
    
    result = fallback._decode_data(b"test", "codonic")
    assert result == b"decoded"

def test_decode_data_symbolic_success():
    """Test successful symbolic decoding"""
    fallback = ClassicalCryptoFallback()
    fallback.symbolic_encoder.decode.return_value = b"decoded"
    
    result = fallback._decode_data(b"test", "symbolic")
    assert result == b"decoded"

def test_decode_data_exception():
    """Test decoding handles exceptions"""
    fallback = ClassicalCryptoFallback()
    fallback.codonic_encoder.decode_symbolic.side_effect = Exception("Decoding failed")
    
    with pytest.raises(Exception, match="Decoding failed"):
        fallback._decode_data(b"test", "codonic")

def test_generate_fallback_key_success():
    """Test successful fallback key generation"""
    fallback = ClassicalCryptoFallback()
    fallback.key_storage.store_key.return_value = None
    
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 32
        result = fallback._generate_fallback_key(32)
        assert result == b'x' * 32

def test_generate_fallback_key_exception():
    """Test key generation handles exceptions"""
    fallback = ClassicalCryptoFallback()
    fallback.key_storage.store_key.side_effect = Exception("Storage failed")
    
    with patch('src.fallback.classical_crypto.generate_random_bytes') as mock_gen:
        mock_gen.return_value = b'x' * 32
        with pytest.raises(Exception, match="Storage failed"):
            fallback._generate_fallback_key(32)

def test_distribute_key_classically_success():
    """Test successful key distribution"""
    fallback = ClassicalCryptoFallback()
    fallback.key_distributor.distribute_key.return_value = True
    fallback.key_distributor.verify_key_integrity.return_value = True
    
    result = fallback._distribute_key_classically(b"key_data", "recipient1")
    assert result is True

def test_distribute_key_classically_failure():
    """Test key distribution failure"""
    fallback = ClassicalCryptoFallback()
    fallback.key_distributor.distribute_key.return_value = False
    
    result = fallback._distribute_key_classically(b"key_data", "recipient1")
    assert result is False

def test_distribute_key_classically_integrity_failure():
    """Test key distribution with integrity check failure"""
    fallback = ClassicalCryptoFallback()
    fallback.key_distributor.distribute_key.return_value = True
    fallback.key_distributor.verify_key_integrity.return_value = False
    
    result = fallback._distribute_key_classically(b"key_data", "recipient1")
    assert result is False