from typing import Optional, List, Dict, Any, Tuple

import aip.store.model_store as model_store
import aip.store.tracking_store as tracking_store

from aip.exceptions import APIException
from aip.constants import FINISHED
from aip.entities.run import Run
from aip.entities.experiment import Experiment
from aip.entities.model_info import ModelInfo
from aip.entities.metric import Metric
from aip.entities.param import Param
from aip.utils.timeutils import get_current_time_millis


class Tracker:
    _type: str
    _run: Optional[Run] = None
    _experiment: Optional[Experiment] = None
    _configs: Optional[Dict[str, Any]] = None
    _model_info: Optional[ModelInfo] = None

    def __init__(
            self,
            tracker_type: str = "BASE",
            configs: Optional[Dict[str, Any]] = None,
            model_info: Optional[Dict[str, Any]] = None
    ):
        self._type = tracker_type
        self._configs = configs
        self._model_info = ModelInfo(**model_info) if model_info is not None else None

    @property
    def type(self):
        return self._type

    @property
    def experiment(self):
        return self._experiment

    @property
    def run(self):
        return self._run

    @property
    def configs(self) -> Dict[str, Any]:
        return self._configs

    @property
    def model_info(self) -> ModelInfo:
        return self._model_info

    @model_info.setter
    def model_info(self, model_info):
        self._model_info = model_info

    @configs.setter
    def configs(self, configs):
        self._configs = configs

    @run.setter
    def run(self, run: Run):
        self._run = run

    @experiment.setter
    def experiment(self, experiment: Experiment):
        self._experiment = experiment

    @classmethod
    def load(cls, run_id: str):
        run = tracking_store.get_run(run_id, detail=True)
        model_info = run.metadata.get("model_info", None)
        config = run.metadata.get("config", None)

        loaded_tracker = cls(
            model_info=model_info,
            configs=config
        )
        loaded_tracker.experiment = tracking_store.get_experiment(run.info.experiment_id)
        loaded_tracker.run = run

        return loaded_tracker

    def set_experiment(self, experiment_name: str, tags: Optional[Dict[str, Any]] = None) -> Experiment:
        experiment = tracking_store.get_experiment_by_name(experiment_name)
        if experiment is None:
            if tags is None:
                tags = {}
            tags['type'] = self._type
            experiment = tracking_store.create_experiment(name=experiment_name, tags=tags)

        self._experiment = experiment

        return self._experiment

    def start_run(self, run_name: Optional[str] = None, run_tags: Optional[Dict[str, Any]] = None) -> Run:
        run = tracking_store.get_run_by_name(self._experiment.experiment_id, run_name, detail=True)
        if run is None:
            if run_tags is None:
                run_tags = {}
            run_tags['type'] = self._type

            metadata = dict()
            if self._configs is not None:
                metadata['config'] = self._configs
            if self._model_info is not None:
                metadata['model_info'] = self._model_info.dict(exclude_unset=True)

            run = tracking_store.create_run(
                experiment_id=self._experiment.experiment_id,
                run_name=run_name,
                tags=run_tags,
                metadata=metadata
            )
        self._run = run
        return self._run

    def set_tag(self, key: str, value: str):
        tracking_store.set_tag(self._run.info.run_id, key, value)

    def update_run(self, status: Optional[str] = None, name: Optional[str] = None) -> None:
        tracking_store.update_run(self._run.info.run_id, status=status, name=name)

    def delete_tag(self, key: str):
        tracking_store.delete_tag(self._run.info.run_id, key)

    def log_param(self, key: str, value: Any):
        tracking_store.log_param(self._run.info.run_id, key, value)

    def log_params(self, params: Dict[str, Any]):
        tracking_store.log_params(self._run.info.run_id, params, self._experiment.experiment_id)

    def log_metric(self, key: str, value: float, timestamp: Optional[int] = None, step: Optional[int] = None):
        if timestamp is None:
            timestamp = get_current_time_millis()
        tracking_store.log_metric(self._run.info.run_id, key, value, timestamp, step)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        tracking_store.log_metrics(self._run.info.run_id, metrics, self._experiment.experiment_id)

    def log_model_metadata(self, tags: Optional[Dict[str, Any]] = None, vertica_insert: bool = True):
        tracking_store.log_model_metadata(
            run_id=self._run.info.run_id,
            model_name=self._model_info.name,
            experiment_id=self._experiment.experiment_id
        )

        if tags is None:
            tags = {}
        tags.update({
            "type": self._type,
            "name": f"{self._model_info.name}",
        })

        registered_model_name = self._model_info.id

        registered_model = model_store.get_registered_model(name=registered_model_name)
        if registered_model is None:
            registered_model = model_store.create_registered_model(
                name=registered_model_name,
                tags=tags,
                description=self._model_info.description
            )

        model_version = model_store.create_model_version(
            name=registered_model.name,
            run_id=self._run.info.run_id,
            tags=tags,
            description=self._model_info.description,
            vertica_insert=vertica_insert
        )

        return model_version

    def refresh_run(self):
        ## IF RUN IS NONE ~~~ ##
        self._run = tracking_store.get_run(self._run.info.run_id)

    def end(self):
        ## IF RUN IS NONE ~~~ ##
        tracking_store.terminate(run_id=self._run.info.run_id, status=FINISHED)
