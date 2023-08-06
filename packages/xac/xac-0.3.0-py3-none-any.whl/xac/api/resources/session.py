"""Create a new explanation session"""
import os
import tempfile
from enum import Enum
from typing import AnyStr
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import httpx
import typer
from munch import Munch
from tabulate import tabulate

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import ExplanationCategory
from xac.api import HTTP_TIMEOUT
from xac.api import ModelType
from xac.api.auth.auth import _get_header
from xac.api.config import config
from xac.api.resources.upload import upload_data
from xac.api.resources.upload import upload_model
from xac.utils.file_utils import exists
from xac.utils.file_utils import isabs
from xac.utils.file_utils import sopen
from xac.utils.helpers import get_human_time
from xac.utils.helpers import multikeysort
from xac.utils.helpers import progress_spinner
from xac.utils.helpers import secho
from xac.utils.helpers import validate_sort_keys
from xac.utils.logger import get_logger
from xac.utils.yaml_loader import yaml_to_specs

logger = get_logger("SESSION", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


class SessionRequestBody(str, Enum):
    title_str = "title"
    coltrans = "coltrans"
    is_rnn = "is_rnn"
    specs = "specs"
    categorical_columns = "categorical_columns"
    target = "target"
    options = "options"
    data_id = "data_id"
    model_id = "model_id"
    session_name = "name"
    description = "description"
    feature_grammar = "feature_grammar"


class SessionResponseBody(str, Enum):
    title_str = "title"
    data_id = "data_id"
    model_id = "model_id"
    session_id = "id"
    session_name = "name"
    description = "description"
    session = "session"
    create_ts = "create_ts"


class SessionInfoSummary(str, Enum):
    data_id = "data_id"
    model_id = "model_id"
    specs = "specs"
    description = "description"
    session_id = "session_id"
    session_name = "name"
    created = "created"


_sort_keys_dict = {
    "created": SessionResponseBody.create_ts.value,
    "-created": f"-{SessionResponseBody.create_ts.value}",
    "name": SessionResponseBody.session_name.value,
    "-name": f"-{SessionResponseBody.session_name.value}",
    "description": SessionResponseBody.description.value,
    "-description": f"-{SessionResponseBody.description.value}",
}


def _load_feature_grammar(specs: Munch) -> Tuple[Optional[AnyStr], bool]:
    feature_grammar_path = specs.get(SessionRequestBody.feature_grammar.value)
    if feature_grammar_path:
        if not isabs(feature_grammar_path):
            feature_grammar_path = os.path.abspath(feature_grammar_path)
        if not exists(feature_grammar_path):
            secho(
                f"❌ Error loading feature_grammar file {feature_grammar_path}",
                fg=typer.colors.RED,
                err=True,
            )
            logger.debug(
                f"Feature grammar file {feature_grammar_path} set "
                f"in specs but does not exist in path"
            )
            return None, False
        return sopen(feature_grammar_path, "r").read(), True
    else:
        logger.debug("Feature grammar file not set in specs itself")
        return None, True


def _generate_req_dict(
    model_id: str,
    dataset_id: str,
    specs: Munch,
    friendly_name=None,
    feature_grammar_text=None,
):
    req_dict = {
        SessionRequestBody.data_id.value: dataset_id,
        SessionRequestBody.model_id.value: model_id,
        SessionRequestBody.specs.value: {},
        SessionRequestBody.description.value: specs.get(
            SessionRequestBody.title_str.value, ""
        ),
    }
    if friendly_name:
        req_dict[SessionRequestBody.session_name.value] = friendly_name
    if feature_grammar_text:
        req_dict[SessionRequestBody.specs.value][
            SessionRequestBody.feature_grammar.value
        ] = feature_grammar_text

    coltrans = specs.get(SessionRequestBody.coltrans.value)
    if coltrans is None:
        if SessionRequestBody.categorical_columns.value in specs:
            req_dict[SessionRequestBody.specs.value][
                SessionRequestBody.categorical_columns.value
            ] = specs.categorical_columns
        if SessionRequestBody.target.value in specs:
            req_dict[SessionRequestBody.specs.value][
                SessionRequestBody.target.value
            ] = specs.target
    req_dict[SessionRequestBody.specs.value][
        SessionRequestBody.options.value
    ] = specs.options
    return req_dict


def _build_session_info_summary(sessions_list, sort_keys=("-created",)):
    result = {
        SessionInfoSummary.session_id.value: [],
        SessionInfoSummary.session_name.value: [],
        SessionInfoSummary.description.value: [],
        SessionInfoSummary.created.value: [],
        # SessionInfoSummary.data_id.value: [],
        # SessionInfoSummary.model_id.value: [],
    }
    if sort_keys:
        sort_keys = validate_sort_keys(sort_keys, _sort_keys_dict)
        logger.debug(f"Sorting session list by: {sort_keys}")
        sessions_list = multikeysort(sessions_list, columns=sort_keys)
    for session in sessions_list:
        session_id = session.get(SessionResponseBody.session_id.value)
        session_name = session.get(SessionResponseBody.session_name.value)
        created_human_ts = session.get(SessionResponseBody.create_ts.value)
        if session_name is None:
            session_name = "-"
        result[SessionInfoSummary.session_name.value].append(session_name)
        result[SessionInfoSummary.session_id.value].append(session_id)
        result[SessionInfoSummary.description.value].append(
            session.get(SessionResponseBody.description.value)
        )
        if created_human_ts:
            created_human = get_human_time(created_human_ts)
        else:
            created_human = "-"
        result[SessionInfoSummary.created.value].append(created_human)
        # result[SessionInfoSummary.data_id.value].append(
        #     session.get(SessionResponseBody.data_id.value)
        # )
        # result[SessionInfoSummary.model_id.value].append(
        #     session.get(SessionResponseBody.model_id.value)
        # )
    return result


def info(session_id: str, raw=False) -> Optional[Dict]:
    """Get session details for a given `session_id`

    Args:
        session_id: valid `session_id` from a initialized session
        raw: if True, return raw json response output else return a
            summarized output (not valid for command line)

    Returns:
        Dict containing raw or summarized session details
        output or None if error

    Equiv Command Line (Ex):
        `xac session info <session_id>`
    """
    return get_session(session_id=session_id, raw=raw)


def get_session(session_id: str, raw=False) -> Optional[Dict]:
    """Get session details for a given `session_id`

    Args:
        session_id: valid `session_id` from a initialized session
        raw: if True, return raw json response output else return a
            summarized output (not valid for command line)

    Returns:
        Dict containing raw or summarized session details
        output or None if error

    Equiv Command Line (Ex):
        `xac session info <session_id>`
    """
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return None
    logger.debug(f"Get Request to {config.get_resource_endpoint(session_id)}")
    try:
        resp = httpx.get(
            config.get_resource_endpoint(session_id),
            headers=headers,
            timeout=HTTP_TIMEOUT,
        )
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            sess = resp.json()
            if raw:
                return sess
            result = _build_session_info_summary([sess])
            if len(result[SessionInfoSummary.session_id.value]) == 0:
                return None
            else:
                return {k: v[0] for k, v in result.items()}
        else:
            secho(
                f"❌ Unable to fetch session info from sever. Details: {resp.json()}",
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌ Error connecting to server. Please contact Xaipient team", err=True)
        return None


def get_sessions(print_only=False, hide_headers=False) -> Optional[Dict[str, List]]:
    """List summary of all jobs

    Args:
        print_only: if True, just print output, else returns a list
            containing session details
        hide_headers: if True, hide header fields from printed output

    Returns:
        Summarized output containing session info or None if error

    Equiv Command Line (Ex):
        `xac sessions` or `xac session ls`
    """
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return None
    logger.debug(f"Get Request to {config.list_resources_endpoint}")
    try:
        resp = httpx.get(
            config.list_resources_endpoint, headers=headers, timeout=HTTP_TIMEOUT
        )
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            session_list = resp.json().get(SessionResponseBody.session.value)
            if session_list is None or session_list == []:
                secho(
                    "No saved sessions found. "
                    "Please initialize a session with `xac session init`"
                )
                return None
            else:
                result = _build_session_info_summary(session_list)
                if print_only:
                    if hide_headers:
                        print(tabulate(result, tablefmt="plain"))
                    else:
                        print(tabulate(result, headers="keys"))
                    return None
                else:
                    return result
        else:
            secho(
                f"❌ Unable to fetch session info from sever. Details: {resp.json()}",
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌ Error connecting to server. Please contact Xaipient team", err=True)
        return None


def remove_all(quiet: bool = False):
    """Remove all sessions

    Args:
        quiet: no messages to stdout

    Equiv Command Line (Ex):
        `xac session rm -a`
    """
    session_list = get_sessions()
    if session_list is None:
        return
    for session_id in session_list.get(SessionInfoSummary.session_id.value, []):
        remove(session_id, quiet=quiet)


def remove(session_id: str, quiet: bool = False) -> bool:
    """Remove a session

    Args:
        session_id: valid `session_id` from a initialized session
        quiet: no messages to stdout

    Equiv Command Line (Ex):
        `xac session rm <session_id>`
    """
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return False
    logger.debug(f"Get Request to {config.get_resource_endpoint(session_id)}")
    try:
        resp = httpx.get(
            config.get_resource_endpoint(session_id),
            headers=headers,
            timeout=HTTP_TIMEOUT,
        )
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            session_info = resp.json()
            session_id = session_info[SessionResponseBody.session_id.value]
            session_name = session_info[SessionResponseBody.session_name.value]
            session_name = session_name if session_name else "--"
            model_id = session_info[SessionResponseBody.model_id.value]
            data_id = session_info[SessionResponseBody.data_id.value]
            logger.debug(
                f"Delete Request to {config.get_resource_endpoint(session_id)}"
            )
            resp_sid = httpx.delete(
                config.get_resource_endpoint(session_id),
                headers=headers,
                timeout=HTTP_TIMEOUT,
            )
            logger.debug(f"Received Response {resp_sid.json()}")
            if resp_sid.status_code != httpx.codes.OK:
                secho(
                    f"❌ Unable to delete session {session_id} ({session_name}). "
                    f"Details: {resp_sid.json()}",
                    err=True,
                )
                return False
            logger.debug(f"Delete Request to {config.get_resource_endpoint(model_id)}")
            resp_mid = httpx.delete(
                config.get_resource_endpoint(model_id),
                headers=headers,
                timeout=HTTP_TIMEOUT,
            )
            logger.debug(f"Received Response {resp_mid.json()}")
            if resp_mid.status_code != httpx.codes.OK:
                secho(
                    f"❌ Unable to delete model {model_id}. Details: {resp_mid.json()}",
                    err=True,
                )
                return False
            logger.debug(f"Delete Request to {config.get_resource_endpoint(data_id)}")
            resp_did = httpx.delete(
                config.get_resource_endpoint(data_id),
                headers=headers,
                timeout=HTTP_TIMEOUT,
            )
            logger.debug(f"Received Response {resp_did.json()}")
            if resp_did.status_code != httpx.codes.OK:
                secho(
                    f"❌ Unable to delete data {data_id}. Details: {resp_did.json()}",
                    err=True,
                )
                return False
            if not quiet:
                typer.secho(
                    f"🎉 ✅ 🆂 Session `{session_id} ({session_name})`"
                    f"successfully deleted",
                    fg=typer.colors.BLUE,
                    err=True,
                )
            return True
        else:
            secho(
                f"❌ Unable to delete session {session_id}. Details: {resp.json()}",
                err=True,
            )
            return False
    except Exception as e:
        logger.debug(str(e))
        secho("❌ Error connecting to server. Please contact Xaipient team", err=True)
        return False


def init(
    config_yaml=None,
    config_yaml_str=None,
    explanation_category: ExplanationCategory = ExplanationCategory.TABULAR,
    friendly_name: str = None,
    paths_relative_to_config=False,
    quiet: bool = False,
) -> Optional[str]:
    """Initialize an explanation session

    Args:
        config_yaml: path to Xaipient yaml config file
        config_yaml_str: YAML string containing config
        explanation_category: category of explanation outlined in
          `ExplanationCategory` .(Currently only ExplanationCategory.TABULAR is
           supported)
        friendly_name: optional friendly name for session
        paths_relative_to_config: if True, any relative paths specified in the
            config file ['model', 'coltrans', 'data', 'feature_grammar'] will
            be relative to the yaml file location.
            If False, will default relative to current working path location.
            Does not matter for absolute paths
        quiet: no messages to stdout, only return a session_id

    Returns:
        A valid `session_id` from server or None if error occurred

    Equiv Command Line:
        `xac session init -f <config_yaml> -c tabular -n <friendly_name> -r `
    """
    if config_yaml is None and config_yaml_str is None:
        secho(
            "❌ `config_yaml` and `config_yaml_str` both cannot be None",
            fg=typer.colors.RED,
            err=True,
        )
        return None
    if config_yaml_str:
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as tmpfile:
            tmpfile.write(config_yaml_str)
            config_yaml = tmpfile.name
        logger.debug(f"Saving YAML string to {tmpfile.name}")
    if not isabs(config_yaml):
        config_yaml = os.path.abspath(os.path.expanduser(config_yaml))
    try:
        specs = yaml_to_specs(
            config_yaml,
            path_keys=("model", "data", "coltrans", "feature_grammar"),
            paths_relative_to_yaml=paths_relative_to_config,
        )
    except (ValueError, FileNotFoundError) as e:
        logger.debug(str(e))
        secho(f"❌ Invalid config file: {config_yaml}", fg=typer.colors.RED, err=True)
        return None
    # Check feature grammar if specified
    feature_grammar_text, file_exist = _load_feature_grammar(specs)
    if feature_grammar_text is None and file_exist is False:
        logger.debug("Feature Grammar not found and exists in config. Exiting")
        return None
    # 1. Upload Data
    dataset_id = upload_data(csv_filepath=specs.data, quiet=quiet)
    logger.debug(f"Uploaded {specs.data} and got {dataset_id} frm server")
    if dataset_id is None:
        return None
    # 2. Upload Model
    is_time_series = specs.options.get(SessionRequestBody.is_rnn.value, False)
    model_id = upload_model(
        model_path=specs.model,
        model_type=ModelType(specs.model_type),
        column_transformer_path=specs.get("coltrans"),
        description=specs.title,
        is_time_series=is_time_series,
        tags=[],
        explanation_category=explanation_category,
        quiet=quiet,
    )
    logger.debug(
        f"Uploaded {specs.model}, {specs.get('coltrans')} and "
        f"got {model_id} from server"
    )
    if model_id is None:
        return None
    if model_id and dataset_id:
        req_dict = _generate_req_dict(
            model_id, dataset_id, specs, friendly_name, feature_grammar_text
        )
        headers = _get_header()
        if headers is None:
            logger.debug("Auth header is None")
            return None
        logger.debug(f"Post request to {config.new_session_endpoint}")
        logger.debug(f"Request Body: {req_dict}")
        try:
            with progress_spinner("Creating a new session", quiet=quiet):
                resp = httpx.post(
                    config.new_session_endpoint,
                    json=req_dict,
                    headers=headers,
                    timeout=HTTP_TIMEOUT,
                )
            logger.debug(f"Received Response: {resp.json()}")
            if resp.status_code == httpx.codes.CREATED:
                resp_data = resp.json()
                session_id = resp_data[SessionResponseBody.session_id.value]
                session_name = resp_data.get(SessionResponseBody.session_name.value, "")
                if not quiet:
                    typer.secho(
                        f"🎉 ✅ 🆂 Session {session_id} [{session_name}] created",
                        fg=typer.colors.GREEN,
                    )
                return session_id
            else:
                secho(
                    f"❌ Error creating session. Details: {resp.json()}",
                    fg=typer.colors.RED,
                    err=True,
                )
                return None
        except Exception as e:
            logger.debug(str(e))
            secho(
                "❌ Error connecting to server. Please contact Xaipient team", err=True
            )
            return None
    else:
        secho("❌ An error occurred: Please contact Xaipient team", err=True)
        return None
