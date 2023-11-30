from typing import Optional, List, Dict, Any, Tuple

import aip._internal._model_regisry_service as model_registry_service
from aip.entities.registered_model import RegisteredModel
from aip.entities.model_version import ModelVersion
from aip.entities.retrain_info import RetrainInfo
from aip.exceptions import APIException


def create_registered_model(
        name: str,
        tags: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
) -> RegisteredModel:
    return model_registry_service.create_registered_model(name, tags, description)


def get_registered_model(name: str) -> Optional[RegisteredModel]:
    try:
        model = model_registry_service.get_registered_model(name)
    except APIException as error:
        if error.error_code == "RESOURCE_DOES_NOT_EXIST":
            return None
        else:
            raise
    return model


def search_registered_models(filter_string: Optional[str] = None,) -> List[RegisteredModel]:
    return model_registry_service.search_registered_models(filter_string)

# def search_registered_models(
#         filter_string: Optional[str] = None,
#         max_results: int = 1000,
#         order_by: Optional[List[str]] = None,
#         page_token: Optional[str] = None
# ) -> Tuple[List[RegisteredModel], str]:
#     return model_registry_service.search_registered_models(filter_string, max_results, order_by, page_token)


def get_latest_model_version(
        name: str,
        stages: Optional[List[str]] = None,
        detail: bool = True
) -> ModelVersion:
    return model_registry_service.get_latest_model_version(name, stages, detail)


def update_registered_model(name: str, description: Optional[str] = None) -> RegisteredModel:
    raise NotImplementedError


def rename_registered_model(name: str, new_name: str) -> RegisteredModel:
    raise NotImplementedError


def set_registered_model_alias(name: str, alias: str, version: str) -> None:
    raise NotImplementedError


def set_registered_model_tag(name: str, key: str, value: Any) -> None:
    model_registry_service.set_registered_model_tag(name, key, value)


def delete_registered_model_tag(name: str, key: str) -> None:
    model_registry_service.delete_registered_model_tag(name, key)


def delete_registered_model(name: str) -> None:
    model_registry_service.delete_registered_model(name)


def delete_registered_model_alias(name: str, alias: str) -> None:
    raise NotImplementedError


def create_model_version(
        name: str,
        source: Optional[str] = None,
        run_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        # run_link: Optional[str] = None,
        description: Optional[str] = None,
        vertica_insert: bool = True
) -> ModelVersion:
    return model_registry_service.create_model_version(
        name=name,
        source=source,
        run_id=run_id,
        tags=tags,
        description=description,
        vertica_insert=vertica_insert
    )


def get_model_version(name: str, version: str, detail: bool = False) -> ModelVersion:
    return model_registry_service.get_model_version(name, version, detail)


def get_retrain_history(name: str, version: str) -> List[RetrainInfo]:
    return model_registry_service.get_retrain_history(name, version)


def search_model_versions(filter_string: Optional[str] = None, detail: bool = False) -> List[ModelVersion]:
    return model_registry_service.search_model_versions(filter_string, detail)


# def search_model_versions(
#         filter_string: Optional[str] = None,
#         max_results: int = 1000,
#         order_by: Optional[List[str]] = None,
#         page_token: Optional[str] = None,
# ) -> Tuple[List[ModelVersion], str]:
#     return search_model_versions(filter_string, max_results, order_by, page_token)


def get_model_version_by_alias(name: str, alias: str) -> ModelVersion:
    raise NotImplementedError


def get_model_version_download_uri(name: str, version: str) -> str:
    return model_registry_service.get_model_version_download_uri(name, version)


# def get_model_version_stages(mlflow_client: MlflowClient, name: str, version: str) -> List[str]:
    # stages: List[str] = mlflow_client.get_model_version_stages(name, version)
    # return stages


def update_model_version(name: str, version: str, description: Optional[str] = None) -> ModelVersion:
    raise NotImplementedError


def set_model_version_tag(name: str, version: str = None, key: str = None, value: Any = None) -> None:
    model_registry_service.set_model_version_tag(name, version, key, value)


def delete_model_version_tag(name: str, version: str = None, key: str = None) -> None:
    model_registry_service.delete_model_version_tag(name, version, key)


def transition_model_version_stage(
        name: str, version: str, stage, vertica_update: bool = False
) -> ModelVersion:
    return model_registry_service.transition_model_version_stage(name, version, stage, vertica_update)


def delete_model_version(name: str, version: str) -> None:
    model_registry_service.delete_model_version(name, version)
