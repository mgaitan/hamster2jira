from django.test import TestCase
from mock import patch
from django.core.management import call_command


class TestLogin(TestCase):

    def log(self):
        call_command('loghours')

    def test_login_with_settings_data(self):
        SERVER = 'https://machinalis.atlassian.net'
        USERNAME = 'YOUR_USER'
        PASSWORD = 'YOUR_PASSWORD'
        with patch('jira.client.JIRA') as mck:

            with self.settings(JIRA_BASE_URL=SERVER,
                               JIRA_USERNAME=USERNAME,
                               JIRA_PASSWORD=PASSWORD):
                self.log()
        expected = {'options': {'server': SERVER},
                    'basic_auth': (USERNAME, PASSWORD)}
        mck.assert_called_once_with(**expected)
