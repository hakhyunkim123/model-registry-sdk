from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any


# class TrainingModelInfo(BaseModel):
#     id: str = Field(description="P000001")
#     name: str = Field(description="고객 알뜰 지수")
#     description: Optional[str] = Field(default=None, description="고객 알뜰 지수 입니다.")
#     pdi_tag: str = Field(description="D")
#     category: str = Field(description="상품단위")
#     target: str = Field(description="신규")
#     target_condition: Dict[str, Any] = Field(description='{"req1": "##"}')
#     algorithm: str = Field(description="LGBM")
#     ob_term: str = Field(description="24")
#     complexity: str = Field(description="5/5")
#     predict_term: str = Field(description="3")
#     tvt_ratio: str = Field(description="7/2/1")
#     active_yn: Optional[int] = Field(default=None, description="1")
#     reg_time: Optional[int] = Field(default=None, description="202311061213")
#     data_jukja_dt: Optional[int] = Field(default=None, description="20231106")


class TrainingInfo(BaseModel):
    params: Optional[Dict] = Field(default=None)
    metrics: Optional[Dict] = Field(default=None)
    tags: Optional[Dict] = Field(default=None)


class InferenceInfo(BaseModel):
    metrics: Optional[Dict] = Field(default=None)


class ModelInfo(BaseModel):
    id: str = Field(description="P000001")
    name: str = Field(description="고객 알뜰 지수")
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
    pdi_tag: Optional[str] = Field(description="D")
    category: Optional[str] = Field(description="상품단위")
    target: Optional[str] = Field(description="신규")
    target_condition: Optional[Dict[str, Any]] = Field(description='{"req1": "##"}')
    algorithm: Optional[str] = Field(description="LGBM")
    ob_term: Optional[str] = Field(description="24")
    complexity: Optional[str] = Field(description="5/5")
    predict_term: Optional[str] = Field(description="3")
    tvt_ratio: Optional[str] = Field(description="7/2/1")
    active_yn: Optional[int] = Field(default=None, description="1")
    reg_time: Optional[str] = Field(default=None, description="202311061213")
    data_jukja_dt: Optional[str] = Field(default=None, description="20231106")

    class Config:
        arbitrary_types_allowed = True
