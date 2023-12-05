from typing import Dict, Any
from datetime import datetime

from aip.entities.tracker import TrackerType
from aip.entities.run import RunType
from aip.entities.model import ModelType
from aip.entities.model_info import ModelInfo
from aip.entities.model_version import ModelVersion, ModelVersionStage
from aip.tracking.trackers.ncai_tracker import NCAITracker
from aip.store.model_store import transition_model_version_stage


def register_basemodel(
        model_info: Dict[str, Any],
        configs: Dict[str, Any],
        model_stage: str = ModelVersionStage.STAGE_NONE,
        vertica_insert: bool = False
) -> ModelVersion:
    """
    Register NCAI basemodel
    :param model_info: ModelInfo data
    :param configs: Configs of NCAI Training
    :param model_stage: Stage of Model(NONE, STAGING, PRODUCTION, ARCHIVED)
    :param vertica_insert: If True, Insert to vertica table (NCAI_MODEL_INFO)
    :return: ModelVersion
    """
    model_info = ModelInfo(**model_info)
    model_id = model_info.id
    experiment_name = model_id
    run_name = f"{model_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    tracker = NCAITracker(model_info=model_info.dict(), configs=configs)
    tracker.set_experiment(experiment_name=experiment_name)
    run_tags = {
        "type": TrackerType.NCAI,
        "run_type": RunType.BASE,
        "model_id": model_id
    }
    tracker.start_run(run_name=run_name, run_tags=run_tags)

    model_tags = {
        "model_type": ModelType.BASE
    }
    model_version = tracker.log_model_metadata(tags=model_tags, vertica_insert=vertica_insert)

    tracker.set_tag("model_version", model_version.version)
    tracker.end()
    tracker.update_run(name=f"{model_version.name}/{model_version.version}")

    if vertica_insert:
        transition_model_version_stage(name=model_version.name, version=model_version.version,
                                       stage=model_stage, vertica_update=vertica_insert)

    return model_version
