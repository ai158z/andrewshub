from unittest.mock import patch, mock_open, MagicMock
from stop_skill_library.security import SecurityManager
from stop_skill_library.models import Skill, SecurityContext
import pytest
import json


@pytest.fixture
def security_manager():
    return SecurityManager()


@pytest.fixture
def sample_skill():
    return Skill(
        id="test-skill-123",
        name="Test Skill",
        owner="user-456",
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z"
    )


def test_init_with_valid_keys():
    with patch("builtins.open", mock_open(read_data="test")) as mock_file:
        with patch("stop_skill_library.security.serialization.load_pem_private_key") as mock_private:
            with patch("stop_skill_library.security.serialization.load_pem_public_key") as mock_public:
                mock_private.return_value = "mock_private_key"
                mock_public.return_value = "mock_public_key"
                
                sm = SecurityManager("private_key.pem", "public_key.pem")
                assert sm._private_key == "mock_private_key"
                assert sm._public_key == "mock_public_key"


def test_init_with_invalid_private_key_path():
    with pytest.raises(ValueError, match="Could not load private key"):
        SecurityManager(private_key_path="nonexistent.pem")


def test_init_with_invalid_public_key_path():
    with pytest.raises(ValueError, match="Could not load public key"):
        SecurityManager(public_key_path="nonexistent.pem")


def test_validate_modification_valid_data(security_manager, sample_skill):
    result = security_manager.validate_modification(sample_skill, {"description": "New description"})
    assert result is True


def test_validate_modification_invalid_skill_missing_id(security_manager):
    skill = Skill(id="", name="Test")
    result = security_manager.validate_modification(skill, {"description": "New description"})
    assert result is False


def test_validate_modification_invalid_data_type(security_manager, sample_skill):
    result = security_manager.validate_modification(sample_skill, "not a dict")
    assert result is False


def test_validate_modification_protected_field_change(security_manager, sample_skill):
    modification_data = {"id": "changed-id"}
    result = security_manager.validate_modification(sample_skill, modification_data)
    assert result is False


def test_validate_modification_protected_owner_field_change(security_manager, sample_skill):
    modification_data = {"owner": "unauthorized-user"}
    result = security_manager.validate_modification(sample_skill, modification_data)
    assert result is False


def test_check_access_valid_parameters(security_manager):
    with patch("stop_skill_library.security.logger") as mock_logger:
        result = security_manager.check_access("user-123", "skill-456", "read")
        assert result is True


def test_check_access_missing_parameters(security_manager):
    result = security_manager.check_access("", "skill-123", "read")
    assert result is False
    
    result = security_manager.check_access("user-123", "", "read")
    assert result is False
    
    result = security_manager.check_access("user-123", "skill-123", "")
    assert result is False


def test_sign_modification_success():
    # Create a mock private key
    mock_private_key = MagicMock()
    mock_private_key.sign.return_value = b"signature".hex()
    
    sm = SecurityManager()
    sm._private_key = mock_private_key
    
    data = {"test": "data"}
    result = sm.sign_modification(data)
    
    assert result == b"signature".hex()
    mock_private_key.sign.assert_called_once()


def test_sign_modification_no_private_key(security_manager):
    with pytest.raises(ValueError, match="No private key available for signing"):
        security_manager.sign_modification({"test": "data"})


def test_sign_modification_exception_handling():
    sm = SecurityManager()
    sm._private_key = MagicMock()
    sm._private_key.sign.side_effect = Exception("Signing failed")
    
    with pytest.raises(RuntimeError, match="Failed to sign modification"):
        sm.sign_modification({"test": "data"})


def test_validate_modification_exception_handling(security_manager, sample_skill):
    # Mock logger to raise exception
    with patch("stop_skill_library.security.logger") as mock_logger:
        mock_logger.info.side_effect = Exception("Logging failed")
        result = security_manager.validate_modification(sample_skill, {"description": "test"})
        # Should handle exception gracefully and return False
        assert result is False


def test_check_access_exception_handling(security_manager):
    # Mock logger to raise exception
    with patch("stop_skill_library.security.logger") as mock_logger:
        mock_logger.info.side_effect = Exception("Logging failed")
        result = security_manager.check_access("user", "skill", "read")
        # Should handle exception gracefully and return False
        assert result is False


def test_validate_modification_empty_skill_fields(security_manager):
    skill = Skill(id="", name="")
    result = security_manager.validate_modification(skill, {"description": "test"})
    assert result is False


def test_validate_modification_protected_created_at_field(security_manager, sample_skill):
    modification_data = {"created_at": "tampered"}
    result = security_manager.validate_modification(sample_skill, modification_data)
    assert result is False


def test_validate_modification_protected_updated_at_field(security_manager, sample_skill):
    modification_data = {"updated_at": "tampered"}
    result = security_manager.validate_modification(sample_skill, modification_data)
    assert result is False


def test_sign_modification_json_serialization():
    # Create a mock private key
    mock_private_key = MagicMock()
    mock_private_key.sign.return_value = b"test_signature"
    
    sm = SecurityManager()
    sm._private_key = mock_private_key
    
    # Test that data is properly serialized for signing
    test_data = {"b": 1, "a": 2}  # This should be sorted in the signature
    sm.sign_modification(test_data)
    
    # Verify the data was serialized with sorted keys
    call_args = mock_private_key.sign.call_args[0]
    serialized_data = call_args[0].decode('utf-8')
    expected_data = json.dumps(test_data, sort_keys=True, separators=(',', ':'))
    assert serialized_data == expected_data


def test_sign_modification_logging():
    sm = SecurityManager()
    sm._private_key = MagicMock()
    sm._private_key.sign.return_value = b"signature"
    
    with patch("stop_skill_library.security.logger") as mock_logger:
        sm.sign_modification({"test": "data"})
        # Verify logging was called
        mock_logger.info.assert_called_with("Modification signed successfully")