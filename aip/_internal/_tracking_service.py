import requests
from typing import Optional, List, Dict, Any, Tuple

from aip.entities.run import Run, RunInfo, RunData
from aip.entities.experiment import Experiment
from aip.entities.metric import NCAIMetric
from aip.exceptions import APIException
from aip.constants import EXPERIMENT_DOMAIN, RUN_DOMAIN, ACTIVE_ONLY, ALL
from aip.utils.timeutils import get_current_time_millis, conv_longdate_to_str
from aip.auth import AuthConfig


def create_experiment(name: str, tags: Optional[Dict[str, Any]] = None) -> Experiment:
    url = f"{EXPERIMENT_DOMAIN}"
    data = {"name": name, "tags": tags}

    response = requests.put(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 201:
        raise APIException(response)
    else:
        return Experiment(**response.json().get("experiment"))


def get_experiment(experiment_id: str) -> Experiment:
    url = f"{EXPERIMENT_DOMAIN}"
    params = {"experiment_id": experiment_id}

    response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return Experiment(**response.json().get("experiment"))


def get_experiment_by_name(experiment_name: str) -> Optional[Experiment]:
    url = f"{EXPERIMENT_DOMAIN}/get-by-name"
    param = {"name": experiment_name}

    response = requests.get(url, params=param, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        experiment = response.json().get("experiment")
        return Experiment(**experiment) if experiment is not None else None


# def search_experiments(
#         filter_string: Optional[str] = None
# ) -> List[Experiment]:
#     url = f"{EXPERIMENT_DOMAIN}/search"
#
#     data = dict()
#     if filter_string is not None:
#         data['filter_string'] = filter_string
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         experiments = response.json().get("experiments", [])
#         return [Experiment(**experiment) for experiment in experiments]


def search_experiments(
        view_type: int = ACTIVE_ONLY,
        max_results: int = 1000,
        filter_string: Optional[str] = None,
        order_by: Optional[List[str]] = None,
        page_token: Optional[str] = None
) -> List[Experiment]: #-> Tuple[List[Experiment], str]:
    url = f"{EXPERIMENT_DOMAIN}/search"

    data = dict()
    data['view_type'] = view_type
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
        experiments = response.json().get("experiments", [])
        # next_page_token = response.json().get("next_page_token", None)
        return [Experiment(**experiment) for experiment in experiments]
        # return [Experiment(**experiment) for experiment in experiments], next_page_token


def set_experiment_tag(experiment_id: str, key: str, value: str) -> None:
    url = f"{EXPERIMENT_DOMAIN}/set-tag"

    data = dict()
    data['experiment_id'] = experiment_id
    data['key'] = key
    data['value'] = value

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def delete_experiment(experiment_id: str) -> None:
    url = f"{EXPERIMENT_DOMAIN}"

    data = dict()
    data['experiment_id'] = experiment_id

    response = requests.delete(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def restore_experiment(experiment_id: str) -> None:
    url = f"{EXPERIMENT_DOMAIN}/restore"

    data = dict()
    data['experiment_id'] = experiment_id

    response = requests.patch(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


# def update_experiment(experiment_id: str, new_name: str) -> None:
#     url = f"{EXPERIMENT_DOMAIN}/update"
#
#     data = dict()
#     data['experiment_id'] = experiment_id
#     data['new_name'] = new_name
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)


def create_run(
        experiment_id: str,
        run_name: str,
        # start_time: Optional[int] = get_current_time_millis(),
        tags: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None

) -> Run:
    url = f"{RUN_DOMAIN}"

    data = dict()
    data['experiment_id'] = experiment_id
    data['name'] = run_name
    # if start_time is not None:
    #     data['start_time'] = start_time
    if tags is not None:
        data['tags'] = tags
    if metadata is not None:
        data['metadata'] = metadata

    response = requests.put(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 201:
        raise APIException(response)
    else:
        return Run(**response.json().get("run"))


def get_run(run_id: str, detail: bool = False) -> Run:
    url = f"{RUN_DOMAIN}"

    params = dict()
    params['run_id'] = run_id
    params['detail'] = detail

    response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return Run(**response.json().get("run"))


def search_run(
        experiment_id: str,
        filter_string: str = "",
        run_view_type: int = ACTIVE_ONLY,
        max_results: int = 1000,
        order_by: Optional[List[str]] = None,
        page_token: Optional[str] = None,
        detail: bool = False
) -> Tuple[List[Run], Optional[str]]:
    url = f"{RUN_DOMAIN}/search"

    data = dict()
    data['experiment_id'] = experiment_id
    data['run_view_type'] = run_view_type
    data['max_results'] = max_results
    data['filter_string'] = filter_string
    if order_by is not None:
        data['order_by'] = order_by
    if page_token is not None:
        data['page_token'] = page_token
    data['detail'] = detail

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        runs = response.json().get("runs", [])
        next_page_token = response.json().get("next_page_token", None)
        return [Run(**run) for run in runs], next_page_token


def list_artifacts(run_id: str, path: Optional[str] = None) -> List[str]:
    url = f"{RUN_DOMAIN}/artifacts/list"

    params = dict()
    params['run_id'] = run_id
    if path is not None:
        params['path'] = path

    response = requests.get(url, params=params, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)
    else:
        return response.json().get("files")


def set_tag(run_id: str, key: str, value: str, experiment_id: Optional[str] = None) -> None:
    url = f"{RUN_DOMAIN}/set-tag"

    data = dict()
    data['run_id'] = run_id
    data['key'] = key
    data['value'] = value
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def delete_tag(run_id: str, key: str, experiment_id: Optional[str] = None) -> None:
    url = f"{RUN_DOMAIN}/delete-tag"

    data = dict()
    data['run_id'] = run_id
    data['key'] = key
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def update_run(
        run_id: str,
        status: Optional[str] = None,
        name: Optional[str] = None
) -> None:
    url = f"{RUN_DOMAIN}"

    data = dict()
    data['run_id'] = run_id
    if status is not None:
        data['status'] = status
    if name is not None:
        data['name'] = name

    response = requests.patch(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)

# def load_dict(run_id: str, artifact_path: str) -> Dict:
#     url = f"{RUN_DOMAIN}/load-dict"
#
#     data = dict()
#     data['run_id'] = run_id
#     data['artifact_path'] = artifact_path
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#     else:
#         return response.json().get("data")


def log_dict(run_id: str, dictionary: Dict[str, Any], artifact_file: str, experiment_id: str = None) -> None:
    url = f"{RUN_DOMAIN}/log-dict"

    data = dict()
    data['run_id'] = run_id
    data['dictionary'] = dictionary
    data['artifact_file'] = artifact_file
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_batch(
        run_id: str,
        params: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, float]] = None,
        tags: Optional[Dict[str, str]] = None,
        experiment_id: str = None
) -> None:
    url = f"{RUN_DOMAIN}/log-batch"

    data = dict()
    data['run_id'] = run_id
    if params is not None:
        data['params'] = params
    if metrics is not None:
        data['metrics'] = metrics
    if tags is not None:
        data['tags'] = tags
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_param(run_id: str, key: str, value: Any, experiment_id: str = None) -> None:
    url = f"{RUN_DOMAIN}/log-param"

    data = dict()
    data['run_id'] = run_id
    data['key'] = key
    data['value'] = value
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_params(run_id: str, params: Dict[str, Any], experiment_id: Optional[str] = None) -> None:
    url = f"{RUN_DOMAIN}/log-params"

    data = dict()
    data['run_id'] = run_id
    data['params'] = params
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_metric(
        run_id: str,
        key: str,
        value: float,
        timestamp: Optional[int] = None,
        step: Optional[int] = 0,
        experiment_id: Optional[str] = None
) -> None:
    url = f"{RUN_DOMAIN}/log-metric"

    if timestamp is None:
        timestamp = get_current_time_millis()

    data = dict()
    data['run_id'] = run_id
    data['key'] = key
    data['value'] = value
    data['timestamp'] = timestamp
    data['step'] = step
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_metrics(run_id: str, metrics: Dict[str, Any], experiment_id: str = None) -> None:
    url = f"{RUN_DOMAIN}/log-metrics"

    data = dict()
    data['run_id'] = run_id
    data['metrics'] = metrics
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_ncai_metrics(run_id: str, metrics: List[Dict],
                     experiment_id: str = None, vertica_insert: bool = False) -> None:
    url = f"{RUN_DOMAIN}/log-ncai-metrics"

    data = dict()
    data['run_id'] = run_id
    data['metrics'] = metrics
    if experiment_id is not None:
        data['experiment_id'] = experiment_id
    data['vertica_insert'] = vertica_insert

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def log_model_metadata(
        run_id: str,
        model_name: str,
        metadata: Optional[Dict[str, Any]] = None,
        experiment_id: str = None
) -> None:
    url = f"{RUN_DOMAIN}/log-model-metadata"

    data = dict()
    data['run_id'] = run_id
    data['name'] = model_name
    if metadata is not None:
        data['metadata'] = metadata
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def terminate(run_id: str, status: str, end_time: Optional[int] = None, experiment_id: str = None) -> None:
    url = f"{RUN_DOMAIN}/terminate"
    end_time = get_current_time_millis() if end_time is None else end_time

    data = dict()
    data['run_id'] = run_id
    data['run_status'] = status
    data['end_time'] = end_time
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def delete_run(run_id: str, experiment_id: Optional[str] = None) -> None:
    url = f"{RUN_DOMAIN}"

    data = dict()
    data['run_id'] = run_id
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.delete(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


def restore_run(run_id: str, experiment_id: Optional[str] = None) -> None:
    url = f"{RUN_DOMAIN}/restore"

    data = dict()
    data['run_id'] = run_id
    if experiment_id is not None:
        data['experiment_id'] = experiment_id

    response = requests.patch(url, json=data, auth=(AuthConfig().username, AuthConfig().password))

    if response.status_code != 200:
        raise APIException(response)


# def log_param(run_id: str, key: str, value: Any) -> None:
#     url = f"{RUN_DOMAIN}/log-parameter"
#
#     data = dict()
#     data['run_id'] = run_id
#     data['key'] = key
#     data['value'] = value
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)


# def log_metric(
#         run_id: str,
#         key: str,
#         value: float,
#         timestamp: Optional[int] = get_current_time_millis(),
#         step: Optional[int] = None
# ) -> None:
#     url = f"{RUN_DOMAIN}/log-metric"
#
#     data = dict()
#     data['run_id'] = run_id
#     data['key'] = key
#     data['value'] = value
#     data['timestamp'] = timestamp
#     data['step'] = step
#
#     response = requests.post(url, json=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)


# def list_artifacts(run_id: str, path: Optional[str] = None) -> List:
#     url = f"http://localhost:5000/api/2.0/mlflow/artifacts/list"
#
#     data = dict()
#     data['run_id'] = run_id
#     if path is not None:
#         data['path'] = path
#
#     response = requests.get(url, params=data, auth=(AuthConfig().username, AuthConfig().password))
#
#     if response.status_code != 200:
#         raise APIException(response)
#
#     return response.json()
#
#
# def load_dict(artifact_uri: str):
#     from mlflow.artifacts import load_dict
#     return load_dict(artifact_uri)
