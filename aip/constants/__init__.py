import os

API_ROOT_DOMAIN = os.environ.get("API_ROOT_DOMAIN", default="http://mlops.arcapi.shinhan.com")
EXPERIMENT_DOMAIN = f"{API_ROOT_DOMAIN}/experiments"
RUN_DOMAIN = f"{API_ROOT_DOMAIN}/runs"
REGISTERED_MODEL_DOMAIN = os.environ.get("REGISTERED_MODEL_DOMAIN", default=f"{API_ROOT_DOMAIN}/models")
MODEL_VERSION_DOMAIN = os.environ.get("MODEL_VERSION_DOMAIN", default=f"{API_ROOT_DOMAIN}/model-versions")

ACTIVE_ONLY, DELETED_ONLY, ALL = range(1, 4)

RUNNING = "RUNNING"
SCHEDULED = "SCHEDULED"
FINISHED = "FINISHED"
FAILED = "FAILED"
KILLED = "KILLED"
