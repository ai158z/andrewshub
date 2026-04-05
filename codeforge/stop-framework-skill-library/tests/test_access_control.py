import pytest
from unittest.mock import Mock, patch
from stop_skill_library.models import Skill
from stop_skill_library.security.access_control import AccessController
from stop_skill_library.security.validation import ModificationValidator

@pytest.fixture
def access_controller():
    return AccessController()

@pytest.fixture
def sample_skill():
    skill = Mock(spec=Skill)
    skill.id = "skill_123"
    skill.permissions = {}
    return skill

def test_check_permission_global_wildcard_grants_access(access_controller, sample_skill):
    access_controller.permissions["user1"] = {"*"}
    result = access_controller.check_permission("user1", sample_skill, "read")
    assert result is True

def test_check_permission_global_specific_action_grants_access(access_controller, sample_skill):
    access_controller.permissions["user1"] = {"read", "write"}
    result = access_controller.check_permission("user1", sample_skill, "read")
    assert result is True

def test_check_permission_skill_specific_permission_grants_access(access_controller, sample_skill):
    sample_skill.permissions = {"user1": {"read"}}
    result = access_controller.check_permission("user1", sample_skill, "read")
    assert result is True

def test_check_permission_no_permissions_denies_access(access_controller, sample_skill):
    result = access_controller.check_permission("user1", sample_skill, "read")
    assert result is False

def test_check_permission_skill_wildcard_grants_access(access_controller, sample_skill):
    sample_skill.permissions = {"user1": {"*"}}
    result = access_controller.check_permission("user1", sample_skill, "execute")
    assert result is True

def test_check_permission_exception_returns_false(access_controller, sample_skill):
    with patch.object(access_controller, 'permissions', side_effect=Exception("Test error")):
        result = access_controller.check_permission("user1", sample_skill, "read")
        assert result is False

def test_grant_access_success(access_controller):
    result = access_controller.grant_access("user1", "skill_123", ["read", "write"])
    assert result is True
    assert access_controller.permissions["user1"] == {"read", "write"}

def test_grant_access_exception_returns_false(access_controller):
    with patch.object(dict, 'setdefault', side_effect=Exception("Test error")):
        result = access_controller.grant_access("user1", "skill_123", ["read"])
        assert result is False

def test_revoke_access_success(access_controller):
    access_controller.permissions["user1"] = {"read", "write"}
    result = access_controller.revoke_access("user1", "skill_123", ["write"])
    assert result is True
    assert access_controller.permissions["user1"] == {"read"}

def test_revoke_access_all_permissions_removes_user(access_controller):
    access_controller.permissions["user1"] = {"read"}
    result = access_controller.revoke_access("user1", "skill_123", ["read"])
    assert result is True
    assert "user1" not in access_controller.permissions

def test_revoke_access_exception_returns_false(access_controller):
    access_controller.permissions["user1"] = {"read"}
    with patch.object(set, 'discard', side_effect=Exception("Test error")):
        result = access_controller.revoke_access("user1", "skill_123", ["read"])
        assert result is False

def test_set_validator(access_controller):
    validator = Mock(spec=ModificationValidator)
    access_controller.set_validator(validator)
    assert access_controller.validator == validator

def test_get_permissions_existing_user(access_controller):
    access_controller.permissions["user1"] = {"read", "write"}
    permissions = access_controller.get_permissions("user1")
    assert permissions == {"read", "write"}

def test_get_permissions_nonexistent_user(access_controller):
    permissions = access_controller.get_permissions("nonexistent")
    assert permissions == set()

def test_list_users_with_access(access_controller):
    access_controller.permissions["user1"] = {"read"}
    access_controller.permissions["user2"] = {"write"}
    access_controller.permissions["user3"] = {"execute"}
    users = access_controller.list_users_with_access("skill_123")
    assert set(users) == {"user1", "user2", "user3"}

def test_list_users_with_access_no_users(access_controller):
    users = access_controller.list_users_with_access("skill_123")
    assert users == []

def test_list_users_with_access_no_permissions_match(access_controller):
    access_controller.permissions["user1"] = set()
    users = access_controller.list_users_with_access("skill_123")
    assert users == []

def test_list_users_with_access_exception_returns_empty_list(access_controller):
    with patch.object(dict, 'items', side_effect=Exception("Test error")):
        users = access_controller.list_users_with_access("skill_123")
        assert users == []

def test_grant_access_multiple_users(access_controller):
    access_controller.grant_access("user1", "skill_123", ["read"])
    access_controller.grant_access("user2", "skill_123", ["write"])
    assert "user1" in access_controller.permissions
    assert "user2" in access_controller.permissions
    assert access_controller.permissions["user1"] == {"read"}
    assert access_controller.permissions["user2"] == {"write"}