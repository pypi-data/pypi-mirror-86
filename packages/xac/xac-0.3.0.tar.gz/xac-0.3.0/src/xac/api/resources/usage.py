"""Compute resource usage for logged in account"""
# import json
# from datetime import datetime
# from enum import Enum
import httpx
import typer

from xac.api import _LOG_TO_FILE_ONLY
from xac.api import _LOGLEVEL
from xac.api import HTTP_TIMEOUT
from xac.api.auth.auth import _get_header
from xac.api.config import config
from xac.utils.helpers import secho
from xac.utils.logger import get_logger

# from tabulate import tabulate

logger = get_logger("USAGE", log_level=_LOGLEVEL, file_only=_LOG_TO_FILE_ONLY)


# class UsageResponseSummary(str, Enum):
#     time_used = "time_used"
#     num_cores = "num_cores"
#     job_id = "job_id"
#     detail = "detail"
#     time = "ts"
#
#
# class UsageInfoSummary(str, Enum):
#     time_used = "cpu_time"
#     num_cores = "cpu_cores"
#     job_id = "job_id"
#     exp_types = "expln_types"
#     date_time = "date"
#
#
# def _abbr_exp_type(value):
#     if value == "local_attributions":
#         return "LA"
#     elif value == "local_rules":
#         return "LR"
#     elif value == "counterfactuals":
#         return "CF"
#     elif value == "global_importances":
#         return "GI"
#     elif value == "global_alignments":
#         return "GA"
#     elif value == "global_rules":
#         return "GR"
#     elif value == "model_metrics":
#         return "MM"
#     elif value == "predictions":
#         return "PD"
#
#
# def _convert_time(time_str):
#     try:
#         dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")
#         return dt.strftime("%d %b %Y, %H:%M")
#     except Exception:
#         return ""
#
#
# def _print_legend():
#     secho("Legend for Explanation Types:", fg=typer.colors.BRIGHT_BLUE)
#     secho(
#         "GI - Global Importances, GR - Global Attributios, GR - Global Rules",
#         fg=typer.colors.GREEN,
#     )
#     secho(
#         "LA - Local Attributions, LR - Local Rules, CF - Counterfactuals",
#         fg=typer.colors.GREEN,
#     )
#     secho("PD - Model Predictions, MM -  Model Metrics", fg=typer.colors.GREEN)
#
#
# def _build_usage_summary(usage_dict):
#     result = {
#         UsageInfoSummary.date_time.value: [],
#         UsageInfoSummary.job_id.value: [],
#         UsageInfoSummary.time_used.value: [],
#         UsageInfoSummary.num_cores.value: [],
#         UsageInfoSummary.exp_types.value: [],
#     }
#     for job in usage_dict:
#         date_time = job.get(UsageResponseSummary.time.value)
#         date_time = _convert_time(date_time)
#         job_id = job.get(UsageResponseSummary.job_id.value)
#         time_used = job.get(UsageResponseSummary.time_used.value)
#         exp_types_json = job.get(UsageResponseSummary.detail)
#         if exp_types_json:
#             exp_types_dict = json.loads(exp_types_json)
#             exp_types = exp_types_dict.keys()
#         else:
#             exp_types = None
#         if exp_types:
#             exp_types = [_abbr_exp_type(exp) for exp in exp_types]
#             exp_types = ",".join(exp_types)
#         else:
#             exp_types = ""
#         num_cores = job.get(UsageResponseSummary.num_cores.value)
#         result[UsageInfoSummary.date_time.value].append(date_time)
#         result[UsageInfoSummary.job_id.value].append(job_id)
#         result[UsageInfoSummary.time_used.value].append(time_used)
#         result[UsageInfoSummary.exp_types.value].append(exp_types)
#         result[UsageInfoSummary.num_cores.value].append(num_cores)
#     return result
#
#
# def get_usage(raw=False):
#     """Get detailed resource usage for current user account"""
#     secho("🧨 [ALPHA Feature]. Stats may not reflect correct usage", fg=typer.colors.RED)
#     headers = _get_header()
#     if headers is None:
#         logger.debug("Auth header is None")
#         return None
#     logger.debug(f"Get Request to {config.usage_endpoint}")
#     try:
#         resp = httpx.get(config.usage_endpoint, headers=headers, timeout=HTTP_TIMEOUT)
#         logger.debug(f"Received Response {resp.json()}")
#         if resp.status_code == httpx.codes.OK:
#             usage_resp = resp.json()
#             result = _build_usage_summary(usage_resp)
#             if raw:
#                 return usage_resp
#             else:
#                 print(tabulate(result, headers="keys"))
#                 print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#                 _print_legend()
#         else:
#             secho(
#                 f"❌ Unable to fetch usage details from sever. Details: {resp.json()}",
#                 err=True,
#             )
#             return None
#     except Exception as e:
#         logger.debug(str(e))
#         secho("❌  Server not responding. Please contact Xaipient team", err=True)
#         return None


def get_quota(raw=False):
    """Check usage against quotas for current user account
    Args:
        raw: if True, return raw server response
    """
    secho("🧨 [ALPHA Feature]. Stats may not reflect correct usage", fg=typer.colors.RED)
    headers = _get_header()
    if headers is None:
        logger.debug("Auth header is None")
        return None
    logger.debug(f"Get Request to {config.quota_endpoint}")
    try:
        resp = httpx.get(config.quota_endpoint, headers=headers, timeout=HTTP_TIMEOUT)
        logger.debug(f"Received Response {resp.json()}")
        if resp.status_code == httpx.codes.OK:
            quota_resp = resp.json()
            if raw:
                return quota_resp
            jobs_in_queue = quota_resp.get("jobs_in_queue", 0)
            quota_jobs_in_queue = quota_resp.get("quota_jobs_in_queue", 0)
            cpu_used = quota_resp.get("cpu_time_in_minutes_current_month", 0)
            quota_cpu = quota_resp.get("quota_cpu_time_in_minutes_per_month", 0)
            secho(
                f"Concurrent Job Usage    : {jobs_in_queue}/"
                f"{quota_jobs_in_queue} jobs",
            )
            secho(
                f"Monthly CPU Usage (mins):{cpu_used: 0.2f}/{quota_cpu: 0.2f} mins"
                f" ({cpu_used/quota_cpu*100:.1f}% used)",
            )
        else:
            secho(
                f"❌ Unable to fetch usage details from sever. Details: {resp.json()}",
                err=True,
            )
            return None
    except Exception as e:
        logger.debug(str(e))
        secho("❌  Server not responding. Please contact Xaipient team", err=True)
        return None
