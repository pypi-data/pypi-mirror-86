"""Main entrypoint for API client."""
import ast
import json
import sys
from typing import List

import click
import typer
from click import Option

from xac.api import __version__
from xac.api import DOCS_URL
from xac.api import ExplanationCategory
from xac.api import ExplanationType
from xac.api import SUPPORTED_API_VERSION
from xac.api.auth.auth import login_with_email
from xac.api.auth.auth import purge_tokens
from xac.api.config_file import _default_options
from xac.api.config_file import generate
from xac.api.config_file import generate_empty
from xac.api.info import display_info
from xac.api.resources.job import get_jobs
from xac.api.resources.job import info as _job_info
from xac.api.resources.job import JobStatus
from xac.api.resources.job import output
from xac.api.resources.job import remove as job_remove
from xac.api.resources.job import remove_all as job_remove_all
from xac.api.resources.job import submit
from xac.api.resources.session import get_sessions
from xac.api.resources.session import info as _sess_info
from xac.api.resources.session import init
from xac.api.resources.session import remove as sess_remove
from xac.api.resources.session import remove_all as sess_remove_all
from xac.api.resources.usage import get_quota

# from xac.api.resources.usage import get_usage

app = typer.Typer()
session_app = typer.Typer()
job_app = typer.Typer()
config_app = typer.Typer()

app.add_typer(
    session_app,
    name="session",
    help="Manage and Create Sessions for Explanations",
)
app.add_typer(
    job_app,
    name="job",
    help="Manage and Generate Explanations with Xaipient API",
)
app.add_typer(
    config_app,
    name="config",
    help="Generate Xaipient YAML config files for customization",
)


def print_version(ctx: click.Context, param: Option, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    typer.echo(f"v{__version__}")
    raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        False,
        "--version",
        help="Print CLI version and exit.",
        callback=print_version,  # type: ignore
    )
):
    """
    Client for the Xaipient Explainability API.
    """
    _ = version


@config_app.command("empty")
def config_empty(
    config_file: str = typer.Option(
        None, "--config-file", "-o", help="Output yaml file to be generated"
    ),
):
    """Generate an empty config file for further customization"""
    yaml_str = generate_empty(config_file=config_file)
    if config_file is None:
        print(yaml_str)
    else:
        print(config_file)


@config_app.command("gen")
def config_generate(
    title: str = typer.Option(
        ..., "--title", "-n", help="A concise description of the task"
    ),
    model_type: str = typer.Option(
        ...,
        "--model-type",
        "-t",
        help="Type of model to be explained (keras|torch|xgboost|lightgbm)",
    ),
    model: str = typer.Option(..., "--model", "-m", help="Path to a valid model file"),
    data: str = typer.Option(
        ..., "--model-type", "-d", help="Path to a valid CSV file"
    ),
    feature_grammar: str = None,
    coltrans: str = None,
    target: str = None,
    categorical_columns: str = None,
    classification: bool = None,
    scale_std: bool = False,
    scale_minmax: bool = False,
    threshold: float = 0.5,
    rule_space_max: int = 10000,
    cf_zoo: bool = True,
    cf_quantile: float = 0.5,
    cf_fixed_features: str = None,
    target_labels: str = None,
    use_preprocessor_ordering: bool = None,
    is_rnn: bool = False,
    time_steps: int = None,
    vstacked: bool = None,
    groupby_columns: str = None,
    slice: str = None,
    n_inputs_torch_model: int = None,
    fairness_dropped_coltrans: str = None,
    fairness_gan_cfg_model_type: str = None,
    fairness_gan_cfg_model: str = None,
    fairness_protected_attr: str = None,
    fairness_in_set: str = None,
    fairness_out_set: str = None,
    fairness_in_label: str = None,
    fairness_out_label: str = None,
    config_file: str = typer.Option(
        None, "--config-file", "-o", help="Output yaml file to be generated"
    ),
):
    """Generate an config file based on parameters"""
    kwargs = dict(locals())
    if categorical_columns:
        categorical_columns = ast.literal_eval(categorical_columns)
        kwargs["categorical_columns"] = categorical_columns
    if cf_fixed_features:
        cf_fixed_features = ast.literal_eval(cf_fixed_features)
        kwargs["cf_fixed_features"] = cf_fixed_features
    if target_labels:
        try:
            target_labels = ast.literal_eval(target_labels)
        except ValueError:
            typer.secho(
                "❌ Enter config_target_labels dict  in following "
                'format as string e.g: \'{0: "bad", 1: "good"}\''
            )
            return
        target_labels = {  # type: ignore
            int(k): v for k, v in target_labels.items()  # type: ignore
        }  # type: ignore
        kwargs["target_labels"] = target_labels
    if fairness_dropped_coltrans:
        fairness_dropped_coltrans = ast.literal_eval(fairness_dropped_coltrans)
        kwargs["fairness_dropped_coltrans"] = fairness_dropped_coltrans
    if fairness_in_set:
        try:
            fairness_in_set = ast.literal_eval(fairness_in_set)
        except ValueError:
            fairness_in_set = fairness_in_set
    if fairness_out_set:
        try:
            fairness_out_set = ast.literal_eval(fairness_out_set)
        except ValueError:
            fairness_out_set = fairness_out_set
    yaml_str = generate(**kwargs)
    if config_file is None:
        print(yaml_str)
    else:
        print(config_file)


