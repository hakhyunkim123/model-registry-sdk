from typing import Optional, List
from datetime import datetime

import aip
from aip.entities.model_version import ModelVersion
from aip.entities.model_info import ModelInfo
from aip.entities.retrain_info import RetrainInfo
from aip.entities.run import RunType
from aip.entities.tracker import TrackerType

from aip import load_tracker_from_model
from aip.store.model_store import get_model_version, get_latest_model_version, get_retrain_history


class Model:
    _model_version: ModelVersion
    name: str
    version: str
    info: Optional[ModelInfo]

    def __init__(self, name: str, version: str, model_version: Optional[ModelVersion] = None) -> None:
        if model_version is None:
            model_version = get_model_version(name=name, version=version, detail=True)
        self._model_version = model_version
        self.name = name
        self.version = version
        if model_version.info is None:
            self._model_version = get_model_version(model_version.name, model_version.version, detail=True)
        self.info = self._model_version.info

    def __repr__(self):
        return f"Model(name={self.name}, version={self.version})"

    @classmethod
    def from_model_version(cls, model_version: ModelVersion):
        return cls(
            name=model_version.name,
            version=model_version.version,
            model_version=model_version
        )

    @classmethod
    def latest_version(cls, name: str):
        model_version = get_latest_model_version(name=name, detail=True)
        return cls.from_model_version(model_version)

    def get_tracker(self):
        return load_tracker_from_model(self.info)

    def get_retrain_history(self) -> List[RetrainInfo]:
        return get_retrain_history(name=self.name, version=self.version)

    def start_retrain_tracker(self, run_name: Optional[str] = None):
        parent_run = self._model_version.run_id
        tracker = aip.create_tracker(
            tracker_type=self._model_version.tags.get("type")
        )
        tracker.set_experiment(experiment_name=self.name)

        if run_name is None:
            run_name = f"{self.name}/{self.version}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        run_tags = {
            "mlflow.parentRunId": parent_run,
            "type": TrackerType.NCAI,
            "run_type": RunType.RETRAIN,
            "model_id": self.name,
            "model_version": self.version,
            "dw_juka_dt": ""
        }

        tracker.start_run(run_name=run_name, run_tags=run_tags)

        return tracker



