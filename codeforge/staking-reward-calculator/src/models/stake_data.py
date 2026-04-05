from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ValidationError as PydanticValidationError
from typing import Union
import datetime


class StakeData(BaseModel):
    amount: float = Field(..., gt=0, description="The amount of tokens to stake")
    duration: int = Field(..., gt=0, description="Staking duration in days")
    network: str = Field(..., min_length=1, description="Blockchain network name")
    start_date: Union[datetime.datetime, None] = Field(default=None, description="Staking start date")
    
    @field_validator('amount', mode='before')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        from src.validator import validate_stake_amount
        if not validate_stake_amount(v):
            raise ValueError("Invalid stake amount")
        return v
        
    @field_validator('network', mode='before')
    @classmethod
    def validate_network(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Network name must be a non-empty string")
        return v.strip()

    @model_validator(mode='after')
    def validate_model(cls, self):
        # The network field will already be stripped by the field validator
        # but we ensure it's not empty after stripping
        if not self.network:
            raise PydanticValidationError("Network name cannot be empty", cls)
        return self

    class Config:
        str_strip_whitespace = True
        validate_assignment = True