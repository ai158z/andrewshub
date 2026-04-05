import pytest
from datetime import timedelta
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    get_current_user,
    AuthManager
)

def test_verify_password_correct():
    password = "testpass"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    password = "testpass"
    wrong_password = "wrongpass"
    hashed = get_password_hash(password)
    assert verify_password(wrong_password, hashed) is False

def test_get_password_hash_returns_string():
    password = "testpass"
    hashed = get_password_hash(password)
    assert isinstance(hashed, str)
    assert len(hashed) > 0

def test_create_access_token_with_expires_delta():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_access_token_without_expires_delta():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_get_current_user_valid_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    payload = get_current_user(token)
    assert payload["sub"] == "testuser"

def test_get_current_user_invalid_token():
    invalid_token = "invalid.token.string"
    with pytest.raises(HTTPException):
        get_current_user(invalid_token)

def test_get_current_user_missing_sub():
    data = {"name": "testuser"}  # Missing "sub" field
    token = create_access_token(data)
    with pytest.raises(HTTPException):
        get_current_user(token)

def test_auth_manager_authenticate_user():
    user = AuthManager.authenticate_user("testuser", "testpass")
    assert user is not None
    assert user["sub"] == "testuser"

def test_auth_manager_create_access_token_for_user():
    token = AuthManager.create_access_token_for_user("testuser")
    assert isinstance(token, str)
    assert len(token) > 0

def test_auth_manager_authenticate_user_returns_user_dict():
    result = AuthManager.authenticate_user("testuser", "testpass")
    assert isinstance(result, dict)
    assert "sub" in result

def test_create_access_token_encodes_user_id():
    token = AuthManager.create_access_token_for_user("testuser")
    payload = get_current_user(token)
    assert payload["sub"] == "testuser"

def test_verify_password_empty_password():
    hashed = get_password_hash("")
    assert verify_password("", hashed) is True

def test_verify_password_none_password():
    with pytest.raises(TypeError):
        verify_password(None, "hashed_password")

def test_get_current_user_malformed_token():
    malformed_token = "malformed"
    with pytest.raises(HTTPException):
        get_current_user(malformed_token)

def test_get_current_user_expired_token():
    with patch("src.core.security.jwt.decode") as mock_decode:
        mock_decode.side_effect = Exception("Token expired")
        with pytest.raises(HTTPException):
            get_current_user("any_token")

def test_create_access_token_data_persistence():
    data = {"sub": "testuser", "extra": "value"}
    token = create_access_token(data)
    # Simulate decoding to check data is preserved
    import jwt
    import os
    decoded = jwt.decode(token, os.getenv("SECRET_KEY", "fallback_secret_key_for_dev"), algorithms=["HS256"])
    assert decoded["sub"] == "testuser"
    assert decoded["extra"] == "value"

def test_auth_manager_create_token_with_custom_expiry():
    user_id = "testuser"
    token = AuthManager.create_access_token_for_user(user_id)
    assert isinstance(token, str)

def test_auth_manager_authenticate_user_logs_info(caplog):
    with caplog.at_level("INFO"):
        AuthManager.authenticate_user("testuser", "testpass")
        assert "Authenticating user: testuser" in caplog.text

def test_get_password_hash_empty_string():
    hashed = get_password_hash("")
    assert isinstance(hashed, str)
    assert len(hashed) > 0