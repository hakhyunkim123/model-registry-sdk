from typing import Optional, Dict, Any, List, Tuple
from aip.utils.timeutils import get_current_time_millis

import aip._internal._tracking_service as _tracking_service

from aip.entities.run import Run, RunInfo, RunData
from aip.entities.experiment import Experiment
from aip.exceptions import APIException
from aip.constants import EXPERIMENT_DOMAIN, RUN_DOMAIN, ACTIVE_ONLY, ALL


def create_experiment(name: str, tags: Optional[Dict[str, Any]] = None) -> Experiment:
    """
    Create experiment
    name is unique variable
    :param name: experiment name
    :param tags: tags for experiment
    :return: experiment_id : str
    """
    return _tracking_service.create_experiment(name, tags)


def get_experiment(experiment_id: str) -> Optional[Experiment]:
    """
    Get Experiment by experiment_id
    :param experiment_id: experiment id
    :return: Experiment
    """
    try:
        experiment = _tracking_service.get_experiment(experiment_id)
    except APIException as error:
        if error.error_code == "RESOURCE_DOES_NOT_EXIST":
            return None
        else:
            raise
    return experiment


def get_experiment_by_name(experiment_name: str) -> Optional[Experiment]:
    """
    Get experiment by experiment name
    :param experiment_name: experiment name to search
    :return: Experiment
    """
    try:
        experiment = _tracking_service.get_experiment_by_name(experiment_name)
    except APIException as error:
        if error.error_code == "RESOURCE_DOES_NOT_EXIST":
            return None
        else:
            raise
    return experiment


def search_experiments(filter_string: Optional[str] = None) -> List[Experiment]:
    """
    Search experiments using filter string
    Example: filter_string = "name = 'iris'"
    :param filter_string: filter string to search
    :return: List[Experiment], next_page_token
    """

    return _tracking_service.search_experiments(filter_string=filter_string)


# def search_experiments(
#         view_type: int = ACTIVE_ONLY,
#         max_results: int = 1000,
#         filter_string: Optional[str] = None,
#         order_by: Optional[List[str]] = None,
#         page_token: Optional[str] = None
# ) -> Tuple[List[Experiment], str]:
#     """
#     Search experiments using filter string
#     Example: filter_string = "name = 'iris'"
#     :param view_type: default: ACTIVE_ONLY otherwise DELETED_ONLY, ALL
#     :param max_results: max result count. default is 1000 (for paging)
#     :param filter_string: filter string to search
#     :param order_by: order by option
#     :param page_token: page token for pagination
#     :return: List[Experiment], next_page_token
#     """
#
#     return _tracking_service.search_experiments(
#         view_type=view_type,
#         max_results=max_results,
#         filter_string=filter_string,
#         order_by=order_by,
#         page_token=page_token
#     )


def set_experiment_tag(experiment_id: str, key: str, value: str) -> None:
    """
    Set experiment tag
    :param experiment_id: experiment id
    :param key: key name of tag
    :param value: value of tag
    :return: None
    """
    _tracking_service.set_experiment_tag(experiment_id, key, value)


def delete_experiment(experiment_id: str) -> None:
    """
    Delete experiment
    Update status active -> deleted
    :param experiment_id: experiment id
    :return: None
    """
    _tracking_service.delete_experiment(experiment_id=experiment_id)


def restore_experiment(experiment_id: str) -> None:
    """
    Restore experiment
    Change status deleted -> active
    :param experiment_id: experiment id
    :return: None
    """
    _tracking_service.restore_experiment(experiment_id=experiment_id)


def update_experiment(experiment_id: str, new_name: str) -> None:
    """
    Update experiment - just change experiment name
    :param experiment_id: experiment id
    :param new_name: new name of experiment
    :return: None
    """
    raise NotImplementedError


def create_run(
        experiment_id: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,

) -> Run:
    """
    Create run
    :param experiment_id: experiment id for create run
    :param run_name: run name (unique)
    :param start_time: start time of run
    :param tags: tags for run
    :return: Run
    """
    filter_string = f"run_name = '{run_name}'"
    # runs, _ = _tracking_service.search_run(
    #     run_view_type=ALL,
    #     experiment_ids=[experiment_id],
    #     filter_string=filter_string
    # )
    # if len(runs) > 0:
    #     raise FileExistsError(f"{run_name} in {experiment_id} is existed")
    return _tracking_service.create_run(experiment_id, run_name, tags)


def get_run(run_id: str) -> Run:
    """
    Get run by run id
    :param run_id: run id
    :return: Run
    """
    run = _tracking_service.get_run(run_id=run_id)
    # artifact_uri = run.info.artifact_uri
    # run_dict = run.model_dump()
    # del run
    # if artifact_files is not None:
    #     run_dict['artifact_data'] = dict()
    #     for artifact_file in artifact_files:
    #         data = _tracking_service.load_dict(f"{artifact_uri}/{artifact_file}.json")
    #         run_dict['artifact_data'][artifact_file] = data

    return run


def get_run_detail(run_id: str, artifact_files: Optional[List[str]] = None) -> Run:
    """
    Get run by run id
    :param artifact_files:
    :param run_id: run id
    :return: Run
    """
    if artifact_files is None:
        artifact_files = ["config", "model_info"]
    run = _tracking_service.get_run_detail(run_id, artifact_files)
    # artifact_uri = run.info.artifact_uri
    # run_dict = run.model_dump()
    # del run
    # if artifact_files is not None:
    #     run_dict['artifact_data'] = dict()
    #     for artifact_file in artifact_files:
    #         data = _tracking_service.load_dict(f"{artifact_uri}/{artifact_file}.json")
    #         run_dict['artifact_data'][artifact_file] = data

    return run


