import pytest
from unittest.mock import AsyncMock, Mock, patch, mock_open
from sqlalchemy.orm import Session
from backend.src.models.repository import Repository
from backend.src.models.analysis import AnalysisResult
from backend.src.services.code_analyzer import CodeAnalyzerService

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def analyzer_service(mock_db):
    return CodeAnalyzerService(mock_db)

@pytest.fixture
def mock_repository():
    repo = Mock(spec=Repository)
    repo.id = 1
    repo.url = "https://github.com/test/repo"
    return repo

@pytest.mark.asyncio
async def test_run_analysis_success(analyzer_service, mock_repository, mock_db):
    # Setup
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    with patch('subprocess.run') as mock_run, \
         patch('tempfile.TemporaryDirectory') as mock_temp_dir, \
         patch('json.loads') as mock_json_loads:
        
        mock_temp_dir.return_value.__enter__.return_value = '/tmp/test'
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = '[]'
        mock_json_loads.return_value = []
        
        # Mock repository files
        with patch('pathlib.Path.rglob') as mock_rglob:
            mock_rglob.return_value = []
            
            # Mock AnalysisResult
            mock_analysis_result = Mock(spec=AnalysisResult)
            mock_analysis_result.status = "completed"
            mock_analysis_result.findings = []
            
            with patch.object(analyzer_service, '_clone_repository', AsyncMock(return_value=True)), \
                 patch.object(analyzer_service, '_run_code_quality_analysis', AsyncMock(return_value=[])), \
                 patch.object(analyzer_service, 'scan_for_vulnerabilities', AsyncMock(return_value=[])):
                
                result = await analyzer_service.run_analysis(mock_repository)
                assert result is not None

@pytest.mark.asyncio
async def test_run_analysis_failure(analyzer_service, mock_repository, mock_db):
    with patch.object(analyzer_service, '_clone_repository', AsyncMock(return_value=False)), \
         patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 1
        
        with pytest.raises(Exception):
            await analyzer_service.run_analysis(mock_repository)

@pytest.mark.asyncio
async def test_clone_repository_success(analyzer_service):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        result = await analyzer_service._clone_repository("http://test.com/repo", "/tmp/test")
        assert result is True

@pytest.mark.asyncio
async def test_clone_repository_timeout(analyzer_service):
    with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("git", 1)):
        result = await analyzer_service._clone_repository("http://test.com/repo", "/tmp/test")
        assert result is False

@pytest.mark.asyncio
async def test_clone_repository_exception(analyzer_service):
    with patch('subprocess.run', side_effect=Exception("Git error")):
        result = await analyzer_service._clone_repository("http://test.com/repo", "/tmp/test")
        assert result is False

@pytest.mark.asyncio
async def test_run_pylint_success(analyzer_service):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.rglob') as mock_rglob, \
         patch('builtins.open', mock_open(read_data='[{"line": 1, "message": "test", "symbol": "test"}]')):
        
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = '[{"line": 1, "message": "test", "symbol": "test"}]'
        mock_rglob.return_value = ["/tmp/test/file.py"]
        
        result = await analyzer_service._run_pylint("/tmp/test")
        assert isinstance(result, list)

@pytest.mark.asyncio
async def test_run_bandit_success(analyzer_service):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = '{"results": []}'
        
        result = await analyzer_service._run_bandit("/tmp/test")
        assert isinstance(result, list)

@pytest.mark.asyncio
async def test_run_pycodestyle_success(analyzer_service):
    with patch('subprocess.run') as mock_run, \
         patch('pathlib.Path.rglob') as mock_rglob:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "/tmp/test/file.py:1:1: E123 test error"
        mock_rglob.return_value = ["/tmp/test/file.py"]
        
        result = await analyzer_service._run_pycodestyle("/tmp/test")
        assert isinstance(result, list)

def test_pylint_type_to_severity(analyzer_service):
    assert analyzer_service._pylint_type_to_severity("convention") == "info"
    assert analyzer_service._pylint_type_to_severity("warning") == "warning"
    assert analyzer_service._pylint_type_to_severity("unknown") == "warning"

@pytest.mark.asyncio
async def test_scan_for_vulnerabilities_success(analyzer_service):
    with patch('builtins.open', mock_open(read_data='test code')), \
         patch('backend.src.services.code_analyzer.scan_code', return_value=[{"test": "finding"}]):
        result = await analyzer_service.scan_for_vulnerabilities(["/tmp/test.py"])
        assert len(result) > 0

@pytest.mark.asyncio
async def test_scan_for_vulnerabilities_file_error(analyzer_service):
    with patch('builtins.open', side_effect=Exception("File error")):
        result = await analyzer_service.scan_for_vulnerabilities(["/tmp/test.py"])
        assert result == []

def test_check_dependencies_success(analyzer_service):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "test-package 1.0.0 12345 vulnerability in package"
        
        result = analyzer_service.check_dependencies("/tmp/requirements.txt")
        assert isinstance(result, list)

def test_check_dependencies_no_vulnerabilities(analyzer_service):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        
        result = analyzer_service.check_dependencies("/tmp/requirements.txt")
        assert result == []

def test_check_dependencies_error(analyzer_service):
    with patch('subprocess.run', side_effect=Exception("safety error")):
        result = analyzer_service.check_dependencies("/tmp/requirements.txt")
        assert result == []