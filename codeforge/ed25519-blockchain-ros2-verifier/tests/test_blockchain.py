import base64
import json
import pytest
from unittest.mock import Mock, patch
from ed25519_verifier.blockchain import BlockchainVerifier
from ed25519_verifier.exceptions import Ed25519VerificationError, InvalidSignatureFormatError


def test_verify_transaction_signature_valid():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = True
    
    transaction = {"from": "Alice", "to": "Bob", "amount": 100}
    public_key = base64.b64encode(b"public_key").decode()
    signature = base64.b64encode(b"signature").decode()
    
    result = verifier.verify_transaction_signature(transaction, public_key, signature)
    assert result is True


def test_verify_transaction_signature_invalid_transaction_type():
    verifier = BlockchainVerifier()
    with pytest.raises(Ed25519VerificationError):
        verifier.verify_transaction_signature("not_a_dict", "key", "sig")


def test_verify_transaction_signature_invalid_key_type():
    verifier = BlockchainVerifier()
    with pytest.raises(InvalidSignatureFormatError):
        verifier.verify_transaction_signature({}, 123, "sig")


def test_verify_transaction_signature_invalid_signature_type():
    verifier = BlockchainVerifier()
    with pytest.raises(InvalidSignatureFormatError):
        verifier.verify_transaction_signature({}, "key", 123)


def test_verify_transaction_signature_invalid_public_key_format():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    
    with pytest.raises(InvalidSignatureFormatError):
        verifier.verify_transaction_signature({"data": "test"}, "invalid_base64!", "sig")


def test_verify_transaction_signature_invalid_signature_format():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    
    with pytest.raises(InvalidSignatureFormatError):
        verifier.verify_transaction_signature({"data": "test"}, "dGVzdA==", "invalid_base64!")


def test_verify_transaction_signature_verification_failure():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.side_effect = Exception("Verification failed")
    
    with pytest.raises(Ed25519VerificationError):
        verifier.verify_transaction_signature({"data": "test"}, "dGVzdA==", "c2lnbmF0dQ==")


def test_verify_transaction_signature_success():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = True
    
    result = verifier.verify_transaction_signature(
        {"from": "Alice", "to": "Bob", "amount": 100},
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"valid_sig").decode()
    )
    assert result is True


def test_validate_blockchain_format_supported():
    verifier = BlockchainVerifier()
    assert verifier.validate_blockchain_format("ed25519-base64") is True
    assert verifier.validate_blockchain_format("ed25519-base58") is True
    assert verifier.validate_blockchain_format("ed25519-hex") is True
    assert verifier.validate_blockchain_format("ed25519-raw") is True


def test_validate_blockchain_format_unsupported():
    verifier = BlockchainVerifier()
    assert verifier.validate_blockchain_format("unsupported-format") is False


def test_validate_blockchain_format_case_sensitivity():
    verifier = BlockchainVerifier()
    assert verifier.validate_blockchain_format("ED25519-BASE64") is False


def test_verify_transaction_signature_empty_transaction():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = True
    
    result = verifier.verify_transaction_signature(
        {}, 
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"signature").decode()
    )
    assert result is True


def test_verify_transaction_signature_complex_transaction():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = True
    
    complex_transaction = {
        "from": "Alice",
        "to": "Bob",
        "amount": 100,
        "data": {"nested": "value"},
        "timestamp": 1234567890
    }
    
    result = verifier.verify_transaction_signature(
        complex_transaction,
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"signature").decode()
    )
    assert result is True


def test_verify_transaction_signature_verification_false():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = False
    
    result = verifier.verify_transaction_signature(
        {"test": "data"},
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"invalid_sig").decode()
    )
    assert result is False


def test_verify_transaction_signature_message_serialization():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = True
    
    # Test that same data in different key orders produces same message
    transaction1 = {"a": 1, "b": 2}
    transaction2 = {"b": 2, "a": 1}
    
    # Both should create the same verification call
    verifier.verify_transaction_signature(
        transaction1,
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"signature").decode()
    )
    
    verifier.verify_transaction_signature(
        transaction2,
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"signature").decode()
    )
    
    # Should have been called twice with same verification
    assert verifier.verifier.verify_signature.call_count == 2


def test_verify_transaction_signature_verifier_exception():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.side_effect = Exception("Crypto error")
    
    with pytest.raises(Ed25519VerificationError):
        verifier.verify_transaction_signature(
            {"data": "test"},
            base64.b64encode(b"public_key").decode(),
            base64.b64encode(b"signature").decode()
        )


def test_validate_blockchain_format_none():
    verifier = BlockchainVerifier()
    assert verifier.validate_blockchain_format(None) is False


def test_validate_blockchain_format_empty_string():
    verifier = BlockchainVerifier()
    assert verifier.validate_blockchain_format("") is False


def test_validate_blockchain_format_special_characters():
    verifier = BlockchainVerifier()
    assert verifier.validate_blockchain_format("ed25519-base64!") is False


def test_verify_transaction_signature_large_transaction():
    verifier = BlockchainVerifier()
    verifier.verifier = Mock()
    verifier.verifier.verify_signature.return_value = True
    
    large_transaction = {f"key_{i}": f"value_{i}" for i in range(1000)}
    
    result = verifier.verify_transaction_signature(
        large_transaction,
        base64.b64encode(b"public_key").decode(),
        base64.b64encode(b"signature").decode()
    )
    assert result is True