from unittest.mock import Mock, patch
import pytest
from pydantic import BaseModel
from stop_skill_library.models import Skill
from stop_skill_library.improvement.safety_constraints import SafetyConstraints

class TestSkill(Skill):
    pass

def create_test_skill():
    return TestSkill(
        id="test-skill-123",
        name="test_skill",
        implementation="original implementation",
        metadata={"version": "1.0"}
    )

def test_validate_passes_all_checks():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    request = {"type": "improve", "implementation": "new implementation"}
    result = constraints.validate(skill, request)
    assert result is True

def test_validate_fails_size_limit():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    constraints.max_modification_size = 10
    request = {"type": "improve", "implementation": "very large implementation code"}
    result = constraints.validate(skill, request)
    assert result is False
    violations = constraints.get_violations()
    assert "Modification exceeds size limit" in violations

def test_validate_fails_invalid_type():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    request = {"type": "malicious", "implementation": "code"}
    result = constraints.validate(skill, request)
    assert result is False
    violations = constraints.get_violations()
    assert "Invalid modification type" in violations

def test_validate_fails_permissions():
    access_controller = Mock()
    access_controller.check_permission.return_value = False
    skill = create_test_skill()
    constraints = SafetyConstraints(access_controller=access_controller)
    request = {"type": "improve", "implementation": "code"}
    result = constraints.validate(skill, request)
    assert result is False
    violations = constraints.get_violations()
    assert "Insufficient permissions" in violations

def test_validate_with_signature_validation():
    modification_validator = Mock()
    modification_validator.validate.return_value = True
    skill = create_test_skill()
    constraints = SafetyConstraints(modification_validator=modification_validator)
    request = {"type": "improve", "implementation": "code"}
    result = constraints.validate(skill, request)
    assert result is True
    modification_validator.validate.assert_called_once()

def test_validate_signature_fails():
    modification_validator = Mock()
    modification_validator.validate.return_value = False
    skill = create_test_skill()
    constraints = SafetyConstraints(modification_validator=modification_validator)
    request = {"type": "improve", "implementation": "code"}
    result = constraints.validate(skill, request)
    assert result is False
    violations = constraints.get_violations()
    assert "Invalid modification signature" in violations

def test_apply_constraint_improve_modification():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    request = {
        "type": "improve",
        "implementation": "improved implementation",
        "metadata": {"version": "2.0"}
    }
    modified_skill = constraints.apply_constraint(skill, request)
    assert modified_skill.implementation == "improved implementation"
    assert modified_skill.metadata["version"] == "2.0"

def test_apply_constraint_update_modification():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    request = {
        "type": "update",
        "updates": {"name": "updated_name", "implementation": "updated implementation"}
    }
    modified_skill = constraints.apply_constraint(skill, request)
    assert modified_skill.name == "updated_name"
    assert modified_skill.implementation == "updated implementation"

def test_apply_constraint_fails_validation():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    constraints.max_modification_size = 10
    request = {"type": "improve", "implementation": "very large implementation"}
    with pytest.raises(ValueError, match="Modification exceeds size limit"):
        constraints.apply_constraint(skill, request)

def test_apply_constraint_refactor_modification():
    skill = create_test_skill()
    constraints = SafetyConstraints()
    request = {"type": "refactor"}
    modified_skill = constraints.apply_constraint(skill, request)
    assert modified_skill.id == skill.id

def test_check_size_limit_success():
    constraints = SafetyConstraints()
    request = {"type": "improve", "implementation": "small code"}
    result = constraints._check_size_limit(request)
    assert result is True

def test_check_size_limit_failure():
    constraints = SafetyConstraints()
    constraints.max_modification_size = 5
    request = {"type": "improve", "implementation": "large implementation"}
    result = constraints._check_size_limit(request)
    assert result is False

def test_validate_modification_type_valid():
    constraints = SafetyConstraints()
    request = {"type": "improve"}
    result = constraints._validate_modification_type(request)
    assert result is True

def test_validate_modification_type_invalid():
    constraints = SafetyConstraints()
    request = {"type": "invalid"}
    result = constraints._validate_modification_type(request)
    assert result is False

def test_check_permissions_no_controller():
    constraints = SafetyConstraints()
    request = {"type": "improve"}
    result = constraints._check_permissions(create_test_skill(), request)
    assert result is True

def test_check_permissions_with_controller_success():
    access_controller = Mock()
    access_controller.check_permission.return_value = True
    constraints = SafetyConstraints(access_controller=access_controller)
    request = {"type": "improve"}
    result = constraints._check_permissions(create_test_skill(), request)
    assert result is True

def test_check_permissions_with_controller_failure():
    access_controller = Mock()
    access_controller.check_permission.return_value = False
    constraints = SafetyConstraints(access_controller=access_controller)
    request = {"type": "improve"}
    result = constraints._check_permissions(create_test_skill(), request)
    assert result is False

def test_add_and_get_violations():
    constraints = SafetyConstraints()
    constraints.add_violation("test violation")
    violations = constraints.get_violations()
    assert "test violation" in violations
    constraints.clear_violations()
    violations = constraints.get_violations()
    assert len(violations) == 0

def test_clear_violations():
    constraints = SafetyConstraints()
    constraints.add_violation("test violation")
    assert len(constraints.get_violations()) > 0
    constraints.clear_violations()
    assert len(constraints.get_violations()) == 0