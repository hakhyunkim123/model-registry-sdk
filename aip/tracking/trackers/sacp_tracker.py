from typing import Dict, Optional, Any

from aip.tracking.trackers import Tracker
from aip.entities.run import Run
from aip.entities.sacp.sacp_task_info import SACPTaskInfo


class SACPTracker(Tracker):

    def __init__(
            self,
            tracker_type: str = "SACP",
            configs: Optional[Dict[str, Any]] = None,
            model_info: Optional[Dict[str, Any]] = None
    ):
        self._task_info = SACPTaskInfo()
        super().__init__(tracker_type=tracker_type, configs=configs, model_info=model_info)

    def start_run(self, run_name: Optional[str] = None, run_tags: Optional[Dict[str, Any]] = None) -> Run:
        if self.experiment is None:
            self.set_experiment(experiment_name=self._task_info.project_id)

        if run_name is None:
            run_name = self._task_info.task_id

        sacp_run_tags = {
            "task_id": self._task_info.task_id,
            "pod_name": self._task_info.pod_name,
            "task_type": self._task_info.task_type,
            "project_id": self._task_info.project_id,
            "current_user": self._task_info.current_user,
        }

        if run_tags is None:
            run_tags = {}
        run_tags.update(sacp_run_tags)

        return super().start_run(run_name=run_name, run_tags=run_tags)
