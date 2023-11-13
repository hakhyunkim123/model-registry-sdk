from typing import Optional, List, Dict, Any, Tuple

import aip._internal._model_regisry_service as model_registry_service
from aip.entities.model_info import TrainingModelInfo, ModelInfo
from aip.entities.model import RegisteredModel
from aip.entities.model_version import ModelVersion
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
        stages: Optional[List[str]] = None
) -> List[ModelVersion]:
    return model_registry_service.get_latest_model_version(name, stages)


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
        description: Optional[str] = None
) -> ModelVersion:
    return model_registry_service.create_model_version(
        name=name,
        source=source,
        run_id=run_id,
        tags=tags,
        # run_link,
        description=description
    )


def get_model_version(name: str, version: str) -> ModelVersion:
    return model_registry_service.get_model_version(name, version)


def _get_model_version_detail(name: str, version: str, json_files: Optional[List[str]] = None) -> ModelVersion:
    return model_registry_service.get_model_version_detail(name, version, json_files)


def get_model_version_detail(name: str, version: str) -> ModelInfo:
    model_version = model_registry_service.get_model_version_detail(name, version)

    from aip.store.tracking_store import load_dict
    # config = load_dict(model_version.run_id, 'config.json')
    # model_info = load_dict(model_version.run_id, 'model_info.json')
    metadata = model_version.run.metadata

    model_info = TrainingModelInfo(**metadata.get("model_info")) if "model_info" in metadata else None
    config = metadata.get("config") if "config" in metadata else None
    result = {
        "id": model_info.id,
        "name": model_info.name,
        "version": model_version.version,
        "tags": model_version.tags,
        "config": config,
        "train": {
            "params": model_version.run.data.params,
            "model_info": model_info
        }
    }

    return ModelInfo(**result)


def search_model_versions(filter_string: Optional[str] = None) -> List[ModelVersion]:
    return model_registry_service.search_model_versions(filter_string)


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
        name: str, version: str, stage
) -> ModelVersion:
    return model_registry_service.transition_model_version_stage(name, version, stage)


def delete_model_version(name: str, version: str) -> None:
    model_registry_service.delete_model_version(name, version)
