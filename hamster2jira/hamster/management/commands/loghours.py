from django.core.management.base import NoArgsCommand
from django.db import settings
from jira.client import JIRA
from jira.exceptions import JIRAError
from hamster2jira.hamster.models import Fact, Tag, FactTag


def days_hours_minutes(td):
    return "%dd %dh %dm" % (td.days,
                            td.seconds // 3600,
                            (td.seconds // 60) % 60)


# Status id for reopen is 4, but for transition is 3
# Jira API sucks. Really

TO_REOPEN = u'3'
TO_CLOSE = u'2'
TO_RESOLVE = u'2'


class Command(NoArgsCommand):
    help = "Syncs your hamster's logs into Jira"

    def handle_noargs(self, **options):

        jira = JIRA(basic_auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD),
                    options={'server': settings.JIRA_BASE_URL})

        print "Logged in..."

        categories = [p.key for p in jira.projects()]
        tag_logged, _ = Tag.objects.get_or_create(name='_logged_')

        facts = Fact.objects \
                    .exclude(tags=tag_logged) \
                    .exclude(end_time=None) \
                    .filter(activity__category__name__in=categories)

        for f in facts:
            reopened = False
            try:
                issue_key = '%s-%s' % (f.category, f.activity.name)
                issue = jira.issue(issue_key)

                if  issue.fields.status.name in ('Closed', 'Resolve'):
                    reopened = True
                    # reopen to allow worklogs
                    jira.transition_issue(issue, TO_REOPEN)
                    jira.add_comment(issue, 'hamster2jira: Automatically reopened for a'
                                            'while to allow add a worklog')
            except JIRAError:
                continue

            spent = days_hours_minutes(f.duration)
            #and post the fact into dotproject!
            worklog = jira.add_worklog(issue, spent)
            worklog.update(comment=f.description)

            #create a tag to associate this worklog whit the fact
            wl_tag = Tag.objects.create(name='wl%s' % worklog.id)
            FactTag.objects.create(tag=wl_tag, fact=f)
            print "Succesfully log %s into %s" % (spent, issue_key)

            #then mark the fact as logged.
            FactTag.objects.create(fact=f, tag=tag_logged)
            if reopened:
                jira.transition_issue(issue, TO_CLOSE)
