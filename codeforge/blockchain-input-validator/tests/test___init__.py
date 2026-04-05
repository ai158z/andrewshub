import pytest
from typing import Any
from blockchain_validator.rules import (
    ValidationRule, ValidationError, ValidationResult,
    SyntaxValidator, SemanticValidator, SecurityValidator
)

class TestValidationRule:
    def test_validate_abstract_method(self):
        # Test that ValidationRule is abstract and cannot be instantiated directly
        with pytest.raises(TypeError):
            ValidationRule()

class TestValidationResult:
    def test_initialization_with_defaults(self):
        result = ValidationResult(True)
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_initialization_with_values(self):
        result = ValidationResult(False, ["error1"], ["warning1"])
        assert result.is_valid is False
        assert result.errors == ["error1"]
        assert result.warnings == ["warning1"]

    def test_add_error_changes_validity(self):
        result = ValidationResult(True)
        result.add_error("Test error")
        assert result.is_valid is False
        assert result.errors == ["Test error"]

    def test_add_warning(self):
        result = ValidationResult(True)
        result.add_warning("Test warning")
        assert result.warnings == ["Test warning"]

class TestSyntaxValidator:
    def test_validate_returns_bool(self):
        validator = SyntaxValidator()
        result = validator.validate("test data")
        assert isinstance(result, bool)

class TestSemanticValidator:
    def test_validate_returns_bool(self):
        validator = SemanticValidator()
        result = validator.validate("test data")
        assert isinstance(result, bool)

class TestSecurityValidator:
    def test_validate_returns_bool(self):
        validator = SecurityValidator()
        result = validator.validate("test data")
        assert isinstance(result, bool)

class TestValidationError:
    def test_initialization_with_message_only(self):
        error = ValidationError("Test message")
        assert error.message == "Test message"
        assert error.rule_name is None

    def test_initialization_with_message_and_rule(self):
        error = ValidationError("Test message", "test_rule")
        assert error.message == "Test message"
        assert error.rule_name == "test_rule"

    def test_inherits_from_exception(self):
        error = ValidationError("Test message")
        assert isinstance(error, Exception)

# Concrete implementation for testing ValidationRule
class ConcreteValidationRule(ValidationRule):
    def validate(self, data: Any) -> bool:
        return True

class TestConcreteValidationRule:
    def test_concrete_implementation_can_be_instantiated(self):
        rule = ConcreteValidationRule()
        assert rule.validate("test") is True

    def test_validation_rule_abstract_methods_must_be_implemented(self):
        class IncompleteRule(ValidationRule):
            pass

        with pytest.raises(TypeError):
            IncompleteRule()

    def test_validation_result_equality(self):
        result1 = ValidationResult(True, [], [])
        result2 = ValidationResult(True, [], [])
        assert result1.is_valid == result2.is_valid

    def test_validation_result_inequality(self):
        result1 = ValidationResult(True)
        result2 = ValidationResult(False, ["error"])
        assert result1.is_valid != result2.is_valid

    def test_validation_result_add_error_method(self):
        result = ValidationResult(True)
        result.add_error("New error")
        assert "New error" in result.errors
        assert result.is_valid is False

    def test_validation_result_add_warning_method(self):
        result = ValidationResult(True)
        result.add_warning("New warning")
        assert "New warning" in result.warnings
        assert result.is_valid is True  # Warnings don't change validity

    def test_validation_rule_is_abstract(self):
        # This should not raise - testing the module's abstract base class
        assert hasattr(ValidationRule, '__abstractmethods__')
        assert 'validate' in ValidationRule.__abstractmethods__

    def test_validation_error_inheritance(self):
        assert issubclass(ValidationError, Exception)
        error = ValidationError("test")
        assert isinstance(error, Exception)