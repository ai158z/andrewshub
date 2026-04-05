import pytest
from ed25519_verifier.exceptions import Ed25519VerificationError, InvalidSignatureFormatError, ROS2SignatureError

def test_ed25519_verification_error_default_message():
    """Test Ed25519VerificationError with default message"""
    error = Ed25519VerificationError()
    assert str(error) == "Ed25519 signature verification failed"
    assert error.message == "Ed25519 signature verification failed"

def test_ed25519_verification_error_custom_message():
    """Test Ed25519VerificationError with custom message"""
    custom_msg = "Custom verification error"
    error = Ed25519VerificationError(custom_msg)
    assert str(error) == custom_msg
    assert error.message == custom_msg

def test_invalid_signature_format_error_default_message():
    """Test InvalidSignatureFormatError with default message"""
    error = InvalidSignatureFormatError()
    assert str(error) == "Invalid signature format provided"
    assert error.message == "Invalid signature format provided"

def test_invalid_signature_format_error_custom_message():
    """Test InvalidSignatureFormatError with custom message"""
    custom_msg = "Custom format error"
    error = InvalidSignatureFormatError(custom_msg)
    assert str(error) == custom_msg
    assert error.message == custom_msg

def test_ros2_signature_error_default_message():
    """Test ROS2SignatureError with default message"""
    error = ROS2SignatureError()
    assert str(error) == "ROS2 signature handling error occurred"
    assert error.message == "ROS2 signature handling error occurred"

def test_ros2_signature_error_custom_message():
    """Test ROS2SignatureError with custom message"""
    custom_msg = "Custom ROS2 error"
    error = ROS2SignatureError(custom_msg)
    assert str(error) == custom_msg
    assert error.message == custom_msg

def test_ed25519_verification_error_inheritance():
    """Test that Ed25519VerificationError inherits from Exception"""
    error = Ed25519VerificationError()
    assert isinstance(error, Exception)
    assert isinstance(error, Ed25519VerificationError)

def test_invalid_signature_format_error_inheritance():
    """Test that InvalidSignatureFormatError inherits from Exception"""
    error = InvalidSignatureFormatError()
    assert isinstance(error, Exception)
    assert isinstance(error, InvalidSignatureFormatError)

def test_ros2_signature_error_inheritance():
    """Test that ROS2SignatureError inherits from Exception"""
    error = ROS2SignatureError()
    assert isinstance(error, Exception)
    assert isinstance(error, ROS2Signature0Error)

def test_ed25519_verification_error_empty_string_message():
    """Test Ed25519VerificationError with empty string message"""
    error = Ed25519VerificationError("")
    assert error.message == ""
    assert str(error) == ""

def test_invalid_signature_format_error_empty_string_message():
    """Test InvalidSignatureFormatError with empty string message"""
    error = InvalidSignatureFormatError("")
    assert error.message == ""
    assert str(error) == ""

def test_ros2_signature_error_empty_string_message():
    """Test ROS2SignatureError with empty string message"""
    error = ROS2SignatureError("")
    assert error.message == ""
    assert str(error) == ""

def test_ed25519_verification_error_none_message():
    """Test Ed25519VerificationError with None message"""
    error = Ed25519VerificationError(None)
    assert error.message is None
    assert str(error) == "None"

def test_invalid_signature_format_error_none_message():
    """Test InvalidSignatureFormatError with None message"""
    error = InvalidSignatureFormatError(None)
    assert error.message is None
    assert str(error) == "None"

def test_ros2_signature_error_none_message():
    """Test ROS2SignatureError with None message"""
    error = ROS2SignatureError(None)
    assert error.message is None
    assert str(error) == "None"

def test_ed25519_verification_error_message_attribute():
    """Test that error objects have message attribute"""
    error = Ed25519VerificationError("test message")
    assert hasattr(error, 'message')
    assert error.message == "test message"

def test_invalid_signature_format_error_message_attribute():
    """Test that error objects have message attribute"""
    error = InvalidSignatureFormatError("test message")
    assert hasattr(error, 'message')
    assert error.message == "test message"

def test_ros2_signature_error_message_attribute():
    """Test that error objects have message attribute"""
    error = ROS2SignatureError("test message")
    assert hasattr(error, 'message')
    assert error.message == "test message"