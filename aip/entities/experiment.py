from pydantic import BaseModel, Field
from typing import Optional, Dict


class Experiment(BaseModel):
    experiment_id: str
    name: str
    artifact_location: str
    lifecycle_stage: str
    tags: Optional[Dict[str, str]] = Field(default={})
    creation_time: int
    last_update_time: int
