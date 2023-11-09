from pydantic import BaseModel, Field
from typing import Any


class Param(BaseModel):
    key: str
    value: Any