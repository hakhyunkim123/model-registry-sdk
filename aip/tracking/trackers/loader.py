from aip.tracking.trackers import Tracker
from aip.tracking.trackers.ncai_tracker import NCAITracker
from aip.tracking.trackers.sacp_tracker import SACPTracker

from aip.store.tracking_store import get_run

from aip.entities.tracker import TrackerType
from aip.entities.model_version import ModelVersion


class TrackerLoader:

    @staticmethod
    def load(run_id: str):
        run = get_run(run_id, detail=False)
        tracker_type = run.data.tags.get("type", None)

        if tracker_type is None:
            return Tracker.load(run_id)
        elif tracker_type == TrackerType.SACP:
            return SACPTracker.load(run_id)
        elif tracker_type == TrackerType.NCAI:
            return NCAITracker.load(run_id)
        else:
            raise NotImplementedError

    @staticmethod
    def from_model(model: ModelVersion):
        tracker_type = model.tags.get("type", None)

        if tracker_type is None:
            return Tracker.load(model.run_id)
        elif tracker_type == "SACP":
            return SACPTracker.load(model.run_id)
        elif tracker_type == "NCAI":
            return NCAITracker.load(model.run_id)
        else:
            raise NotImplementedError
