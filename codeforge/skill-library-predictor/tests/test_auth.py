import pytest
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from src.auth import AuthManager, auth_manager, authenticate
from fastapi.security import HTTPAuthorizationCredentials

@pytest.fixture
def auth_manager_instance():
    return AuthManager("test_secret_key")

@pytest.fixture
def valid_token(auth_manager_instance):
    return auth_manager_instance.generate_token("test_user")

def test_auth_manager_init_with_secret_key():
    am = AuthManager("test_key")
    assert am.secret_key == "test_key"

def test_auth_manager_init_without_secret_key():
    am = AuthManager()
    assert am.secret_key is not None
    assert len(am.secret_key) == 64  # 32 bytes = 64 hex chars

def test_generate_token_valid_user_id(auth_manager_instance):
    token = auth_manager_instance.generate_token("user123")
    assert isinstance(token, str)
    assert len(token) > 0

def test_generate_token_empty_user_id(auth_manager_instance):
    with pytest.raises(HTTPException) as exc_info:
        auth_manager_instance.generate_token("")
    assert exc_info.value.status_code == 500

def test_generate_token_none_user_id(auth_manager_instance):
    with pytest.raises(HTTPException) as exc_info:
        auth_manager_instance.generate_token(None)
    assert exc_info.value.status_code == 500

def test_verify_token_valid(auth_manager_instance, valid_token):
    payload = auth_manager_instance.verify_token(valid_token)
    assert payload["user_id"] == "test_user"

def test_verify_token_invalid_format(auth_manager_instance):
    with pytest.raises(HTTPException) as exc_info:
        auth_manager_instance.verify_token("invalid.token.string")
    assert exc_info.value.status_code == 401

def test_verify_token_expired(auth_manager_instance):
    # Create an expired token
    payload = {
        "user_id": "test_user",
        "exp": datetime.utcnow() - timedelta(seconds=10),
        "iat": datetime.utcnow() - timedelta(seconds=3600)
    }
    expired_token = jwt.encode(payload, auth_manager_instance.secret_key, algorithm="HS256")
    with pytest.raises(HTTPException) as exc_info:
        auth_manager_instance.verify_token(expired_token)
    assert exc_info.value.status_code == 401

def test_verify_token_missing_token(auth_manager_instance):
    with pytest.raises(HTTPException) as exc_info:
        auth_manager_instance.verify_token(None)
    assert exc_info.value.status_code == 401

def test_verify_token_empty_string(auth_manager_instance):
    with pytest.raises(HTTPException) as exc_info:
        auth_manager_instance.verify_token("")
    assert exc_info.value.status_code == 401

def test_token_expiration():
    am = AuthManager("test_key")
    # Generate token with short expiration
    token = am.generate_token("test_user", expires_in=1)
    # Wait for token to expire
    import time
    time.sleep(2)
    with pytest.raises(HTTPException) as exc_info:
        am.verify_token(token)
    assert exc_info.value.status_code == 401

def test_authenticate_valid_token(auth_manager_instance, valid_token):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=valid_token)
    payload = authenticate(credentials)
    assert payload["user_id"] == "test_user"

def test_authenticate_invalid_token(auth_manager_instance):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")
    with pytest.raises(HTTPException) as exc_info:
        authenticate(credentials)
    assert exc_info.value.status_code == 401

def test_authenticate_missing_credentials():
    with pytest.raises(HTTPException) as exc_info:
        authenticate(None)
    assert exc_info.value.status_code == 401

def test_generate_token_custom_expiration(auth_manager_instance):
    token = auth_manager_instance.generate_token("test_user", expires_in=7200)
    payload = auth_manager_instance.verify_token(token)
    assert "exp" in payload
    assert payload["user_id"] == "test_user"

def test_generate_token_default_expiration(auth_manager_instance):
    token = auth_manager_instance.generate_token("test_user")
    payload = auth_manager_instance.verify_token(token)
    assert "exp" in payload

def test_verify_token_manipulated_secret():
    # Test with a token signed with different secret
    fake_am = AuthManager("different_secret")
    token = fake_am.generate_token("test_user")
    with pytest.raises(HTTPException) as exc_info:
        auth_manager.verify_token(token)
    assert exc_info.value.status_code == 401

def test_verify_token_freshly_expired():
    am = AuthManager("test_key")
    # Create a token that expires now
    payload = {
        "user_id": "test_user",
        "exp": datetime.utcnow(),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, am.secret_key, algorithm="HS256")
    with pytest.raises(HTTPException) as exc_info:
        am.verify_token(token)
    assert exc_info.value.status_code == 401

def test_auth_manager_consistency():
    am1 = AuthManager("key1")
    am2 = AuthManager("key1")
    token1 = am1.generate_token("user1")
    # Should work with same secret
    payload = am2.verify_token(token1)
    assert payload["user_id"] == "user1"