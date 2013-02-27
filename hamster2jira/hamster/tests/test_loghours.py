from datetime import timedelta
from hamster.tests.factories import FactFactory
from django.test import TestCase
from mock import Mock, patch
from django.core.management import call_command


def JiraClientMock():
    attrs = {'projects.return_value': [Mock(key='CPI'),
                                       Mock(key='CPINB')]}
    return Mock(**attrs)


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
        self.jira = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def log(self):
        call_command('loghours')

    def test_login_with_settings_data(self):
        SERVER = 'https://machinalis.atlassian.net'
        USERNAME = 'YOUR_USER'
        PASSWORD = 'YOUR_PASSWORD'

        with self.settings(JIRA_BASE_URL=SERVER,
                           JIRA_USERNAME=USERNAME,
                           JIRA_PASSWORD=PASSWORD):
            self.log()
        expected = {'options': {'server': SERVER},
                    'basic_auth': (USERNAME, PASSWORD)}
        self.jira.assert_called_once_with(**expected)


    def test_all_fact_finished_and_not_excluded_are_logged(self):
        self.jira.configure_mock(return_value=JiraClientMock())

        f1 = FactFactory('1@CPI', finished=True)
        f2 = FactFactory('2@CPINB', finished=True)
        self.log()
        # to do check jira.issue is called