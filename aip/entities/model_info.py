from pandas import DataFrame
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ModelInfo(BaseModel):
    # Mlflow ModelVersion data
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

    # Config Data
    config: Optional[Dict[str, Any]] = Field(default=None, repr=False)

    # Table ModelInfo Data
    eng_name: Optional[str] = Field(default=None)
    target_query: Optional[str] = Field(default=None, repr=False)
    pdi_tag: Optional[str] = Field(default=None, description="D")
    category: Optional[str] = Field(default=None, description="상품단위")
    target: Optional[str] = Field(default=None, description="신규")
    target_condition: Optional[str] = Field(default=None, description='{"req1": "##"}', repr=False)
    algorithm: Optional[str] = Field(default=None, description="LGBM")
    ob_term: Optional[str] = Field(default=None, description="24")
    complexity: Optional[str] = Field(default=None, description="5/5")
    predict_term: Optional[str] = Field(default=None, description="3")
    tvt_ratio: Optional[str] = Field(default=None, description="7/2/1")
    active_yn: Optional[int] = Field(default=None, description="1")
    reg_time: Optional[str] = Field(default=None, description="202311061213")
    data_jukja_dt: Optional[str] = Field(default=None, description="20231106")

    @classmethod
    def from_vertica_entity(cls, data) -> "ModelInfo":
        if isinstance(data, DataFrame):
            data_dict = data.to_dict('records')[0]
        elif isinstance(data, Dict):
            data_dict = data
        else:
            raise NotImplementedError
        return cls(
            id=data_dict.get("model_id"),
            name=data_dict.get("model_name"),
            eng_name=data_dict.get("model_eng_name"),
            description=data_dict.get("model_description", None),
            version=data_dict.get("model_version", None),
            pdi_tag=data_dict.get("model_tag"),
            category=data_dict.get("model_category"),
            target=data_dict.get("model_target"),
            target_condition=data_dict.get("model_target_condition"),
            algorithm=data_dict.get("model_algorithm"),
            ob_term=data_dict.get("model_ob_term"),
            complexity=data_dict.get("model_complexity"),
            predict_term=data_dict.get("model_predict_term"),
            tvt_ratio=data_dict.get("model_tvt_ratio"),
            active_yn=data_dict.get("model_active_yn"),
            target_query=data_dict.get("model_target_query"),
            reg_time=data_dict.get("model_reg_time"),
            data_jukja_dt=data_dict.get("data_jukja_dt")
        )

    class Config:
        arbitrary_types_allowed = True
