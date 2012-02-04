import datetime
import calendar
import pytz
from .version import VERSION

__author__ = 'Vincent Driessen <vincent@3rdcloud.com>'
__version__ = VERSION


def to_universal(local_dt, timezone=None):
    """Converts the given local datetime or UNIX timestamp to a universal
    datetime.
    """
    if isinstance(local_dt, (int, float)):
        if timezone is not None:
            raise ValueError(
                'Timezone argument illegal when using UNIX timestamps.'
            )
        return from_unix(local_dt)
    else:
        return from_local(local_dt, timezone)


def from_local(local_dt, timezone=None):
    """Converts the given local datetime to a universal datetime."""
    if not isinstance(local_dt, datetime.datetime):
        raise ValueError('First argument should be int, float or datetime.')

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


def from_unix(ut):
    """Converts a UNIX timestamp, as returned by `time.time()`, to universal
    time.  Assumes the input is in UTC, as `time.time()` does.
    """
    if not isinstance(ut, (int, float)):
        raise ValueError(
            'First argument to from_unix should be an int or float'
        )

    return datetime.datetime.utcfromtimestamp(float(ut))


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


def to_unix(dt):
    """Converts a datetime object to unixtime"""
    if not isinstance(dt, datetime.datetime):
        raise ValueError(
            'First argument to to_unix should be a datetime object'
        )

    return calendar.timegm(dt.utctimetuple())


def format(dt, timezone, fmt=None):
    """Formats the given universal time for display in the given time zone."""

    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S%z'
    if timezone is None:
        raise ValueError('Please give an explicit timezone.')
    return to_local(dt, timezone).strftime(fmt)


now = datetime.datetime.utcnow
