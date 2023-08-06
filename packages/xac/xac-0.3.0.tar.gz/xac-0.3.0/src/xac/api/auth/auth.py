"""Authorization API functionality."""
import getpass
import re
from datetime import datetime
from enum import Enum

import httpx
import typer
from munch import Munch

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import HTTP_TIMEOUT
from xac.api.config import config
from xac.api.config import XacConfigFileType
from xac.utils.helpers import get_expiry_human
from xac.utils.helpers import secho
from xac.utils.logger import get_logger

logger = get_logger("AUTH", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


class AuthRequestBody(str, Enum):
    email = "email"
    password = "password"  # noqa: S105


class AuthResponseBody(str, Enum):
    email = "email"
    display_name = "display_name"
    id_token = "id_token"  # noqa: S105
    refresh_token = "refresh_token"  # noqa: S105
    expires_by = "expires_by"


def _get_header():
    token = _get_access_token()
    if token:
        return {"Authorization": f"bearer {token}"}
    else:
        return None


def _get_access_token(login=False):
    expires_by = config.get_val(AuthResponseBody.expires_by.value)
    requires_refresh = True
    if expires_by:
        expiry_time = datetime.fromtimestamp(float(expires_by))
        if expiry_time <= datetime.now():
            requires_refresh = True
        else:
            requires_refresh = False
    access_token = config.access_token
    if access_token and not requires_refresh:
        return access_token
    else:
        refresh_token = config.refresh_token
        if refresh_token is None:
            if login and config.password:
                secho(
                    "❌ No token available. Logging in with password",
                    fg=typer.colors.RED,
                    err=True,
                )
            else:
                secho(
                    "❌ No token available. Kindly login again ",
                    fg=typer.colors.RED,
                    err=True,
                )
            return None
        try:
            logger.debug(f"Post request to endpoint: {config.refresh_endpoint}")
            logger.debug(f"Request Body: 'refresh_token': {refresh_token}")
            resp = httpx.post(
                config.refresh_endpoint,
                json={AuthResponseBody.refresh_token.value: refresh_token},
                timeout=HTTP_TIMEOUT,
            )
            logger.debug(f"Response Received: {resp.json()}")
            if resp.status_code == httpx.codes.OK:
                response = resp.json()
                id_token = response[AuthResponseBody.id_token.value]
                refresh_token = response[AuthResponseBody.refresh_token.value]
                expires_by = response[AuthResponseBody.expires_by.value]
                config.save_tokens(id_token, refresh_token, expires_by)
                return id_token
            else:
                secho(
                    f"❌ Error getting token from server. Details: {resp.json()}",
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


def _is_email_valid(email):
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return False
    else:
        return True


def _login_success_msg(email, display_name, expires_by):
    _ = get_expiry_human(expires_by)
    typer.secho(
        f"👋.Welcome {display_name} <{email}>. Type `xac --help` to explore further",
        fg=typer.colors.GREEN,
    )


def _save_user_settings(email: str, display_name: str):
    config.save_setting(AuthResponseBody.email.value, email)
    config.save_setting(AuthResponseBody.display_name.value, display_name)


def purge_tokens():
    config.purge(file_type=XacConfigFileType.All)
    typer.secho(
        "✅ [Logout Success]. Saved tokens have been purged. Please relogin to access API",
        fg=typer.colors.BLUE,
    )


def current_user():
    user_email = config.get_val(AuthResponseBody.email.value)
    if user_email:
        return Munch(
            {
                "email": user_email,
                "display_name": config.get_val(AuthResponseBody.display_name.value),
            }
        )
    else:
        return None


def login_with_email(email: str):
    user = current_user()
    logger.debug(f"User : {user}")
    if user and email != user.email:
        secho(
            f"❌ No token available for {email}. Authenticating with password..",
            fg=typer.colors.RED,
            err=True,
        )
    else:
        if _get_access_token(login=True):
            logger.debug("Getting cached token data")
            user_display_name = user.display_name
            expires_by = config.get_val(AuthResponseBody.expires_by.value)
            _login_success_msg(user.email, user_display_name, expires_by)
            return True
    if not _is_email_valid(email):
        secho(
            f"❌ Email: {email} is not a valid email address. Please retry again",
            fg=typer.colors.RED,
            err=True,
        )
        return False
    password = config.password
    if password is None:
        password = getpass.getpass(prompt="Password: ")
    try:
        logger.debug(f"Post request to {config.login_endpoint}")
        logger.debug(f"Request Body : email: {email}, password: {password}")
        resp = httpx.post(
            config.login_endpoint,
            data={
                AuthRequestBody.email.value: email,
                AuthRequestBody.password.value: password,
            },
            timeout=HTTP_TIMEOUT,
        )
        logger.debug(f"Response received: {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            response = resp.json()
            user_email = response[AuthResponseBody.email.value]
            user_display_name = response[AuthResponseBody.display_name.value]
            expires_by = response[AuthResponseBody.expires_by.value]
            id_token = response[AuthResponseBody.id_token.value]
            refresh_token = response[AuthResponseBody.refresh_token.value]
            _save_user_settings(user_email, user_display_name)
            config.save_tokens(id_token, refresh_token, expires_by)
            _login_success_msg(user_email, user_display_name, expires_by)
            return True
        elif (
            resp.status_code == httpx.codes.BAD_REQUEST
            or resp.status_code == httpx.codes.UNAUTHORIZED
        ):
            secho(
                "❌ Invalid credentials. Please check your email or password",
                fg=typer.colors.RED,
                err=True,
            )
            return False
        else:
            secho(
                f"❌ Error Occurred. Details: {resp.json()}",
                fg=typer.colors.RED,
                err=True,
            )
        return False
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return False
