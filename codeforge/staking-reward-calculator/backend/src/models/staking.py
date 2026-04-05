from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StakingCalculation(BaseModel):
    stake_amount: float = Field(..., gt=0)
    network: str = Field(..., min_length=1)
    duration_days: int = Field(..., gt=0, le=3650)
    compound_frequency: Optional[int] = Field(default=365, ge=1)
    include_price_change: bool = Field(default=False)
    price_change_percentage: Optional[float] = Field(default=0.0, ge=-100.0, le=100.0)

    class Config:
        orm_mode = True

class StakingResult(BaseModel):
    total_rewards: float
    total_value: float
    roi_percentage: float
    apy: float
    projected_values: Optional[dict] = None
    calculation_time: Optional[datetime] = None

    class Config:
        orm_mode = True

class NetworkStats(Base):
    __tablename__ = "network_stats"

    id = Column(Integer, primary_key=True, index=True)
    network_name = Column(String, index=True)
    total_staked = Column(Float)
    total_rewards = Column(Float)
    average_apy = Column(Float)
    active_stakers = Column(Integer)
    total_validators = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NetworkStats(network_name='{self.network_name}', total_staked={self.total_staked}, total_rewards={self.total_rewards})>"