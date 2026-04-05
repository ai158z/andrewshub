from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from typing import Union


class MetricBase(BaseModel):
    agent_id: int
    metric_type: str
    value: float
    timestamp: Optional[datetime] = None

    @field_validator('timestamp', mode='before')
    @classmethod
    def set_default_timestamp(cls, v: Union[datetime, None]) -> datetime:
        if v is None:
            return datetime.now()
        return v

    @field_validator('agent_id', 'value')
    @classmethod
    def validate_positive_numbers(cls, v, field):
        if field.field_name == 'agent_id' and v < 0:
            raise ValueError('agent_id must be positive')
        if field.field_name == 'value' and v < 0:
            raise ValueError('value must be positive')
        return v


class MetricCreate(MetricBase):
    pass


class Metric(MetricBase):
    id: int

    class Config:
        orm_mode = True

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v: datetime) -> datetime:
        if v is None:
            raise ValueError('timestamp cannot be None')
        return v

    def __str__(self):
        return f"Metric(id={self.id}, name='{self.metric_type}', value={self.value}, timestamp={self.timestamp})"

    def __repr__(self):
        return f"Metric(id={self.id}, name='{self.metric_type}', value={self.value}, timestamp={self.timestamp})"

    def __lt__(self, other):
        if not isinstance(other, Metric):
            raise ValueError("Can only compare with another Metric")
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, Metric):
            raise ValueError("Can only compare with another Metric")
        return self.value <= other.value

    def __gt__(self, other):
        if not isinstance(other, Metric):
            raise ValueError("Can only compare with another Metric")
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, Metric):
            raise ValueError("Can only compare with another Metric")
        return self.value >= other.value

    def __eq__(self, other):
        if not isinstance(other, Metric):
            return False
        return self.value == other.value and self.metric_type == other.metric_type

    def __ne__(self, other):
        if not isinstance(other, Metric):
            return True
        return not self.__eq__(other)