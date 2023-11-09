from abc import ABCMeta

from typing import Optional, List, Dict, Any, Tuple

import aip.store.model_store as model_store
import aip.store.tracking_store as tracking_store

from aip.exceptions import APIException
from aip.constants import FINISHED
from aip.entities.run import Run
from aip.entities.experiment import Experiment
from aip.entities.model_info import ModelInfo, TrainingModelInfo
from aip.entities.metric import Metric
from aip.entities.param import Param
from aip.utils.timeutils import get_current_time_millis
from aip.auth import AuthConfig


class Tracker:
    _run: Optional[Run] = None
    _experiment: Optional[Experiment] = None
    _configs: Optional[Dict[str, Any]] = None
    _model_info: Optional[TrainingModelInfo] = None
    # _auth_config: AuthConfig

    def __init__(
            self,
            configs: Optional[Dict[str, Any]] = None,
            model_info: Optional[Dict[str, Any]] = None
    ):
        self._configs = configs
        self._model_info = TrainingModelInfo(**model_info)

    @property
    def experiment(self):
        return self._experiment

    @property
    def run(self):
        return self._run

    @property
    def configs(self):
        return self._configs

    @property
    def model_info(self):
        return self._model_info

    def set_experiment(self, experiment_name: str, tags: Optional[Dict[str, Any]] = None) -> Experiment:
        experiment = tracking_store.get_experiment_by_name(experiment_name)
        if experiment is None:
            experiment = tracking_store.create_experiment(name=experiment_name, tags=tags)

        self._experiment = experiment

        return self._experiment

    def start_run(self, run_name: str, run_tags: Optional[Dict[str, Any]] = None) -> Run:
        run = tracking_store.get_run_by_name(self._experiment.experiment_id, run_name)
        if run is None:
            run = tracking_store.create_run(
                experiment_id=self._experiment.experiment_id,
                run_name=run_name,
                tags=run_tags
            )
            if self._configs is not None:
                tracking_store.log_dict(run.run_id, self._configs, "config.json")
            if self._model_info is not None:
                tracking_store.log_dict(run.run_id, self._model_info.model_dump(), "model_info.json")
        else:
            self._configs = tracking_store.load_dict(run.info.run_id, artifact_path="config.json")
            model_info = tracking_store.load_dict(run.info.run_id, artifact_path="model_info.json")
            self._model_info = TrainingModelInfo(**model_info)

        self._run = run

        return self._run

    def set_tag(self, key: str, value: str):
        tracking_store.set_tag(self._run.info.run_id, key, value)

    def delete_tag(self, key:str):
        tracking_store.delete_tag(self._run.info.run_id, key)

    def log_param(self, key: str, value: Any):
        tracking_store.log_param(self._run.info.run_id, key, value)

    def log_params(self, params: Dict[str, Any]):
        tracking_store.log_params(self._run.info.run_id, params, self._experiment.experiment_id)

    def log_metric(self, key: str, value: float, timestamp: Optional[int] = get_current_time_millis(), step: Optional[int] = None):
        tracking_store.log_metric(self._run.info.run_id, key, value, timestamp, step)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        tracking_store.log_metrics(self._run.info.run_id, metrics, self._experiment.experiment_id)

    def log_model_metadata(self):
        model_metadata = {'model_code': self._model_info.id}
        tracking_store.log_model_metadata(
            run_id=self._run.info.run_id,
            model_name=self._model_info.name,
            metadata=model_metadata,
            experiment_id=self._experiment.experiment_id
        )

        model_tags = {
            "model_code": self._model_info.id,
            "pdi_tag": self.model_info.pdi_tag,
            "category": self._model_info.category,
            "target": self._model_info.target,
            "algorithm": self._model_info.algorithm
        }

        registered_model = model_store.get_registered_model(name=self._model_info.name)
        if registered_model is None:
            registered_model = model_store.create_registered_model(name=self._model_info.name, tags=model_tags)

        model_version = model_store.create_model_version(
            name=registered_model.name,
            run_id=self._run.info.run_id,
            tags=model_tags
        )

        return model_version

    def log_model(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        # TODO
        from mlflow.models import Model
        mlflow_model = Model(
            run_id=self._run.info.run_id,
            artifact_path="model",
            metadata=metadata
        )

        mlflow_model.save("MLmodel")

        from mlflow.client import MlflowClient
        mlflow_client = MlflowClient("http://localhost:5000")
        mlflow_client.log_artifact (
            self._run.info.run_id,
            local_path="MLmodel",
            artifact_path="model"
        )

        # if 'mlflow.log-model.history' in self.run.data.tags:
        # self._mlflow_client.delete_tag(run_id, 'mlflow.log-model.history')
        mlflow_client._record_logged_model(self._run.info.run_id, mlflow_model)

        model = model_store.get_registered_model(name)
        if model is None:
            model = model_store.create_registered_model(name=name)

        model_version = model_store.create_model_version(
            name=name,
            source=f"{self._run.info.artifact_uri}/model",
            run_id=self._run.info.run_id
            # tags=request.tags,
            # description=request.description
        )

        # self._mlflow_client.transition_model_version_stage(
        #     name=model_version.name,
        #     version=model_version.version,
        #     stage="Staging"
        # )
        # raise NotImplementedError

    def register_model(self):
        # TODO
        raise NotImplementedError

    def refresh_run(self):
        ## IF RUN IS NONE ~~~ ##
        self._run = tracking_store.get_run(self._run.info.run_id)

    def end(self):
        ## IF RUN IS NONE ~~~ ##
        tracking_store.terminate(run_id=self._run.info.run_id, status=FINISHED)