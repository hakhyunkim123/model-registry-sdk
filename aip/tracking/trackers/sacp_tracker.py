from aip.tracking.trackers import Tracker


class SACPTracker(Tracker):

    def __init__(self, experiment_name: str):
        super().__init__(experiment_name)
