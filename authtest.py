# from mlflow.client import MlflowClient
#
# mc = MlflowClient("http://localhost:5000")
#
# mc.create_experiment(name="aaaaaaaaa")
import os
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "new1234!"
from mlflow.server import get_app_client

tracking_uri = "http://localhost:5000/"

auth_client = get_app_client("basic-auth", tracking_uri=tracking_uri)
auth_client.create_user("20100094", "new1234!")
# import requests
#
# response = requests.get(
#     tracking_uri,
#     auth=("admin", "new1234"),
# )
#
# print(response.status_code)
# print(response.text)
# from mlflow.server.auth.entities import User
# ppp: User = auth_client.get_user(username="admin")


# from mlflow.server.auth.entities import User
# from werkzeug.security import check_password_hash, generate_password_hash
# ppp: User = auth_client.get_user(username="user1")
# from mlflow.server.auth import store
# print(store.authenticate_user("admin", "new1234!"))
# print(ppp.password_hash)
# # print(generate_password_hash("new1234!"))
# # print(ppp.password_hash == generate_password_hash("new1234!"))
# print(check_password_hash(generate_password_hash("new1234!"), ppp.password_hash))
# print(ppp.experiment_permissions)
# from mlflow.server.auth.entities import ExperimentPermission
# pp: ExperimentPermission = auth_client.get_experiment_permission("2", "admin")
# print(pp.permission)
# auth_client.update_user_admin(username="user1", is_admin=True)
