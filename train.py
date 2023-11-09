import xgboost as xgb
from sklearn.datasets import load_breast_cancer
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("mlflow-bentoml-poc")

# with mlflow.start_run() as run:
#     cancer = load_breast_cancer()
#
#     X = cancer.data
#     y = cancer.target
#
#     dt = xgb.DMatrix(X, label=y)
#
#     param = {"max_depth": 3, "eta": 0.3, "objective": "multi:softprob", "num_class": 2}
#     bst = xgb.train(param, dt)
#
#     mlflow.log_params(param)
#     mlflow.xgboost.log_model(bst, "model")
#
#     bentoml_uri = f"{run.info.artifact_uri}/bento_model"
#     print(bentoml_uri)
#
#     import bentoml
#
#     bento_model = bentoml.xgboost.save_model("booster_tree", bst)
#     bento_model.export(path=f"{bentoml_uri}/model")
#     bentoml.models.delete("booster_tree")
#
#     print(run.info.run_id)

r = mlflow.get_run(run_id="69797f51728145fead9d01c9cf2f0a51")
print(r.info.artifact_uri)
import os
os.environ['BENTOML_HOME'] = "s3://hhk-mlflow/12/69797f51728145fead9d01c9cf2f0a51/artifacts/bento_model"

import bentoml.models
models = bentoml.models.list()
print(models)


# booster_model = bentoml.models.import_model(f"{r.info.artifact_uri}/bento_model/model.bentomodel")
# booster = bentoml.xgboost.load_model(booster_model.tag)
# booster.predict(xgb.DMatrix([[1.308e+01, 1.571e+01, 8.563e+01, 5.200e+02, 1.075e-01, 1.270e-01,
#     4.568e-02, 3.110e-02, 1.967e-01, 6.811e-02, 1.852e-01, 7.477e-01,
#     1.383e+00, 1.467e+01, 4.097e-03, 1.898e-02, 1.698e-02, 6.490e-03,
#     1.678e-02, 2.425e-03, 1.450e+01, 2.049e+01, 9.609e+01, 6.305e+02,
#     1.312e-01, 2.776e-01, 1.890e-01, 7.283e-02, 3.184e-01, 8.183e-02]]))

# cancer = load_breast_cancer()
#
# X = cancer.data
# y = cancer.target
#
# dt = xgb.DMatrix(X, label=y)
#
# param = {"max_depth": 3, "eta": 0.3, "objective": "multi:softprob", "num_class": 2}
# bst = xgb.train(param, dt)
#
