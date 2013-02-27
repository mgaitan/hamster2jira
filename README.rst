Hamster to Jira logs sync tool
--------------------------------

This tool aims to save your time posting your Hamster_ facts to Jira_
in an automatic way.

.. _Hamster: http://projecthamster.wordpress.com/
.. _Jira: http://www.atlassian.com/es/software/jira/overview


Install
-------

You can install it directly from Github using pip::

    $ pip install git+git://github.com/mgaitan/hamster2jira.git

Usage
-----

Configure ``~/.hamster2jira/local_settings.py``. You can use the provided
``local_settings.py.template`` as a template.

Then run the script::

    $ hamster2jira


How it works
-------------

Suppose you have a Jira project with the key *CPI*, then a hamster fact
like *"45@CPI*  will add a worklog
into the issue *CPI-45* on your Jira account (if it exists, of course)

TODO
----

- Manage newEstimate / reduceBy times
- Summarize worktime
- Manage ticket status (through tags?)
- Tests

