from datetime import timedelta
from hamster.tests.factories import FactFactory
from django.test import TestCase


class TestFact(TestCase):

    def test_duration_finished(self):
        f = FactFactory()
        delta = timedelta(hours=1)
        f.end_time = f.start_time + delta
        self.assertEqual(f.duration, delta)

    def test_duration_raises_exception_when_not_finished(self):
        f = FactFactory()
        assert f.end_time is None
        with self.assertRaises(ValueError):
            f.duration
