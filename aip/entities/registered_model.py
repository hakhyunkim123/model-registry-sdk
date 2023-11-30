from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from aip.entities.model_version import ModelVersion


class RegisteredModel(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    tags: Optional[Dict] = Field(default=None)
    latest_versions: Optional[List[ModelVersion]] = Field(default=[])
    creation_timestamp: int
    last_updated_timestamp: int
    aliases: Optional[Dict[str, Any]] = Field(default={})
