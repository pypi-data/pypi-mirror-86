"""Misc utilities for file/paths"""
import os
from pathlib import Path

import botocore.client
import requests
from google.cloud import storage
from smart_open import open
from smart_open import parse_uri

GCS_CREDENTIALS_PATH = "GCS_CREDENTIAL_PATH"


def sopen(path: str, *args, **kwargs):
    """Wrapper to smart open to handle certain edge cases."""
    scheme = parse_uri(path).scheme
    try:
        if scheme == "gs" and os.getenv(GCS_CREDENTIALS_PATH):
            print(f"Using {os.getenv(GCS_CREDENTIALS_PATH)}")
            storage_client = storage.Client.from_service_account_json(
                os.getenv(GCS_CREDENTIALS_PATH)
            )
            ret = open(path, "rb", transport_params=dict(client=storage_client))
            return ret
        else:
            ret = open(path, *args, **kwargs)
            return ret
    except Exception as e:
        # Anonymous access for GCS/S3
        if scheme == "gs":
            client = storage.Client.create_anonymous_client()
            transport_params = dict(client=client)
            kwargs.update({"transport_params": transport_params})
            ret = open(path, *args, **kwargs)
            return ret
        elif scheme == "s3":
            config = botocore.client.Config(signature_version=botocore.UNSIGNED)
            transport_params = {"resource_kwargs": {"config": config}}
            kwargs.update({"transport_params": transport_params})
            ret = open(path, *args, **kwargs)
            return ret
        else:
            raise e


def isabs(path: str):
    """Returns whether a given path is absolute or relative"""
    scheme = parse_uri(path).scheme
    if scheme in ("s3", "s3a", "s3n", "hdfs", "http", "https", "gs", "azure"):
        return True
    else:
        return os.path.isabs(path)


def get_extensions_from_file(path: str):
    as_path = Path(path)
    return as_path.suffixes


def exists(path: str):
    scheme = parse_uri(path).scheme
    if scheme in ("s3", "s3a", "s3n", "hdfs", "http", "https", "gs", "azure"):
        try:
            sopen(path)
            return True
        except Exception:
            return False
    else:
        return os.path.exists(path)


def download_file(url, file_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path
