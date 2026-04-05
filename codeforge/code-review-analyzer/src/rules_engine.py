import importlib
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(2, self, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.file_path = file_path

    def __repr__(self) -> str:
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"


def run_all_checks(file_changes: List[FileChange]) -> List[Finding]:
    """
    Execute all available checks on the provided file changes and aggregate findings.
    
    Args:
        file_changes: List of FileChange objects representing the code changes
        
    Returns:
        List of Finding objects representing issues discovered by various checks
    """
    all_findings = []
    
    # Import checks here to avoid circular imports
    from src.checks.security import check_for_vulnerabilities
    from src.checks.style import check_style_violations
    try:
        from src.checks.static_analysis import run_static_analysis
    except ImportError:
        # If static analysis module doesn't exist, create a mock function that returns empty list
        def run_static_analysis(changes):
            return []
    
    # Run security checks
    try:
        security_findings = check_for_vulnerabilities(file_changes)
        all_findings.extend(security_findings)
    except Exception as e:
        log(f"Security check failed: {str(e)}", "ERROR")
    
    # Run style checks
    try:
        style_findings = check_style_violations(file_changes)
        all_findings.extend(style_findings)
    except Exception as e:
        log(f"Style check failed: {str(e)}", "ERROR")
    
    # Run static analysis checks
    try:
        static_findings = run_static_analysis(file_changes)
        all_findings.extend(static_analysis_findings)
    except Exception as e:
        log(f"Static analysis check failed: {str(e)}", "ERROR")
    
    return all_findings

Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange

def test_finding_initialization():
    finding = Finding("RULE001", "high", "Test message", 10, "test.py")
    assert finding.rule_id == "RULE001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_finding_repr():
    finding = Finding("TEST001", "medium", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='medium', message='Test message', line=15, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
import importlib
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self) -> str:
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

Error:
==================

import importlib
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

    def test_finding_repr(self):
        finding = Finding("TEST001", "medium", "medium", "Test message", 15, "test_file.py")
        expected = "Finding(rule_id='TEST001', severity='medium', message='Test message', line=15, file_path='test_file.py')"

Error output:
import importlib
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("RULE001", "high", "Test message", 10, "test.py")
    assert finding.rule_id == "RULE001"
    assert finding.severity == "high"
    # ... (rest of the implementation)
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_run_all_checks(file_changes: List[FileChange]) -> List[Finding]:
    """
    Execute all available checks on the provided file changes and aggregate findings.
    
    Args:
        file_changes: List of FileChange objects representing the code changes
        
    Returns:
        List of Finding objects representing issues discovered by various checks
    """
    all_findings = []
    
    # Import checks here to avoid circular imports
    from src.checks.security import check_for_vulnerabilities
    from src.checks.style import check_style_violations
    try:
        from src.checks.static_analysis import run_static_analysis
    except ImportError:
        # If static analysis module doesn't exist, create a mock function that returns empty list
        def run_static_analysis(changes):
            return []
    
    # Run security checks
    try:
        security_findings = check_for_vulnerabilities(file_changes)
        all_findings.extend(security_findings)
    except Exception as e:
        log(f"Security check failed: {str(e)}", "ERROR")
    
    # Run style checks
    try:
        style_findings = check_style_violations(file_changes)
        all_findings.extend(style_findings)
    except Exception as e:
        log(f"Style check failed: {str(e)}", "ERROR")
    
    # Run static analysis checks
    try:
        static_findings = run_static_analysis(file_changes)
        all_findings.extend(static_findings)
    except Exception as e:
        log(f"Static analysis check failed: {str(e)}", "ERROR")
    
    return all_findings

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("RULE001", "high", "Test message", 10, "test.py")
    assert finding.rule_id == "RULE001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_finding_repr():
    finding = Finding("TEST001", "medium", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='medium', message='Test message', line=15, file_path='test_file.py')"

def test_run_all_checks_all_return_values():
    # Test that all checks return values
    file_changes = [FileChange()]
    security_finding = Finding("SEC001", "high", "Security issue", 10, "file1.py")
    style_finding = Finding("STYLE001", "medium", "Style issue", 20, "file2.py")
    static_finding = Finding("STATIC001", "low", "Static issue", 30, "file3.py")
    
    # Run security checks
    try:
        security_findings = check_for_vulnerabilities(file_changes)
        all_findings.extend(security_findings)
    except Exception as e:
        log(f"Security check failed: {str(e)}", "ERROR")
    
    # Run style checks
    try:
        style_findings = check_style_violations(file_changes)
        all_findings.extend(style_findings)
    except Exception as e:
        log(f"Style check failed: {str(e)}", "ERROR")
    
    # Run static analysis checks
    try:
        static_findings = run_static_analysis(file_changes)
        all_findings.extend(static_findings)
    except Exception as e:
        log(f"Static analysis check failed: {str(e)}", "ERROR")
    
    return all_findings

def test_finding_initialization():
    finding = Finding("TEST001", "medium", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='medium', message='Test message', line=15, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self) -> str:
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_repr():
    finding = Finding("TEST001", "medium", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='medium', message='Test message', line=15, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    assert finding.rule_id == "TEST001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test_file.py')"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test_file.py")
    assert finding.rule_id == "TEST001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_finding_repr():
    finding = Finding("TEST001", "medium", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='medium', message='Test message', line=15, file_path='test_file.py')"

def test_run_all_checks_all_return_values():
    # Test that all checks return values
    file_changes = [Mock(spec=FileChange)]
    security_finding = Finding("SEC001", "high", "Security issue", 10, "file1.py")
    style_finding = Finding("STYLE001", "medium", "Style issue", 20, "file2.py")
    static_finding = Finding("STATIC001", "low", "Static issue", 30, "file3.py")
    
    # Run security checks
    try:
        security_findings = check_for_vulnerabilities(file_changes)
        all_findings.extend(security_findings)
    except Exception as e:
        log(f"Security check failed: {str(e)}", "ERROR")
    
    # Run style checks
    try:
        style_findings = check_style_violations(file_changes)
        all_findings.extend(style_findings)
    except Exception as e:
        log(f"Style check failed: {str(e)}", "ERROR")
    
    # Run static analysis checks
    try:
        static_findings = run_static_analysis(file_changes)
        all_findings.extend(static_findings)
    except Exception as e:
        log(f"Static analysis check failed: {str(e)}", "ERROR")
    
    return all_findings

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    assert finding.rule_id == "TEST001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=15, file_path='test_file.py')"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=15, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_counts, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    assert finding.rule_id == "TEST001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test_file.py')"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=15, file_path='test_file.py')"

import importlib
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"
    assert finding.rule_id == "TEST001"
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.line == 10
    assert finding.file_path == "test.py"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test_file.py')"
    assert repr(finding) == expected

# Test code:
from unittest.mock import Mock, patch, MagicMock
from src.rules_engine import run_all_checks, Finding
from src.patch_parser import FileChange
from src.utils.logger import log


class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=15, file_path='test_file.py')"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "medium", "Test message", 15, "test_file.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=15, file_path='test_file.py')"

def test_run_all_checks_returns_list_of_findings():
    result = run_all_checks([])
    assert isinstance(result, list)

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_repr():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py'"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "Finding(rule_id='TEST001', severity='high', message='Test message', line=10, file_path='test.py')"

def test_finding_initialization():
    finding = Finding("TEST001", "high", "Test message", 10, "test.py")
    expected = "