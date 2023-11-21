from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field


class SACPTaskInfo(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASK_")

    task_id: str
    pod_name: str
    task_type: str = Field(alias="TASK_TYPE")
    project_id: str = Field(alias="PROJECT_ID")
    current_user: str = Field(alias="AICENTRO_CURRENT_USER")