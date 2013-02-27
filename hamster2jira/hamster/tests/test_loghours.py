from datetime import timedelta
from hamster.tests.factories import FactFactory
from django.test import TestCase
from mock import patch
from django.core.management import call_command


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


class TestLogHour(TestCase):

    def setUp(self):
        self.patcher = patch('jira.client.JIRA')
        self.JIRA = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def log(self):
        call_command('loghours')

    def test_log_with_settings_data(self):
        SERVER = 'https://machinalis.atlassian.net'
        USERNAME = 'YOUR_USER'
        PASSWORD = 'YOUR_PASSWORD'

        with self.settings(JIRA_BASE_URL=SERVER,
                           JIRA_USERNAME=USERNAME,
                           JIRA_PASSWORD=PASSWORD):

            self.log()

        expected = {'options': {'server': SERVER},
                    'basic_auth': (USERNAME, PASSWORD)}
        self.JIRA.assert_called_once_with(**expected)

    def test_all_fact_finished_and_not_excluded_are_logged(self):
        pass
