from datetime import timedelta
from hamster.tests.factories import FactFactory
from django.test import TestCase
from mock import Mock, patch, call
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
        self.jira = JiraClientMock()    # the client instance
        patcher = patch('jira.client.JIRA', return_value=self.jira)
        self.JIRA = patcher.start()    # the mocked class
        self.addCleanup(patcher.stop)

    def log(self):
        call_command('loghours')

    def test_only_fact_finished_not_logged_and_not_excluded_are_used(self):

        FactFactory('1@CPI', finished=True)
        FactFactory('2@CPINB', finished=True)
        FactFactory('3@OTHER', finished=True)  # not belong to a know projects
        FactFactory('4@CPI', finished=False)   # not finished
        FactFactory('5@CPINB', finished=True, logged=True)   # already_logged

        self.log()
        self.assertEqual(self.jira.issue.call_count, 2)
        self.jira.issue.assert_has_call(call('CPI-1'))
        self.jira.issue.assert_has_call(call('CPI-2'))
