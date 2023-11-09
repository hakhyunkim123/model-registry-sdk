from typing import Optional, Dict, Any, List

from aip.tracking.trackers import (
    Tracker
)
from aip.store.model_store import (
    get_registered_model,
    get_model_version,
    get_model_version_detail
)
from aip.store.tracking_store import (
    get_experiment,
    get_experiment_by_name,
    get_run,
    get_run_detail,
    search_run
)


def create_tracker(
        tracker_type: str = "SACP",
        configs: Dict[str, Any] = None,
        model_info: Dict[str, Any] = None
):
    if tracker_type == "SACP":
        return Tracker(
            configs=configs,
            model_info=model_info
        )


