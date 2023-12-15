import requests
from typing import Optional, List, Dict, Any, Tuple

from aip.auth import AuthConfig
from aip.entities.registered_model import RegisteredModel
from aip.entities.model_version import ModelVersion
from aip.entities.retrain_info import RetrainInfo
from aip.exceptions import APIException
from aip.constants import REGISTERED_MODEL_DOMAIN, MODEL_VERSION_DOMAIN


def create_registered_model(
        name: str,
        tags: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
) -> RegisteredModel:
    url = f"{REGISTERED_MODEL_DOMAIN}"
    data = {"name": name, "tags": tags, "description": description}

    response = requests.put(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 201:
        raise APIException(response)
    else:
        return RegisteredModel(**response.json().get("registered_model"))


def get_registered_model(name: str) -> RegisteredModel:
    url = f"{REGISTERED_MODEL_DOMAIN}"
    params = {"name": name}

    response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return RegisteredModel(**response.json().get("registered_model"))


def search_registered_models(
        filter_string: Optional[str] = None,
        max_results: int = 1000,
        order_by: Optional[List[str]] = None,
        page_token: Optional[str] = None
) -> List[RegisteredModel]: #-> Tuple[List[RegisteredModel], str]:
    url = f"{REGISTERED_MODEL_DOMAIN}/search"

    data = dict()
    data['max_results'] = max_results
    if filter_string is not None:
        data['filter'] = filter_string
    if order_by is not None:
        data['order_by'] = order_by
    if page_token is not None:
        data['page_token'] = page_token

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        models = response.json().get("registered_models", [])
        # next_page_token = response.json().get("next_page_token", None)
        return [RegisteredModel(**model) for model in models]
        # return [RegisteredModel(**model) for model in models], next_page_token


def get_latest_model_version(
        name: str,
        stages: Optional[List[str]] = None,
        detail: bool = True
) -> ModelVersion:
    url = f"{REGISTERED_MODEL_DOMAIN}/get-latest-version"

    data = dict()
    data["name"] = name
    if stages is not None:
        data["stages"] = stages
    data['detail'] = detail

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return ModelVersion(**response.json().get("model_version"))


def get_latest_model_versions(
        name: str,
        stages: Optional[List[str]] = None,
        detail: bool = True
) -> List[ModelVersion]:
    url = f"{REGISTERED_MODEL_DOMAIN}/get-latest-versions"

    data = dict()
    data["name"] = name
    if stages is not None:
        data["stages"] = stages
    data['detail'] = detail

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        model_versions = response.json().get("model_versions")
        return [ModelVersion(**model_version) for model_version in model_versions]


def set_registered_model_tag(name: str, key: str, value: Any) -> None:
    url = f"{REGISTERED_MODEL_DOMAIN}/set-tag"
    data = {"name": name, "key": key, "value": value}

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def delete_registered_model_tag(name: str, key: str) -> None:
    url = f"{REGISTERED_MODEL_DOMAIN}/delete-tag"
    data = {"name": name, "key": key}

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def delete_registered_model(name: str) -> None:
    url = f"{REGISTERED_MODEL_DOMAIN}/delete"
    data = {"name": name}

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def create_model_version(
        name: str,
        source: Optional[str] = None,
        run_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        vertica_insert: bool = True

) -> ModelVersion:
    url = f"{MODEL_VERSION_DOMAIN}"

    data = dict()
    data["name"] = name
    if source is not None:
        data["source"] = source
    if run_id is not None:
        data["run_id"] = run_id
    if tags is not None:
        data["tags"] = tags
    if description is not None:
        data["description"] = description
    data["vertica_insert"] = vertica_insert

    response = requests.put(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 201:
        raise APIException(response)
    else:
        return ModelVersion(**response.json().get("model_version"))


def get_model_version(name: str, version: str, detail: bool = True) -> ModelVersion:
    url = f"{MODEL_VERSION_DOMAIN}"

    params = dict()
    params["name"] = name
    params["version"] = version
    params["detail"] = detail

    response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return ModelVersion(**response.json().get("model_version"))


def get_retrain_history(name: str, version: str) -> List[RetrainInfo]:
    url = f"{MODEL_VERSION_DOMAIN}/get-retrain-history"

    params = dict()
    params["name"] = name
    params["version"] = version

    response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return [RetrainInfo(**retrain_info) for retrain_info in response.json().get("retrain_history")]


def search_model_versions(
        filter_string: str = "",
        max_results: int = 10000,
        order_by: Optional[List[str]] = None,
        page_token: Optional[str] = None,
        detail: bool = False
) -> Tuple[List[ModelVersion], str]:
    url = f"{MODEL_VERSION_DOMAIN}/search"

    data = dict()
    data['filter_string'] = filter_string
    data['max_results'] = max_results
    if order_by is not None:
        data['order_by'] = order_by
    if page_token is not None:
        data['page_token'] = page_token
    data['detail'] = detail

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        model_versions = response.json().get("model_versions", [])
        next_page_token = response.json().get("next_page_token", None)
        return [ModelVersion(**model_version) for model_version in model_versions], next_page_token


def get_model_version_download_uri(name: str, version: str) -> str:
    url = f"{MODEL_VERSION_DOMAIN}/get-download-uri"

    data = dict()
    data['name'] = name
    data['version'] = version

    response = requests.get(url, params=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return response.json().get("artifact_uri")


def set_model_version_tag(name: str, version: str = None, key: str = None, value: Any = None) -> None:
    url = f"{MODEL_VERSION_DOMAIN}/set-tag"

    data = dict()
    data["name"] = name
    data["version"] = version
    data["key"] = key
    data["value"] = value

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def delete_model_version_tag(name: str, version: str = None, key: str = None) -> None:
    url = f"{MODEL_VERSION_DOMAIN}/delete-tag"

    data = dict()
    data["name"] = name
    data["version"] = version
    data["key"] = key

    response = requests.delete(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def transition_model_version_stage(name: str, version: str, stage: str, vertica_update: bool = False) -> ModelVersion:
    url = f"{MODEL_VERSION_DOMAIN}/transition-stage"

    data = dict()
    data["name"] = name
    data["version"] = version
    data["stage"] = stage
    data["vertica_update"] = vertica_update

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return ModelVersion(**response.json().get("model_version"))


def delete_model_version(name: str, version: str) -> None:
    url = f"{MODEL_VERSION_DOMAIN}"

    data = dict()
    data["name"] = name
    data["version"] = version

    response = requests.delete(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
