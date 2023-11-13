from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

# from aip.entities.metric import


class TrainingModelInfo(BaseModel):
    id: str = Field(description="P000001")
    name: str = Field(description="고객 알뜰 지수")
    description: Optional[str] = Field(default=None, description="고객 알뜰 지수 입니다.")
    pdi_tag: str = Field(description="D")
    category: str = Field(description="상품단위")
    target: str = Field(description="신규")
    target_condition: Dict[str, Any] = Field(description='{"req1": "##"}')
    algorithm: str = Field(description="LGBM")
    ob_term: str = Field(description="24")
    complexity: str = Field(description="5/5")
    predict_term: str = Field(description="3")
    tvt_ratio: str = Field(description="7/2/1")
    active_yn: Optional[int] = Field(default=None, description="1")
    reg_time: Optional[int] = Field(default=None, description="202311061213")
    data_jukja_dt: Optional[int] = Field(default=None, description="20231106")


class TrainingInfo(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=()
    )
    model_info: TrainingModelInfo
    model_target_query: Optional[str] = Field(default=None)


class InferenceInfo(BaseModel):
    metrics: Dict


class ModelInfo(BaseModel):
    id: str
    name: str
    version: Optional[str] = Field(default=None)
    tags: Optional[Dict[str, Any]] = Field(default=None)
    config: Optional[Dict[str, Any]] = Field(default=None)
    train: Optional[TrainingInfo] = Field(default=None)
    inference: Optional[InferenceInfo] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
