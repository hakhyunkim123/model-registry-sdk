from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from aip.entities.run import Run


class ModelVersion(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=()
    )

    model_uuid: Optional[str] = Field(default=None)
    name: str
    version: str
    run_id: Optional[str] = Field(default=None)
    source: str
    description: Optional[str] = Field(default=None)
    tags: Optional[Dict] = Field(default=None)
    current_stage: Optional[str]
    status_message: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    run_link: Optional[str] = Field(default=None)
    aliases: Optional[List[Dict]] = Field(default=[])
    creation_timestamp: Optional[int]
    last_updated_timestamp: Optional[int]
    metadata: Optional[Dict] = Field(default={})
    run: Optional[Run] = Field(default={})
