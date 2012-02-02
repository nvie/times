import datetime
import pytz
from .version import VERSION

__author__ = 'Vincent Driessen <vincent@3rdcloud.com>'
__version__ = VERSION

now = datetime.datetime.utcnow
"""Returns a safe-to-store datetime without tzinfo representing the current moment."""


def to_universal(local_dt, timezone=None):
    """Converts the given local datetime to a universal datetime."""
    if timezone is not None:
        if local_dt.tzinfo is not None:
            raise ValueError('Cannot use timezone-aware datetime with explicit timezone argument.')
        if isinstance(timezone, basestring):
            timezone = pytz.timezone(timezone)
        dt_with_tzinfo = timezone.localize(local_dt)
    else:
        if local_dt.tzinfo is None:
            raise ValueError('Explicit timezone required to convert naive datetimes.')
        dt_with_tzinfo = local_dt
    univ_dt = dt_with_tzinfo.astimezone(pytz.utc)
    return univ_dt.replace(tzinfo=None)

from_local = to_universal
"""Converts the given local datetime to a universal datetime."""


def to_local(dt, timezone):
    """Converts the given universal datetime to a local representation in the
    given timezone.
    """
    if dt.tzinfo is not None:
        raise ValueError('First argument to to_local() should be a universal time.')
    if isinstance(timezone, basestring):
        timezone = pytz.timezone(timezone)
    return pytz.utc.localize(dt).astimezone(timezone)

from_universal = to_local
"""Converts the given universal datetime to a local representation in the given
timezone.
"""


def format(dt, timezone, fmt=None):
    """Formats the given universal time for display in the given time zone."""
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S%z'
    if timezone is None:
        raise ValueError('Please give an explicit timezone.')
    return to_local(dt, timezone).strftime(fmt)


