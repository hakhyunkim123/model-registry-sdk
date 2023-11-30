import aip
import aip.ncai
from aip.models import Model

import os


def init():
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

    return model_info, configs


def test(test_type: str = None):
    model_info, configs = init()
    if test_type == "REGISTER":
        model_version = aip.ncai.register_basemodel(model_info=model_info, configs=configs)
        # print(model_version)

    from aip.models import Model
    model = Model.latest_version(name="T000004")
    print(model.name)
    print(model.version)

    if test_type == "RETRAIN":
        tracker = model.start_retrain_tracker()

        metrics = [
            {
                "metric_code_id": "M000001",
                "metric_seq": "0",
                "threshold": "3.5",
                "numeric_value": "4.65",
                "object_value": "오브젝트 값",
                "metric_cal_time": "20231127180012",
            },
            {
                "metric_code_id": "M000002",
                "metric_seq": "0",
                "threshold": "3.5",
                "numeric_value": "4.65",
                "object_value": "오브젝트 값",
                "metric_cal_time": "20231127180012",
            },
            {
                "metric_code_id": "M0000015",
                "metric_seq": "0",
                "numeric_value": "4.65",
                "object_value": "오브젝트 값",
                "metric_cal_time": "20231127180012",
            },
            {
                "metric_code_id": "M0000015",
                "metric_seq": "1",
                "numeric_value": "4.65",
                "object_value": "오브젝트 값",
                "metric_cal_time": "20231127180012",
            }
        ]
        tracker.log_ncai_metrics(metrics)

        tracker.end()

    if test_type == "HISTORY":
        retrain_history = model.get_retrain_history()
        for retrain_info in retrain_history:
            print(retrain_info.ncai_metrics)


    # model_versions = aip.search_model_versions(filter_string="tags.type='NCAI' and tags.model_type='BASE'")
    # model = Model.from_model_version(model_versions[0])
    # retrain_history = model.get_retrain_history()
    # for retrain_info in retrain_history:
    #     print(retrain_info.ncai_metrics)


if __name__ == "__main__":
    test_type = "HISTORY"
    test(test_type=test_type)
