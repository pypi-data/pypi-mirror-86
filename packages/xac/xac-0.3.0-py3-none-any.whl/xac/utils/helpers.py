"""Better formatting and printing using lexers/colors."""
import contextlib
import datetime as dt
from contextlib import contextmanager
from functools import cmp_to_key
from operator import itemgetter as i
from pprint import pformat

import humanize
import typer
from alive_progress import alive_bar
from halo import HaloNotebook as Halo
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import Python3Lexer


def type_of_script():
    try:
        ipy_str = str(type(get_ipython()))
        if "zmqshell" in ipy_str or "google.colab" in ipy_str:
            return "jupyter"
        if "terminal" in ipy_str:
            return "ipython"
    except:
        return "terminal"


is_notebook = True if type_of_script() == "jupyter" else False


def get_expiry_human(expires_by):
    """Get human friendly expiration text for timestamps.

    Args:
        expires_by: string containing timestamp

    Returns:
        Humann friendly expires by text

    """
    expiry_time = dt.datetime.fromtimestamp(float(expires_by))
    expire_delta = humanize.naturaldelta(expiry_time - dt.datetime.now())
    return expire_delta


def human_time_abbr(human_time: str):
    time_abbr = {
        "hour": "hr",
        "minute": "min",
        "second": "sec",
        "week": "wk",
        "day": "day",
        "month": "mth",
        "year": "yr",
    }
    result = human_time
    for k, v in time_abbr.items():
        result = result.replace(k, v)
    return result


def get_human_time(timestamp, abbr=True):
    """Get human friendly time timestamps.

    Args:
        timestamp: string containing timestamp
        abbr: abbreviate strings (minute to mins)

    Returns:
        Human friendly text

    """
    time = dt.datetime.fromtimestamp(float(timestamp))
    time_delta = humanize.naturaldelta(dt.datetime.now() - time)
    if abbr:
        return human_time_abbr(f" {time_delta} ago")
    else:
        return f" {time_delta} ago"


def get_human_diff(timestamp1, timestamp2, abbr=True):
    """Get human friendly difference between 2 timestamps.

    Args:
        timestamp1: string containing timestamp
        timestamp1: string containing timestamp


    Returns:
        Humann friendly text

    """
    time1 = dt.datetime.fromtimestamp(float(timestamp1))
    time2 = dt.datetime.fromtimestamp(float(timestamp2))
    time_delta = humanize.naturaldelta(time2 - time1)
    if abbr:
        return human_time_abbr(time_delta)
    else:
        return time_delta


def secho(str_, *args, **kwargs):
    if is_notebook:
        print(str_)
    else:
        typer.secho(str_, *args, **kwargs)


def xpprint_dict(d):
    """Print beautifully formatted dictionaries to the terminal.

    Args:
        d: dictionary to format.
    """
    out_str = pformat(d, indent=2)
    if len(out_str) > 500:
        out_str = out_str[:500]

    out_str = highlight(pformat(out_str, indent=2), Python3Lexer(), TerminalFormatter())
    print(out_str)


def progress_spinner(title_text, quiet=False):
    @contextmanager
    def nullcontext(enter_result=None):
        yield enter_result

    if quiet:
        return nullcontext()
    if is_notebook:
        return Halo(text=title_text, spinner="dots")
    else:
        return alive_bar(
            title=title_text,
            unknown="balls_scrolling",
        )


def tabular_context_placeholder():
    text = """
# Enter the context dictionary specific to your data
{
  'data_target': 'RiskPerformance', # change this with relevant target feature!!
  'class_labels' : {
    # description of encoded class labels e.g 0: 'Reject', 1: 'Accept'
    0: 'Reject',
    1: 'Accept'
  }
}
"""
    return text


def validate_data_range(df, start, end):
    """Validate and return valid start and end rows supplied by user.

    Args:
        df: pandas dataframe
        start: index to start row
        end: index to end row [-1 indicates last row]

    Returns:
        tuple of valid start and end rows.

    """
    total_items = len(df)
    end = total_items if end == -1 else end
    try:
        start = int(start)
        if start > total_items or start < 0:
            raise ValueError
    except ValueError:
        secho("start must be a valid integer index (0 < start < nrows)." "Setting to 0")
        start = 0
    try:
        end = int(end)
        if end > total_items or end < start:
            raise ValueError
    except ValueError:
        secho(
            "end must be a valid integer index (start < end < nrows)." "Setting to 10"
        )
        end = 10
    return start, end


def shorten_text(text, width=25, placeholder="..."):
    length = len(text)
    if length <= width:
        return text
    else:
        placeholder_len = len(placeholder)
        available_width = width - placeholder_len
        left = available_width // 2
        right = available_width - left
        return f"{text[:left]}{placeholder}{text[-right:]}"


def cmp(x, y):
    if x is None and y is None:
        return 0
    elif x is None:
        return -1
    elif y is None:
        return 1
    else:
        return (x > y) - (x < y)


def multikeysort(items, columns):
    """Sort by multiple keys
    stackoverflow.com/questions/1143671/how-to-sort-objects-by-multiple-keys-in-python

    Args:
        items: collection of items
        columns: list/tuple of keys to sort by

    Returns:
        sorted collection

    """
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith("-") else (i(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (cmp(fn(left), fn(right)) * mult for fn, mult in comparers)
        return next((result for result in comparer_iter if result), 0)

    return sorted(items, key=cmp_to_key(comparer))


def validate_sort_keys(sort_keys, _sort_keys_dict, default=("-created",)):
    """ Checks whether the sort keys are allowed before doing a multikey sort"""
    _sort_keys_ = []
    for key_ in sort_keys:
        if key_ in _sort_keys_dict:
            _sort_keys_.append(_sort_keys_dict[key_])
        else:
            secho(
                f"❌ Sort keys must be a list of these "
                f"values: {_sort_keys_dict.keys()}"
            )
            _sort_keys_ = default
            break
    return _sort_keys_
