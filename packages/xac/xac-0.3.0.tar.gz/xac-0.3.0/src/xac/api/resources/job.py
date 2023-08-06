import os
import time
import warnings  # noqa
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import httpx
import requests
import typer
from tabulate import tabulate

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import ExplanationType
from xac.api import HTTP_TIMEOUT
from xac.api.auth.auth import _get_header
from xac.api.config import config
from xac.api.config_file import _default_options
from xac.api.config_file import _generate_options_dict
from xac.utils.file_utils import download_file
from xac.utils.file_utils import exists
from xac.utils.file_utils import isabs
from xac.utils.file_utils import sopen
from xac.utils.helpers import get_human_diff
from xac.utils.helpers import get_human_time
from xac.utils.helpers import multikeysort
from xac.utils.helpers import progress_spinner
from xac.utils.helpers import secho
from xac.utils.helpers import shorten_text
from xac.utils.helpers import validate_data_range
from xac.utils.helpers import validate_sort_keys
from xac.utils.logger import get_logger

warnings.filterwarnings("ignore")  # noqa
import pandas as pd  # noqa

logger = get_logger("JOB", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


class JobRequestBody(str, Enum):
    session_id = "session_id"
    job_name = "name"
    explanation_types = "explanation_types"
    input_ = "input"
    option_overrides = "option_overrides"
    raw_rules = "raw_rules"
    start = "start"
    end = "end"


class JobResponseBody(str, Enum):
    job_id = "id"
    job_name = "name"
    payload = "payload"
    session_id = "session_id"
    create_ts = "create_ts"
    complete_ts = "complete_ts"
    end_ts = "end_ts"
    total_tasks = "total_tasks"
    finished_tasks = "finished_tasks"
    status = "status"


class JobInfoSummary(str, Enum):
    job_id = "job_id"
    job_name = "name"
    status = "status"
    created = "created"
    run_time = "run_time"
    completed = "% comp"
    session_id = "sess_id"


class JobStatus(str, Enum):
    accepted = "accepted"
    running = "running"
    completed = "completed"
    error = "error"
    cancelled = "cancelled"
    deleted = "deleted"


_sort_keys_dict = {
    "created": JobResponseBody.create_ts.value,
    "-created": f"-{JobResponseBody.create_ts.value}",
    "name": JobResponseBody.job_name.value,
    "-name": f"-{JobResponseBody.job_name.value}",
    "status": JobResponseBody.status.value,
    "-status": f"-{JobResponseBody.status.value}",
}


def _build_job_info_summary(
    jobs_list, job_status: Optional[JobStatus], sort_keys=("-created",)
):
    result: dict = {
        JobInfoSummary.job_id.value: [],
        JobInfoSummary.job_name.value: [],
        JobInfoSummary.status.value: [],
        JobInfoSummary.created.value: [],
        JobInfoSummary.run_time.value: [],
        # JobInfoSummary.completed.value: [],
        JobInfoSummary.session_id.value: [],
    }
    if sort_keys:
        sort_keys = validate_sort_keys(sort_keys, _sort_keys_dict)
        logger.debug(f"Sorting jobs list by: {sort_keys}")
        jobs_list = multikeysort(jobs_list, columns=sort_keys)
    for job in jobs_list:
        status = job.get(JobResponseBody.status.value)
        if job_status:
            if status != job_status.value:
                continue
        job_id = job.get(JobResponseBody.job_id.value)
        job_name = job.get(JobResponseBody.job_name.value)
        payload = job.get(JobResponseBody.payload.value)
        if payload:
            session_id = payload.get(JobResponseBody.session_id.value)
            session_name = config.get_session_name_from_id(session_id)
            session_str = (
                f"{session_id} ({session_name})" if session_name else session_id
            )
        else:
            session_str = "-"
        created_human_ts = job.get(JobResponseBody.create_ts.value)
        completed_human_ts = job.get(JobResponseBody.end_ts.value)
        if completed_human_ts:
            run_time = get_human_diff(created_human_ts, completed_human_ts)
        else:
            run_time = "-"
        if created_human_ts:
            created_human = get_human_time(created_human_ts)
        else:
            created_human = "-"
        total_tasks = job.get(JobResponseBody.total_tasks.value, 0)
        finished_tasks = job.get(JobResponseBody.finished_tasks.value, 0)
        completed = (finished_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        completed = f"{completed:.2f}"
        result[JobInfoSummary.job_id.value].append(job_id)
        result[JobInfoSummary.job_name.value].append(job_name)
        result[JobInfoSummary.status.value].append(
            job.get(JobResponseBody.status.value)
        )
        result[JobInfoSummary.created.value].append(created_human)
        result[JobInfoSummary.run_time.value].append(run_time)
        # result[JobInfoSummary.completed.value].append(completed)
        result[JobInfoSummary.session_id.value].append(session_str)
    return result


def get_jobs(
    status: Optional[JobStatus] = None, print_only=False, hide_headers=False
) -> Optional[Dict[str, List]]:
    """List summary of all jobs

    Args:
        status: filter by a desired status given in `JobStatus` enum. One of
            JobStatus.
            accepted
            running
            completed
            error
            cancelled
            deleted

        print_only: if True, just print output, else returns a list containing
            job details
        hide_headers: if True, hide header fields from printed output

    Returns:
        summarized output containing job info or None if error

    Equiv Command Line (Ex):
        `xac jobs` or `xac job ls`
    """
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return None
    if status:
        if not isinstance(status, JobStatus):
            secho("❌ {status} must be of type `xac.job.JobStatus`")
            return None
    logger.debug(f"Get Request to {config.list_jobs_endpoint}")
    try:
        resp = httpx.get(
            config.list_jobs_endpoint, headers=headers, timeout=HTTP_TIMEOUT
        )
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            jobs_list = resp.json()
            if jobs_list is None or jobs_list == []:
                secho("No jobs found. " "Please submit a new job with `xac job submit`")
                return None
            else:
                result = _build_job_info_summary(jobs_list, job_status=status)
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
                f"❌ Unable to fetch job info from sever. Details: {resp.json()}",
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return None


def info(job_id: str, raw=False) -> Optional[Dict[str, Any]]:
    """Get job details for a given `job_id`

    Args:
        job_id: valid `job_id` from a submitted job
        raw: if True, return raw json response output else return a summarized
            output (not valid for command line)

    Returns:
        Dict containing raw or summarized job details or None if error

    Equiv Command Line (Ex):
        `xac job info <job_id>`
    """
    return get_job(job_id, raw=raw)


def get_job(job_id: str, raw=False) -> Optional[Dict[str, Any]]:
    """Get job details for a given `job_id`

    Args:
        job_id: valid `job_id` from a submitted job
        raw: if True, return raw json response output else return a summarized
            output (not valid for command line)

    Returns:
        Dict containing raw or summarized job details or None if error

    Equiv Command Line (Ex):
        `xac job info <job_id>`
    """
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return None
    logger.debug(f"Get Request to {config.get_job_endpoint(job_id)}")
    try:
        resp = httpx.get(
            config.get_job_endpoint(job_id), headers=headers, timeout=HTTP_TIMEOUT
        )
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            job = resp.json()
            if raw:
                return job
            result = _build_job_info_summary([job], job_status=None)
            if len(result[JobInfoSummary.job_id.value]) == 0:
                return None
            else:
                return {k: v[0] for k, v in result.items()}
        else:
            secho(
                f"❌ Unable to fetch job info from sever. Details: {resp.json()}",
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return None


def submit(
    session_id: str,
    input_file: str = None,
    features_list: List[Dict] = None,
    start: int = None,
    end: int = None,
    explanation_types: List[ExplanationType] = None,
    friendly_name: str = None,
    quiet=False,
    raw_rules=False,
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
) -> Optional[str]:
    """Submit a explanation job to the server for a initialized session

    Args:
        session_id: a valid `session_id`. Use `xac.session.init` to create one
        input_file: optional csv file whose rows need explanation
        features_list: list of features (as dict) if `input_file` is None
            (not available in command line)
        start: start row in csv file if a `input_file` is specified
        end: end row in csv file if a `input_file` is specified
        explanation_types: list of supported explanation types outlined in
          `ExplanationType`. One or all of following
           ExplanationType.
                counterfactuals
                local_rules
                local_attributions
                predictions
                global_rules
                global_importances
                model_metrics
                all (a shortcut for all of the above)
        friendly_name:  optional friendly name for the job
        raw_rules: (legacy) if True, return unprocessed rules and counterfactuals
        quiet: no messages to stdout, only return a job_id
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

    Returns:
        A valid `job_id` from server or None if error occurred

    Equiv Command Line (Ex):
        `xac job submit -s <session_id> -i <input_file>  --start <start>
           --end <end> -e local_attributions -e global_importances
           -n <friendly_name> `
    """
    req_body = {}
    kwargs = {k: v for k, v in dict(locals()).items() if k in _default_options}
    options_dict = _generate_options_dict(**kwargs)
    logger.debug(f"Options Dict: {options_dict}")
    if input_file is None and features_list is None:
        if explanation_types is None:
            explanation_types = [ExplanationType.all]
        if isinstance(explanation_types, ExplanationType):
            explanation_types = [explanation_types]
        for et in explanation_types:
            if et in [
                ExplanationType.local_attributions,
                ExplanationType.local_rules,
                ExplanationType.counterfactuals,
                ExplanationType.predictions,
                ExplanationType.model_metrics,  # server wrongly requires start/end
                ExplanationType.all,
            ]:
                start = 0 if start is None else start
                end = 1 if end is None else end
                if et != ExplanationType.model_metrics:
                    logger.debug(f"Start row: {start}, End Row: {end}")
                    if not quiet:
                        secho(
                            f"⚠️  No `input_file` or features specified, "
                            f"using rows {start} to {end} from uploaded dataset"
                        )
                break

    if input_file:
        if not isabs(input_file):
            input_file = os.path.abspath(input_file)
        if not exists(input_file):
            secho(f"❌ File not found : {input_file}", fg=typer.colors.RED, err=True)
            return None
        df = pd.read_csv(sopen(input_file, "r"))
        start, end = validate_data_range(df, start=start, end=end)
        if not quiet:
            secho(
                f"🔢 Sending records {start} to {end} from "
                f"{shorten_text(input_file, width=40)} for explanation"
            )
        req_body[JobRequestBody.input_.value] = df.iloc[start:end].to_dict(
            orient="records"
        )
    else:
        req_body[JobRequestBody.input_.value] = features_list
    session_id = config.get_session_id(session_id)
    req_body[JobRequestBody.session_id.value] = session_id
    if friendly_name:
        req_body[JobRequestBody.job_name.value] = friendly_name
    if explanation_types is None or explanation_types == [ExplanationType.all]:
        pass
    else:
        if isinstance(explanation_types, ExplanationType):
            explanation_types = [explanation_types]
        req_body[JobRequestBody.explanation_types.value] = [
            e.value for e in explanation_types
        ]
    if len(options_dict) > 0:
        req_body[JobRequestBody.option_overrides.value] = options_dict
    if start is not None:
        req_body[JobRequestBody.start.value] = start
    if end is not None:
        req_body[JobRequestBody.end.value] = end
    req_body[JobRequestBody.raw_rules.value] = raw_rules
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return None
    logger.debug(f"Post request to {config.explain_endpoint}")
    logger.debug(f"Request Body: {req_body}")
    try:
        with progress_spinner("Submitting an explanation job", quiet=quiet):
            resp = httpx.post(
                config.explain_endpoint,
                json=req_body,
                headers=headers,
                timeout=HTTP_TIMEOUT,
            )
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.ACCEPTED:
            response = resp.json()
            job_id = response[JobResponseBody.job_id.value]
            job_name = response.get(JobResponseBody.job_name.value, "")
            if not quiet:
                typer.secho(
                    f"🎉 ✅ 🆇 Submitted Explanation Job {job_id} [{job_name}] "
                    f"based on session: [{session_id}]",
                    fg=typer.colors.GREEN,
                )
            return job_id
        else:
            secho(
                f"❌ Error submitting explanation job. Details: {resp.json()}",
                fg=typer.colors.RED,
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return None


def remove_all(quiet: bool = False):
    """Remove all jobs

    Args:
        quiet: no messages to stdout

    Equiv Command Line (Ex):
        `xac job rm -a`
    """
    job_list = get_jobs()
    if job_list is None:
        return
    for job_id in job_list.get(JobInfoSummary.job_id.value, []):
        remove(job_id, quiet=quiet)


def remove(job_id: str, quiet: bool = False) -> bool:
    """Remove a job

    Args:
        job_id: valid `job_id` from server
        quiet: no messages to stdout

    Equiv Command Line (Ex):
        `xac job rm <job_id>`
    """
    headers = _get_header()
    if headers is None:
        return False
    try:
        resp = httpx.get(
            config.get_job_endpoint(job_id), headers=headers, timeout=HTTP_TIMEOUT
        )
        if resp.status_code == httpx.codes.OK:
            job_info = resp.json()
            job_id = job_info[JobResponseBody.job_id.value]
            job_name = job_info[JobResponseBody.job_name.value]
            resp_jid = httpx.delete(
                config.get_job_endpoint(job_id), headers=headers, timeout=HTTP_TIMEOUT
            )
            if resp_jid.status_code != httpx.codes.OK:
                secho(
                    f"❌ Unable to delete job {job_id} " f"Details: {resp_jid.json()}",
                    err=True,
                )
                return False
            if not quiet:
                typer.secho(
                    f"🎉 ✅ 🅹 Job `{job_id} ({job_name})` successfully deleted",
                    fg=typer.colors.BLUE,
                )
            return True
        else:
            secho(f"❌ Unable to delete jon {job_id}. Details: {resp.json()}", err=True)
            return False
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return False


def output(
    job_id: str,
    output_file: Optional[str] = None,
    poll_till_complete: bool = False,
    poll_every: int = 10,
    quiet: bool = False,
) -> Optional[str]:
    """Return or Save  output of an completed explanation job. Optionally, we
    can wait and poll till the job completes.

    Args:
        job_id: valid `job_id` of a explanation job
        output_file: optional path to a file to save the JSON output. If None
            the function will return the JSON string.
        poll_till_complete: optionally poll the server every `poll_very` secs
           till the job completes and save the output
        poll_every: polling interval in seconds. Note this is a blocking call
           and can be used for short-lived jobs. Minimum of 10 seconds and
           maximum of 3600 seconds
        quiet: no messages to stdout, only returns json output

    Returns:
        JSON output if job completed successfully and `config_file` is None
        config_file name if job completed successfully `config_file` is valid
        None if error occured

    Equiv Command Line (Ex):
        `xac job output <job_id> -o <config_file> -w -t 20 `

    """
    result = get_job(job_id)
    if result is None:
        secho("❌ Unable to get job info from server", err=True)
        return None
    if (
        result[JobInfoSummary.status.value] == JobStatus.error.value
        or result[JobInfoSummary.status.value] == JobStatus.deleted.value
        or result[JobInfoSummary.status.value] == JobStatus.cancelled.value
    ):
        secho(
            f"❌ No output can be generated for `{result['status']}` status. ", err=True
        )
        return None
    if poll_till_complete is False:
        if result[JobInfoSummary.status.value] != JobStatus.completed.value:
            secho(
                f"⌛️ Job {job_id} is still in `{result['status']}` status. "
                f"Please wait till completion",
                err=True,
            )
            return None
    else:
        if poll_every is None or poll_every == "":
            poll_every = 10
        poll_every = sorted((10, poll_every, 3600))[1]  # clamp values
        if not quiet:
            print(f"⌛️ [Polling every {poll_every} secs till complete]", end="")
        while True:
            result = get_job(job_id)
            if result is None:
                secho("❌ Error occurred when getting job details from server", err=True)
                return None
            if (
                result[JobInfoSummary.status.value] == JobStatus.completed.value
                or result[JobInfoSummary.status.value] == JobStatus.error.value
                or result[JobInfoSummary.status.value] == JobStatus.deleted.value
                or result[JobInfoSummary.status.value] == JobStatus.cancelled.value
            ):
                if not quiet:
                    print("\n")
                break
            time.sleep(poll_every)
            if not quiet:
                print(".", end="")
    if (
        result[JobInfoSummary.status.value] == JobStatus.error.value
        or result[JobInfoSummary.status.value] == JobStatus.deleted.value
        or result[JobInfoSummary.status.value] == JobStatus.cancelled.value
    ):
        secho(
            f"❌ No output can be generated for `{result['status']}` status. ", err=True
        )
        return None
    if output_file:
        if not isabs(output_file):
            output_file = os.path.abspath(os.path.expanduser(output_file))
    headers = _get_header()
    if headers is None:
        return None
    try:
        resp = requests.get(config.get_job_output_endpoint(job_id), headers=headers)
        if resp.status_code == httpx.codes.OK:
            if output_file:
                download_file(resp.url, output_file)
                typer.secho(
                    f"🎉 ✅ 🅹 Output file for job {job_id} saved to`{output_file}`",
                    fg=typer.colors.GREEN,
                )
                return output_file
            else:
                if not quiet:
                    typer.secho(
                        "🎉 ✅ 🅹 Explanations successfully generated",
                        fg=typer.colors.GREEN,
                    )
                return resp.json()
        else:
            secho(f"❌ Unable to get output. Details: {resp.json()}", err=True)
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return None
