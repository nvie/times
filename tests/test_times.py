from unittest import TestCase
import times
import pytz
from datetime import datetime


class TestTimes(TestCase):
    def setUp(self):
        est = pytz.timezone('EST')
        ams = pytz.timezone('Europe/Amsterdam')

        self.time_in_ny = est.localize(datetime(2012, 2, 1, 6, 56, 31))
        self.time_in_ams = ams.localize(datetime(2012, 2, 1, 12, 56, 31))
        self.sometime_univ = datetime(2012, 2, 1, 11, 56, 31)


    # now()
    def test_now(self):  # noqa
        """times.now() has no attached timezone info"""
        now = times.now()
        self.assertIsNone(now.tzinfo)


    # to_universal()
    def test_to_universal_with_tzinfo(self):  # noqa
        """Convert local dates with timezone info to universal date"""
        ny_time = self.time_in_ny
        ams_time = self.time_in_ams

        self.assertEquals(
                times.to_universal(ny_time),
                self.sometime_univ)
        self.assertEquals(
                times.to_universal(ams_time),
                self.sometime_univ)

        self.assertEquals(ny_time.hour, 6)
        self.assertEquals(
                times.to_universal(ny_time).hour, 11)

        self.assertEquals(ams_time.hour, 12)
        self.assertEquals(
                times.to_universal(ams_time).hour, 11)

        # Test alias from_local, too
        self.assertEquals(
                times.from_local(ny_time),
                self.sometime_univ)

    def test_to_universal_without_tzinfo(self):
        """Convert local dates without timezone info to universal date"""

        # Same as above, but with tzinfo stripped off (as if a NY and Amsterdam
        # user used datetime.now())
        ny_time = self.time_in_ny.replace(tzinfo=None)
        ams_time = self.time_in_ams.replace(tzinfo=None)

        # When time has no tzinfo attached, it should be specified explicitly
        est = pytz.timezone('EST')
        self.assertEquals(
                times.to_universal(ny_time, est),
                self.sometime_univ)

        # ...or simply with a string
        self.assertEquals(
                times.to_universal(ams_time, 'Europe/Amsterdam'),
                self.sometime_univ)

    def test_to_universal_with_unix_timestamp(self):
        """Convert UNIX timestamps to universal date"""
        unix_time = 1328257004.456  # as returned by time.time()
        self.assertEquals(
            times.to_universal(unix_time),
            datetime(2012, 2, 3, 8, 16, 44, 456000)
        )

    def test_to_universal_with_string(self):
        dt = self.sometime_univ

        # Timezone-aware strings
        self.assertEquals(dt, times.to_universal('2012-02-02 00:56:31+13:00'))
        self.assertEquals(dt, times.to_universal('2012-02-01 12:56:31+01:00'))
        self.assertEquals(dt, times.to_universal('2012-02-01 06:56:31-05:00'))

        # Timezone-less strings require explicit source timezone
        self.assertEquals(dt, times.to_universal('2012-02-02 00:56:31',
            'Pacific/Auckland'))
        self.assertEquals(dt, times.to_universal('2012-02-01 12:56:31', 'CET'))
        self.assertEquals(dt, times.to_universal('2012-02-01 06:56:31', 'EST'))

        # Timezone-less strings are rejected if source timezone is not
        # specified
        with self.assertRaises(ValueError):
            self.assertEquals(dt, times.to_universal('2012-02-01 12:56:31'))


    def test_to_universal_rejects_no_tzinfo(self):  # noqa
        """Converting to universal times requires source timezone"""
        now = datetime.now()
        with self.assertRaises(ValueError):
            times.to_universal(now)

    def test_to_universal_rejects_non_date_arguments(self):
        """to_universal rejects non-date arguments"""
        with self.assertRaises(TypeError):
            times.to_universal([1, 2, 3])


    # from_unix()
    def test_convert_unix_time_to_datetime(self):  # noqa
        """Can convert from UNIX time to universal time."""
        unix_time = 1328257004.456  # as returned by time.time()
        self.assertEquals(
            times.from_unix(unix_time),
            datetime(2012, 2, 3, 8, 16, 44, 456000)
        )

        self.assertEquals(
            times.format(times.from_unix(unix_time), 'UTC'),
            '2012-02-03T08:16:44.456000+00:00')
        self.assertEquals(
            times.format(times.from_unix(unix_time), 'Europe/Amsterdam'),
            '2012-02-03T09:16:44.456000+01:00')
        self.assertEquals(
            times.format(times.from_unix(unix_time), 'Pacific/Auckland'),
            '2012-02-03T21:16:44.456000+13:00')

    def test_convert_non_numeric_from_unix(self):
        """from_unix refuses to accept non-numeric input"""
        with self.assertRaises(TypeError):
            times.from_unix('lol')


    # to_unix()
    def test_convert_datetime_to_unix_time(self):  # noqa
        """Can convert UNIX time to universal time."""
        self.assertEquals(
            times.to_unix(datetime(2012, 2, 3, 8, 16, 44)),
            1328257004.0
        )

    def test_convert_non_numeric_to_unix(self):
        """to_unix refuses to accept non-numeric input"""
        with self.assertRaises(TypeError):
            times.to_unix('lol')


    # to_local()
    def test_convert_universal_to_local(self):  # noqa
        """Convert universal time to local time"""
        univ = self.sometime_univ
        self.assertEquals(
                times.to_local(univ, pytz.timezone('Europe/Amsterdam')),
                self.time_in_ams)
        self.assertEquals(
                times.to_local(univ, pytz.timezone('EST')),
                self.time_in_ny)

    def test_convert_refuses_local_to_local(self):
        """Refuses to convert between timezones directly"""
        loc = self.time_in_ams
        with self.assertRaises(ValueError):
            times.to_local(loc, pytz.timezone('Europe/Amsterdam'))


    # format()
    def test_format_without_tzinfo(self):  # noqa
        """Format times without timezone info"""
        dt = self.sometime_univ
        auckland = pytz.timezone('Pacific/Auckland')
        est = pytz.timezone('EST')
        ams = pytz.timezone('Europe/Amsterdam')
        self.assertEquals(times.format(dt, auckland),
                '2012-02-02T00:56:31+13:00')
        self.assertEquals(times.format(dt, ams), '2012-02-01T12:56:31+01:00')
        self.assertEquals(times.format(dt, est), '2012-02-01T06:56:31-05:00')

    def test_custom_format(self):
        dt = self.sometime_univ
        auckland = pytz.timezone('Pacific/Auckland')
        est = pytz.timezone('EST')
        self.assertEquals(times.format(dt, auckland, '%H'), '00')
        self.assertEquals(times.format(dt, est, '%H'), '06')

    def test_format_refuses_local_times(self):
        """Format refuses local time input"""
        auckland = pytz.timezone('Pacific/Auckland')
        with self.assertRaises(ValueError):
            times.format(self.time_in_ams, auckland)


    # from/to unix and back
    def test_convert_between_unix_times(self):  # noqa
        """Can convert UNIX time to universal time and back."""
        given_unix = 1328257004.456  # as returned by time.time()
        self.assertEquals(
            times.to_unix(times.from_unix(given_unix)),
            int(given_unix)
        )

        given_dt = self.sometime_univ
        self.assertEquals(
            times.from_unix(times.to_unix(given_dt)),
            given_dt
        )
