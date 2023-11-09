from aip.tracking.trackers import Tracker
from aip.store.tracking_store import *
from pprint import pprint

configs = {
    "a": "bbb",
    "test2": "test2"
}

model_info = {
    "name": "test",
    "target": "target2"
}

experiment_name = "sdk-test"
run_name = "test-05"

# tracker = Tracker(experiment_name="sdk-test", configs=configs, model_info=model_info)
# tracker.start(run_name="test-11")
# tracker.log_param("param1", "test1")
# tracker.log_metric("l5", 1.5)
# tracker.log_model(name=model_info.get("name"))
# tracker.end()

import aip.store.model_store as model_store
import aip.store.tracking_store as tracking_store
mv = model_store.get_model_version(name="test", version="2")
artifact_uri = mv.source
run_id = mv.run_id
run = tracking_store.get_run(run_id)

import mlflow
response = {
    "name": mv.name,
    "version": mv.version,
    "run_info": run.info.model_dump(),
    "run_data": run.data.model_dump(),
    "config": mlflow.artifacts.load_dict(artifact_uri=f"{run.info.artifact_uri}/config.json"),
    "model_info": mlflow.artifacts.load_dict(artifact_uri=f"{run.info.artifact_uri}/model_info.json")
}

pprint(response, sort_dicts=False)


# import mlflow
# from mlflow.client import MlflowClient
# mlflow_client = MlflowClient("http://localhost:5000")
# pprint(mlflow.artifacts.load_dict(artifact_uri=f"{run.info.artifact_uri}/config.json"))
# artifact_list = mlflow_client.list_artifacts(run.info.run_id)
# # from tracking._tracking_service import list_artifacts
# # artifact_list = list_artifacts(run.info.run_id)




# run = search_run(experiment_ids=["11"], filter_string="run_name = 'test-04'")

# pprint(run)