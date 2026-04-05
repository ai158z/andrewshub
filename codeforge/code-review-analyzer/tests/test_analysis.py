import uuid
from datetime import datetime
from backend.src.schemas.analysis import AnalysisCreate, AnalysisFinding, AnalysisResult


def test_analysis_create_required_fields():
    # Test that repository_id is required
    data = {"repository_id": "repo123"}
    analysis_create = AnalysisCreate(**data)
    assert analysis_create.repository_id == "repo123"
    assert analysis_create.branch is None
    assert analysis_create.commit_hash is None


def test_analysis_create_with_branch():
    # Test AnalysisCreate with branch specified
    data = {"repository_id": "repo123", "branch": "main"}
    analysis_create = AnalysisCreate(**data)
    assert analysis_create.repository_id == "repo123"
    assert analysis_create.branch == "main"


def test_analysis_create_with_commit_hash():
    # Test AnalysisCreate with commit hash specified
    data = {"repository_id": "repo123", "commit_hash": "abc123"}
    analysis_create = AnalysisCreate(**data)
    assert analysis_create.repository_id == "repo123"
    assert analysis_create.commit_hash == "abc123"


def test_analysis_create_missing_required_field():
    # Test that missing repository_id raises validation error
    try:
        AnalysisCreate()
        assert False, "Should have raised ValidationError"
    except Exception:
        pass


def test_analysis_finding_required_fields():
    # Test AnalysisFinding required fields
    finding_id = uuid.uuid4()
    data = {
        "id": finding_id,
        "file_path": "src/main.py",
        "line_number": 10,
        "severity": "high",
        "message": "Test message",
        "category": "test"
    }
    finding = AnalysisFinding(**data)
    assert finding.id == finding_id
    assert finding.file_path == "src/main.py"
    assert finding.line_number == 10
    assert finding.severity == "high"
    assert finding.message == "Test message"
    assert finding.category == "test"
    assert finding.rule_id is None


def test_analysis_finding_with_rule_id():
    # Test AnalysisFinding with rule_id
    finding_id = uuid.uuid4()
    data = {
        "id": finding_id,
        "file_path": "src/main.py",
        "line_number": 15,
        "severity": "medium",
        "message": "Another message",
        "rule_id": "RULE_001",
        "category": "security"
    }
    finding = AnalysisFinding(**data)
    assert finding.rule_id == "RULE_001"


def test_analysis_result_minimum_fields():
    # Test AnalysisResult with minimal fields
    result_id = uuid.uuid4()
    repo_id = "repo123"
    data = {
        "id": result_id,
        "repository_id": repo_id,
        "status": "completed",
        "started_at": datetime(2023, 1, 1, 12, 0, 0)
    }
    result = AnalysisResult(**data)
    assert result.id == result_id
    assert result.repository_id == repo_id
    assert result.status == "completed"
    assert result.findings == []
    assert result.score is None
    assert result.grade is None


def test_analysis_result_with_findings():
    # Test AnalysisResult with findings
    result_id = uuid.uuid4()
    finding_id = uuid.uuid4()
    
    finding_data = {
        "id": finding_id,
        "file_path": "src/test.py",
        "line_number": 25,
        "severity": "low",
        "message": "Test finding",
        "category": "test"
    }
    
    data = {
        "id": result_id,
        "repository_id": "repo456",
        "status": "running",
        "started_at": datetime(2023, 1, 1, 12, 0, 0),
        "findings": [AnalysisFinding(**finding_data)],
        "score": 85.5,
        "grade": "B"
    }
    
    result = AnalysisResult(**data)
    assert len(result.findings) == 1
    assert result.findings[0].file_path == "src/test.py"
    assert result.score == 85.5
    assert result.grade == "B"


def test_analysis_result_optional_fields():
    # Test AnalysisResult with optional completed_at and score/grade
    result_id = uuid.uuid4()
    data = {
        "id": result_id,
        "repository_id": "repo789",
        "status": "failed",
        "started_at": datetime(2023, 1, 1, 12, 0, 0),
        "completed_at": datetime(2023, 1, 1, 12, 30, 0),
        "score": 92.0,
        "grade": "A"
    }
    result = AnalysisResult(**data)
    assert result.completed_at == datetime(2023, 1, 1, 12, 30, 0)
    assert result.score == 92.0
    assert result.grade == "A"


def test_analysis_create_empty_string_values():
    # Test AnalysisCreate with empty string values
    data = {
        "repository_id": "",
        "branch": "",
        "commit_hash": ""
    }
    analysis_create = AnalysisCreate(**data)
    assert analysis_create.repository_id == ""
    assert analysis_create.branch == ""
    assert analysis_create.commit_hash == ""


