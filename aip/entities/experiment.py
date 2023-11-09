from pydantic import BaseModel, Field
from typing import Dict


class Experiment(BaseModel):
    experiment_id: str = Field(alias="experiment_id")
    name: str = Field(alias="name")
    artifact_location: str = Field(alias="artifact_location")
    lifecycle_stage: str = Field(alias="lifecycle_stage")
    tags: Dict = Field(default=None, alias="tags")
    creation_time: int = Field(alias="creation_time")
    last_update_time: int = Field(alias="last_update_time")
