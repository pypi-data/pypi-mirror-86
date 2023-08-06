import os
from pathlib import Path
from typing import Tuple

import yamale
import yaml
from munch import Munch

from .file_utils import isabs
from .file_utils import sopen as open


def yaml_to_specs(
    yaml_file: str,
    path_keys: Tuple = (),
    paths_relative_to_yaml: bool = False,
):
    """Fix paths during conversions"""
    if not isabs(yaml_file):
        yaml_file = os.path.abspath(yaml_file)
    validate_specs_yaml(yaml_file)
    yaml_path = os.path.dirname(yaml_file)
    loaded_dict = Munch(yaml.safe_load(open(yaml_file)))
    if paths_relative_to_yaml:
        for path in path_keys:
            if path not in loaded_dict:
                continue
            if loaded_dict[path] is None:
                continue
            if isabs(loaded_dict[path]):
                continue
            loaded_dict[path] = os.path.abspath(
                os.path.join(yaml_path, loaded_dict[path])
            )
    return loaded_dict


def validate_specs_yaml(specs_yaml_file: str):
    """Validate specs file according to schema defined.
    Returns True if valid. Raises ValueError if not valid
    """
    schema_file = os.path.abspath(
        os.path.join(str(Path(__file__).parent), "../api/schema/specs-schema.yaml")
    )
    schema = yamale.make_schema(schema_file)
    data = yamale.make_data(specs_yaml_file)
    try:
        yamale.validate(schema, data)
        return True
    except yamale.YamaleError as e:
        print(f"Validation failed! for {specs_yaml_file}")
        for result in e.results:
            print(
                "Error validating data '%s' with '%s'\n\t"
                % (result.data, result.schema)
            )
            for error in result.errors:
                print("\t%s" % error)
        raise ValueError
