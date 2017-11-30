import pendulum
from datetime import datetime
from pendulum import Period, DateTime

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_with_datetimes(self):
        dt1 = datetime(2000, 1, 1)
        dt2 = datetime(2000, 1, 31)

        p = Period(dt1, dt2)
        self.assertIsInstanceOfDateTime(p.start)
        self.assertIsInstanceOfDateTime(p.end)
        self.assertDateTime(p.start, 2000, 1, 1)
        self.assertDateTime(p.end, 2000, 1, 31)

    def test_with_pendulum(self):
        dt1 = DateTime(2000, 1, 1)
        dt2 = DateTime(2000, 1, 31)

        p = Period(dt1, dt2)
        self.assertIsInstanceOfDateTime(p.start)
        self.assertIsInstanceOfDateTime(p.end)
        self.assertDateTime(p.start, 2000, 1, 1)
        self.assertDateTime(p.end, 2000, 1, 31)

    def test_inverted(self):
        dt1 = DateTime(2000, 1, 1)
        dt2 = DateTime(2000, 1, 31)

        p = Period(dt2, dt1)
        self.assertIsInstanceOfDateTime(p.start)
        self.assertIsInstanceOfDateTime(p.end)
        self.assertDateTime(p.start, 2000, 1, 31)
        self.assertDateTime(p.end, 2000, 1, 1)

    def test_inverted_and_absolute(self):
        dt1 = DateTime(2000, 1, 1)
        dt2 = DateTime(2000, 1, 31)

        p = Period(dt2, dt1, True)
        self.assertIsInstanceOfDateTime(p.start)
        self.assertIsInstanceOfDateTime(p.end)
        self.assertDateTime(p.start, 2000, 1, 1)
        self.assertDateTime(p.end, 2000, 1, 31)

    def test_accuracy(self):
        dt1 = DateTime(2000, 11, 20)
        dt2 = DateTime(2000, 11, 25)
        dt3 = DateTime(2016, 11, 5)

        p1 = Period(dt1, dt3)
        p2 = Period(dt2, dt3)

        self.assertEqual(15, p1.years)
        self.assertEqual(15, p1.in_years())
        self.assertEqual(11, p1.months)
        self.assertEqual(191, p1.in_months())
        self.assertEqual(5829, p1.days)
        self.assertEqual(2, p1.remaining_days)
        self.assertEqual(5829, p1.in_days())

        self.assertEqual(15, p2.years)
        self.assertEqual(15, p2.in_years())
        self.assertEqual(11, p2.months)
        self.assertEqual(191, p2.in_months())
        self.assertEqual(5824, p2.days)
        self.assertEqual(4, p2.remaining_days)
        self.assertEqual(5824, p2.in_days())

    def test_dst_transition(self):
        start = pendulum.create(2017, 3, 7, tz='America/Toronto')
        end = start.add(days=6)
        period = end - start

        assert period.days == 5
        assert period.seconds == 82800

        assert period.remaining_days == 6
        assert period.hours == 0
        assert period.remaining_seconds == 0

        assert period.in_days() == 6
        assert period.in_hours() == 5 * 24 + 23

    def test_timedelta_behavior(self):
        dt1 = DateTime(2000, 11, 20, 1)
        dt2 = DateTime(2000, 11, 25, 2)
        dt3 = DateTime(2016, 11, 5, 3)

        p1 = Period(dt1, dt3)
        p2 = Period(dt2, dt3)
        it1 = p1.as_timedelta()
        it2 = p2.as_timedelta()

        self.assertEqual(p1.total_seconds(), it1.total_seconds())
        self.assertEqual(p2.total_seconds(), it2.total_seconds())
        self.assertEqual(p1.days, it1.days)
        self.assertEqual(p2.days, it2.days)
        self.assertEqual(p1.seconds, it1.seconds)
        self.assertEqual(p2.seconds, it2.seconds)
        self.assertEqual(p1.microseconds, it1.microseconds)
        self.assertEqual(p2.microseconds, it2.microseconds)

    def test_different_timezones_same_time(self):
        dt1 = pendulum.create(2013, 3, 31, 1, 30, tz='Europe/Paris')
        dt2 = pendulum.create(2013, 4, 1, 1, 30, tz='Europe/Paris')
        period = dt2 - dt1

        assert period.in_words() == '1 day'
        assert period.in_hours() == 23

        dt1 = pendulum.create(2013, 3, 31, 1, 30, tz='Europe/Paris')
        dt2 = pendulum.create(2013, 4, 1, 1, 30, tz='America/Toronto')
        period = dt2 - dt1

        assert period.in_words() == '1 day 5 hours'
        assert period.in_hours() == 29
