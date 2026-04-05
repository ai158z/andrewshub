import enum
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.core.database import Base

# Add missing Pydantic models for API/DTO usage
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SeverityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    findings_count = Column(Integer, default=0, nullable=False)
    high_findings_count = Column(Integer, default=0, nullable=False)
    medium_findings_count = Column(Integer, default=0, nullable=False)
    low_findings_count = Column(Integer, default=0, nullable=False)
    grade = Column(String(1), nullable=True)
    lines_of_code = Column(Integer, nullable=True)
    cyclomatic_complexity = Column(Float, nullable=True)
    score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    repository = relationship("Repository", back_populates="analysis_results")
    findings = relationship("AnalysisFinding", back_populates="analysis_result", cascade="all, delete-orphan")

    @validates('status')
    def validate_status(self, key, value):
        if value not in AnalysisStatus.__members__.values():
            raise ValueError(f"Invalid status: {value}")
        return value

    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, repository_id={self.repository_id}, status={self.status})>"


class AnalysisFinding(Base):
    __tablename__ = "analysis_findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analysis_results.id"), nullable=False)
    file_path = Column(Text, nullable=False)
    line_number = Column(Integer, nullable=True)
    severity = Column(Enum(SeverityLevel), nullable=False)
    issue_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    suggestion = Column(Text, nullable=True)
    code_snippet = Column(Text, nullable=True)
    is_violation = Column(Boolean, default=True, nullable=False)
    rule_id = Column(String, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    analysis_result = relationship("AnalysisResult", back_populates="findings")

    @validates('severity')
    def validate_severity(self, key, value):
        if value not in SeverityLevel.__members__.values():
            raise ValueError(f"Invalid severity: {value}")
        return value

    def __repr__(self):
        return f"<AnalysisFinding(id={self.id}, analysis_id={self.analysis_id}, issue_type={self.issue_type})>"


# Pydantic models for API/DTO usage
class AnalysisCreate(BaseModel):
    repository_id: uuid.UUID
    branch: Optional[str] = None
    commit_hash: Optional[str] = None


class AnalysisUpdate(BaseModel):
    status: Optional[AnalysisStatus] = None
    completed_at: Optional[datetime] = None
    findings_count: Optional[int] = None
    high_findings_count: Optional[int] = None
    medium_findings_count: Optional[int] = None
    low_findings_count: Optional[int] = None
    grade: Optional[str] = None
    lines_of_code: Optional[int] = None
    cyclomatic_complexity: Optional[float] = None
    score: Optional[int] = None


class FindingCreate(BaseModel):
    file_path: str
    line_number: Optional[int] = None
    severity: SeverityLevel
    issue_type: str
    description: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    is_violation: bool = True
    rule_id: Optional[str] = None
    category: Optional[str] = None


class FindingUpdate(BaseModel):
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    severity: Optional[SeverityLevel] = None
    issue_type: Optional[str] = None
    description: Optional[str] = None
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    is_violation: Optional[bool] = None
    rule_id: Optional[str] = None
    category: Optional[str] = None