@session_app.command("init")
def session_init(
    config_file: str = typer.Option(
        ..., "--config-file", "-f", help="path to Xaipient config file (YAML)"
    ),
    category: ExplanationCategory = typer.Option(
        ExplanationCategory.TABULAR, "--category", "-c", help="Explanation Category"
    ),
    friendly_name: str = typer.Option(
        None, "--name", "-n", help="Friendly session name"
    ),
    paths_relative_to_config: bool = typer.Option(
        False,
        "--relative-to-config",
        "-r",
        help="(non-absolute) paths specified in config-file (model, data, coltrans) "
        "are relative to config-file location ",
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Silence messages to stdout"
    ),
):
    """Initialize new session with config file"""
    session_id = init(
        config_yaml=config_file,
        explanation_category=category,
        friendly_name=friendly_name,
        paths_relative_to_config=paths_relative_to_config,
        quiet=quiet,
    )
    if session_id and quiet:
        print(session_id)


@app.command("sessions")
def list_sessions(
    hide_headers: bool = typer.Option(False, "-h", help="Hide headers from table")
):
    """ List all created sessions. Shortcut for `xac job ls`"""
    get_sessions(print_only=True, hide_headers=hide_headers)


@session_app.command("ls")
def session_ls(
    hide_headers: bool = typer.Option(False, "-h", help="Hide headers from table")
):
    """List all previously created sessions"""
    get_sessions(print_only=True, hide_headers=hide_headers)


@session_app.command("rm")
def session_remove(
    session_id: str = typer.Argument(None, help="Session Id for session to delete"),
    all: bool = typer.Option(
        False, "--all", "-a", help="Delete all sessions (Might take a while)"
    ),
):
    """Remove a session by its name or id"""
    if session_id is None and all is False:
        typer.secho("❌ Session name or id required: `xac session rm <session-id>`")
        return None
    if all:
        typer.confirm("Are you sure you want to delete all sessions?", abort=True)
        sess_remove_all()
    else:
        sess_remove(session_id)


@session_app.command("info")
def session_info(session_id: str = typer.Argument(..., help="Session Id")):
    """ Get details of an explanation session by its `session_id`"""
    print(json.dumps(_sess_info(session_id, raw=True)))


@job_app.command("submit")
def job_submit(
    input_file: str = typer.Option(
        None, "--input_file", "-i", help="CSV file to explain"
    ),
    session_id_or_name: str = typer.Option(
        ...,
        "--session-id-or-name",
        "-s",
        help="Session name generated from a previously initialized session",
    ),
    explanation_type: List[ExplanationType] = typer.Option(
        ...,
        "--explanation-type",
        "-e",
        help="Explanation Type. Use -e multiple times for multiple explanation types "
        "[use `all` to return every available explanation type]",
    ),
    start: int = typer.Option(
        0, "--start", help="start index of data csv file to be explained"
    ),
    end: int = typer.Option(
        1,
        "--end",
        help="ending index of data csv file to be explained. enter -1 for last row",
    ),
    friendly_name: str = typer.Option(None, "--name", "-n", help="Friendly job name"),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Silence messages to stdout"
    ),
    raw_rules: bool = typer.Option(
        False,
        "--raw-rules",
        help="Return unprocessed rules ans counterfactuals (legacy)",
    ),
    classification: bool = None,
    scale_std: bool = None,
    scale_minmax: bool = None,
    threshold: float = None,
    rule_space_max: int = None,
    cf_zoo: bool = None,
    cf_quantile: float = None,
    cf_fixed_features: str = None,
    target_labels: str = None,
    use_preprocessor_ordering: bool = None,
    is_rnn: bool = None,
    time_steps: int = None,
    vstacked: bool = None,
    groupby_columns: str = None,
    slice: str = None,
    n_inputs_torch_model: int = None,
):
    """Submit explanation jobs from a previously initialized session"""
    kwargs = {k: v for k, v in dict(locals()).items() if k in _default_options}
    if cf_fixed_features:
        cf_fixed_features = ast.literal_eval(cf_fixed_features)
        kwargs["cf_fixed_features"] = cf_fixed_features
    if target_labels:
        try:
            target_labels = ast.literal_eval(target_labels)
        except ValueError:
            typer.secho(
                "❌ Enter config_target_labels dict  in following "
                'format as string e.g: \'{0: "bad", 1: "good"}\''
            )
            return
        target_labels = {  # type: ignore
            int(k): v for k, v in target_labels.items()  # type: ignore
        }  # type: ignore
        kwargs["target_labels"] = target_labels
    job_id = submit(
        session_id=session_id_or_name,
        input_file=input_file,
        start=start,
        end=end,
        explanation_types=explanation_type,
        friendly_name=friendly_name,
        quiet=quiet,
        raw_rules=raw_rules,
        **kwargs,
    )
    if job_id and quiet:
        print(job_id)


