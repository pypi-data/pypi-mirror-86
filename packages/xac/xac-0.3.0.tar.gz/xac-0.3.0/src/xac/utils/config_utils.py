import os
from collections import OrderedDict
from copy import deepcopy
from typing import Any

import yamale
import yaml

yaml.Dumper.ignore_aliases = lambda *args: True  # type: ignore
represent_dict_order = lambda self, data: self.represent_mapping(  # noqa
    "tag:yaml.org,2002:map", data.items()  # noqa
)
yaml.add_representer(OrderedDict, represent_dict_order)

_types_dict = {
    "str": str,
    "int": int,
    "bool": bool,
    "num": float,
    "list": list,
    "map": dict,
    "any": Any,
}

_types_str_dict = {
    "str": "str",
    "int": "int",
    "bool": "bool",
    "num": "float",
    "list": "list",
    "map": "dict",
    "any": "any",
}

_default_dict = {
    "str": "",
    "int": 0,
    "bool": False,
    "num": 0.0,
    "list": ["item1", "item2"],
    "map": {0: "label1", 1: "label2"},
    "any": 0,
}

_default_options = {
    "classification": "options_classification",
    "scale_std": "options_scale_std",
    "scale_minmax": "options_scale_minmax",
    "threshold": "options_threshold",
    "rule_space_max": "options_rule_space_max",
    "cf_zoo": "options_cf_zoo",
    "cf_quantile": "options_cf_quantile",
    "cf_fixed_features": "options_cf_fixed_features",
    "target_labels": "options_target_labels",
    "use_preprocessor_ordering": "options_use_preprocessor_ordering",
    "is_rnn": "options_is_rnn",
    "time_steps": "options_time_steps",
    "vstacked": "options_vstacked",
    "groupby_columns": "options_groupby_columns",
    "slice": "options_slice",
    "n_inputs_torch_model": "options_n_inputs_torch_model",
}

_help_strings = {
    "title": "A concise description of the task (e.g German Credit Data)",
    "model_type": "Type of model to be explained (keras|torch|xgboost|lightgbm)",
    "model": "Path to a valid model file",
    "data": "Path to a valid CSV file for computing features and global explns",
    "feature_grammar": "Path to grammar file specifying feature-grouping",
    "coltrans": "Path to a scikit-learn column transformer pickle file",
    "target": "The target column in CSV file (optional if coltrans is provided)",
    "categorical_columns": "List of categorical columns (optional if coltrans is provided)",
    "classification": "if true, whether this is a classification task",
    "scale_std": "if true, apply standard scaling to numeric columns",
    "scale_minmax": "if true, apply minmax scaling to numeric columns",
    "threshold": "Threshold for binary classification (0.0 to 1.0)",
    "rule_space_max": "Max set of examples to use for rules",
    "cf_zoo": "If true, use zoo for counterfactual",
    "cf_quantile": "max quantile-change for counterfactual (0.0 to 1.0)",
    "cf_fixed_features": "List of features to hold fixed for counterfactual",
    "target_labels": "Map of target (int) ->labels (str), e.g {0: 'Good', 1: 'Bad'}",
    "use_preprocessor_ordering": "respect preprocessor ordering in column transformer",
    "is_rnn": "If true, model is a timeseries (rnn) model",
    "time_steps": "for an rnn model: number of timesteps are in an input seq",
    "vstacked": "If true, rnn model the given dataframe has stacked sequences",
    "groupby_columns": "for an rnn model: grouping columns for extracting sequences",
    "slice": "dataframe query to pre-slice the data",
    "n_inputs_torch_model": "Number of inputs to model (only for pytorch models)",
}


def _parse_schema(schema, schema_dict=None, prefix=None, key=None):
    if schema_dict is None:
        schema_dict = OrderedDict()
    for k, v in schema.dict.items():
        if isinstance(v, yamale.validators.Include):
            name = v.include_name
            schema_dict[k] = OrderedDict()
            _parse_schema(schema.includes[name], schema_dict[k], prefix=k, key=key)
        else:
            if key == "required":
                schema_dict[k] = v.is_required
            elif key == "default":
                schema_dict[k] = _default_dict[v.tag]
            elif key == "type_str":
                schema_dict[k] = _types_str_dict[v.tag]
            elif key == "type":
                schema_dict[k] = _types_dict[v.tag]
            elif key == "name":
                schema_dict[k] = f"{prefix}_{k}" if prefix else k
            elif key == "help":
                schema_dict[k] = _help_strings.get(k, "")
            elif key == "params":
                name = f"{prefix}_{k}" if prefix else k
                schema_dict[name] = _types_str_dict[v.tag]
            else:
                schema_dict[k] = {
                    "required": v.is_required,
                    "type_str": _types_str_dict[v.tag],
                    "type": _types_dict[v.tag],
                    "name": f"{prefix}_{k}" if prefix else k,
                    "help": _help_strings.get(k, ""),
                    "default": _default_dict[v.tag],
                }


def _get_config_info(key=None):
    schema_file = os.path.join(
        os.path.join(os.path.dirname(os.path.dirname(__file__))),
        "api/schema/specs-schema.yaml",
    )
    schema = yamale.make_schema(schema_file)
    my_dict = OrderedDict()
    _parse_schema(schema, my_dict, key=key)
    return deepcopy(my_dict)
