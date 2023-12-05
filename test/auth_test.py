import os
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"

from typing import List
from mlflow.exceptions import MlflowException
from mlflow.server import get_app_client
from mlflow.server.auth.client import AuthServiceClient
from mlflow.server.auth.entities import User, ExperimentPermission, RegisteredModelPermission
from mlflow.server.auth.permissions import (
    EDIT
)

auth_client: AuthServiceClient = get_app_client("basic-auth", tracking_uri="http://localhost:5000")


# created_user = auth_client.create_user(username="ncai", password="new1234!")
user: User = auth_client.get_user(username="admin")
experiment_permissions: List[ExperimentPermission] = user.experiment_permissions
model_permissions: List[RegisteredModelPermission] = user.registered_model_permissions
# try:
#     experiment_permissions: List[ExperimentPermission] = user.experiment_permissions
# except MlflowException as error:
#     if error.error_code == "RESOURCE_DOES_NOT_EXIST":
#         experiment_permissions = []
#
# try:
#     model_permissions: List[RegisteredModelPermission] = user.registered_model_permissions
# except MlflowException as error:
#     if error.error_code == "RESOURCE_DOES_NOT_EXIST":
#         model_permissions = []

# print(type(user))

# print(experiment_permissions)
# for experiment_permission in experiment_permissions:
#     print(experiment_permission.experiment_id, experiment_permission.permission)

for model_permission in model_permissions:
    print(model_permission.name, model_permission.permission)
# print(model_permissions)


