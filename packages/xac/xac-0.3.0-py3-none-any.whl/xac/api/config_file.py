"""Helper utils for generating xac explainability config"""
# flake8: noqa
import os
from collections import OrderedDict
from typing import Union

import yaml

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.utils.config_utils import _default_options
from xac.utils.config_utils import _get_config_info
from xac.utils.file_utils import isabs
from xac.utils.file_utils import sopen
from xac.utils.logger import get_logger

logger = get_logger("CONFIG_GEN", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


def generate_empty(config_file: str = None):
    """Generate an empty YAML config file for further modification

    Args:
        config_file: Path to output YAML config file to be generated

    Returns:
        A valid Xaipient config YAML string. This YAML strings includes
        all optional keys. Please refer to documentation to check
        which keys are required for the explanation task at hand
    """
    config_dict = _get_config_info(key="default")
    if config_file:
        if not (isabs(config_file)):
            config_file = os.path.abspath(os.path.expanduser(config_file))
        yaml.dump(config_dict, sopen(config_file, "w"), default_flow_style=False)
    return yaml.dump(config_dict, default_flow_style=False)


def generate(
    title: str,
    model_type: str,
    model: str,
    data: str,
    feature_grammar: str = None,
    coltrans: str = None,
    target: str = None,
    categorical_columns: list = None,
    classification: bool = None,
    scale_std: bool = False,
    scale_minmax: bool = False,
    threshold: float = 0.5,
    rule_space_max: int = 10000,
    cf_zoo: bool = True,
    cf_quantile: float = 0.5,
    cf_fixed_features: list = None,
    target_labels: dict = None,
    use_preprocessor_ordering: bool = None,
    is_rnn: bool = False,
    time_steps: int = None,
    vstacked: bool = None,
    groupby_columns: list = None,
    slice: str = None,
    n_inputs_torch_model: int = None,
    fairness_dropped_coltrans: list = None,
    fairness_gan_cfg_model_type: str = None,
    fairness_gan_cfg_model: str = None,
    fairness_protected_attr: str = None,
    fairness_in_set: Union[int, bool, str] = None,
    fairness_out_set: Union[int, bool, str] = None,
    fairness_in_label: str = None,
    fairness_out_label: str = None,
    config_file: str = None,
    as_dict: bool = False,
):
    """Generate config file from parameters

    Args:
        title: A concise description of the task (e.g German Credit Data)
        model_type: Type of model to be explained (keras|torch|xgboost|lightgbm)
        model: Path to a valid model file
        data: Path to a valid CSV file for computing features and global explns
        feature_grammar: Path to a .lark file for advanced parsing (WIP)
        coltrans: Path to a scikit-learn column transformer pickle file
        target: The target column in CSV file (optional if coltrans is provided)
        categorical_columns: List of categorical columns (optional if coltrans is valid)
        classification: if true, whether this is a classification task
        scale_std: if true, apply standard scaling to numeric columns
        scale_minmax: if true, apply minmax scaling to numeric columns
        threshold: Threshold for binary classification (0.0 to 1.0)
        rule_space_max: Max set of examples to use for rules
        cf_zoo: If true, use zoo for counterfactuals
        cf_quantile: max quantile-change for counterfactual (0.0 to 1.0)
        cf_fixed_features: List of features to hold fixed for counterfactual
        target_labels: Map of target (int) ->labels (str), {0: 'Good', 1: 'Bad'}
        use_preprocessor_ordering:
            if true, respect preprocessor ordering in column transformer
        is_rnn: If true, model is a time-series (rnn) model
        time_steps: number of timesteps in an input seq for a rnn model
        vstacked: If true, rnn model the given dataframe has stacked sequences
        groupby_columns:
            for an rnn model, list of grouping columns for extracting sequences
        slice: dataframe query string to pre-slice the data
        n_inputs_torch_model:
            Number of inputs to model (only for pytorch models)
        fairness_dropped_coltrans:
            for fairness, columns to be dropped [optional, list of string]
        fairness_gan_cfg_model_type:
            for fairness, GAN model type
        fairness_gan_cfg_model:
            for fairness, GAN model path
        fairness_protected_attr: for fairness, protected attribute
        fairness_in_set: for fairness, protected group value (class) input to GAN
        fairness_out_set: for fairness, protected group value (class) output of GAN
        fairness_in_label: for fairness, label of in-set
        fairness_out_label: for fairness, label of out-set
        config_file: Path to output YAML config file to be generated
        as_dict: Return a dictionary instead of yaml string

    Returns:
        A valid Xaipient config YAML string or a dict

    """
    kwargs: OrderedDict = OrderedDict(locals())
    logger.debug(f"Received Params: {dict(kwargs)}")
    config_dict: OrderedDict = OrderedDict()
    for k, v in kwargs.items():
        # Handle default options carefully
        if k in _default_options:
            k = _default_options[k]
        if k == "config_file" or k == "as_dict":
            continue
        if "options_" in k:
            if "options" in config_dict:
                if v is not None and v != "":
                    name = k.split("options_")[-1]
                    config_dict["options"][name] = v
            else:
                config_dict["options"] = OrderedDict()
                if v is not None and v != "":
                    name = k.split("options_")[-1]
                    config_dict["options"][name] = v
        elif "fairness_" in k:
            if "fairness" in config_dict:
                if v is not None and v != "":
                    name = k.split("fairness_")[-1]
                    config_dict["fairness"][name] = v
            else:
                config_dict["fairness"] = OrderedDict()
                if v is not None and v != "":
                    name = k.split("fairness_")[-1]
                    config_dict["fairness"][name] = v
            if len(config_dict["fairness"]) == 0:
                del config_dict["fairness"]
        else:
            if v is not None and v != "":
                config_dict[k] = v
    if "fairness" in config_dict:
        fairness_dict: OrderedDict = OrderedDict()
        for k, v in config_dict["fairness"].items():
            if "gan_cfg_" in k:
                if "gan_cfg" in fairness_dict:
                    if v is not None and v != "":
                        name = k.split("gan_cfg_")[-1]
                        fairness_dict["gan_cfg"][name] = v
                else:
                    fairness_dict["gan_cfg"] = OrderedDict()
                    if v is not None and v != "":
                        name = k.split("gan_cfg_")[-1]
                        fairness_dict["gan_cfg"][name] = v
            else:
                fairness_dict[k] = config_dict["fairness"][k]
        config_dict["fairness"] = fairness_dict
    logger.debug(f"Generated YAML Dict: {dict(config_dict)}")
    if as_dict:
        return dict(config_dict)
    if config_file:
        if not (isabs(config_file)):
            config_file = os.path.abspath(os.path.expanduser(config_file))
        yaml.dump(config_dict, sopen(config_file, "w"), default_flow_style=False)
    return yaml.dump(config_dict, default_flow_style=False)


def _generate_options_dict(
    classification: bool = None,
    scale_std: bool = None,
    scale_minmax: bool = None,
    threshold: float = None,
    rule_space_max: int = None,
    cf_zoo: bool = None,
    cf_quantile: float = None,
    cf_fixed_features: list = None,
    target_labels: dict = None,
    use_preprocessor_ordering: bool = None,
    is_rnn: bool = None,
    time_steps: int = None,
    vstacked: bool = None,
    groupby_columns: list = None,
    slice: str = None,
    n_inputs_torch_model: int = None,
):
    kwargs: OrderedDict = OrderedDict(locals())
    kwargs["title"] = ""
    kwargs["model_type"] = ""
    kwargs["model"] = ""
    kwargs["data"] = ""
    kwargs["as_dict"] = True
    config_dict = generate(**kwargs)
    return dict(config_dict["options"])
