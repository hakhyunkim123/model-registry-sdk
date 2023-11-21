from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TrainingInfo(BaseModel):
    params: Optional[Dict] = Field(default=None)
    metrics: Optional[Dict] = Field(default=None)
    tags: Optional[Dict] = Field(default=None)


class InferenceInfo(BaseModel):
    metrics: Optional[Dict] = Field(default=None)


class ModelInfo(BaseModel):
    id: str = Field(description="P000001")
    name: str = Field(description="고객 알뜰 지수")
    eng_name: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, description="고객 알뜰 지수 입니다.")
    creation_time: Optional[str] = Field(default=None)
    stage: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    run_id: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    tags: Optional[Dict[str, Any]] = Field(default=None)

    config: Optional[Dict[str, Any]] = Field(default=None)
    train: Optional[TrainingInfo] = Field(default=None)
    inference: Optional[InferenceInfo] = Field(default=None)

    target_query: Optional[str] = Field(default=None)
    pdi_tag: Optional[str] = Field(default=None, description="D")
    category: Optional[str] = Field(default=None, description="상품단위")
    target: Optional[str] = Field(default=None, description="신규")
    target_condition: Optional[str] = Field(default=None, description='{"req1": "##"}')
    algorithm: Optional[str] = Field(default=None, description="LGBM")
    ob_term: Optional[str] = Field(default=None, description="24")
    complexity: Optional[str] = Field(default=None, description="5/5")
    predict_term: Optional[str] = Field(default=None, description="3")
    tvt_ratio: Optional[str] = Field(default=None, description="7/2/1")
    active_yn: Optional[int] = Field(default=None, description="1")
    reg_time: Optional[str] = Field(default=None, description="202311061213")
    data_jukja_dt: Optional[str] = Field(default=None, description="20231106")

    class Config:
        arbitrary_types_allowed = True
