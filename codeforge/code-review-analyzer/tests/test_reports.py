import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_repository():
    return {"id": "test-repo-123", "name": "test-repo"}

@pytest.fixture
def mock_analysis_result():
    return {
        "id": "analysis-123",
        "repository_id": "test-repo-123",
        "results": [{"issue": "test issue", "severity": "medium"}]
    }

def test_generate_report_success():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze, \
         patch('backend.src.api.routes.reports.generate_analysis_report') as mock_generate_report:
        
        mock_get_repo.return_value = {"id": "test-repo-123", "name": "test-repo"}
        mock_analyze.return_value = {"id": "analysis-123", "results": []}
        mock_generate_report.return_value = "Test report content"
        
        response = generate_report("test-repo-123")
        
        assert "report_id" in response
        assert "status" in response
        assert response["status"] == "completed"
        assert response["report_id"] is not None

def test_generate_report_repository_not_found():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo:
        mock_get_repo.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            generate_report("nonexistent-repo")
        
        assert exc_info.value.status_code == 404

def test_generate_report_analysis_failure():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze:
        
        mock_get_repo.return_value = {"id": "test-repo-123", "name": "test-repo"}
        mock_analyze.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            generate_report("test-repo-123")
        
        assert exc_info.value.status_code == 500

def test_get_report_success():
    with patch('backend.src.api.routes.reports.get_report') as mock_get:
        mock_get.return_value = {
            "id": "test-report-123",
            "generated_at": datetime.utcnow().isoformat(),
            "data": {"test": "data"}
        }
        
        response = get_report("test-report-123")
        assert "id" in response
        assert response["id"] == "test-report-123"

def test_get_report_not_found():
    with patch('backend.src.api.routes.reports.get_report') as mock_get:
        mock_get.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_report("nonexistent-report")
        
        assert exc_info.value.status_code == 404

def test_get_report_exception():
    with patch('backend.src.api.routes.reports.get_report') as mock_get:
        mock_get.side_effect = Exception("Database error")
        
        with pytest.raises(HTTPException) as exc_info:
            get_report("test-report-123")
        
        assert exc_info.value.status_code == 500

def test_generate_report_with_valid_uuid():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze, \
         patch('backend.src.api.routes.reports.generate_analysis_report') as mock_generate:
        
        mock_get_repo.return_value = {"id": "test-repo-123"}
        mock_analyze.return_value = {"results": []}
        mock_generate.return_value = "Test report"
        
        response = generate_report("test-repo-123")
        report_uuid = uuid.UUID(response["report_id"])
        
        assert str(report_uuid) == response["report_id"]

def test_generate_report_with_no_analysis_results():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze:
        
        mock_get_repo.return_value = {"id": "test-repo-123"}
        mock_analyze.return_value = {"results": []}
        
        response = generate_report("test-repo-123")
        
        assert response["status"] == "completed"
        assert "report_id" in response

def test_generate_report_with_exception():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo:
        mock_get_repo.side_effect = Exception("Test exception")
        
        with pytest.raises(HTTPException) as exc_info:
            generate_report("test-repo-123")
        
        assert exc_info.value.status_code == 500

def test_generate_analysis_report_import():
    # Test that generate_analysis_report function can be imported
    from backend.src.services.report_generator import generate_analysis_report
    assert callable(generate_analysis_report)

def test_get_repository_import():
    # Test that get_repository function can be imported
    from backend.src.api.routes.repositories import get_repository
    assert callable(get_repository)

def test_analyze_code_import():
    # Test that analyze_code function can be imported
    from backend.src.api.routes.analysis import analyze_code
    assert callable(analyze_code)

def test_get_report_returns_dict():
    response = get_report("test-id")
    assert isinstance(response, dict)

def test_generate_report_returns_dict():
    response = generate_report("test-id")
    assert isinstance(response, dict)

def test_generate_report_empty_repository_id():
    with pytest.raises(HTTPException):
        generate_report("")

def test_get_report_empty_id():
    with pytest.raises(HTTPException):
        get_report("")

def test_generate_report_none_repository():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo:
        mock_get_repo.return_value = None
        
        with pytest.raises(HTTPException):
            generate_report("test")

def test_generate_report_none_analysis():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze:
        
        mock_get_repo.return_value = {"id": "test"}
        mock_analyze.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            generate_report("test")
        assert exc_info.value.status_code == 500

def test_generate_report_content_generation():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze, \
         patch('backend.src.api.routes.reports.generate_analysis_report') as mock_generate:
        
        mock_get_repo.return_value = {"id": "test"}
        mock_analyze.return_value = {"results": []}
        mock_generate.return_value = "Generated report content"
        
        response = generate_report("test")
        assert "data" in response
        assert response["status"] == "completed"

def test_generate_report_with_no_findings():
    with patch('backend.src.api.routes.reports.get_repository') as mock_get_repo, \
         patch('backend.src.api.routes.reports.analyze_code') as mock_analyze:
        
        mock_get_repo.return_value = {"id": "test"}
        mock_analyze.return_value = {"results": []}
        
        response = generate_report("test")
        assert response["status"] == "completed"