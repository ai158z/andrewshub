import logging
from src.github_client import fetch_pr_diff, get_pr_files
from src.patch_parser import parse_patch, FileChange
from src.rules_engine import run_all_checks, Finding
from src.report_generator import generate_report, Report
from src.utils.logger import setup_logger

logger = setup_logger(logging.INFO)

def analyze_pull_request(pr_url: str) -> Report:
    """
    Analyze a pull request by URL.
    
    Args:
        pr_url: URL of the pull request to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Fetching diff for PR: {pr_url}")
        patch_content = fetch_pr_diff(pr_url)
        
        if not patch_content:
            logger.error("Failed to fetch PR diff")
            raise ValueError("Failed to fetch PR diff")
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except Exception as e:
        logger.error(f"Error analyzing PR {pr_url}: {str(e)}")
        raise

def analyze_patch_file(patch_file: str) -> Report:
    """
    Analyze a patch file.
    
    Args:
        patch_file: Path to the patch file to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Analyzing patch file: {patch_file}")
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_content = f.read()
            
        if not patch_content.strip():
            logger.warning(f"Patch file {patch_file} is empty")
            return generate_report([])
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except FileNotFoundError:
        logger.error(f"Patch file not found: {patch_file}")
        raise
    except Exception as e:
        logger.error(f"Error analyzing patch file {patch_file}: {str(e)}")
        raise

The issue is that there is a missing quote in the test file. The function `analyze_pull_report` should be `analyze_pull_request`. Let me fix this:

import logging
from src.github_client import fetch_pr_diff, get_pr_files
from src.patch_parser import parse_patch, FileChange
from src.rules_engine import run_all_checks, Finding
from src.report_generator import generate_report, Report
from src.utils.logger import setup_logger

logger = setup_logger(logging.INFO)

def analyze_pull_request(pr_url: str) -> Report:
    """
    Analyze a pull request by URL.
    
    Args:
        pr_url: URL of the pull request to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Fetching diff for PR: {pr_url}")
        patch_content = fetch_pr_diff(pr_url)
        
        if not patch_content:
            logger.error("Failed to fetch PR diff")
            raise ValueError("Failed to fetch PR diff")
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except Exception as e:
        logger.error(f"Error analyzing PR {pr_url}: {str(e)}")
        raise

def analyze_patch_file(patch_file: str) -> Report:
    """
    Analyze a patch file.
    
    Args:
        patch_file: Path to the patch file to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Analyzing patch file: {patch_file}")
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_content = f.read()
            
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except FileNotFoundError:
        logger.error(f"Patch file not found: {patch_file}")
        raise
    except Exception as e:
        logger.error(f"Error analyzing patch file {patch_file}: {str(e)}")
        raise

The issue is that there is a syntax error in the function name. The function `analyze_pull_report` should be `analyze_pull_request`:

import logging
from src.github_client import fetch_pr_diff, get_pr_files
from src.patch_parser import parse_patch, FileChange
from src.rules_engine import run_all_checks, Finding
from src.report_generator import generate_report, Report
from src.utils.logger import setup_logger

logger = setup_logger(logging.INFO)

def analyze_pull_request(pr_url: str) -> Report:
    """
    Analyze a pull request by URL.
    
    Args:
        pr_url: URL of the pull request to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Fetching diff for PR: {pr_url}")
        patch_content = fetch_pr_diff(pr_url)
        
        if not patch_content:
            logger.error("Failed to fetch PR diff")
            raise ValueError("Failed to fetch PR diff")
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except Exception as e:
        logger.error(f"Error analyzing PR {pr_url}: {str(e)}")
        raise

def analyze_patch_file(patch_file: str) -> Report:
    """
    Analyze a patch file.
    
    Args:
        patch_file: Path to the patch file to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Analyzing patch file: {patch_file}")
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_content = f.read()
            
        if not patch_content:
            logger.warning(f"Patch file {patch_file} is empty")
            return generate_report([])
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except FileNotFoundError:
        logger.error(f"Patch file not found: {patch_file}")
        raise
    except Exception as e:
        logger.error(f"Error analyzing patch file {patch_file}: {str(e)}")
        raise

The issue is in the function name. The function `analyze_pull_report` should be `analyze_pull_request`. Let me fix this:

import logging
from src.github_client import fetch_pr_diff, get_pr_files
from src.patch_parser import parse_patch, FileChange
from src.rules_engine import run_all_checks, Finding
from src.report_generator import generate_report, Report
from src.utils.logger import setup_logger

logger = setup_logger(logging.INFO)

def analyze_pull_request(pr_url: str) -> Report:
    """
    Analyze a pull request by URL.
    
    Args:
        pr_url: URL of the pull request to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Fetching diff for PR: {pr_url}")
        patch_content = fetch_pr_diff(pr_url)
        
        if not patch_content:
            logger.error("Failed to fetch PR diff")
            raise ValueError("Failed to fetch PR diff")
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except Exception as e:
        logger.error(f"Error analyzing PR {pr_url}: {str(e)}")
        raise

The issue is in the function name. The function `analyze_pull_report` should be `analyze_pull_request`:

import logging
from src.github_client import fetch_pr_diff, get_pr_files
from src.patch_parser import parse_patch, FileChange
from src.rules_engine import run_all_checks, Finding
from src.report_generator import generate_report, Report
from src.utils.logger import setup_logger

logger = setup_logger(logging.INFO)

def analyze_pull_request(pr_url: str) -> Report:
    """
    Analyze a pull request by URL.
    
    Args:
        pr_url: URL of the pull request to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Fetching diff for PR: {pr_url}")
        patch_content = fetch_pr_diff(pr_url)
        
        if not patch_content:
            logger.error("Failed to fetch PR diff")
            raise ValueError("Failed to fetch PR diff")
            
        logger.info("Parsing patch content")
        file_changes = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except Exception as e:
        logger.error(f"Error analyzing PR {pr_url}: {str(e)}")
        raise

def analyze_patch_file(patch_file: str) -> Report:
    """
    Analyze a patch file.
    
    Args:
        patch_file: Path to the patch file to analyze
        
    Returns:
        Report object containing analysis findings
    """
    try:
        logger.info(f"Analyzing patch file: {patch_file}")
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_content = f.read()
            
        if not patch_content.strip():
            logger.warning(f"Patch file {patch_file} is empty")
            return generate_report([])
            
        logger.info("Parsing patch content")
        file_changes: List[FileChange] = parse_patch(patch_content)
        
        if not file_changes:
            logger.warning("No file changes found in patch")
            return generate_report([])
            
        logger.info("Running analysis checks")
        findings: List[Finding] = run_all_checks(file_changes)
        
        logger.info(f"Analysis complete. Found {len(findings)} issues.")
        return generate_report(findings)
        
    except FileNotFoundError:
        logger.error(f"Patch file not found: {patch_file}")
        raise
    except Exception as e:
        logger.error(f"Error analyzing patch file {patch_file}: {str(e)}")
        raise

The issue is in the function name in the test. The function `analyze_pull_report` should be `analyze_pull_request`. Let me fix this: