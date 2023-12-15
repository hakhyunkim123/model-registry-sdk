from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from aip.entities.model_info import ModelInfo


class ModelVersionStage:
    STAGE_NONE = "None"
    STAGE_STAGING = "Staging"
    STAGE_PRODUCTION = "Production"
    STAGE_ARCHIVED = "Archived"


class ModelVersion(BaseModel):
    name: str
    version: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    current_stage: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    run_id: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    tags: Optional[Dict[str, Any]] = Field(default=None, repr=False)
    creation_timestamp: int
    last_updated_timestamp: int
    info: Optional[ModelInfo] = Field(default=None)
