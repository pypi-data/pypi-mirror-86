"""Upload resources to Xaipient API server"""
import os
import tarfile
import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional

import httpx
import typer

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import ExplanationCategory
from xac.api import ModelType
from xac.api import TF_SAVEDMODEL_FILENAME
from xac.api import TF_SAVEDMODEL_FILENAME_TXT
from xac.api.auth.auth import _get_header
from xac.api.config import config
from xac.utils.file_utils import exists
from xac.utils.file_utils import get_extensions_from_file
from xac.utils.file_utils import isabs
from xac.utils.file_utils import sopen
from xac.utils.helpers import progress_spinner
from xac.utils.helpers import secho
from xac.utils.helpers import shorten_text
from xac.utils.logger import get_logger

logger = get_logger("UPLOAD", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


class UploadRequestBody(str, Enum):
    dataset_type = "dataset_type"
    dataset_ext = "dataset_ext"
    dataset = "dataset"
    model = "model"
    model_type = "model_type"
    model_ext = "model_ext"
    column_transformer = "column_transformer"
    is_rnn = "is_rnn"
    tags = "tags"
    description = "description"
    explanation_category = "explanation_category"


class UploadResponseBody(str, Enum):
    dataset_id = "id"
    model_id = "id"


def _check_allowed_datafile(filepath: str):
    extn = get_extensions_from_file(filepath)
    if extn == [".csv"] or extn == [".csv", ".gz"] or extn == [".csv", ".zip"]:
        return True
    if extn == [".txt"] or extn == [".txt", ".gz"] or extn == [".txt", ".zip"]:
        return True
    return False


def upload_data(csv_filepath: str, quiet: bool = False) -> Optional[str]:
    if not isabs(csv_filepath):
        csv_filepath = os.path.abspath(csv_filepath)
    if not exists(csv_filepath):
        secho(f"❌ Not found: {csv_filepath}", err=True)
        return None
    if _check_allowed_datafile(csv_filepath):
        try:
            headers = _get_header()
            if headers is None:
                logger.debug("Auth header is None")
                return None
            req_body = {
                UploadRequestBody.dataset_type.value: "csv",
                UploadRequestBody.dataset_ext.value: get_extensions_from_file(
                    csv_filepath
                )[-1],
            }
            logger.debug(f"CSV File to be uploaded: {csv_filepath}")
            files = {
                UploadRequestBody.dataset.value: sopen(
                    csv_filepath, "rb", ignore_ext=True
                ).read()
            }
            logger.debug(f"Post request to {config.upload_data_endpoint}")
            logger.debug(f"Request Body: {req_body}")
            with progress_spinner("Uploading data", quiet=quiet):
                resp = httpx.post(
                    config.upload_data_endpoint,
                    data=req_body,
                    files=files,
                    headers=headers,
                    timeout=60,
                )
            logger.debug(f"Received Response: {resp.json()}")
            if resp.status_code == httpx.codes.CREATED:
                response = resp.json()
                dataset_id = response[UploadResponseBody.dataset_id.value]
                if not quiet:
                    typer.secho(
                        f"⬆  ✅ 🅳 Uploaded `{shorten_text(csv_filepath, width=40)}`, "
                        f"Dataset ID: {dataset_id}"
                    )
                return dataset_id
            else:
                secho(
                    f"❌ Error uploading data. Details: {resp.json()}",
                    fg=typer.colors.RED,
                    err=True,
                )
                return None
        except Exception as e:
            logger.debug(str(e))
            secho(f"❌ Unable to open/process file: {csv_filepath}", err=True)
            return None
    else:
        secho(
            "❌ FileAllowed extensions: *.[csv|txt], [*.csv.gz|*.txt.gz], [*.csv.zip",
            err=True,
        )
        return None


def upload_model(
    model_path: str,
    model_type: ModelType,
    column_transformer_path: Optional[str] = None,
    is_time_series: bool = False,
    tags=None,
    description=None,
    explanation_category=ExplanationCategory.TABULAR,
    quiet: bool = False,
) -> Optional[str]:
    if not isabs(model_path):
        model_path = os.path.abspath(model_path)
    if column_transformer_path:
        if not isabs(column_transformer_path):
            column_transformer_path = os.path.abspath(column_transformer_path)
        if not exists(column_transformer_path):
            secho(
                f"❌ ColumnTransformer file not found: {column_transformer_path}",
                err=True,
            )
            return None
    if not exists(model_path):
        secho(f"❌ Model path not found: {model_path}", err=True)
        return None
    if os.path.isdir(model_path):
        valid_model = (Path(model_path) / TF_SAVEDMODEL_FILENAME).exists() or (
            Path(model_path) / TF_SAVEDMODEL_FILENAME_TXT
        ).exists()
        if not valid_model:
            secho(
                f"❌ Path: {shorten_text(model_path, width=25)}"
                f"is a directory and does not have 'saved_model.[pb|pbtxt]'",
                err=True,
            )
            return None
        tempdir = tempfile.gettempdir()
        model_file = Path(tempdir) / Path(model_path).name
        model_file = f"{str(model_file)}.tgz"  # type: ignore
        with tarfile.open(model_file, "w:gz") as tar:
            tar.add(model_path, arcname=os.path.basename(model_path))
        model_path = model_file  # type: ignore
    try:
        headers = _get_header()
        if headers is None:
            logger.debug("Auth header is None")
            return None
        req_body = {
            UploadRequestBody.model_type.value: model_type.value,
            UploadRequestBody.model_ext.value: get_extensions_from_file(model_path)[-1],
            UploadRequestBody.tags.value: [] if tags is None else tags,
            UploadRequestBody.description.value: ""
            if description is None
            else description,
            UploadRequestBody.is_rnn.value: "true" if is_time_series else "false",
            UploadRequestBody.explanation_category.value: explanation_category.value,
        }

        files = {UploadRequestBody.model.value: sopen(model_path, "rb").read()}
        if column_transformer_path:
            files[UploadRequestBody.column_transformer.value] = sopen(
                column_transformer_path, "rb"
            ).read()
        logger.debug(f"Post request to {config.upload_model_endpoint}")
        logger.debug(f"Request Body: {req_body}")
        with progress_spinner(
            "Uploading models [and column transformers]", quiet=quiet
        ):
            resp = httpx.post(
                config.upload_model_endpoint,
                data=req_body,
                files=files,
                headers=headers,
                timeout=60,
            )
        logger.debug(f"Received Response: {resp.json()}")
        if resp.status_code == httpx.codes.CREATED:
            response = resp.json()
            model_id = response[UploadResponseBody.model_id.value]
            if column_transformer_path:
                if not quiet:
                    typer.secho(
                        f"⬆  ✅ 🆃 Uploaded ColumnTransformer"
                        f" `{shorten_text(column_transformer_path, width=40)}`"
                    )
            if not quiet:
                typer.secho(
                    f"⬆  ✅ 🅼 Uploaded Model `{shorten_text(model_path, width=40)}`, "
                    f"Model ID: {model_id}"
                )

            return model_id
        else:
            secho(
                f"❌ Error uploading model/transformer. Details: {resp.json()}",
                fg=typer.colors.RED,
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho(f"❌ Unable to open/process file: {model_path}", err=True)
        return None
