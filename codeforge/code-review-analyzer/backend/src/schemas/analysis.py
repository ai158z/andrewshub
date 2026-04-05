from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from uuid import UUID


class AnalysisCreate(BaseModel):
    repository_id: str = Field(..., description="The ID of the repository to analyze")
    branch: Optional[str] = Field(None, description="The branch to analyze")
    commit_hash: Optional[str] = Field(None, description="Specific commit to analyze")

    model_config = ConfigDict(from_attributes=True)


class AnalysisFinding(BaseModel):
    id: UUID
    file_path: str
    line_number: int
    severity: str
    message: str
    rule_id: Optional[str] = None
    category: str

    model_config = ConfigDict(from_attributes=True)


class AnalysisResult(BaseModel):
    id: UUID
    repository_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    findings: List[AnalysisFinding] = Field(default_factory=list)
    score: Optional[float] = None
    grade: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)