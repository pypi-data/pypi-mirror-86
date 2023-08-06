"""Displays key info"""
import httpx
import typer

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import _RELEASE
from xac.api import HTTP_TIMEOUT
from xac.api import SUPPORTED_API_VERSION
from xac.api.auth.auth import current_user
from xac.api.config import config
from xac.utils.helpers import secho
from xac.utils.logger import get_logger

logger = get_logger("XAC_INFO", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


def display_info():
    if _RELEASE is False:
        secho("🧨  Running in DEVELOPMENT mode ", fg=typer.colors.GREEN)
    else:
        secho("✅  Running in PRODUCTION mode", fg=typer.colors.GREEN)
    user = current_user()
    if user is None:
        secho("🔓  Not logged in.", fg=typer.colors.RED)
    else:
        secho(
            f"😄  Logged in as {user.display_name}<{user.email}>", fg=typer.colors.GREEN
        )
    if _RELEASE is False:
        secho(f"🖥  Hostname: {config.hostname}")
    try:
        response = httpx.get(config.version_endpoint, timeout=HTTP_TIMEOUT)
        if response.status_code == httpx.codes.OK:
            secho(
                f"✅   Server UP: "
                f"[Response time: {response.elapsed.microseconds/1000:.2f} ms]"
            )
            secho(
                f"🅥  Current API Version"
                f": {response.json().get('server_version','Not Found')} "
                f"(Supported Versions: {SUPPORTED_API_VERSION})"
            )
        else:
            secho(
                f"❌  Error occurred when connecting to {config.hostname}. "
                f"Details {response.json()}",
                err=True,
            )
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
    secho(
        "🅴  Supported explanation types:"
        "\n    GLOBAL"
        "\n    - global_importances"
        "\n    - global_alignments"
        "\n    - global_rules"
        "\n    - model_metrics"
        "\n    LOCAL"
        "\n    - local_attributions"
        "\n    - local_rules"
        "\n    - counterfactuals"
        "\n    - predictions"
    )
