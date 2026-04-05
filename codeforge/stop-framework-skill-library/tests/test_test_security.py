import pytest
from unittest.mock import Mock, patch
from stop_skill_library.models import Skill, SecurityContext
from stop_skill_library.security import SecurityManager
from stop_skill_library.security.access_control import AccessController
from stop_skill_library.security.validation import ModificationValidator


def test_access_controller_check_permission():
    access_controller = AccessController()
    security_context = SecurityContext(
        user_id="test_user",
        permissions=["read", "write"],
        role="developer"
    )
    
    # Test unauthorized access
    assert not access_controller.check_permission("delete", security_context)
    assert access_controller.check_permission("read", security_context)
    assert access_controller.check_permission("write", security_context)
    
    # Test permission granting and revocation
    access_controller.grant_access("delete", security_context)
    assert access_controller.check_permission("delete", security_context)
    
    # Test permission revocation
    access_controller.revoke_access("delete", security_context)
    assert not access_controller.check_permission("delete", security_context)


def test_modification_validator_sign():
    # Test data
    validator = ModificationValidator()
    # Test valid modification
    original = "test data"
    signature = validator.sign(original)
    assert not validator.verify("tampered data", signature)
    
    # Test with skill library
    skill = Skill(
        id="test-skill-id",
        name="Test Skill",
        description="A test skill",
        code="print('Hello World')",
        version=1,
        metadata={}
    )
    
    # Test that modifications are properly validated
    assert validator.verify(str(skill.dict()), signature)
    assert not validator.verify("tampered data", signature)


def test_security_manager_validation():
    # Test that access control mechanisms work properly
    security_manager = SecurityManager(AccessController(), ModificationValidator())
    # Test that the security manager correctly validates modifications
    assert security_manager.check_permission("read", security_context)
    assert not security_manager.check_permission("delete", security_context)


def test_unauthorized_access_denied():
    # Test that unauthorized access is properly denied
    access_controller = AccessController()
    security_context = SecurityContext(
        user_id="unauthorized_user",
        permissions=[],
        role="guest"
    )
    
    assert not access_controller.check_permission("write", security_context)
    assert not access_controller.check_permission("delete", security_context)


def test_authorized_access():
    # Test authorized access
    access_controller = AccessController()
    security_context = SecurityContext(
        user_id="test_user",
        permissions=["read", "write"],
        role="developer"
    )
    
    assert access_controller.check_permission("read", security_context)
    assert access_controller.check_permission("write", security_context)
    
    access_controller.revoke_access("delete", security_context)
    assert not access_controller.check_permission("delete", security_context)


def test_modification_validation():
    # Test that modifications are properly validated
    validator = ModificationValidator()
    # Valid test data
    assert validator.verify("test data", validator.sign("test data"))
    assert not validator.verify("tampered data", signature)