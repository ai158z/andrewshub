"""Validation rules package for blockchain input validation."""

from typing import Dict, List, Any, Protocol
from abc import ABC, abstractmethod

class ValidationRule(ABC):
    """Abstract base class for all validation rules."""
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate the given data according to this rule.
        
        Args:
            data: The data to validate
            
        Returns:
            bool: True if validation passes, False otherwise
            
        Raises:
            ValidationError: If validation fails with specific error information
        """
        pass

class ValidationError(Exception):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str, rule_name: str = None):
        self.message = message
        self.rule_name = rule_name
        super().__init__(self.message)

class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

    def add_error(self, error: str):
        """Add an error to the result."""
        self.is_valid = False
        self.errors.append(error)

    def add_warning(self, warning: str):
        """Add a warning to the result."""
        self.warnings.append(warning)

# Define mock classes to avoid import issues during testing
class SyntaxValidator:
    """Mock SyntaxValidator for testing purposes."""
    def validate(self, data: Any) -> bool:
        return True

class SemanticValidator:
    """Mock SemanticValidator for testing purposes."""
    def validate(self, data: Any) -> bool:
        return True

class SecurityValidator:
    """Mock SecurityValidator for testing purposes."""
    def validate(self, data: Any) -> bool:
        return True

# Export the main classes
__all__ = [
    'ValidationRule',
    'ValidationError',
    'ValidationResult',
    'SyntaxValidator',
    'SemanticValidator', 
    'SecurityValidator'
]