import os
import subprocess
import tempfile
import json
from typing import List, Dict, Any
from pathlib import Path
import logging
from sqlalchemy.orm import Session

from ..models.repository import Repository
from ..models.analysis import AnalysisResult
from ..services.vulnerability_scanner import scan_code, check_dependencies
from ..core.config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

class CodeAnalyzerService:
    def __init__(self, db: Session):
        self.db = db
        self.github_token = settings.GITHUB_TOKEN

    async def run_analysis(self, repository: Repository) -> AnalysisResult:
        """Run code analysis on a repository"""
        try:
            # Create analysis result record
            analysis_result = AnalysisResult(
                repository_id=repository.id,
                status="running"
            )
            self.db.add(analysis_result)
            self.db.commit()
            self.db.refresh(analysis_result)
            
            # Create temporary directory for code checkout
            with tempfile.TemporaryDirectory() as temp_dir:
                repo_path = Path(temp_dir) / "repo"
                
                # Clone repository
                clone_result = await self._clone_repository(repository.url, str(repo_path))
                if not clone_result:
                    raise Exception("Failed to clone repository")
                
                # Run various code quality checks
                findings = await self._run_code_quality_analysis(str(repo_path))
                
                # Run security scans
                vulnerabilities = await self.scan_for_vulnerabilities([str(p) for p in Path(repo_path).rglob("*.py")])
                
                # Combine all findings
                all_findings = findings + vulnerabilities
                
                # Update analysis result with findings
                analysis_result.status = "completed"
                analysis_result.findings = all_findings
                self.db.commit()
                
                return analysis_result
                
        except Exception as e:
            logger.error(f"Analysis failed for repository {repository.id}: {str(e)}")
            analysis_result = AnalysisResult(
                repository_id=repository.id,
                status="failed",
                findings=[],
                error_message=str(e)
            )
            self.db.add(analysis_result)
            self.db.commit()
            raise e

    async def _clone_repository(self, repo_url: str, local_path: str) -> bool:
        """Clone repository to local path"""
        try:
            # Use git CLI to clone repository
            result = subprocess.run(
                ["git", "clone", repo_url, local_path],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logger.error("Git clone timed out")
            return False
        except Exception as e:
            logger.error(f"Git clone failed: {str(e)}")
            return False

    async def _run_code_quality_analysis(self, repo_path: str) -> List[Dict[str, Any]]:
        """Run various code quality analysis tools"""
        findings = []
        
        # Run pylint
        pylint_findings = await self._run_pylint(repo_path)
        findings.extend(pylint_findings)
        
        # Run bandit for security issues
        bandit_findings = await self._run_bandit(repo_path)
        findings.extend(bandit_findings)
        
        # Run pycodestyle
        pycodestyle_findings = await self._run_pycodestyle(repo_path)
        findings.extend(pycodestyle_findings)
        
        return findings

    async def _run_pylint(self, repo_path: str) -> List[Dict[str, Any]]:
        """Run pylint analysis"""
        findings = []
        python_files = list(Path(repo_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                # Run pylint on each file
                result = subprocess.run(
                    ["pylint", "--output-format=json", str(file_path)],
                    capture_output=True,
                    text=True
                )
                if result.returncode in [0, 1, 2, 4, 8, 16, 32]:  # Pylint returns these codes for various issues
                    if result.stdout:
                        pylint_results = json.loads(result.stdout)
                        for issue in pylint_results:
                            findings.append({
                                "type": "pylint",
                                "file": str(file_path.relative_to(repo_path)),
                                "line": issue.get("line", 0),
                                "message": issue.get("message", ""),
                                "symbol": issue.get("symbol", ""),
                                "severity": self._pylint_type_to_severity(issue.get("type", ""))
                            })
            except (json.JSONDecodeError, FileNotFoundError):
                continue
            except Exception as e:
                logger.warning(f"Error running pylint on {file_path}: {str(e)}")
                
        return findings

    async def _run_bandit(self, repo_path: str) -> List[Dict[str, Any]]:
        """Run bandit security linter"""
        findings = []
        try:
            result = subprocess.run(
                ["bandit", "-f", "json", "-r", repo_path],
                capture_output=True,
                text=True
            )
            if result.returncode in [0, 1]:  # Bandit returns 1 when issues found
                if result.stdout:
                    bandit_results = json.loads(result.stdout)
                    for issue in bandit_results.get("results", []):
                        findings.append({
                            "type": "bandit",
                            "file": issue.get("filename", ""),
                            "line": issue.get("line_number", 0),
                            "message": issue.get("issue_text", ""),
                            "severity": issue.get("issue_severity", "").lower(),
                            "confidence": issue.get("issue_confidence", "").lower()
                        })
        except Exception as e:
            logger.warning(f"Bandit analysis failed: {str(e)}")
            
        return findings

    async def _run_pycodestyle(self, repo_path: str) -> List[Dict[str, Any]]:
        """Run pycodestyle (pep8) checker"""
        findings = []
        python_files = list(Path(repo_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                result = subprocess.run(
                    ["pycodestyle", str(file_path)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 1:  # Issues found
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line:
                            parts = line.split(':')
                            if len(parts) >= 3:
                                findings.append({
                                    "type": "pycodestyle",
                                    "file": str(file_path.relative_to(repo_path)),
                                    "line": int(parts[1]) if parts[1].isdigit() else 0,
                                    "message": ':'.join(parts[2:]).strip() if len(parts) > 2 else "",
                                    "severity": "warning"
                                })
            except Exception as e:
                logger.warning(f"Error running pycodestyle on {file_path}: {str(e)}")
                
        return findings

    def _pylint_type_to_severity(self, pylint_type: str) -> str:
        """Convert pylint issue type to severity level"""
        mapping = {
            "convention": "info",
            "warning": "warning",
            "error": "error",
            "fatal": "critical"
        }
        return mapping.get(pylint_type, "warning")

    async def scan_for_vulnerabilities(self, code_files: List[str]) -> List[Dict[str, Any]]:
        """Scan code files for vulnerabilities"""
        all_vulnerabilities = []
        
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    
                # Scan the code for vulnerabilities
                vulnerabilities = scan_code(code)
                all_vulnerabilities.extend(vulnerabilities)
                
            except Exception as e:
                logger.error(f"Error scanning {file_path}: {str(e)}")
                continue
                
        return all_vulnerabilities

    def check_dependencies(self, requirements_file: str) -> List[Dict[str, Any]]:
        """Check dependencies for known vulnerabilities"""
        try:
            # Run safety check
            result = subprocess.run(
                ["safety", "check", "--full-report", "-r", requirements_file],
                capture_output=True,
                text=True
            )
            
            vulnerabilities = []
            if result.returncode == 1:  # Safety returns 1 if vulnerabilities found
                # Parse safety output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line and not line.startswith('-'):
                        parts = line.split()
                        if len(parts) >= 3:
                            vulnerabilities.append({
                                "package": parts[0],
                                "affected_version": parts[1],
                                "vulnerability_id": parts[2],
                                "advisory": " ".join(parts[3:]) if len(parts) > 3 else ""
                            })
            
            return vulnerabilities
        except Exception as e:
            logger.error(f"Dependency check failed: {str(e)}")
            return []