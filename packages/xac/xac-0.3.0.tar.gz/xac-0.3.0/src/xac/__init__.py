import xac.api as api
import xac.api.auth.auth as _auth
import xac.api.info as _display_info
import xac.api.resources.job as job
import xac.api.resources.session as session
from xac.api import config_file as config  # noqa
from xac.api import ExplanationCategory  # noqa
from xac.api import ExplanationType  # noqa
from xac.api.resources.usage import get_quota
from xac.qexplain import explainer

# from xac.api.resources.usage import get_usage


__version__ = api.__version__
API_VERSION = api.SUPPORTED_API_VERSION
login = _auth.login_with_email
logout = _auth.purge_tokens
info = _display_info.display_info
# usage = get_usage
quota = get_quota
Explainer = explainer.Explainer
ExplainPromise = explainer.ExplainPromise
transforms = explainer.Transforms


sessions = session.get_sessions
jobs = job.get_jobs
