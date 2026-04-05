from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union
from datetime import datetime

class MetricBase(BaseModel):
    value: Union[float, int]
    timestamp: datetime
    agent_id: Optional[int] = None
    unit: Optional[str] = None
    description: Optional[str] = None

class MetricCreate(MetricBase):
    pass

class MetricResponse(MetricBase):
    id: int
    data: List[dict] = []

    model_config = ConfigDict(from_attributes=True)

class MetricListResponse(BaseModel):
    data: List[MetricResponse]

    model_config = ConfigDict(from_attributes=True)

class MetricResponseList(BaseModel):
    data: List[MetricResponse]

    model_config = ConfigDict(from_attributes=True)

class MetricCreateList(MetricBase):
    pass

class MetricBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)