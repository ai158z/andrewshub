import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.routes.repositories import list_repositories, add_repository, sync_repository
from src.models.repository import Repository
from src.schemas.repository import RepositoryCreate
from src.services.github_service import GitHubRepo

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_current_user():
    user = MagicMock()
    user.id = 1
    user.username = "testuser"
    return user

@pytest.fixture
def mock_repository():
    repo = MagicMock(spec=Repository)
    repo.id = "test-repo-id"
    repo.name = "test-repo"
    repo.owner_name = "testuser"
    repo.url = "https://github.com/testuser/test-repo"
    repo.is_active = True
    return repo

def test_list_repositories_success(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db):
        mock_db.query().filter().all.return_value = []
        result = list_repositories(db=mock_db, current_user=mock_current_user)
        assert result == []

def test_list_repositories_db_error(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db):
        mock_db.query.side_effect = Exception("DB error")
        with pytest.raises(HTTPException) as exc_info:
            list_repositories(db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 500

def test_add_repository_success(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db), \
         patch('src.api.routes.repositories.github_get_repo') as mock_github_get:
        
        github_repo = MagicMock()
        github_repo.name = "test-repo"
        github_repo.owner.login = "testuser"
        github_repo.html_url = "https://github.com/testuser/test-repo"
        mock_github_get.return_value = github_repo
        
        repo_create = RepositoryCreate(url="https://github.com/testuser/test-repo")
        mock_db.query().filter().first.return_value = None
        
        result = add_repository(repository=repo_create, db=mock_db, current_user=mock_current_user)
        
        assert result.name == "test-repo"

def test_add_repository_invalid_url(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db):
        repo_create = RepositoryCreate(url="invalid-url")
        with pytest.raises(HTTPException) as exc_info:
            add_repository(repository=repo_create, db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 400

def test_add_repository_already_exists(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db):
        mock_db.query().filter().first.return_value = MagicMock()
        repo_create = RepositoryCreate(url="https://github.com/testuser/existing-repo")
        with pytest.raises(HTTPException) as exc_info:
            add_repository(repository=repo_create, db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 409

def test_add_repository_github_not_found(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db), \
         patch('src.api.routes.repositories.github_get_repo', side_effect=Exception("Not found")):
        mock_db.query().filter().first.return_value = None
        repo_create = RepositoryCreate(url="https://github.com/testuser/nonexistent-repo")
        with pytest.raises(HTTPException) as exc_info:
            add_repository(repository=repo_create, db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 400

def test_add_repository_db_error(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db), \
         patch('src.api.routes.repositories.github_get_repo') as mock_github_get:
        github_repo = MagicMock()
        github_repo.name = "test-repo"
        github_repo.owner.login = "testuser"
        github_repo.html_url = "https://github.com/testuser/test-repo"
        mock_github_get.return_value = github_repo
        
        mock_db.add.side_effect = Exception("DB error")
        repo_create = RepositoryCreate(url="https://github.com/testuser/test-repo")
        with pytest.raises(HTTPException) as exc_info:
            add_repository(repository=repo_create, db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 500

def test_sync_repository_success(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db), \
         patch('src.api.routes.repositories.sync_pull_requests') as mock_sync_pr, \
         patch('src.api.routes.repositories.run_analysis') as mock_run_analysis:
        
        mock_repo = MagicMock()
        mock_repo.id = "test-repo-id"
        mock_db.query().filter().first.return_value = mock_repo
        mock_run_analysis.return_value = MagicMock(id="test-analysis-id")
        
        result = sync_repository(repository_id="test-repo-id", db=mock_db, current_user=mock_current_user)
        
        assert result["status"] == "success"
        assert "analysis_id" in result

def test_sync_repository_not_found(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db):
        mock_db.query().filter().first.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            sync_repository(repository_id="nonexistent-id", db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 404

def test_sync_repository_error(mock_db, mock_current_user):
    with patch('src.api.routes.repositories.get_db', return_value=mock_db), \
         patch('src.api.routes.repositories.sync_pull_requests', side_effect=Exception("Sync error")):
        
        mock_repo = MagicMock()
        mock_repo.id = "test-repo-id"
        mock_db.query().filter().first.return_value = mock_repo
        
        with pytest.raises(HTTPException) as exc_info:
            sync_repository(repository_id="test-repo-id", db=mock_db, current_user=mock_current_user)
        assert exc_info.value.status_code == 500

def test_add_repository_url_parsing():
    # Test with valid GitHub URL
    repo_create = RepositoryCreate(url="https://github.com/user/repo")
    assert repo_create.url == "https://github.com/user/repo"

def test_add_repository_url_parsing_edge_cases():
    # Test with trailing slash
    repo_create = RepositoryCreate(url="https://github.com/user/repo/")
    assert repo_create.url == "https://github.com/user/repo/"

def test_add_repository_url_parsing_invalid():
    # Test with invalid URL
    repo_create = RepositoryCreate(url="invalid")
    assert repo_create.url == "invalid"