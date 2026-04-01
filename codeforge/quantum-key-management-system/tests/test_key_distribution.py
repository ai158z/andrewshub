import pytest
from unittest.mock import Mock, patch, MagicMock
from src.qkd.key_distribution import KeyDistributor, KeyDistributionResult
from src.core.key_storage import KeyStorage

@pytest.fixture
def key_distributor():
    kd = KeyDistributor()
    kd.key_storage = KeyStorage()
    return kd

@pytest.fixture
def mock_dependencies(mocker):
    # Mock all external dependencies
    mocks = {}
    mock_names = [
        'src.qkd.protocol.QKDProtocol',
        'src.qkd.quantum_channels.QuantumChannel',
        'src.auth.edge_node_auth.EdgeNodeAuthenticator',
        'src.auth.certificate_manager.CertificateManager',
        'src.encoding.codonic_layer.CodonicEncoder',
        'src.encoding.symbolic_encoder.SymbolicEncoder',
        'src.fallback.classical_crypto.ClassicalCryptoFallback',
        'src.fallback.backup_channels.BackupChannel',
        'src.core.key_storage.KeyStorage'
    ]
    
    for mock_name in mock_names:
        mocks[mock_name] = mocker.patch(mock_name, autospec=True)
    
    return mocks

def test_distribute_key_success(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True), \
         patch.object(key_distributor.protocol, 'generate_keys', return_value=b'fake_key_data'), \
         patch.object(key_distributor.symbolic_encoder, 'encode', return_value=b'encoded_key'), \
         patch('src.qkd.key_distribution.hash_key', return_value=b'hash'), \
         patch.object(key_distributor.quantum_channel, 'transmit', return_value=True):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is True
        assert result.key_id is not None

def test_distribute_key_auth_failure_source(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=False), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Source node authentication failed" in result.error_message

def test_distribute_key_auth_failure_target(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', 
                     side_effect=[True, False]), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Target node authentication failed" in result.error_message

def test_distribute_key_cert_validation_failure_source(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', 
                     side_effect=[False, True]):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Invalid source node certificate" in result.error_message

def test_distribute_key_cert_validation_failure_target(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate',
                     side_effect=[True, False]):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Invalid target node certificate" in result.error_message

def test_distribute_key_key_generation_failure(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True), \
         patch.object(key_distributor.protocol, 'generate_keys', return_value=None):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Key generation failed" in result.error_message

def test_distribute_key_encoding_failure(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True), \
         patch.object(key_distributor.protocol, 'generate_keys', return_value=b'key'), \
         patch.object(key_distributor.symbolic_encoder, 'encode', return_value=None):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Key encoding failed" in result.error_message

def test_distribute_key_transmission_failure(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True), \
         patch.object(key_distributor.protocol, 'generate_keys', return_value=b'key'), \
         patch.object(key_distributor.quantum_channel, 'transmit', return_value=False):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Quantum channel transmission failed" in result.error_message

def test_verify_key_integrity_valid(key_distributor):
    with patch.object(key_distributor.key_storage, 'retrieve_key', return_value=b'key'), \
         patch.object(key_distributor.protocol, 'validate_protocol', return_value=True):
        assert key_distributor.verify_key_integrity("key123", b'key') is True

def test_verify_key_integrity_invalid_hash(key_distributor):
    with patch.object(key_distributor.key_storage, 'retrieve_key', return_value=b'key'), \
         patch.object(key_distributor.protocol, 'validate_protocol', return_value=True):
        # Test with different key data to trigger hash mismatch
        result = key_distributor.verify_key_integrity("key123", b'different_key')
        assert result is False

def test_verify_key_integrity_protocol_invalid(key_distributor):
    with patch.object(key_distributor.key_storage, 'retrieve_key', return_value=b'key'), \
         patch.object(key_distributor.protocol, 'validate_protocol', return_value=False):
        result = key_distributor.verify_key_integrity("key123", b'key')
        assert result is False

def test_distribute_key_happy_path(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', return_value=True), \
         patch.object(key_distributor.certificate_manager, 'validate_certificate', return_value=True), \
         patch.object(key_distributor.protocol, 'generate_keys', return_value=b'key'), \
         patch.object(key_distributor.symbolic_encoder, 'encode', return_value=b'key'), \
         patch.object(key_distributor.quantum_channel, 'transmit', return_value=True):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is True

def test_distribute_key_with_exception_during_execution(key_distributor):
    with patch.object(key_distributor.authenticator, 'authenticate_node', 
                     side_effect=Exception("Network error")):
        result = key_distributor.distribute_key("node1", "node2", {"cred": "value"})
        assert result.success is False
        assert "Network error" in result.error_message

def test_key_distribution_result_structure():
    result = KeyDistributionResult(success=True, key_id="test", error_message=None)
    assert result.success is True
    assert result.key_id == "test"
    assert result.error_message is None

def test_transmit_key_data_success(key_distributor):
    with patch.object(key_distributor.codonic_encoder, 'encode_symbolic', return_value=b'encoded'), \
         patch.object(key_distributor.codonic_encoder, 'decode_symbolic', return_value=b'key'), \
         patch.object(key_distributor.quantum_channel, 'transmit', return_value=True), \
         patch.object(key_distributor, 'verify_key_integrity', return_value=True):
        success = key_distributor._transmit_key_data("node1", "node2", b'key')
        assert success is True

def test_transmit_key_data_encoding_failure(key_distributor):
    with patch.object(key_distributor.codonic_encoder, 'encode_symbolic', 
                     side_effect=Exception("Encoding failed")):
        success = key_distributor._transmit_key_data("node1", "node2", b'key')
        assert success is False

def test_transmit_key_data_transmission_failure(key_distributor):
    with patch.object(key_distributor.codonic_encoder, 'encode_symbolic', return_value=b'encoded'), \
         patch.object(key_distributor.quantum_channel, 'transmit', return_value=False), \
         patch.object(key_distributor, 'verify_key_integrity', return_value=False):
        success = key_distributor._transmit_key_data("node1", "node2", b'key')
        assert success is False

def test_transmit_key_data_integrity_failure(key_distributor):
    with patch.object(key_distributor.codonic_encoder, 'encode_symbolic', return_value=b'encoded'), \
         patch.object(key_distributor.quantum_channel, 'transmit', return_value=True), \
         patch.object(key_distributor.codonic_encoder, 'decode_symbolic', return_value=b'key'), \
         patch.object(key_distributor, 'verify_key_integrity', return_value=False):
        success = key_distributor._transmit_key_data("node1", "node2", b'key')
        assert success is False

def test_transmit_key_data_exception_handling(key_distributor):
    with patch.object(key_distributor.codonic_encoder, 'encode_symbolic', 
                     side_effect=Exception("Transmission error")):
        success = key_distributor._transmit_key_data("node1", "node2", b'key')
        assert success is False

def test_distribute_key_latency_measurement(key_distributor):
    # Test that we can measure and return latency in results
    result = KeyDistributionResult(success=True, key_id="123", latency=0.5)
    assert result.latency == 0.5