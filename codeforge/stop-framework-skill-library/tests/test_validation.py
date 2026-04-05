import pytest
import json
from cryptography.hazmat.primitives import serialization
from stop_skill_library.models import SecurityContext
from stop_skill_library.security.validation import ModificationValidator


def test_validator_initialization():
    """Test that ModificationValidator can be initialized successfully."""
    validator = ModificationValidator()
    assert validator is not None


def test_sign_and_verify_valid_data():
    """Test that signing and verification work correctly for valid data."""
    validator = ModificationValidator()
    data = {"skill_id": "test_skill", "version": "1.0"}
    signature = validator.sign(data)
    is_valid = validator.verify(data, signature)
    assert is_valid is True


def test_verify_with_invalid_signature():
    """Test that verification fails with an invalid signature."""
    validator = ModificationValidator()
    data = {"skill_id": "test_skill", "version": "1.0"}
    signature = validator.sign(data)
    
    # Modify the data to make signature invalid
    invalid_data = {"skill_id": "different_skill", "version": "1.0"}
    is_valid = validator.verify(invalid_data, signature)
    assert is_valid is False


def test_sign_invalid_data_type():
    """Test that sign method raises TypeError for non-dict data."""
    validator = ModificationValidator()
    with pytest.raises(TypeError, match="Data must be a dictionary"):
        validator.sign("not a dict")


def test_validate_invalid_data_type():
    """Test that validate method raises TypeError for non-dict data."""
    validator = ModificationValidator()
    with pytest.raises(TypeError, match="Data must be a dictionary"):
        validator.validate("not a dict", b"fake_signature")


def test_hash_data_with_dict():
    """Test that _hash_data correctly hashes dictionary data."""
    validator = ModificationValidator()
    data = {"key": "value"}
    # Access the private method through the instance
    hashed = validator._hash_data(data)
    assert isinstance(hashed, bytes)
    assert len(hashed) == 32  # SHA-256 produces 32-byte hash


def test_hash_data_with_string():
    """Test that _hash_data correctly hashes string data."""
    validator = ModificationValidator()
    data = "test string"
    hashed = validator._hash_data(data)
    assert isinstance(hashed, bytes)
    assert len(hashed) == 32


def test_hash_data_with_bytes():
    """Test that _hash_data correctly handles bytes data."""
    validator = ModificationValidator()
    data = b"test bytes"
    hashed = validator._hash_data(data)
    assert isinstance(hashed, bytes)
    assert len(hashed) == 32


def test_hash_data_invalid_type():
    """Test that _hash_data raises TypeError for invalid data type."""
    validator = ModificationValidator()
    with pytest.raises(TypeError, match="Data must be dict, str, or bytes"):
        validator._hash_data(123)


def test_verify_with_custom_public_key():
    """Test verification with a custom public key."""
    validator = ModificationValidator()
    data = {"skill": "test"}
    signature = validator.sign(data)
    
    # Get the public key in PEM format
    public_key_pem = validator._public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    is_valid = validator.verify(data, signature, public_key_pem)
    assert is_valid is True


def test_verify_with_invalid_custom_public_key():
    """Test verification with invalid custom public key."""
    validator = ModificationValidator()
    data = {"skill": "test"}
    signature = validator.sign(data)
    
    # Generate a different key pair to use as invalid public key
    different_validator = ModificationValidator()
    public_key_pem = different_validator._public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    is_valid = validator.verify(data, signature, public_key_pem)
    assert is_valid is False


def test_sign_and_verify_large_data():
    """Test signing and verification with large data payload."""
    validator = ModificationValidator()
    large_data = {"data": "x" * 10000}  # 10KB of data
    signature = validator.sign(large_data)
    is_valid = validator.verify(large_data, signature)
    assert is_valid is True


def test_verify_modified_data():
    """Test that verification fails when signed data is modified."""
    validator = ModificationValidator()
    original_data = {"skill_id": "test", "config": {"param": "value"}}
    signature = validator.sign(original_data)
    
    # Modify the data
    modified_data = {"skill_id": "test", "config": {"param": "modified_value"}}
    is_valid = validator.verify(modified_data, signature)
    assert is_valid is False


def test_validate_with_correct_signature():
    """Test that validate returns True for correct signature."""
    validator = ModificationValidator()
    data = {"skill": "test"}
    signature = validator.sign(data)
    result = validator.validate(data, signature)
    assert result is True


def test_validate_with_tampered_signature():
    """Test that validate returns False for tampered signature."""
    validator = ModificationValidator()
    data = {"skill": "test"}
    signature = validator.sign(data)
    
    # Tamper with the signature
    tampered_signature = signature[:-1] + b'X'  # Change last byte
    result = validator.validate(data, tampered_sed_signature)
    assert result is False


def test_generate_keys_creates_valid_keys():
    """Test that _generate_keys creates valid RSA key pair."""
    validator = ModificationValidator()
    assert validator._private_key is not None
    assert validator._public_key is not None


def test_sign_and_verify_with_none_public_key():
    """Test signing and verification when public key is None."""
    validator = ModificationValidator()
    data = {"test": "data"}
    signature = validator.sign(data)
    is_valid = validator.verify(data, signature, public_key_pem=None)
    assert is_valid is True


def test_verify_with_corrupted_signature():
    """Test that verify returns False with corrupted signature."""
    validator = ModificationValidator()
    data = {"test": "data"}
    signature = validator.sign(data)
    
    # Corrupt the signature
    corrupted_signature = signature[:-2] + b'XX'
    is_valid = validator.verify(data, corrupted_signature)
    assert is_valid is False


def test_sign_empty_data():
    """Test signing and verifying empty dictionary."""
    validator = ModificationValidator()
    data = {}
    signature = validator.sign(data)
    is_valid = validator.verify(data, signature)
    assert is_valid is True


def test_verify_with_different_validator():
    """Test that verification fails when using different validator's key."""
    validator1 = ModificationValidator()
    validator2 = ModificationValidator()
    
    data = {"test": "data"}
    signature = validator1.sign(data)
    
    # Try to verify with different validator's public key
    public_key_pem = validator2._public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    is_valid = validator1.verify(data, signature, public_key_pem)
    assert is_valid is False