import pytest
from unittest.mock import patch, MagicMock
from ed22519_verifier.core import Ed25519Verifier
from cryptography.exceptions import InvalidSignature

@pytest.fixture
def verifier():
    return Ed25519Verifier()

@pytest.fixture
def valid_public_key():
    return b"public_key_bytes"

@pytest.fixture
def valid_message():
    return b"test message"

@pytest.fixture
def valid_signature():
    return b"signature_bytes_64_length" * 4  # 64 bytes

def test_verify_signature_valid(verifier, valid_public_key, valid_message, valid_signature):
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.return_value = None  # No exception means success
        result = verifier.verify_signature(valid_public_key, valid_message, valid_signature)
        assert result is True

def test_verify_signature_invalid_public_key_type(verifier, valid_message, valid_signature):
    with pytest.raises(ValueError, match="Invalid public key provided"):
        verifier.verify_signature("not_bytes", valid_message, valid_signature)

def test_verify_signature_empty_public_key(verifier, valid_message, valid_signature):
    with pytest.raises(ValueError, match="Invalid public key provided"):
        verifier.verify_signature(b"", valid_message, valid_signature)

def test_verify_signature_invalid_message_type(verifier, valid_public_key, valid_signature):
    with pytest.raises(ValueError, match="Invalid message provided"):
        verifier.verify_signature(valid_public_key, "not_bytes", valid_signature)

def test_verify_signature_empty_message(verifier, valid_public_key, valid_signature):
    with pytest.raises(ValueError, match="Invalid message provided"):
        verifier.verify_signature(valid_public_key, b"", valid_signature)

def test_verify_signature_invalid_signature_type(verifier, valid_public_key, valid_message):
    with pytest.raises(ValueError, match="Invalid signature provided - must be 64 bytes"):
        verifier.verify_signature(valid_public_key, valid_message, "not_bytes")

def test_verify_signature_invalid_signature_length(verifier, valid_public_key, valid_message):
    with pytest.raises(ValueError, match="Invalid signature provided - must be 64 bytes"):
        verifier.verify_signature(valid_public_key, valid_message, b"short")

def test_verify_signature_invalid_signature_value(verifier, valid_public_key, valid_message):
    with patch("ed225519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.side_effect = InvalidSignature("Invalid signature")
        result = verifier.verify_signature(valid_public_key, valid_message, b"invalid_signature_32_bytes_long!")
        assert result is False

def test_verify_signature_invalid_key_format(verifier, valid_message, valid_signature):
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes", side_effect=ValueError("Invalid key format")):
        result = verifier.verify_signature(b"invalid_key", valid_message, valid_signature)
        assert result is False

def test_batch_verify_success(verifier, valid_public_key, valid_message, valid_signature):
    signatures = [(valid_public_key, valid_message, valid_signature)]
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.return_value = None
        results = verifier.batch_verify(signatures)
        assert results == [True]

def test_batch_verify_invalid_input_type(verifier):
    with pytest.raises(ValueError, match="Signatures must be provided as a list of tuples"):
        verifier.batch_verify("not_a_list")

def test_batch_verify_invalid_tuple_format(verifier):
    invalid_signatures = [("too", "few")]
    results = verifier.batch_verify(invalid_signatures)
    assert results == [False]

def test_batch_verify_invalid_types_in_tuple(verifier):
    invalid_signatures = [("key", "msg", "sig")]  # Strings instead of bytes
    results = verifier.batch_verify(invalid_signatures)
    assert results == [False]

def test_batch_verify_mixed_valid_invalid_tuples(verifier, valid_public_key, valid_message, valid_signature):
    invalid_item = ("key", "msg", "sig")
    valid_item = (valid_public_key, valid_message, valid_signature)
    signatures = [invalid_item, valid_item]
    
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.return_value = None
        results = verifier.batch_verify(signatures)
        assert results == [False, True]

def test_batch_verify_multiple_invalid_signatures(verifier):
    # Test with multiple invalid signatures
    results = verifier.batch_verify([("k", "m", "s")] * 3)
    assert results == [False, False, False]

def test_batch_verify_empty_list(verifier):
    results = verifier.batch_verify([])
    assert results == []

def test_verify_signature_exception_handling(verifier, valid_public_key, valid_message, valid_signature):
    with patch("ed225519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.side_effect = Exception("Test exception")
        result = verifier.verify_signature(valid_public_key, valid_message, valid_signature)
        assert result is False

def test_verify_signature_logging_success(mocker, verifier, valid_public_key, valid_message, valid_signature):
    mock_logger = mocker.patch("ed22519_verifier.core.logger")
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.return_value = None
        verifier.verify_signature(valid_public_key, valid_message, valid_signature)
        mock_logger.debug.assert_called_with("Signature verification successful")

def test_verify_signature_logging_failure(mocker, verifier, valid_public_key, valid_message, valid_signature):
    mock_logger = mocker.patch("ed22519_verifier.core.logger")
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.side_effect = InvalidSignature("Invalid signature")
        verifier.verify_signature(valid_public_key, valid_message, valid_signature)
        mock_logger.debug.assert_called_with("Signature verification failed: Invalid signature", exc_info=True)

def test_batch_verify_mixed_results(verifier, valid_public_key, valid_message, valid_signature):
    # One valid, one invalid
    invalid_signature = b"invalid_signature_32_bytes_long!"  # 32 bytes, not 64
    signatures = [
        (valid_public_key, valid_message, valid_signature),  # Valid
        (valid_public_key, valid_message, invalid_signature)  # Invalid length
    ]
    with patch("ed22519_verifier.core.Ed25519PublicKey.from_public_bytes") as mock_key:
        mock_key_instance = mock_key.return_value
        mock_key_instance.verify.return_value = None
        results = verifier.batch_verify(signatures)
        assert results == [True, False]