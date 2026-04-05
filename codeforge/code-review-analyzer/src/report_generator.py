import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    line: int
    file_path: str

@dataclass
class ReportMetadata:
    generated_at: str
    tool_name: str
    tool_version: int

@dataclass
class FileChange:
    path: str
    added_lines: List[int]
    removed_lines: List[int]

class Report:
    def __init__(self, findings: List[Finding], metadata: Dict[str, Any]):
        self.findings = findings
        self.metadata = metadata

    def generate_report(self) -> Dict[str, Any]:
        return {
            "findings": [
                {
                    "rule_id": finding.rule_id,
                    "file": finding.file_path,
                    "line": finding.line,
                    "message": finding.message,
                    "severity": finding.severity
                }
                for finding in self.findings
            ],
            "metadata": self.metadata
        }

def generate_report(findings: List[Finding]) -> dict:
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "tool_name": "Code Review Analyzer",
        "tool_version": "1.0.0", 
        "total_findings": len(findings)
    }
    
    return Report(findings, metadata).generate_report()

# src/report_generator.py
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    line: int
    file_path: str

@dataclass
class ReportMetadata:
    generated_at: str
    tool_name: str
    tool_version: str
    total_findings: int

@dataclass
class FileChange:
    path: str
    added_lines: List[int]
    removed_lines: List[int]

class Report:
    def __init__(self, findings: List[Finding], metadata: Dict[str, Any]):
        self.findings = findings
        self.metadata = metadata

    def generate_report(self) -> Dict[str, Any]:
        return {
            "findings": [
                {
                    "rule_id": finding.rule_id,
                    "file": finding.file_path,
                    "line": finding.line,
                    "message": finding.message,
                    "severity": finding.severity
                }
                for finding in self.findings
            ],
            "metadata": self.metadata
        }

def generate_report(findings: List[Finding]) -> dict:
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "tool_name": "Code Review Analyzer",
        "tool_version": "1.0.0",
        "total_findings": len(findings)
    }
    
    return Report(findings, metadata).generate_report()

# src/report_generator.py
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    line: int
    file_path: str

@dataclass
class ReportMetadata:
    generated_at: str
    tool_name: str
    tool_version: str
    total_findings: int

@dataclass
class FileChange:
    path: str
    added_lines: List[int]
    removed_lines: List[int]

class Report:
    def __init__(self, findings: List[Finding], metadata: Dict[str, Any]):
        self.findings = findings
        self.metadata = metadata

    def generate_report(self) -> Dict[str, Any]:
        return {
            "findings": [
                {
                    "rule_id": finding.rule_id,
                    "file": finding.file_path,
                    "line": finding.line,
                    "message": finding.message,
                    "severity": finding.severity
                }
                for finding in self.findings
            ],
            "metadata": self.metadata
        }

def generate_report(findings: List[Finding]) -> dict:
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "tool_name": "Code Review Analyzer",
        "tool_version": "1.0.0",
        "total_findings": len(findings)
    }
    
    return Report(findings, metadata).generate_report()