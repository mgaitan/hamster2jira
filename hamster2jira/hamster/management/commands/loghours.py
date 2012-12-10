from django.core.management.base import NoArgsCommand, CommandError
from django.db import settings
from jira.client import JIRA
from jira.exceptions import JIRAError
from hamster2jira.hamster.models import Fact, Tag, FactTag


def days_hours_minutes(td):
    return "%dd %dh %dm" % (td.days, td.seconds//3600, (td.seconds//60) % 60)


class Command(NoArgsCommand):
    help = "Syncs your hamster's logs into Jira"

    def handle_noargs(self, **options):

        jira = JIRA(basic_auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD),
                    options={'server': settings.JIRA_BASE_URL })

        print "Logged in..."
        categories = [p.key for p in jira.projects()]
        tag_logged, _ = Tag.objects.get_or_create(name = '_logged_in_dp_')
        facts = Fact.objects \
                    .exclude(tags=tag_logged) \
                    .exclude(end_time=None) \
                    .filter(activity__category__name__in=categories)

        for f in facts:
            try:
                issue_key = '%s-%s' % (f.category, f.activity.name)
                issue = jira.issue(issue_key)
            except JIRAError:
                continue

            spent = days_hours_minutes(f.duration)
            #and post the fact into dotproject!
            jira.add_worklog(issue, spent)
            print "Succesfully log %s into %s" % (spent, issue_key)

            #then mark the fact as logged.
            FactTag.objects.create(fact=f, tag=tag_logged)
