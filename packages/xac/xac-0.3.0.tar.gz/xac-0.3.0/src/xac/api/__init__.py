from enum import Enum
from pathlib import Path

from dynaconf import Dynaconf

_RELEASE = True
__version__ = "0.3.0"
SUPPORTED_API_VERSION = "1.1.0+"

HOSTNAME = "https://api.xaipient.com/v1/"
DOCS_URL = "https://xaipient.github.io/xaipient-docs/docs/"
_LOGLEVEL = "error" if _RELEASE else "debug"
_LOG_TO_FILE_ONLY = True
_DEV_ENV_PREFIX = "XAC_DEV"
_PROD_ENV_PREFIX = "XAC"

HTTP_TIMEOUT = 20


class ModelType(str, Enum):
    KERAS = "keras"
    TORCH = "torch"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"


class ExplanationType(str, Enum):
    counterfactuals = "counterfactuals"
    local_rules = "local_rules"
    local_attributions = "local_attributions"
    global_rules = "global_rules"
    global_importances = "global_importances"
    global_alignments = "global_alignments"
    model_metrics = "model_metrics"
    predictions = "predictions"
    all = "all"


class ExplanationCategory(str, Enum):
    TABULAR = "tabular"


def get_settings():
    if _RELEASE is False:
        envvar_prefix_for_dynaconf = _DEV_ENV_PREFIX
        dynaconf_settings_file = Path.home() / ".xaipient-dev" / "settings.yaml"
        dynaconf_secrets_file = Path.home() / ".xaipient-dev" / ".secrets.yaml"
        settings = Dynaconf(
            envvar_prefix=envvar_prefix_for_dynaconf,
            settings_files=[str(dynaconf_settings_file), str(dynaconf_secrets_file)],
        )
    else:
        envvar_prefix_for_dynaconf = _PROD_ENV_PREFIX
        dynaconf_settings_file = Path.home() / ".xaipient" / "settings.yaml"
        dynaconf_secrets_file = Path.home() / ".xaipient" / ".secrets.yaml"
        settings = Dynaconf(
            envvar_prefix=envvar_prefix_for_dynaconf,
            settings_files=[str(dynaconf_settings_file), str(dynaconf_secrets_file)],
        )

    return settings


TF_SAVEDMODEL_FILENAME = "saved_model.pb"
TF_SAVEDMODEL_FILENAME_TXT = "saved_model.pbtxt"
