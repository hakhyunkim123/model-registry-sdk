import aip
import os
from datetime import datetime

## SACP DUMMPY TAGS
os.environ["TASK_TASK_ID"] = "12345"
os.environ["TASK_POD_NAME"] = "sample-pod-name"
os.environ["TASK_TYPE"] = "NOTEBOOK"
os.environ["PROJECT_ID"] = "asdfd12a"
os.environ["AICENTRO_CURRENT_USER"] = "admin"

## DEFAULT ENV
os.environ["AIP_USERNAME"] = "admin"
os.environ["AIP_PASSWORD"] = "new1234!"

# DICT YAML
import yaml
with open("model_info.yaml", encoding="utf-8") as f:
    model_info = yaml.load(f, Loader=yaml.FullLoader)
configs = {
    "a": "bbb",
    "test2": "test2"
}


def register_model():
    model_id = model_info.get("id")
    run_name = f"{model_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    tracker = aip.create_tracker(tracker_type="NCAI", model_info=model_info, configs=configs)
    tracker.set_experiment(experiment_name=model_id)
    tracker.start_run(run_name=run_name)
    tracker.log_model_metadata()
    tracker.end()


def load_model():
    model_id = model_info.get("id")
    latest_model = aip.get_latest_model_version(name=model_id)
    return latest_model


def load_and_train():
    model_id = model_info.get("id")
    latest_model = aip.get_latest_model_version(name=model_id)
    tracker = aip.create_tracker(tracker_type="NCAI")
    tracker.set_experiment(latest_model.name)

    from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID
    run_name = f"{latest_model.name}/{latest_model.version}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    run_tags = {
        "model_id": latest_model.name,
        "model_version": latest_model.version,
        MLFLOW_PARENT_RUN_ID: latest_model.run_id
    }

    # print(run_name)
    run = tracker.start_run(run_name=run_name, run_tags=run_tags)

    metrics = [
        {
            "metric_code_id": "M000001",
            "metric_seq": "0",
            "threshold": "3.5",
            "numeric_value": "4.65",
            "object_value": "오브젝트 값",
            "metric_cal_time": "20231127180012",
        }
    ]
    tracker.log_ncai_metrics(metrics)

    tracker.end()

# load_and_train()

from mlflow.client import MlflowClient
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"
client = MlflowClient("http://localhost:5000")
print(client.get_parent_run(run_id="d7167cacf89240c78fd508e409223d31"))
# print(client.search_runs(experiment_ids=["2"], filter_string="run_name='T000001/1-20231127175144'"))
# print(aip.search_run(experiment_id="2", filter_string="run_name='T000001'"))



# register_model()
# aip.get_run(run_id="4f73cb7dce1a4cb2a784fcbb106d421f", detail=True)
# load_and_train()
# print(aip.search_run(experiment_id="2"))


def nested_run():
    from mlflow.client import MlflowClient
    os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
    os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"

    client = MlflowClient("http://localhost:5000")
    exp_id = "2"
    run_id = "4f73cb7dce1a4cb2a784fcbb106d421f"
    from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID
    print(MLFLOW_PARENT_RUN_ID)
    child_run_1 = client.create_run(
        experiment_id=exp_id,
        tags={
            MLFLOW_PARENT_RUN_ID: run_id
        }
    )

def model_stage():
    from mlflow.client import MlflowClient
    os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
    os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"

    client = MlflowClient("http://localhost:5000")

    model = client.get_model_version(name="T000001", version="3")
    from mlflow.entities.model_registry.model_version_stages import ALL_STAGES, STAGE_STAGING, STAGE_NONE, STAGE_PRODUCTION
    client.transition_model_version_stage(name=model.name, version=model.version, stage=STAGE_STAGING)
    print(model)


# nested_run()

def model_test():
    model_id = model_info.get("id")
    latest_model = aip.get_latest_model_version(name=model_id)
    from aip.models import Model
    model = Model.from_model_info(latest_model)
    print(model.info)

# register_model()
# model_stage()
# model_test()

# model_name = "T000001"
# print(aip.get_registered_model(model_name))
# print(aip.get_latest_model_version(model_name, detail=True))
# model_version = aip.get_model_version(name=model_name, version="1", detail=True)
# print(model_version.info)