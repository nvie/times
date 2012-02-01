Times
=====

Times is a minimalistic, super-small, Python library for dealing with date and
time conversions for once and for all.

It is simple, clear and designed to set a standard.

Armin Ronacher blogged about Python datetime best practices in his blog post
[Dealing with Timezones in Python][1].  The *tl;dr* summary is that everything
sucks about our mechanisms to represent absolute moments in time, but the least
worse of all (as in _an absolute moment in time_) in the universe is UTC.

[1]: http://lucumr.pocoo.org/2011/7/15/eppur-si-muove/


Recording times
---------------

When you want to record the current time, always use this:

    >>> import times
    >>> print times.now()
    datetime.datetime(2012, 2, 1, 10, 20, 1, 621491)

It's actually an alias for `datetime.utcnow`, but it prevents you from using
`datetime.now` accidentally.


Accepting times from end users
------------------------------

Say you get a date or time as input from the end user (i.e. you get a locally
formatted time).  Either the input is a tzinfo-less datetime object, like
`datetime.now` gives you, or it has some time zone info attached to it.  In
both cases, simply use the `normalize()` method:

    >>> import times, pytz
    >>> local_time = datetime.now()   # given a local_time without tzinfo
    >>> local_time
    datetime.datetime(2012, 2, 1, 11, 31, 45, 781262)
    >>> ams = pytz.timezone('Europe/Amsterdam')
    >>> times.normalize(local_time, ams)
    datetime.datetime(2012, 2, 1, 10, 31, 45, 781262)

If the given local date time contains time zone information, you can leave the
second argument to `normalize()` out:

    >>> import times
    >>> local_time                    # given a local_time with tzinfo
    datetime.datetime(2012, 2, 1, 11, 44, 29, 403115, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>)
    >>> times.normalize(local_time)
    datetime.datetime(2012, 2, 1, 10, 44, 29, 403115)

This obeys to the conventions suggested by Armin in his orginal article.


Presenting times
----------------
To _present_ times to the end user of your software, you should format your
absolute time to your user's local timezone.

    import times, pytz
    now = times.now()
    ams = pytz.timezone('Europa/Amsterdam')
    print times.format(now, ams)

