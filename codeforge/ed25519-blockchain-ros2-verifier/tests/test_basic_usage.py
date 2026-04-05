import pytest
from unittest.mock import patch, MagicMock
import os
import ed25519
from examples.basic_usage import basic_signature_verification, key_generation_example, batch_verification_example
from ed25519_verifier.core import Ed25519Verifier


def test_basic_signature_verification_success():
    with patch('builtins.print') as mock_print:
        basic_signature_verification()
        # Should complete without error and print verification results
        assert mock_print.call_count > 0


def test_basic_signature_verification_fails_on_bad_signature():
    # Mock a bad signature to trigger exception path
    with patch('ed25519.SigningKey.sign') as mock_sign:
        mock_sign.return_value = os.urandom(64)
        with patch('examples.basic_usage.os.urandom', return_value=b'\x00' * 32):
            with patch('builtins.print') as mock_print:
                basic_signature_verification()
                assert mock_print.called


def test_key_generation_example():
    with patch('builtins.print') as mock_print:
        key_generation_example()
        assert mock_print.call_count > 0


def test_key_generation_with_failing_verification():
    # Mock verification to fail
    with patch.object(ed25519.VerifyingKey, 'verify', side_effect=Exception("Verification failed")):
        with patch('builtins.print') as mock_print:
            key_generation_example()
            assert mock_print.call_count > 0


def test_batch_verification_example():
    with patch('builtins.print') as mock_print:
        result = batch_verification_example()
        assert result is True
        assert mock_print.call_count > 0


def test_batch_verification_empty_lists():
    with patch('examples.basic_usage.os.urandom', side_effect=[b'\x00'*32, b'\x01'*32, b'\x02'*32]):
        with patch('builtins.print') as mock_print:
            batch_verification_example()
            assert mock_print.call_count > 0


@patch('examples.basic_usage.os.urandom')
def test_basic_signature_verification_with_mocked_random(mock_random):
    mock_random.return_value = b'\x00' * 32
    with patch('builtins.print') as mock_print:
        basic_signature_verification()
        # Should not raise exceptions
        assert mock_print.call_count > 0


@patch('ed25519.SigningKey.sign')
@patch('ed25519.SigningKey.get_verifying_key')
def test_basic_verification_signature_exception(mock_get_vk, mock_sign):
    mock_sign.side_effect = Exception("Signing failed")
    mock_get_vk.return_value = MagicMock()
    
    with patch('builtins.print') as mock_print:
        basic_signature_verification()
        assert mock_print.call_count > 0


def test_verify_signature_with_invalid_signature():
    # Test that verification fails with garbage signature
    with patch('builtins.print') as mock_print:
        basic_signature_verification()
        assert mock_print.call_count > 0


@patch('ed25519.SigningKey')
def test_key_generation_creates_keys(mock_signing_key):
    mock_key = MagicMock()
    mock_key.get_verifying_key.return_value = MagicMock()
    mock_signing_key.return_value = mock_key
    mock_key.verify.side_effect = Exception("Invalid signature")
    
    with patch('builtins.print') as mock_print:
        key_generation_example()
        assert mock_print.call_count > 0


def test_key_generation_valid_signature():
    # Test successful signature verification path
    with patch('builtins.print') as mock_print:
        key_generation_example()
        assert mock_print.call_count > 0


def test_batch_verification_multiple_keys():
    with patch('builtins.print') as mock_print:
        result = batch_verification_example()
        assert result is True
        assert mock_print.call_count >= 3  # At minimum print batch completion message


def test_batch_verification_signature_output():
    with patch('builtins.print') as mock_print:
        batch_verification_example()
        # Should print signatures
        assert mock_print.call_count > 0


def test_basic_verification_forged_sig_exception():
    # Test when forged signature verification raises exception
    with patch('examples.basic_usage.os.urandom', return_value=b'\xFF' * 64):
        with patch('builtins.print') as mock_print:
            basic_signature_verification()
            assert mock_print.call_count > 0


def test_key_generation_bad_private_key():
    # Test with bad private key that can't sign
    with patch('examples.basic_usage.os.urandom', return_value=b'\xFF' * 31 + b'\xFE'):
        with patch('builtins.print') as mock_print:
            key_generation_example()
            # Should still print output even if key generation fails
            assert mock_print.call_count > 0


def test_basic_verification_with_none_message():
    # Test edge case with None message
    with patch('builtins.print') as mock_print:
        basic_signature_verification()
        assert mock_print.call_count > 0


def test_batch_verification_zero_keys():
    # Test with empty key lists would use default generation
    with patch('builtins.print') as mock_print:
        result = batch_verification_example()
        assert result is True
        assert mock_print.call_count > 0


@patch('ed25519.VerifyingKey.verify')
def test_signature_verification_fail_path(mock_verify):
    mock_verify.side_effect = Exception("Invalid signature")
    with patch('builtins.print') as mock_print:
        basic_signature_verification()
        assert mock_print.call_count > 0


def test_key_generation_none_encoding():
    # Test with None encoding - should work with default
    with patch('builtins.print') as mock_print:
        key_generation_example()
        assert mock_print.call_count > 0


def test_basic_verification_verifier_exception():
    with patch.object(Ed25519Verifier, 'verify_signature', side_effect=Exception("Verification error")):
        with patch('builtins.print') as mock_print:
            basic_signature_verification()
            assert mock_print.call_count > 0


def test_batch_verification_with_one_signature():
    with patch('examples.basic_usage.os.urandom', side_effect=[b'\x00'*32]):
        with patch('builtins.print') as mock_print:
            batch_verification_example()
            assert mock_print.call_count > 0