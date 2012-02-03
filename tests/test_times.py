from unittest import TestCase
import times, pytz
from datetime import datetime


class TestTimes(TestCase):
    def setUp(self):
        est = pytz.timezone('EST')
        ams = pytz.timezone('Europe/Amsterdam')

        self.sometime_in_newyork = est.localize(datetime(2012, 2, 1, 6, 56, 31))
        self.sometime_in_amsterdam = ams.localize(datetime(2012, 2, 1, 12, 56, 31))
        self.sometime_univ = datetime(2012, 2, 1, 11, 56, 31)


    def test_now_has_no_tzinfo(self):
        """times.now() has no attached timezone info"""
        now = times.now()
        self.assertIsNone(now.tzinfo)


    def test_local_time_with_tzinfo_to_universal(self):
        """Convert local dates with timezone info to universal date"""
        ny_time = self.sometime_in_newyork
        ams_time = self.sometime_in_amsterdam

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


    def test_local_time_without_tzinfo_to_universal(self):
        """Convert local dates without timezone info to universal date"""

        # Same as above, but with tzinfo stripped off (as if a NY and Amsterdam
        # user used datetime.now())
        ny_time = self.sometime_in_newyork.replace(tzinfo=None)
        ams_time = self.sometime_in_amsterdam.replace(tzinfo=None)

        # When time has no tzinfo attached, it should be specified explicitly
        est = pytz.timezone('EST')
        self.assertEquals(
                times.to_universal(ny_time, est),
                self.sometime_univ)

        # ...or simply with a string
        self.assertEquals(
                times.to_universal(ams_time, 'Europe/Amsterdam'),
                self.sometime_univ)


    def test_to_universal_rejects_no_tzinfo(self):
        """Converting to universal times requires source timezone"""
        now = datetime.now()
        with self.assertRaises(ValueError):
            times.to_universal(now)


    def test_format_without_tzinfo(self):
        """Format times without timezone info"""
        dt = self.sometime_univ
        auckland = pytz.timezone('Pacific/Auckland')
        est = pytz.timezone('EST')
        ams = pytz.timezone('Europe/Amsterdam')
        self.assertEquals(times.format(dt, auckland), '2012-02-02 00:56:31+1300')
        self.assertEquals(times.format(dt, ams), '2012-02-01 12:56:31+0100')
        self.assertEquals(times.format(dt, est), '2012-02-01 06:56:31-0500')

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
            times.format(self.sometime_in_amsterdam, auckland)


    def test_convert_universal_to_local(self):
        """Convert universal time to local time"""
        univ = self.sometime_univ
        self.assertEquals(
                times.to_local(univ, pytz.timezone('Europe/Amsterdam')),
                self.sometime_in_amsterdam)
        self.assertEquals(
                times.to_local(univ, pytz.timezone('EST')),
                self.sometime_in_newyork)


    def test_convert_refuses_local_to_local(self):
        """Refuses to convert between timezones directly"""
        loc = self.sometime_in_amsterdam
        with self.assertRaises(ValueError):
            times.to_local(loc, pytz.timezone('Europe/Amsterdam'))


    def test_convert_unix_time_to_datetime(self):
      """Can convert unix_time_to_datetime"""
      self.assertEquals(
        times.from_unix(1233456789.0),
        datetime(2009, 1, 31, 18, 53, 9)
      )


    def test_convert_non_numeric(self):
        """from_unix refuses to accept non-numeric input"""
        with self.assertRaises(ValueError):
            times.from_unix('lol')


    def test_convert_non_numeric(self):
        """to_unix refuses to accept non-numeric input"""
        with self.assertRaises(ValueError):
            times.to_unix('lol')


    def test_convert_datetime_to_unix_time(self):
       self.assertEquals(
        times.to_unix(datetime(2009, 1, 31, 18, 53, 9)),
        1233456789.0
      )

