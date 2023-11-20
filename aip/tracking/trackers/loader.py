from aip.tracking.trackers import Tracker
from aip.tracking.trackers.ncai_tracker import NCAITracker
from aip.tracking.trackers.sacp_tracker import SACPTracker
from aip.store.tracking_store import get_run
from aip.entities.model_info import ModelInfo


class TrackerLoader:

    @staticmethod
    def load(run_id: str):
        run = get_run(run_id)
        tracker_type = run.data.tags.get("type", None)

        if tracker_type is None:
            return Tracker.load(run_id)
        elif tracker_type == "SACP":
            return SACPTracker.load(run_id)
        elif tracker_type == "NCAI":
            return NCAITracker.load(run_id)
        else:
            raise NotImplementedError

    @staticmethod
    def from_model(model: ModelInfo):
        run = get_run(model.run_id)
        tracker_type = run.data.tags.get("type", None)

        if tracker_type is None:
            return Tracker.load(model.run_id)
        elif tracker_type == "SACP":
            return SACPTracker.load(model.run_id)
        elif tracker_type == "NCAI":
            return NCAITracker.load(model.run_id)
        else:
            raise NotImplementedError