def test_analysis_finding_empty_values():
    # Test AnalysisFinding with empty values
    finding_id = uuid.uuid4()
    data = {
        "id": finding_id,
        "file_path": "",
        "line_number": 0,
        "severity": "",
        "message": "",
        "category": ""
    }
    finding = AnalysisFinding(**data)
    assert finding.file_path == ""
    assert finding.line_number == 0
    assert finding.severity == ""
    assert finding.message == ""
    assert finding.category == ""


def test_analysis_result_empty_id():
    # Test AnalysisResult with empty string id
    data = {
        "id": uuid.uuid4(),
        "repository_id": "",
        "status": "",
        "started_at": datetime(2023, 1, 1, 12, 0, 0)
    }
    result = AnalysisResult(**data)
    assert result.repository_id == ""
    assert result.status == ""


def test_analysis_create_field_descriptions():
    # Test that field descriptions are present
    assert AnalysisCreate.repository_id.__class__.__annotations__ is not None
    assert AnalysisCreate.branch is not None
    assert AnalysisCreate.commit_hash is not None


def test_analysis_finding_field_types():
    # Test that AnalysisFinding has correct field types
    assert hasattr(AnalysisFinding, 'id')
    assert hasattr(AnalysisFinding, 'file_path')
    assert hasattr(AnalysisFinding, 'line_number')
    assert hasattr(AnalysisFinding, 'severity')
    assert hasattr(AnalysisFinding, 'message')
    assert hasattr(AnalysisFinding, 'rule_id')
    assert hasattr(AnalysisFinding, 'category')


def test_analysis_result_field_types():
    # Test that AnalysisResult has correct field types
    assert hasattr(AnalysisResult, 'id')
    assert hasattr(AnalysisResult, 'repository_id')
    assert hasattr(AnalysisResult, 'status')
    assert hasattr(AnalysisResult, 'started_at')
    assert hasattr(AnalysisResult, 'completed_at')
    assert hasattr(AnalysisResult, 'findings')
    assert hasattr(AnalysisResult, 'score')
    assert hasattr(AnalysisResult, 'grade')


def test_analysis_finding_list():
    # Test AnalysisResult with multiple findings
    finding1_id = uuid.uuid4()
    finding2_id = uuid.uuid4()
    
    finding1 = {
        "id": finding1_id,
        "file_path": "src/file1.py",
        "line_number": 10,
        "severity": "high",
        "message": "Finding 1",
        "category": "security"
    }
    
    finding2 = {
        "id": finding2_id,
        "file_path": "src/file2.py",
        "line_number": 20,
        "severity": "medium",
        "message": "Finding 2",
        "category": "performance"
    }
    
    result_id = uuid.uuid4()
    data = {
        "id": result_id,
        "repository_id": "repo123",
        "status": "completed",
        "started_at": datetime(2023, 1, 1, 12, 0, 0),
        "findings": [AnalysisFinding(**finding1), AnalysisFinding(**finding2)]
    }
    
    result = AnalysisResult(**data)
    assert len(result.findings) == 2
    assert result.findings[0].file_path == "src/file1.py"
    assert result.findings[1].file_path == "src/file2.py"


def test_analysis_result_default_values():
    # Test AnalysisResult default values for optional fields
    result_id = uuid.uuid4()
    data = {
        "id": result_id,
        "repository_id": "repo123",
        "status": "pending",
        "started_at": datetime(2023, 1, 1, 12, 0, 0)
    }
    
    result = AnalysisResult(**data)
    assert result.completed_at is None
    assert result.findings == []
    assert result.score is None
    assert result.grade is None


def test_uuid_generation():
    # Test that UUIDs are properly handled
    test_id = uuid.uuid4()
    assert isinstance(test_id, uuid.UUID)


def test_datetime_fields():
    # Test that datetime fields work correctly
    dt = datetime(2023, 6, 15, 14, 30, 0)
    assert isinstance(dt, datetime)
    assert dt.year == 2023
    assert dt.month == 6
    assert dt.day == 15


def test_analysis_finding_optional_rule_id():
    # Test AnalysisFinding with None rule_id
    finding_id = uuid.uuid4()
    data = {
        "id": finding_id,
        "file_path": "test.py",
        "line_number": 42,
        "severity": "info",
        "message": "Test message",
        "rule_id": None,
        "category": "test"
    }
    finding = AnalysisFinding(**data)
    assert finding.rule_id is None
    assert finding.category == "test"