from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
# from mlflow.entities.run_status import RunStatus


class RunStatus:
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    KILLED = "KILLED"


class RunType:
    BASE = "BASE"
    TRAIN = "TRAIN"
    RETRAIN = "RETRAIN"
    SERVING = "SERVING"


class RunInfo(BaseModel):
    experiment_id: str
    run_id: str
    run_name: str
    lifecycle_stage: str
    artifact_uri: str
    status: str
    user_id: str = Field(default=None)
    start_time: int = Field(default=None)
    end_time: Optional[int] = Field(default=None)


class RunData(BaseModel):
    metrics: Optional[Dict[str, float]] = Field(default={})
    params: Optional[Dict[str, Any]] = Field(default={})
    tags: Optional[Dict[str, str]] = Field(default={})


class Run(BaseModel):
    info: RunInfo
    data: RunData
    metadata: Optional[Dict[str, Any]] = Field(default={})
    logged_model: Optional[Dict] = Field(default={})
    artifact_data: Optional[Dict[str, Any]] = Field(default={})

    class Config:
        arbitrary_types_allowed = True

