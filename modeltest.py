import os
from mlflow.client import MlflowClient
from mlflow.models import Model

os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"

mc = MlflowClient("http://localhost:5000")
exp = mc.get_experiment_by_name("internal_test")
# run = mc.create_run(exp.experiment_id, run_name="model-logging-test")
run = mc.get_run("08142ad6b58541ac96135331a816935f")
mlf_model = Model(artifact_path="model", run_id=run.info.run_id)
mlf_model.save("MLmodel")
mc.log_artifact(run.info.run_id, "MLmodel", "model")
os.remove("MLmodel")
import requests
json_body = {
    "run_id": run.info.run_id,
    "model_json": mlf_model.to_json()
}
resp = requests.post("http://localhost:5000/api/2.0/mlflow/runs/log-model"
                     , json=json_body
                     , auth=("admin", "new1234!"))
print(resp.status_code)
# print(resp.json())