import os
import safer
import shutil
from enum import Enum
from pathlib import Path

import yaml
from yarl import URL

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import _RELEASE
from xac.api import get_settings
from xac.api import HOSTNAME
from xac.utils.logger import get_logger

logger = get_logger("CONFIG", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)
logger.debug("----")


class TokenType(Enum):
    AccessToken = 1
    RefreshToken = 2
    ExpiresBy = 3


class XacConfigFileType(Enum):
    SettingsFile = 1
    SecretsFile = 2
    SessionsFile = 3
    All = 4


class ConfigKeys(str, Enum):
    access_token = "access_token"  # noqa: S105
    refresh_token = "refresh_token"  # noqa: S105
    expires_by = "expires_by"
    hostname = "hostname"
    password = "password"  # noqa: S105


class EndPoints(str, Enum):
    login = "login"
    refresh_token = "refresh-token"  # noqa: S105
    upload_dataset = "resources/upload-dataset"
    upload_model = "resources/upload-model"
    new_session = "resources/new-session"
    explain = "explain"
    resources_list = "resources/list"
    job_list = "job/list"
    version = "version"
    usage = "me/usage"
    quota = "me/quota"


class Config:
    def __init__(self):
        self.host_name = HOSTNAME
        self.config_loc = ".xaipient" if _RELEASE else ".xaipient-dev"
        self.config_path = Path.home() / self.config_loc
        self.secrets_path = self.config_path / ".secrets.yaml"
        self.settings_path = self.config_path / "settings.yaml"
        self.sessions_path = self.config_path / "sessions.yaml"
        if not Path.exists(self.config_path):
            os.makedirs(str(self.config_path))
        logger.debug(self.__dict__)

    def purge(self, file_type: XacConfigFileType):
        if file_type == XacConfigFileType.All:
            if Path.exists(self.config_path):
                shutil.rmtree(str(self.config_path))
        if file_type == XacConfigFileType.SecretsFile:
            if Path.exists(self.secrets_path):
                os.remove(str(self.secrets_path))
        if file_type == XacConfigFileType.SettingsFile:
            if Path.exists(self.settings_path):
                os.remove(str(self.settings_path))
        if file_type == XacConfigFileType.SessionsFile:
            if Path.exists(self.sessions_path):
                os.remove(str(self.sessions_path))

    def save_token(self, token, token_type: TokenType):
        if self.secrets_path.exists():
            secrets_dict = yaml.load(
                open(str(self.secrets_path)), Loader=yaml.SafeLoader
            )
        else:
            if not Path.exists(self.config_path):
                os.makedirs(str(self.config_path))
            secrets_dict = {}
        if token_type == token_type.AccessToken:
            secrets_dict[ConfigKeys.access_token.value] = token
        if token_type == token_type.RefreshToken:
            secrets_dict[ConfigKeys.refresh_token.value] = token
        if token_type == token_type.ExpiresBy:
            secrets_dict[ConfigKeys.expires_by.value] = token
        with safer.open(str(self.secrets_path), "w") as fp:
            yaml.dump(secrets_dict, fp)

    def save_tokens(self, access_token, refresh_token, expires_by):
        if self.secrets_path.exists():
            secrets_dict = yaml.load(
                open(str(self.secrets_path)), Loader=yaml.SafeLoader
            )
        else:
            if not Path.exists(self.config_path):
                os.makedirs(str(self.config_path))
            secrets_dict = {}
        secrets_dict[ConfigKeys.access_token.value] = access_token
        secrets_dict[ConfigKeys.refresh_token.value] = refresh_token
        secrets_dict[ConfigKeys.expires_by.value] = expires_by
        with safer.open(str(self.secrets_path), "w") as fp:
            yaml.dump(secrets_dict, fp)

    def save_setting(self, key: str, value):
        if self.settings_path.exists():
            settings_dict = yaml.load(
                open(str(self.settings_path)), Loader=yaml.SafeLoader
            )
        else:
            if not Path.exists(self.config_path):
                os.makedirs(str(self.config_path))
            settings_dict = {}
        settings_dict[key] = value
        with safer.open(str(self.settings_path), "w") as fp:
            yaml.dump(settings_dict, fp)

    def save_session(self, session_name: str, session_id: str, default=False):
        if self.sessions_path.exists():
            session_dict = yaml.load(
                open(str(self.sessions_path)), Loader=yaml.SafeLoader
            )
        else:
            if not Path.exists(self.config_path):
                os.makedirs(str(self.config_path))
            session_dict = {}
        if default:
            session_dict["default"] = session_id
        session_dict[session_id] = session_name
        with safer.open(str(self.sessions_path), "w") as fp:
            yaml.dump(session_dict, fp)

    def get_session_id(self, session_name_or_id: str = None):
        if self.sessions_path.exists():
            session_dict = yaml.load(
                open(str(self.sessions_path)), Loader=yaml.SafeLoader
            )
            if session_name_or_id is None:
                session_id = session_dict.get("default")
                return session_id
            if session_name_or_id in session_dict.keys():
                return session_name_or_id
            else:
                session_id = self.get_session_id_from_name(session_name_or_id)
                if session_id is None:
                    return session_name_or_id
                else:
                    return session_id
        else:
            return session_name_or_id

    def get_session_id_from_name(self, session_name: str = None):
        if self.sessions_path.exists():
            session_dict = yaml.load(
                open(str(self.sessions_path)), Loader=yaml.SafeLoader
            )
            if session_name is None:
                session_name = session_dict.get("default")
            for k, v in session_dict.items():
                if v == session_name:
                    return k
            return None
        else:
            return None

    def get_session_name_from_id(self, session_id: str = None):
        if self.sessions_path.exists():
            session_dict = yaml.load(
                open(str(self.sessions_path)), Loader=yaml.SafeLoader
            )
            if session_id is None:
                session_id = session_dict.get("default")
            session_name = session_dict.get(session_id)
            return session_name
        else:
            return None

    @property
    def hostname(self) -> str:
        settings = get_settings()
        self.host_name = settings.get(ConfigKeys.hostname.value, HOSTNAME, fresh=True)
        if self.host_name == "":
            self.host_name = HOSTNAME
        return self.host_name

    @property
    def password(self) -> str:
        settings = get_settings()
        pwd = settings.get(ConfigKeys.password.value, None, fresh=True)
        if pwd:
            pwd = str(pwd)
            if pwd.strip() == "":
                pwd = None
        return pwd

    @property
    def access_token(self) -> str:
        settings = get_settings()
        access_token = settings.get(ConfigKeys.access_token.value, fresh=True)
        return access_token

    @property
    def refresh_token(self) -> str:
        settings = get_settings()
        refresh_token = settings.get(ConfigKeys.refresh_token.value, fresh=True)
        return refresh_token

    @property
    def expires_by(self) -> str:
        settings = get_settings()
        expires_by = settings.get(ConfigKeys.expires_by.value, fresh=True)
        return expires_by

    def get_val(self, key):
        settings = get_settings()
        val = settings.get(key, fresh=True)
        return val

    @property
    def login_endpoint(self):
        hostname = self.hostname
        login_url = URL(hostname) / EndPoints.login.value
        return login_url.human_repr()

    @property
    def refresh_endpoint(self):
        hostname = self.hostname
        refresh_url = URL(hostname) / EndPoints.refresh_token.value
        return refresh_url.human_repr()

    @property
    def upload_data_endpoint(self):
        hostname = self.hostname
        upload_url = URL(hostname) / EndPoints.upload_dataset.value
        return upload_url.human_repr()

    @property
    def upload_model_endpoint(self):
        hostname = self.hostname
        upload_url = URL(hostname) / EndPoints.upload_model.value
        return upload_url.human_repr()

    @property
    def new_session_endpoint(self):
        hostname = self.hostname
        session_url = URL(hostname) / EndPoints.new_session.value
        return session_url.human_repr()

    @property
    def explain_endpoint(self):
        hostname = self.hostname
        explain_url = URL(hostname) / EndPoints.explain.value
        return explain_url.human_repr()

    @property
    def list_resources_endpoint(self):
        hostname = self.hostname
        list_resources_url = URL(hostname) / EndPoints.resources_list.value
        return list_resources_url.human_repr()

    def get_resource_endpoint(self, resource):
        hostname = self.hostname
        resource_url = URL(hostname) / f"resources/{resource}"
        return resource_url.human_repr()

    @property
    def list_jobs_endpoint(self):
        hostname = self.hostname
        list_jobs_url = URL(hostname) / EndPoints.job_list.value
        return list_jobs_url.human_repr()

    def get_job_endpoint(self, job):
        hostname = self.hostname
        job_url = URL(hostname) / f"job/{job}"
        return job_url.human_repr()

    def get_job_output_endpoint(self, job):
        hostname = self.hostname
        job_output_url = URL(hostname) / f"job/{job}/output"
        return job_output_url.human_repr()

    @property
    def version_endpoint(self):
        hostname = self.hostname
        version_url = URL(hostname) / EndPoints.version.value
        return version_url.human_repr()

    @property
    def usage_endpoint(self):
        hostname = self.hostname
        usage_url = URL(hostname) / EndPoints.usage.value
        return usage_url.human_repr()

    @property
    def quota_endpoint(self):
        hostname = self.hostname
        quota_url = URL(hostname) / EndPoints.quota.value
        return quota_url.human_repr()


config = Config()
