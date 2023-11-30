import os
import aip
import yaml
from aip.auth import AuthConfig

os.environ["AIP_USERNAME"] = "admin"
os.environ["AIP_PASSWORD"] = "new1234!"
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"

os.environ["TASK_TASK_ID"] = "12345"
os.environ["TASK_POD_NAME"] = "sample-pod-name"
os.environ["TASK_TYPE"] = "NOTEBOOK"
os.environ["PROJECT_ID"] = "asdfd12a"
os.environ["AICENTRO_CURRENT_USER"] = "admin"


def final():
    with open("model_info.yaml", encoding="utf-8") as f:
        model_info = yaml.load(f, Loader=yaml.FullLoader)
    configs = {
        "a": "bbb",
        "test2": "test2"
    }


    params = {
        "param1": "p1",
        "param2": 123
    }

    metrics = {
        "l5": 1.5,
        "auc": 0.85
    }

    tracker = aip.create_tracker(tracker_type="NCAI", model_info=model_info, configs=configs)

    tracker.set_experiment(experiment_name="test-ncai_base_model-11")

    run_tags = {
        "task_type": "NOTEBOOK",
        "task_id": "1234",
    }
    tracker.start_run(run_name="s3-test-32", run_tags=run_tags)

    # tracker.log_params(params)
    # tracker.log_metrics(metrics)
    # # print(tracker.model_info)
    tracker.log_model_metadata()
    # print(tracker.run.metadata)

    tracker.end()


# def get_model_version():
#     name = "고객 알뜰 지수"
#     model = aip.get_registered_model(name)
#     mv = model.latest_versions[0]
#     # print(mv)
#     from pprint import pprint
#     aip.get_model_version(name=name, version="3")


def load():
    model = aip.get_model_version(name="B000001", version="1")
    tracker = aip.load_tracker_from_model(model)
    metrics = {
        "metric_code_id": "M000001",
        "metric_seq": "10",
        "threshold": 0.7,
        "numeric_value": 0.8,
        "object_value": "test"
    }
    tracker.log_inference_metrics([metrics])

# get_model_version()
# final()
# load()
from pprint import pprint
# pprint(aip.get_model_version(name="T000001", version="1", detail=True).model_dump(), sort_dicts=False)
pprint(aip.get_latest_model_version(name="T000001").model_dump(), sort_dicts=False)
# pprint(aip.search_model_versions())
# pprint(aip.search_model_versions(filter_string="name='P000001'"))