from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class RepositoryBase(BaseModel):
    name: str
    url: HttpUrl
    description: Optional[str] = None


class RepositoryCreate(RepositoryBase):
    pass


class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None


class Repository(RepositoryBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    last_synced: Optional[datetime] = None
    findings: Optional[List[dict]] = []

    class Config:
        from_attributes = True


class RepositorySync(BaseModel):
    repository_id: UUID
    status: str
    last_commit_sha: Optional[str] = None


class RepositoryAnalysis(BaseModel):
    repository_id: UUID
    analysis_id: UUID
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    findings_count: int = 0
    vulnerabilities_count: int = 0

    class Config:
        from_attributes = True


class RepositoryListResponse(BaseModel):
    repositories: List[Repository]
    total: int
    page: int
    size: int