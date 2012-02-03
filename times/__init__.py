import datetime

import pytz

from .version import VERSION

__author__ = 'Vincent Driessen <vincent@3rdcloud.com>'
__version__ = VERSION


def now(*args, **kw):
    return datetime.datetime.utcnow(*args, **kw)


def to_universal(local_dt, timezone=None):
    """Converts the given local datetime to a universal datetime."""

    if timezone is not None:
        if local_dt.tzinfo is not None:
            raise ValueError(
                'Cannot use timezone-aware datetime with explicit timezone '
                'argument.'
            )

        if isinstance(timezone, basestring):
            timezone = pytz.timezone(timezone)
        dt_with_tzinfo = timezone.localize(local_dt)

    else:
        if local_dt.tzinfo is None:
            raise ValueError(
                'Explicit timezone required to convert naive datetimes.'
            )
        dt_with_tzinfo = local_dt
    univ_dt = dt_with_tzinfo.astimezone(pytz.utc)
    return univ_dt.replace(tzinfo=None)


def from_local(*args, **kw):
    """Converts the given local datetime to a universal datetime."""
    return from_local(*args, **kw)


def to_local(dt, timezone):
    """Converts universal datetime to a local representation in given timezone.
    """
    if dt.tzinfo is not None:
        raise ValueError(
            'First argument to to_local() should be a universal time.'
        )
    if isinstance(timezone, basestring):
        timezone = pytz.timezone(timezone)
    return pytz.utc.localize(dt).astimezone(timezone)


def from_universal(*args, **kw):
    return to_local(*args, **kw)


def format(dt, timezone, fmt=None):
    """Formats the given universal time for display in the given time zone."""

    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S%z'
    if timezone is None:
        raise ValueError('Please give an explicit timezone.')
    return to_local(dt, timezone).strftime(fmt)


now.__doc__ = datetime.datetime.utcnow.__doc__
from_universal.__doc__ = to_local.__doc__
