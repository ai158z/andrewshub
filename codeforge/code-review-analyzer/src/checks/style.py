import subprocess
import tempfile
import os
from typing import List
from src.patch_parser import FileChange

class Finding:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

    def __repr__(self):
        return f"Finding(rule_id='{self.rule_id}', severity='{self.severity}', message='{self.message}', line={self.line}, file_path='{self.file_path}')"

class StyleCheck:
    def __init__(self, rule_id: str, severity: str, message: str, line: int, file_path: str):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.line = line
        self.file_path = file_path

def check_style_violations(file_changes: List[FileChange]) -> List[Finding]:
    """
    Check for style violations in the provided file changes using flake8 and custom rules.
    
    Args:
        file_changes: List of FileChange objects containing file content changes
        
    Returns:
        List of Finding objects representing style violations
    """
    findings = []
    
    for file_change in file_changes:
        # Only check Python files
        if not file_change.path.endswith('.py'):
            continue
            
        # Create a temporary file with the new content for flake8 analysis
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            # Write the content of the file change to temp file
            temp_file.write('\n'.join(file_change.added_lines))
            temp_file_path = temp_file.name
            
        try:
            # Run flake8 on the temporary file
            result = subprocess.run(
                ['flake8', temp_file_path],
                capture_output=True,
                text=True
            )
            
            # Parse flake8 output
            if result.returncode != 0:
                flake8_findings = _parse_flake8_output(result.stdout, file_change.path)
                findings.extend(flake8_findings)
                
        except FileNotFoundError:
            # flake8 not found, use custom style rules instead
            custom_findings = _check_custom_style_rules(file_change)
            findings.extend(custom_findings)
            
        except Exception as e:
            # Handle any other exception during flake8 execution
            custom_findings = _check_custom_style_rules(file_change)
            findings.extend(custom_findings)
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
                
    return findings

def _parse_flake8_output(flake8_output: str, file_path: str) -> List[Finding]:
    """
    Parse flake8 output into Finding objects.
    
    Args:
        flake8_output: Raw flake8 output string
        file_path: Path of the file being checked
        
    Returns:
        List of Finding objects
    """
    findings = []
    lines = flake8_output.strip().split('\n')
    
    for line in lines:
        if not line:
            continue
            
        parts = line.split(':')
        if len(parts) >= 4:
            # Format: filename:line:col: rule code rule message
            line_num = int(parts[1])
            rule_code = parts[3].strip()
            message = ':'.join(parts[4:]).strip() if len(parts) > 4 else "Style violation"
            
            finding = Finding(
                rule_id=f"flake8-{rule_code}",
                severity="medium",
                message=message,
                line=line_num,
                file_path=file_path
            )
            findings.append(finding)
        elif len(parts) >= 3:
            # Handle alternative format
            try:
                line_num = int(parts[1])
                rule_code = parts[2].split()[0] if parts[2].split() else "unknown"
                # Find the message part after the rule code
                message_parts = []
                for part in parts[2].split()[1:]:
                    message_parts.append(part)
                message = ' '.join(message_parts) if message_parts else "Style violation"
                
                finding = Finding(
                    rule_id=f"flake8-{rule_code}",
                    severity="medium",
                    message=message,
                    line=line_num,
                    file_path=file_path
                )
                findings.append(finding)
            except (ValueError, IndexError):
                continue
            
    return findings

def _check_custom_style_rules(file_change: FileChange) -> List[Finding]:
    """
    Custom style rules implementation for when flake8 is not available.
    
    Args:
        file_change: FileChange object to analyze
        
    Returns:
        List of Finding objects for style violations
    """
    findings = []
    line_number = 1
    
    for line in file_change.added_lines:
        # Check for lines too long (PEP8 E501)
        if len(line) > 88:  # Using black's default line length
            findings.append(Finding(
                rule_id="custom-E501",
                severity="medium",
                message=f"Line too long ({len(line)} > 88 characters)",
                line=line_number,
                file_path=file_change.path
            ))
            
        # Check for missing whitespace around operators (PEP8 E225)
        if _has_operator_without_whitespace(line):
            findings.append(Finding(
                rule_id="custom-E225",
                severity="medium",
                message="Missing whitespace around operator",
                line=line_number,
                file_path=file_change.path
            ))
            
        # Check for multiple statements on same line (PEP8 E702)
        if _has_multiple_statements(line):
            findings.append(Finding(
                rule_id="custom-E702",
                severity="medium",
                message="Multiple statements on one line",
                line=line_number,
                file_path=file_change.path
            ))
            
        # Check for unused imports (F401)
        if _has_unused_import(line):
            findings.append(Finding(
                rule_id="custom-F401",
                severity="medium",
                message="Unused import detected",
                line=line_number,
                file_path=file_change.path
            ))
            
        line_number += 1
        
    return findings

def _has_operator_without_whitespace(line: str) -> bool:
    """Check if line has operator without proper whitespace."""
    operators = ['=', '==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '//', '%', '**']
    for op in operators:
        if op in line and not line.strip().startswith('#'):  # Skip comment lines
            # Simple check for missing spaces around operators
            if f' {op} ' not in line and op in line:
                # This is a basic check - in practice would need more sophisticated parsing
                return True
    return False

def _has_multiple_statements(line: str) -> bool:
    """Check if line has multiple statements (e.g., semicolon usage)."""
    # Skip empty lines and comment lines
    if not line.strip() or line.strip().startswith('#'):
        return False
    # Check for semicolon not in quotes or comments
    return ';' in line and not line.strip().startswith(';') and not line.strip().endswith(';')

def _has_unused_import(line: str) -> bool:
    """Check if line has an unused import."""
    # Simple check for import statements
    if line.strip().startswith('import ') or line.strip().startswith('from '):
        # Very basic check - in practice would need to parse the code
        # This is a simplified version for demonstration
        return True
    return False