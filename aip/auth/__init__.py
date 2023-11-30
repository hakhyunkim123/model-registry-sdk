from pydantic import BaseSettings, Field


class AuthConfig(BaseSettings):
    username: str = Field(env="AIP_USERNAME")
    password: str = Field(env="AIP_PASSWORD")
