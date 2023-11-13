import requests
from typing import Optional, List, Dict, Any, Tuple

from aip.auth import AuthConfig
from aip.entities.model import RegisteredModel
from aip.entities.model_version import ModelVersion
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


def search_registered_models(filter_string: Optional[str] = None) -> List[RegisteredModel]:
    url = f"{REGISTERED_MODEL_DOMAIN}/search"

    data = dict()
    if filter_string is not None:
        data['filter_string'] = filter_string

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        models = response.json().get("registered_models", [])
        return [RegisteredModel(**model) for model in models]

# def search_registered_models(
#         filter_string: Optional[str] = None,
#         max_results: int = 1000,
#         order_by: Optional[List[str]] = None,
#         page_token: Optional[str] = None
# ) -> Tuple[List[RegisteredModel], str]:
#     url = f"{REGISTERED_MODEL_DOMAIN}/search"
#
#     data = dict()
#     data['max_results'] = max_results
#     if filter_string is not None:
#         data['filter'] = filter_string
#     if order_by is not None:
#         data['order_by'] = order_by
#     if page_token is not None:
#         data['page_token'] = page_token
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         models = response.json().get("registered_models", [])
#         next_page_token = response.json().get("next_page_token", None)
#         return [RegisteredModel(**model) for model in models], next_page_token


def get_latest_model_version(
        name: str,
        stages: Optional[List[str]] = None
) -> List[ModelVersion]:
    url = f"{REGISTERED_MODEL_DOMAIN}/get-latest-versions"

    data = dict()
    data["name"] = name
    if stages is not None:
        data["stages"] = stages

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return [ModelVersion(**model_version) for model_version in response.json().get("model_versions")]


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

# def update_registered_model(name: str, description: Optional[str] = None) -> RegisteredModel:
#     url = f"{REGISTERED_MODEL_DOMAIN}/update"
#     data = {"name": name, "description": description}
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         return RegisteredModel(**response.json().get("registered_model"))


# def rename_registered_model(name: str, new_name: str) -> RegisteredModel:
#     url = f"{REGISTERED_MODEL_DOMAIN}/rename"
#     data = {"name": name, "new_name": new_name}
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         return RegisteredModel(**response.json().get("registered_model"))


# def set_registered_model_alias(name: str, alias: str, version: str) -> None:
#     url = f"{REGISTERED_MODEL_DOMAIN}/alias"
#     data = {"name": name, "alias": alias, "version": version}
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)


# def delete_registered_model_alias(name: str, alias: str) -> None:
#     url = f"{REGISTERED_MODEL_DOMAIN}/alias"
#     data = {"name": name, "alias": alias}
#
#     response = requests.delete(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)


def create_model_version(
        name: str,
        source: Optional[str] = None,
        run_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        # run_link: Optional[str] = None,
        description: Optional[str] = None
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
    # if run_link is not None:
    #     data["run_link"] = run_link
    if description is not None:
        data["description"] = description

    response = requests.put(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 201:
        raise APIException(response)
    else:
        return ModelVersion(**response.json().get("model_version"))


def get_model_version(name: str, version: str, detail: bool = False) -> ModelVersion:
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


def get_model_version_detail(name: str, version: str, json_files: Optional[List[str]] = None) -> ModelVersion:
    url = f"{MODEL_VERSION_DOMAIN}/detail"

    data = dict()
    data["name"] = name
    data["version"] = version
    if json_files is not None:
        data["json_files"] = json_files

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return ModelVersion(**response.json().get("model_version"))


def search_model_versions(filter_string: Optional[str] = None) -> List[ModelVersion]:
    url = f"{MODEL_VERSION_DOMAIN}/search"

    data = dict()
    if filter_string is not None:
        data['filter'] = filter_string

    response = requests.get(url, params=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        model_versions = response.json().get("model_versions", [])
        return [ModelVersion(**model_version) for model_version in model_versions]


# def search_model_versions(
#         filter_string: Optional[str] = None,
#         max_results: int = 1000,
#         order_by: Optional[List[str]] = None,
#         page_token: Optional[str] = None,
# ) -> Tuple[List[ModelVersion], str]:
#     url = f"{MODEL_VERSION_DOMAIN}/search"
#
#     data = dict()
#     data['max_results'] = max_results
#     if filter_string is not None:
#         data['filter'] = filter_string
#     if order_by is not None:
#         data['order_by'] = order_by
#     if page_token is not None:
#         data['page_token'] = page_token
#
#     response = requests.get(url, params=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         model_versions = response.json().get("model_versions", [])
#         next_page_token = response.json().get("next_page_token", None)
#         return [ModelVersion(**model_version) for model_version in model_versions], next_page_token


# def get_model_version_by_alias(name: str, alias: str) -> ModelVersion:
#     url = f"{MODEL_VERSION_DOMAIN}/alias"
#
#     params = dict()
#     params['name'] = name
#     params['version'] = alias
#
#     response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         return ModelVersion(**response.json().get("model_version"))


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


# def get_model_version_stages(mlflow_client: MlflowClient, name: str, version: str) -> List[str]:
    # stages: List[str] = mlflow_client.get_model_version_stages(name, version)
    # return stages


# def update_model_version(name: str, version: str, description: Optional[str] = None) -> ModelVersion:
#     url = f"{MODEL_VERSION_DOMAIN}/update"
#
#     data = dict()
#     data["name"] = name
#     data["version"] = version
#     if description is not None:
#         data["description"] = description
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         return ModelVersion(**response.json().get("model_version"))


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


def transition_model_version_stage(name: str, version: str, stage: str) -> ModelVersion:
    url = f"{MODEL_VERSION_DOMAIN}/transition-stage"

    data = dict()
    data["name"] = name
    data["version"] = version
    data["stage"] = stage

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
