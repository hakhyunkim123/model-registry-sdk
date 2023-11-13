import os
import aip
import yaml
from aip.auth import AuthConfig

os.environ["AIP_USERNAME"] = "admin"
os.environ["AIP_PASSWORD"] = "new1234!"
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"


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

    tracker = aip.create_tracker(tracker_type="SACP", model_info=model_info, configs=configs)

    experiment_tags = {
        "type": "NCAI"
    }

    tracker.set_experiment(experiment_name="ncai_base_model", tags=experiment_tags)

    run_tags = {
        "type": "NCAI",
        "task_type": "NOTEBOOK",
        "task_id": "1234",
    }
    tracker.start_run(run_name="test3", run_tags=run_tags)

    tracker.log_params(params)
    tracker.log_metrics(metrics)
    # print(tracker.model_info)
    # tracker.log_model_metadata()
    # print(tracker.run.metadata)

    tracker.end()


def get_model_version():
    name = "고객 알뜰 지수"
    model = aip.get_registered_model(name)
    mv = model.latest_versions[0]
    # print(mv)
    from pprint import pprint
    aip.get_model_version_detail(name=name, version="3")


def load():
    tracker = aip.load_tracker(run_id="34499753774e454c8177ebc38ff886ba")
    tracker.log_model_metadata()
# get_model_version()
# final()
# load()

# print(aip.get_registered_model(name="P000001"))
from pprint import pprint
pprint(aip.get_model_version_detail(name="P000001", version="1").model_dump(), sort_dicts=False)