@app.command("jobs")
def list_jobs(
    status: JobStatus = typer.Option(
        None, "--status", "-s", help="Filter Job by status"
    ),
    hide_headers: bool = typer.Option(False, "-h", help="Hide headers from table"),
):
    """ List explanation jobs. Shortcut for `xac job ls`"""
    get_jobs(status=status, print_only=True, hide_headers=hide_headers)


@job_app.command("ls")
def jobs_ls(
    status: JobStatus = typer.Option(
        None, "--status", "-s", help="Filter Job by status"
    ),
    hide_headers: bool = typer.Option(False, "-h", help="Hide headers from table"),
):
    """List all previously created explanation jobs"""
    get_jobs(status=status, print_only=True, hide_headers=hide_headers)


@job_app.command("rm")
def jobs_remove(
    job_id: str = typer.Argument(None, help="Job id to delete"),
    all: bool = typer.Option(
        False, "--all", "-a", help="Delete all jobs (Might take a while)"
    ),
):
    """Remove an explanation job by `job_id`"""
    if job_id is None and all is False:
        typer.secho("❌ Job Id required: `xac job rm <job-id>")
        return None
    if all:
        typer.confirm("Are you sure you want to delete all jobs?", abort=True)
        job_remove_all()
    else:
        job_remove(job_id)


@job_app.command("info")
def jobs_info(job_id: str = typer.Argument(..., help="Job id")):
    """ Get details of an explanation job by its `job_id`"""
    print(json.dumps(_job_info(job_id, raw=True)))


@job_app.command("output")
def jobs_output(
    job_id: str = typer.Argument(..., help="Job id to save if completed"),
    output_file: str = typer.Option(
        None, "--output-file", "-o", help="Name of output (JSON) file"
    ),
    poll_till_complete: bool = typer.Option(
        False,
        "--wait-till-complete",
        "-w",
        help="Wait for job to complete and save output",
    ),
    poll_every: int = typer.Option(10, "-t", help="Poll every t seconds"),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Silence messages to stdout"
    ),
):
    """Get output from a completed job by `job_id`"""
    if job_id is None:
        typer.secho("❌ Job Id required: `xac job output <job-id>")
        return None
    json_out = output(
        job_id=job_id,
        output_file=output_file,
        poll_till_complete=poll_till_complete,
        poll_every=poll_every,
        quiet=quiet,
    )
    if output_file is None:
        print(json.dumps(json_out))


@app.command()
def login(
    email: str = typer.Option(default=None),
):
    """Login with email and password."""
    if not email:
        email = click.prompt("Email", type=str)
        email = email.strip()
    success = login_with_email(email)
    if not success:
        sys.exit(1)
    sys.exit(0)


@app.command()
def logout():
    """Logout and purge any tokens."""
    purge_tokens()


@app.command()
def info():
    """Display key information about API"""
    display_info()


@app.command()
def docs():
    """Open xac documentation in a new browser tab"""
    import webbrowser

    typer.confirm("Are you sure you want open URL in a new browser tab?", abort=True)
    typer.secho(f"Opening {DOCS_URL} in default browser tab...")
    try:
        webbrowser.open_new_tab(DOCS_URL)
    except webbrowser.Error:
        typer.secho(
            f"Cannot open {DOCS_URL} in default browser tab",
            err=True,
            fg=typer.colors.RED,
        )


@app.command()
def version():
    """Display current version of client and API."""
    typer.secho(
        f"XAC API version: v{SUPPORTED_API_VERSION} (Supported by CLI)",
        fg=typer.colors.GREEN,
    )
    typer.secho(f"XAC CLI version: v{__version__}", fg=typer.colors.GREEN)


# @app.command()
# def usage():
#     """Check usage against quotas for current user account"""
#     return get_usage(raw=False)


@app.command()
def quota():
    """Check usage against quotas for current user account"""

    return get_quota(raw=False)
