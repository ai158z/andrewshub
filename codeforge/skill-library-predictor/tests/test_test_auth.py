import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import jwt

from src.auth import AuthManager


@pytest.fixture
def auth_manager():
    return AuthManager()


@pytest.fixture
def valid_payload():
    return {
        "user_id": "test_user_123",
        "exp": (datetime.utcnow() + timedelta(hours=1)).timestamp()
    }


@pytest.fixture
def expired_payload():
    return {
        "user_id": "test_user_expired",
        "exp": (datetime.utcnow() - timedelta(hours=1)).timestamp()
    }


def test_verify_token_valid_token(auth_manager, valid_payload):
    token = auth_manager.generate_token(valid_payload)
    result = auth_manager.verify_token(token)
    assert result is True


def test_verify_token_invalid_format(auth_manager):
    result = auth_manager.verify_token("invalid.token.string")
    assert result is False


def test_verify_token_expired_token(auth_manager, expired_payload):
    token = auth_manager.generate_token(expired_payload)
    result = auth_manager.verify_token(token)
    assert result is False


def test_generate_token_returns_string(auth_manager, valid_payload):
    token = auth_manager.generate_token(valid_payload)
    assert isinstance(token, str)
    assert len(token) > 0


def test_generate_token_creates_valid_token(auth_manager, valid_payload):
    token = auth_manager.generate_token(valid_payload)
    result = auth_manager.verify_token(token)
    assert result is True


def test_generate_token_invalid_payload_type(auth_manager):
    with pytest.raises((TypeError, AttributeError)):
        auth_manager.generate_token("invalid_payload")


def test_generate_token_empty_payload(auth_manager):
    with pytest.raises((jwt.exceptions.InvalidTokenError, Exception)):
        invalid_token = auth_manager.generate_token({})
        auth_manager.verify_token(invalid_token)


@patch('jwt.encode')
def test_generate_token_calls_jwt_encode(mock_encode, auth_manager, valid_payload):
    mock_encode.return_value = "mocked_token"
    token = auth_manager.generate_token(valid_payload)
    assert token == "mocked_token"
    mock_encode.assert_called_once()


@patch('jwt.decode')
def test_verify_token_calls_jwt_decode(mock_decode, auth_manager, valid_payload):
    token = auth_manager.generate_token(valid_payload)
    mock_decode.return_value = valid_payload
    result = auth_manager.verify_token(token)
    assert result is True
    mock_decode.assert_called_once()


def test_verify_token_invalid_signature(auth_manager):
    # Test that invalid signature returns False
    result = auth_manager.verify_token("a.b.c")
    assert result is False


def test_verify_token_none_input(auth_manager):
    result = auth_manager.verify_token(None)
    assert result is False


def test_verify_token_empty_string(auth_manager):
    result = auth_manager.verify_token("")
    assert result is False


def test_generate_and_verify_token_integration(auth_manager, valid_payload):
    token = auth_manager.generate_token(valid_payload)
    assert isinstance(token, str)
    assert len(token) > 0
    result = auth_manager.verify_token(token)
    assert result is True


def test_generate_token_with_none_payload(auth_manager):
    with pytest.raises((TypeError, AttributeError)):
        auth_manager.generate_token(None)


def test_generate_token_with_missing_exp_field(auth_manager, valid_payload):
    # Remove exp field to test
    payload = valid_payload.copy()
    payload.pop("exp", None)
    with pytest.raises((KeyError, Exception)):
        auth_manager.generate_token(payload)


def test_verify_token_malformed_jwt(auth_manager):
    # Test various malformed token formats
    result = auth_manager.verify_token("just.a.string")
    assert result is False
    
    result = auth_manager.verify_token("missing.parts.here")
    assert result is False
    
    result = auth_manager.verify_token("")
    assert result is False


def test_verify_token_valid_but_unsupported_algorithm(auth_manager):
    # Create a token with different algorithm that our auth manager doesn't support
    payload = {"some": "payload"}
    # This creates a token but with potentially unsupported algorithm
    token = jwt.encode(payload, "secret", algorithm="HS256")
    result = auth_manager.verify_token(token)
    # Should still return False for tokens that can't be decoded properly
    assert result is False


def test_generate_token_with_insufficient_payload(auth_manager):
    insufficient_payload = {"user_id": "test"}  # Missing exp field
    with pytest.raises((Exception, KeyError)):
        auth_manager.generate_token(insufficient_payload)


def test_verify_token_edge_cases(auth_manager):
    # Test None, empty string, and malformed tokens
    assert auth_manager.verify_token(None) is False
    assert auth_manager.verify_token("") is False
    assert auth_manager.verify_token("invalid_format_token") is False
    assert auth_manager.verify_token("a.b.c") is False


def test_generate_and_verify_round_trip(auth_manager, valid_payload):
    token = auth_manager.generate_token(valid_payload)
    result = auth_manager.verify_token(token)
    assert result is True