def search_run(
        experiment_id: str,
        filter_string: str = None,
) -> List[Run]:
    """
    Search run using filter option
    :param experiment_id: list of experiment id to search
    :param filter_string: filter string option (example: filter_string = "run_name = 'iris-01'"
    :return: List[Run], next_page_token
    """
    return _tracking_service.search_run(experiment_id=experiment_id, filter_string=filter_string)

# def search_run(
#         experiment_ids: List[str],
#         filter_string: str = None,
#         run_view_type: int = ACTIVE_ONLY,
#         max_results: int = 1000,
#         order_by: Optional[List[str]] = None,
#         page_token: Optional[str] = None
# ) -> Tuple[List[Run], str]:
#     """
#     Search run using filter option
#     :param experiment_ids: list of experiment id to search
#     :param filter_string: filter string option (example: filter_string = "run_name = 'iris-01'"
#     :param run_view_type: default: ACTIVE_ONLY otherwise DELETED_ONLY, ALL
#     :param max_results :max result count. default is 1000 (for paging)
#     :param order_by: order by option
#     :param page_token: page token for pagination
#     :return: List[Run], next_page_token
#     """
#     return _tracking_service.search_run(experiment_ids, filter_string, run_view_type, max_results, order_by, page_token)


def get_run_by_name(experiment_id: str, run_name: str) -> Optional[Run]:
    """
    Get run by run id
    :param experiment_id: experiment_id
    :param run_name: run name
    :return: Run
    """
    runs = search_run(experiment_id=experiment_id, filter_string=f"run_name = '{run_name}'")
    if len(runs) == 0:
        return None
    return runs[-1]


# def update_run(
#         run_id: str,
#         status: Optional[str] = None,
#         end_time: Optional[int] = get_current_time_millis(),
#         run_name: Optional[str] = None
# ) -> RunInfo:
#     """
#     Update run status, end time or name
#     :param run_id: run id to update
#     :param status: RUNNING, FINISHED, ...
#     :param end_time: end time of run
#     :param run_name: new name of run
#     :return: None
#     """
#     return _tracking_service.update_run(run_id, status, end_time, run_name)


def set_tag(run_id: str, key: str, value: Any) -> None:
    """
    Set tag
    :param run_id: run id
    :param key: key of tag
    :param value: value of tag
    :return: None
    """
    _tracking_service.set_tag(run_id, key, value)


def delete_tag(run_id: str, key: str) -> None:
    """
    Delete tag
    :param run_id: run id
    :param key: tag to delete
    :return: None
    """
    _tracking_service.delete_tag(run_id, key)


def load_dict(run_id: str, artifact_path: str) -> Dict:
    return _tracking_service.load_dict(run_id, artifact_path)


def log_dict(run_id: str, dictionary: Dict[str, Any], artifact_file: str, experiment_id: str = None) -> None:
    _tracking_service.log_dict(run_id, dictionary, artifact_file, experiment_id)


def log_batch(
        run_id: str,
        params: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, float]] = None,
        tags: Optional[Dict[str, str]] = None,
        experiment_id: str = None
) -> None:
    _tracking_service.log_batch(
        run_id, params, metrics, tags, experiment_id
    )


def log_param(run_id: str, key: str, value: Any) -> None:
    """
    log parameter
    :param run_id: run id
    :param key: parameter key
    :param value: parameter value
    :return: None
    """
    _tracking_service.log_param(run_id, key, value)


def log_metric(
        run_id: str,
        key: str,
        value: float,
        timestamp: Optional[int] = get_current_time_millis(),
        step: Optional[int] = None
) -> None:
    """
    Log metric variable
    :param run_id: run id
    :param key: metric key
    :param value: metric value
    :param timestamp: timestamp to logging
    :param step: step
    :return: None
    """
    _tracking_service.log_metric(run_id, key, value, timestamp, step)


def log_params(run_id: str, params: Dict[str, Any], experiment_id: str = None) -> None:
    """
    log parameter
    :param run_id: run id
    :param key: parameter key
    :param value: parameter value
    :return: None
    """
    _tracking_service.log_params(run_id, params, experiment_id)


def log_metrics(run_id: str, metrics: Dict[str, Any], experiment_id: str = None) -> None:
    """
    log parameter
    :param run_id: run id
    :param key: parameter key
    :param value: parameter value
    :return: None
    """
    _tracking_service.log_metrics(run_id, metrics, experiment_id)


def log_model_metadata(
        run_id: str,
        model_name: str,
        metadata: Optional[Dict[str, Any]] = None,
        experiment_id: Optional[str] = None
) -> None:
    _tracking_service.log_model_metadata(run_id, model_name, metadata, experiment_id)


def terminate(run_id: str, status: str,
              end_time: Optional[int] = get_current_time_millis(), experiment_id: str = None) -> None:
    _tracking_service.terminate(run_id, status, end_time, experiment_id)


def delete_run(run_id: str, experiment_id: Optional[str] = None) -> None:
    """
    Delete run
    Update stage active to deleted
    :param run_id: run id
    :return: None
    """
    _tracking_service.delete_run(run_id=run_id, experiment_id=experiment_id)


def restore_run(run_id: str, experiment_id: Optional[str] = None) -> None:
    """
    Restore deleted run
    Update stage deleted to active
    :param run_id:
    :return: None
    """
    _tracking_service.restore_run(run_id=run_id, experiment_id=experiment_id)