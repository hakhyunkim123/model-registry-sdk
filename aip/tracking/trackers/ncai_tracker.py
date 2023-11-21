from typing import Optional, Any, List, Dict

from aip.tracking.trackers.sacp_tracker import SACPTracker
from aip.tracking.trackers import Tracker
from aip.entities.metric import NCAIMetric
from aip.store.tracking_store import log_dict
from aip.utils.timeutils import conv_longdate_to_str, get_current_time_millis


class NCAITracker(SACPTracker):

    def __init__(self, configs: Optional[Dict[str, Any]] = None, model_info: Optional[Dict[str, Any]] = None):
        self._metrics: Dict = {}
        super().__init__(tracker_type="NCAI", model_info=model_info, configs=configs)

    def log_inference_metrics(self, metrics: List[Dict]):
        current_time = get_current_time_millis()
        ncai_metrics: List[NCAIMetric] = list()
        for metric in metrics:
            metric['metric_cal_time'] = conv_longdate_to_str(current_time, str_format="%Y%m%d%H%M%S").split(" ")[0]
            metric['data_jukja_dt'] = conv_longdate_to_str(current_time, str_format="%Y%m%d").split(" ")[0]
            ncai_metrics.append(NCAIMetric(**metric))
        for metric in ncai_metrics:
            metric_key = f"{metric.metric_code_id}.{metric.metric_seq}"
            metric_value = metric.model_dump(exclude={'metric_code_id', 'metric_seq'})
            self._metrics[metric_key] = metric_value

        metric_dict = {"metrics": self._metrics}
        log_dict(self.run.info.run_id, metric_dict, f"metadata/inference.json")
