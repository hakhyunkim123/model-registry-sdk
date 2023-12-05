from pydantic import BaseModel, Field
from typing import Optional


class Metric(BaseModel):
    key: str
    value: float
    timestamp: Optional[int] = Field(default=None)
    step: Optional[int] = Field(default=0)


class NCAIMetric(BaseModel):
    metric_code_id: str
    metric_seq: str
    threshold: Optional[float] = Field(default=None)
    numeric_value: float
    object_value: Optional[str] = Field(default=None)
    metric_cal_time: Optional[str] = Field(default=None)
    data_jukja_dt: Optional[str] = Field(default=None)