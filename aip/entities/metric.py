from pydantic import BaseModel, Field
from typing import Optional
from aip.utils.timeutils import get_current_time_millis


class Metric(BaseModel):
    key: str
    value: float
    timestamp: Optional[int] = Field(default=None)
    step: Optional[int] = Field(default=0)


class NCAIMetric(BaseModel):
    metric_code_id: str
    metric_seq: str
    threshold: Optional[float]
    numeric_value: float
    object_value: str
    metric_cal_time: int = Field(default=get_current_time_millis())
    data_jukja_dt: str