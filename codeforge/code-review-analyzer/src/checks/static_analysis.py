import subprocess
import tempfile
import os
import json
from typing import List
from src.patch_parser import FileChange

class StaticAnalysisError(Exception):
    """Custom exception for static analysis errors"""
    pass

def run_pylint_analysis(file_content: str, file_path: str) -> List['Finding']:
    """Run pylint analysis on a single file"""
    try:
        # Import here to avoid circular imports at module level
        from src.rules_engine import Finding
        
        findings = []
        
        # Create a temporary file for pylint analysis
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Run pylint on the temporary file
            result = subprocess.run([
                'pylint',
                '--output-format=json',
                '--disable=all',
                '--enable=C0103,C0111,C0104,W0613,W0612,R0903,R0913,W0603,W0904',
                temp_file_path
            ], capture_output=True, text=True, check=False)
            
            if result.returncode not in [0, 4, 8, 16, 32]:  # Pylint returns these codes for issues found
                raise StaticAnalysisError(f"Pylint failed with return code {result.returncode}")
            
            # Parse pylint output
            findings = _parse_pylint_output(result.stdout, file_path)
            
        except Exception as e:
            raise StaticAnalysisError(f"Error running pylint: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        return findings
    except StaticAnalysisError:
        raise
    except Exception as e:
        raise StaticAnalysisError(f"Error running pylint: {str(e)}")

def _parse_pylint_output(output: str, file_path: str) -> List['Finding']:
    """Parse pylint output and return findings"""
    findings = []
    
    # Import here to avoid circular imports at module level
    from src.rules_engine import Finding
    
    try:
        pylint_results = json.loads(output)
        for issue in pylint_results:
            findings.append(Finding(
                rule_id=issue.get('symbol', 'pylint-issue'),
                severity=issue.get('type', 'warning'),
                message=issue.get('message', 'Pylint issue found'),
                line=issue.get('line', 1),
                file_path=file_path
            ))
    except json.JSONDecodeError:
        # If JSON parsing fails, return empty list
        pass
    
    return findings

def run_static_analysis(file_changes: List[FileChange]) -> List['Finding']:
    """Run static analysis checks on file changes"""
    all_findings = []
    
    # Import here to avoid circular imports at module level
    from src.rules_engine import Finding
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):  # Only analyze Python files
            try:
                # Create content from file changes
                content_lines = []
                for i, line in enumerate(file_change.added_lines):
                    content_lines.append(line)
                
                content = '\n'.join(content_lines)
                
                # Run static analysis if we have content
                if content.strip():
                    findings = run_pylint_analysis(content, file_change.path)
                    all_findings.extend(findings)
                else:
                    # If no content, create an empty list of findings
                    findings = []
                    all_findings.extend(findings)
                    
            except StaticAnalysisError as e:
                raise StaticAnalysisError(f"Static analysis failed: {str(e)}")
            except Exception as e:
                raise StaticAnalysisError(f"Unexpected error during static analysis: {str(e)}")
    
    return all_findings

def run_custom_analysis(file_changes: List[FileChange]) -> List['Finding']:
    """Run custom static analysis rules"""
    findings = []
    
    # Import here to avoid circular imports at module level
    from src.rules_engine import Finding
    
    for file_change in file_changes:
        if not file_change.path.endswith('.py'):
            continue
            
        # Custom rule: Check for print statements in production code
        for line_num, line in enumerate(file_change.added_lines, 1):
            if 'print(' in line and not line.strip().startswith('#'):
                findings.append(Finding(
                    rule_id="no-print-statements",
                    severity="warning",
                    message="Print statements should be removed from production code",
                    line=line_num,
                    file_path=file_change.path
                ))
        
        # Custom rule: Check for TODO comments
        for line_num, line in enumerate(file_change.added_lines, 1):
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                findings.append(Finding(
                    rule_id="leftover-todo-comments",
                    severity="info",
                    message="Remove TODO/FIXME comments before merging",
                    line=line_num,
                    file_path=file_change.path
                ))
    
    return findings