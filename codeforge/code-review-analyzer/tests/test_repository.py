import uuid
from datetime import datetime
from typing import List
import pytest
from pydantic import ValidationError
from backend.src.schemas.repository import (
    RepositoryBase, RepositoryCreate, RepositoryUpdate, Repository, 
    RepositorySync, RepositoryAnalysis, RepositoryListResponse
)

@pytest.fixture
def valid_http_url():
    return "https://github.com/example/repo"

@pytest.fixture
def valid_uuid():
    return uuid.uuid4()

def test_repository_base_valid_data(valid_http_url):
    data = {"name": "test-repo", "url": valid_http_url, "description": "A test repository"}
    repo = RepositoryBase(**data)
    assert repo.name == "test-repo"
    assert str(repo.url) == valid_http_url
    assert repo.description == "A test repository"

def test_repository_base_invalid_url():
    with pytest.raises(ValidationError):
        RepositoryBase(name="test-repo", url="not-a-url", description="Invalid URL")

def test_repository_create_inherits_from_repository_base(valid_http_url):
    data = {"name": "test-repo", "url": valid_http_url}
    repo_create = RepositoryCreate(**data)
    assert repo_create.name == "test-repo"

def test_repository_update_allows_optional_fields():
    update = RepositoryUpdate()
    assert update.name is None
    assert update.url is None
    assert update.description is None

    update_with_values = RepositoryUpdate(name="new-name", url="http://example.com", description="new desc")
    assert update_with_values.name == "new-name"

def test_repository_model_with_all_required_fields(valid_http_url, valid_uuid):
    repo_id = valid_uuid
    owner_id = valid_uuid
    now = datetime.now()
    
    repo = Repository(
        id=repo_id,
        owner_id=owner_id,
        name="test-repo",
        url=valid_http_url,
        created_at=now,
        updated_at=now
    )
    
    assert repo.id == repo_id
    assert repo.owner_id == owner_id
    assert repo.is_active is True

def test_repository_model_defaults():
    repo_id = uuid.uuid4()
    owner_id = uuid.uuid4()
    now = datetime.now()
    
    repo = Repository(
        id=repo_id,
        owner_id=owner_id,
        name="test",
        url="http://example.com",
        created_at=now,
        updated_at=now
    )
    
    assert repo.is_active is True
    assert repo.findings == []
    assert repo.last_synced is None

def test_repository_sync_model():
    repo_id = uuid.uuid4()
    sync = RepositorySync(repository_id=repo_id, status="success", last_commit_sha="abc123")
    
    assert sync.repository_id == repo_id
    assert sync.status == "success"
    assert sync.last_commit_sha == "abc123"

def test_repository_analysis_model():
    repo_id = uuid.uuid4()
    analysis_id = uuid.uuid4()
    now = datetime.now()
    
    analysis = RepositoryAnalysis(
        repository_id=repo_id,
        analysis_id=analysis_id,
        status="running",
        started_at=now
    )
    
    assert analysis.repository_id == repo_id
    assert analysis.analysis_id == analysis_id
    assert analysis.status == "running"
    assert analysis.started_at == now
    assert analysis.findings_count == 0
    assert analysis.vulnerabilities_count == 0

def test_repository_list_response():
    repo_id = uuid.uuid4()
    owner_id = uuid.uuid4()
    now = datetime.now()
    
    repo = Repository(
        id=repo_id,
        owner_id=owner_id,
        name="test",
        url="http://example.com",
        created_at=now,
        updated_at=now
    )
    
    response = RepositoryListResponse(
        repositories=[repo],
        total=1,
        page=1,
        size=10
    )
    
    assert response.total == 1
    assert response.page == 1
    assert response.size == 10
    assert len(response.repositories) == 1

def test_repository_analysis_optional_completed_at():
    now = datetime.now()
    analysis = RepositoryAnalysis(
        repository_id=uuid.uuid4(),
        analysis_id=uuid.uuid4(),
        status="completed",
        started_at=now,
        completed_at=now
    )
    
    assert analysis.completed_at == now

def test_repository_url_validation():
    with pytest.raises(ValidationError):
            RepositoryBase(name="test", url="not-a-valid-url")

def test_repository_url_valid_urls():
    valid_urls = [
        "https://github.com/user/repo",
        "http://github.com/user/repo",
        "https://gitlab.com/group/project"
    ]
    
    for url in valid_urls:
        repo = RepositoryBase(name="test-repo", url=url)
        assert str(repo.url) == url

def test_empty_repository_list():
    response = RepositoryListResponse(
        repositories=[],
        total=0,
        page=1,
        size=10
    )
    
    assert response.repositories == []
    assert response.total == 0
    assert response.page == 1
    assert response.size == 10

def test_repository_update_partial_update():
    update = RepositoryUpdate(name="updated-name")
    assert update.name == "updated-name"
    assert update.url is None
    assert update.description is None

def test_repository_model_config_from_orm():
    # Test that the Config allows from_orm by creating a model from dict
    repo_data = {
        "id": str(uuid.uuid4()),
        "owner_id": str(uuid.uuid4()),
        "name": "test",
        "url": "http://example.com",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True
    }
    
    repo = Repository.model_validate(repo_data)
    assert repo.name == "test"

def test_repository_analysis_minimal_fields():
    now = datetime.now()
    analysis = RepositoryAnalysis(
        repository_id=uuid.uuid4(),
        analysis_id=uuid.uuid4(),
        status="pending",
        started_at=now
    )
    
    assert analysis.status == "pending"
    assert analysis.findings_count == 0
    assert analysis.vulnerabilities_count == 0

def test_repository_base_no_description():
    repo = RepositoryBase(name="test", url="http://example.com")
    assert repo.description is None

def test_repository_update_all_fields_none_by_default():
    update = RepositoryUpdate()
    assert update.name is None
    assert update.url is None
    assert update.description is None

def test_repository_list_response_defaults():
    response = RepositoryListResponse(
        repositories=[],
        total=0,
        page=1,
        size=50
    )
    assert response.total == 0
    assert response.repositories == []

def test_repository_sync_optional_fields():
    sync = RepositorySync(repository_id=uuid.uuid4(), status="pending")
    assert sync.status == "pending"
    assert sync.last_commit_sha is None