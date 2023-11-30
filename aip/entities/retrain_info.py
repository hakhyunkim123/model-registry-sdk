from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from aip.entities.metric import NCAIMetric


class RetrainInfo(BaseModel):
    run_id: str
    model_name: str
    model_version: str
    creation_time: int
    params: Optional[Dict[str, Any]] = Field(default={})
    metrics: Optional[Dict[str, float]] = Field(default={})
    ncai_metrics: Optional[List[NCAIMetric]] = Field(default=[])


class RetrainHistory(BaseModel):
    retrain_history: List[RetrainInfo]