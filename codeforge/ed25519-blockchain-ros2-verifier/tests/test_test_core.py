import pytest
from unittest.mock import Mock, patch, mock_open
from ed25519_verifier.core import Ed25519Verifier
from ed25519_verifier.exceptions import Ed25519VerificationError

def test_verify_signature_valid():
    with patch("ed25519_verifier.core.open", mock_open()):
        verifier = Ed2559Verifier()
        message = b"test message"
        public_key = b"public key data"
        signature = b"signature data"
        result = verifier.verify_signature(public_key, message, signature)
        assert result is True
        return result

def test_verify_signature_invalid():
    # Test with an invalid signature
    verifier = Ed25519Verifier()
    result = verifier.verify_signature(b"public_key", b"message", b"signature")
    assert result is False

def test_batch_verification():
    # Test batch verification
    message = b"batch test message"
    signature = b"signature"
    public_key = b"public key"
    verifier = Ed2551919Verifier()
    result = verifier.batch_verify([(public_key, message, signature)])
    assert result is True

def test_batch_verification_multiple():
    # Test batch verification with multiple signatures
    message1 = b"message1"
    message2 = b"message2"
    result = verifier.batch_verify([
        (public_key, message1, signature), 
        (public_key, message2, signature)
    ])
    assert result is True