from typing import Optional, Dict, Any, List

from aip.tracking.trackers import Tracker
from aip.tracking.trackers.ncai_tracker import NCAITracker
from aip.tracking.trackers.sacp_tracker import SACPTracker
from aip.tracking.trackers.loader import TrackerLoader

from aip.store.model_store import (
    get_registered_model,
    search_registered_models,
    get_model_version,
    search_model_versions,
    get_latest_model_version,
    get_retrain_history
)
from aip.store.tracking_store import (
    get_experiment,
    get_experiment_by_name,
    search_experiments,
    get_run,
    search_run
)


def create_tracker(
        tracker_type: str = "SACP",
        configs: Dict[str, Any] = None,
        model_info: Dict[str, Any] = None
):
    if tracker_type == "SACP":
        return SACPTracker(
            configs=configs,
            model_info=model_info
        )
    elif tracker_type == "NCAI":
        return NCAITracker(
            configs=configs,
            model_info=model_info
        )


def load_tracker(run_id: str):
    return TrackerLoader.load(run_id)


def load_tracker_from_model(model):
    return TrackerLoader.from_model(model)


