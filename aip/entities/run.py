from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any


class RunInfo(BaseModel):
    experiment_id: str = Field(alias="experiment_id")
    run_id: str = Field(alias="run_id")
    run_name: str = Field(alias="run_name")
    lifecycle_stage: str = Field(alias="lifecycle_stage")
    artifact_uri: str = Field(alias="artifact_uri")
    status: str = Field(alias="status")
    user_id: str = Field(default=None, alias="user_id")
    start_time: int = Field(default=None, alias="start_time")
    end_time: Optional[int] = Field(default=None, alias="end_time")


class RunData(BaseModel):
    metrics: Optional[Dict[str, float]] = Field(default=None, alias="metrics")
    params: Optional[Dict[str, Any]] = Field(default=None, alias="params")
    tags: Optional[Dict[str, str]] = Field(default=None, alias="tags")


class Run(BaseModel):
    info: RunInfo = Field(default=None, alias="info")
    data: RunData = Field(default=None, alias="data")
    artifact_data: Optional[Dict[str, Any]] = Field(default={})
    logged_model: Optional[Dict] = Field(default={})

    class Config:
        arbitrary_types_allowed = True

