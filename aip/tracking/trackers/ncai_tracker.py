from aip.tracking.trackers.sacp_tracker import SACPTracker


class NCAITracker(SACPTracker):

    def __init__(self, experiment_name: str):
        super().__init__(experiment_name)

    def log_inference_metric(self, metrics):
        from aip.store import tracking_store
        metric_dict = {"metrics": metrics}
        tracking_store.log_dict(self.run.info.run_id, metric_dict, f"metadata/metrics.json")


    # def log_metric(self, ):
