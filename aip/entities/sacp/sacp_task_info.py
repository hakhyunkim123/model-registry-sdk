from pydantic import BaseSettings, Field


class SACPTaskInfo(BaseSettings):
    task_id: str = Field(env="TASK_TASK_ID")
    pod_name: str = Field(env="TASK_POD_NAME")
    task_type: str = Field(env="TASK_TYPE")
    project_id: str = Field(env="PROJECT_ID")
    current_user: str = Field(env="AICENTRO_CURRENT_USER")


    # def to_dict(self):
    #     return {
    #     }
