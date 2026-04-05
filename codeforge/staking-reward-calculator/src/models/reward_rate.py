from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RewardRate(BaseModel):
    network: str
    annual_rate: float = Field(..., gt=0, le=100)
    timestamp: datetime
    validator_address: Optional[str] = None
    commission_rate: Optional[float] = Field(None, ge=0, le=100)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
    
    def get_effective_rate(self) -> float:
        """Calculate the effective annual rate after commission if applicable"""
        if self.commission_rate is not None:
            return self.annual_rate * (1 - self.commission_rate / 100)
        return self.annual_rate