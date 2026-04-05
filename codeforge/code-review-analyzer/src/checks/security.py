import tempfile
import os
import subprocess
import sys
from typing import List
from src.patch_parser import FileChange
from src.rules_engine import Finding
import re

def check_for_vulnerabilities(file_changes: List[FileChange]) -> List[Finding]:
    """
    Check for security vulnerabilities using bandit and custom rules.
    
    Args:
        file_changes: List of FileChange objects
        
    Returns:
        List of security findings
    """
    
    findings = []
    
    # Check for security anti-patterns
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for hardcoded credentials
            findings.extend(check_hardcoded_credentials([file_change]))
            # Check for insecure functions
            findings.extend(check_insecure_functions([file_change]))
                
    return findings

def check_hardcoded_credentials(file_changes: List[FileChange]) -> List[Finding]:
    """Check for hardcoded credentials in file changes"""
    findings = []
    
    for file_change in file_changes:
        if not file_change.path.endswith('.py'):
            continue
            
        # Check for hardcoded credentials
        if file_change.content:
            if 'password' in file_change.content.lower() or 'secret' in file_change.content.lower():
                findings.append(Finding(
                    rule_id='security/hardcoded_credential_check',
                    severity='high',
                    message='Hardcoded credential found',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[File1. Fix the test code to not call fixtures directly
2. Fix the test functions to properly use the fixture
3. Fix the implementation to handle the actual FileChange object, not the fixture

import tempfile
import os
import subprocess
import sys
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.rules_engine import Finding
import re

def check_for_vulnerabilities(file_changes: List[FileChange]) -> List[Finding]:
    """
    Check for security vulnerabilities using bandit and custom rules.
    
    Args:
        file_changes: List of FileChange objects
        
    Returns:
        List of security findings
    """
    
    findings = []
    
    # Check for security anti-patterns
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for hardcoded credentials
            findings.extend(check_hardcoded_credentials([file_change]))
            # Check for insecure functions
            findings.extend(check_insecure_functions([file_change]))
                
    return findings

def check_hardcoded_credentials(file_changes: List[FileChange]) -> List[Finding]:
    """Check for hardcoded credentials in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for hardcoded credentials
            if 'password' in file_change.content.lower() or 'secret' in file_change.content.lower():
                findings.append(Finding(
                    rule_id='security/hardcoded_credential_check',
                    severity='high',
                    message='Hardcoded credential found',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Funding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[File0. Fix the test code to not call fixtures directly
2. Fix the test functions to properly use the fixture
3. Fix the implementation to handle the actual FileChange object, not the fixture

import tempfile
import os
import subprocess
import sys
from typing import List, Dict, Any
from src.patch_parser import FileChange
from src.rules_engine import Finding
import re

def check_for_vulnerabilities(file_changes: List[FileChange]) -> List[FileChange]:
    """
    Check for security vulnerabilities using bandit and custom rules.
    
    Args:
        file_changes: List of FileChange objects
        
    Returns:
        List of security findings
    """
    
    findings = []
    
    # Check for security anti-patterns
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for hardcoded credentials
            findings.extend(check_hardcoded_credentials([file_change]))
            # Check for insecure functions
            findings.extend(check_insecure_functions([file_change]))
                
    return findings

def check_hardcoded_credentials(file_changes: List[FileChange]) -> List[Finding]:
    """Check for hardcoded credentials in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for hardcoded credentials
            if 'password' in file_change.content.lower() or 'secret' in file_change.content.lower():
                findings.append(Finding(
                    rule_id='security/hardcoded_credential_check',
                    severity='high',
                    message='Hardcoded credential found',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule_id='security/insecure_function_check',
                    severity='high',
                    message='Insecure function usage detected',
                    line=1,
                    file_path=file_change.path
                ))
                
    return findings

def check_insecure_functions(file_changes: List[FileChange]) -> List[Finding]:
    """Check for insecure functions in file changes"""
    findings = []
    
    for file_change in file_changes:
        if file_change.path.endswith('.py'):
            # Check for insecure deserialization
            content = file_change.content
            if content and ('pickle' in content or 'eval' in content):
                findings.append(Finding(
                    rule