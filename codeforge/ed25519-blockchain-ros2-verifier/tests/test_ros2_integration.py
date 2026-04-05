import json
from unittest.mock import Mock, patch, MagicMock
import pytest
from ed25519 import SigningKey, VerifyingKey
from ed25519 import BadSignatureError
from ed25519_verifier.exceptions import ROS2SignatureError, Ed25519VerificationError
from ed25519_verifier.ros2_integration import ROS2SignatureHandler

def test_sign_message_success():
    handler = ROS2SignatureHandler()
    message = b"test message"
    private_key = SigningKey(b"test" * 8)  # 32 bytes
    
    with patch('ed25519_verifier.ros2_integration.normalize_key_format') as mock_normalize:
        mock_normalize.return_value = private_key.to_bytes()
        signature = handler.sign_message(message, private_key.to_bytes())
        assert isinstance(signature, bytes)
        assert len(signature) > 0

def test_sign_message_failure():
    handler = ROS2SignatureHandler()
    message = b"test message"
    private_key = b"invalid"
    
    with pytest.raises(ROS2SignatureError):
        handler.sign_message(message, private_key)

def test_verify_message_valid():
    handler = ROS2SignatureHandler()
    message = b"test message"
    private_key = SigningKey(b"test" * 8)
    public_key = private_key.get_verifying_key()
    signature = private_key.sign(message)
    
    with patch('ed25519_verifier.ros2_integration.normalize_key_format') as mock_normalize:
        mock_normalize.return_value = public_key.to_bytes()
        result = handler.verify_message(message, signature, public_key.to_bytes())
        assert result is True

def test_verify_message_invalid():
    handler = ROS2SignatureHandler()
    message = b"test message"
    private_key = SigningKey(b"test" * 8)
    public_key = private_key.get_verifying_key()
    fake_signature = b"fake" * 16
    
    with patch('ed25519_verifier.ros2_integration.normalize_key_format') as mock_normalize:
        mock_normalize.return_value = public_key.to_bytes()
        result = handler.verify_message(message, fake_signature, public_key.to_bytes())
        assert result is False

def test_verify_message_exception():
    handler = ROS2SignatureHandler()
    message = b"test message"
    signature = b"test signature"
    public_key = b"invalid key"
    
    with pytest.raises(ROS2SignatureError):
        handler.verify_message(message, signature, public_key)

def test_create_signed_ros_message_success():
    handler = ROS2SignatureHandler()
    data = {
        'timestamp': 1234567890,
        'data': {'sensor': 'camera', 'value': 42},
        'private_key': SigningKey(b"test" * 8).to_bytes()
    }
    
    result = handler.create_signed_ros_message(data)
    assert isinstance(result, bytes)
    
    parsed = json.loads(result.decode('utf-8'))
    assert 'timestamp' in parsed
    assert 'data' in parsed
    assert 'signature' in parsed

def test_create_signed_ros_message_missing_timestamp():
    handler = ROS2SignatureHandler()
    data = {
        'data': {'sensor': 'camera', 'value': 42},
        'private_key': SigningKey(b"test" * 8).to_bytes()
    }
    
    with pytest.raises(ROS2SignatureError) as exc_info:
        handler.create_signed_ros_message(data)
    assert "Missing required 'timestamp' field" in str(exc_info.value)

def test_create_signed_ros_message_missing_data():
    handler = ROS2SignatureHandler()
    data = {
        'timestamp': 1234567890,
        'private_key': SigningKey(b"test" * 8).to_bytes()
    }
    
    with pytest.raises(ROS2SignatureError) as exc_info:
        handler.create_signed_ros_message(data)
    assert "Missing required 'data' field" in str(exc_info.value)

def test_create_signed_ros_message_no_private_key():
    handler = ROS2SignatureHandler()
    data = {
        'timestamp': 1234567890,
        'data': {'sensor': 'camera', 'value': 42}
    }
    
    result = handler.create_signed_ros_message(data)
    parsed = json.loads(result.decode('utf-8'))
    assert 'signature' not in parsed

def test_sign_message_empty_message():
    handler = ROS2SignatureHandler()
    message = b""
    private_key = SigningKey(b"test" * 8)
    
    with patch('ed25519_verifier.ros2_integration.normalize_key_format') as mock_normalize:
        mock_normalize.return_value = private_key.to_bytes()
        signature = handler.sign_message(message, private_key.to_bytes())
        assert isinstance(signature, bytes)

def test_sign_message_none_message():
    handler = ROS2SignatureHandler()
    private_key = b"test key"
    
    with pytest.raises(ROS2SignatureError):
        handler.sign_message(None, private_key)

def test_verify_message_empty_message():
    handler = ROS2SignatureHandler()
    message = b""
    private_key = SigningKey(b"test" * 8)
    public_key = private_key.get_verifying_key()
    signature = private_key.sign(message)
    
    with patch('ed25519_verifier.ros2_integration.normalize_key_format') as mock_normalize:
        mock_normalize.return_value = public_key.to_bytes()
        result = handler.verify_message(message, signature, public_key.to_bytes())
        assert result is True

def test_verify_message_bad_signature_error():
    handler = ROS2SignatureHandler()
    message = b"test message"
    private_key = SigningKey(b"test" * 8)
    public_key = private_key.get_verifying_key()
    
    with patch('ed25519.VerifyingKey.verify') as mock_verify:
        mock_verify.side_effect = BadSignatureError("Bad signature")
        result = handler.verify_message(message, b"fake_sig", public_key.to_bytes())
        assert result is False

def test_create_signed_ros_message_exception():
    handler = ROS2SignatureHandler()
    data = {
        'timestamp': "invalid_timestamp",
        'data': {'sensor': 'camera', 'value': 42},
        'private_key': b"test"
    }
    
    with pytest.raises(ROS2SignatureError):
        handler.create_signed_ros_message(data)

def test_sign_message_normalize_key_exception():
    handler = ROS2SignatureHandler()
    message = b"test"
    private_key = b"invalid key"
    
    with patch('ed25519_verifier.ros2_integration.normalize_key_format', side_effect=Exception("Key error")):
        with pytest.raises(ROS2SignatureError):
            handler.sign_message(message, private_key)