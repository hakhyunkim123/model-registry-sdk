import os

import mlflow
from mlflow.client import MlflowClient
from aip.entities.run import Run
from pprint import pprint

os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"

client = MlflowClient("http://localhost:5000")

run = client.get_run(run_id="4f73cb7dce1a4cb2a784fcbb106d421f")
parent_run = client.get_parent_run(run.info.run_id)
child_run_ids = client.search_runs(experiment_ids=[run.info.experiment_id],
                                   filter_string=f"tags.mlflow.parentRunId='{run.info.run_id}'")

run_dict = run.to_dictionary()
del run_dict['data']['tags']['mlflow.log-model.history']
run_dict['info']['parent_run_id'] = parent_run.info.run_id if parent_run is not None else None
run_dict['info']['child_run_ids'] = [child_run.info.run_id for child_run in child_run_ids]
pprint(run_dict, sort_dicts=False)


# run.data.metrics
client.get_metric_history()