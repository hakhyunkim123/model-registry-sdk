from aip.entities.sacp.sacp_task_info import SACPTaskInfo

import os
os.environ["TASK_TASK_ID"] = "12345"
os.environ["TASK_POD_NAME"] = "sample-pod-name"
os.environ["TASK_TYPE"] = "NOTEBOOK"
os.environ["PROJECT_ID"] = "asdfd12a"
os.environ["AICENTRO_CURRENT_USER"] = "admin"