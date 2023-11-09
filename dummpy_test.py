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
    tracker.start_run(run_name="ncai_base_model", run_tags=run_tags)

    tracker.log_params(params)
    tracker.log_metrics(metrics)
    tracker.log_model_metadata()

    tracker.end()


def get_model_version():
    name = "고객 알뜰 지수"
    model = aip.get_registered_model(name)
    mv = model.latest_versions[0]
    # print(mv)
    from pprint import pprint
    aip.get_model_version_detail(name=name, version="3")


get_model_version()
#
#
#
#
#
#
#
#
#
#
# # tracker = aip.create_tracker(configs=configs, model_info=model_info)
# # tracker.set_experiment(experiment_name="ftest-01")
# # # print(tracker.experiment)
# # run = tracker.start_run(run_name="test", run_tags={"type": "NCAI"})
# # tracker.log_params(params)
# # tracker.log_metrics(metrics)
# # tracker.set_tag(key="test", value="test2")
# # tracker.log_model_metadata()
# # tracker.end()
# from pprint import pprint
# pprint(aip.get_run_detail(run_id="76777c7f27e649edbfe6dca97492e97e").model_dump(), sort_dicts=False)
# # print(run)
#
# # tracker = aip.create_tracker(tracker_type="SACP", experiment_name="auth-test", configs=configs, model_info=model_info)
# # tracker.start_run(run_name="sdk-test-01")
# # tracker.log_param("n_threads", "10")
# # tracker.log_metric("l5", 1.5)
# # # tracker.log_model()
# # tracker.refresh_run()
# # # print(tracker.run)
# # tracker.end()
#
# # tracker = aip.create_tracker(tracker_type="SACP", experiment_name="sdk-test", configs=configs, model_info=model_info)
# # tracker.start_run(run_name="sdk-test-01")
# # tracker.log_param("n_threads", "10")
# # tracker.log_metric("l5", 1.5)
# # # tracker.log_model()
# # tracker.refresh_run()
# # # print(tracker.run)
# # tracker.end()
# # from pprint import pprint
# # r = aip.get_run("7defd911d22f49ad80a27f30de124081", ["config", "model_info"])
# # r = aip.get_run("7defd911d22f49ad80a27f30de124081")
# # pprint(r.model_dump(), sort_dicts=False)
# # mv = aip.get_model_version(name="test", version="2")
# # from mlflow.client import MlflowClient
# # mc = MlflowClient("http://localhost:5000")
# # exp = mc.get_experiment_by_name("sdk-test")
# # run = mc.get_run("7defd911d22f49ad80a27f30de124081")
# # print(run)
# # mc.create_run(exp.experiment_id, run_name="run1", sour)
#
#
# # import mlflow
# # mlflow.log_params()
# # mlflow.log_metrics()
# import aip.store.model_store
#
# print(aip.store.model_store.search_registered_models(filter_string="name='ai-test23'"))
# print(aip.store.model_store.get_registered_model("ai-test23"))