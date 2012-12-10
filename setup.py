#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as readme:
    __doc__ = readme.read()


setup(
    name = 'hamster2jira',
    version = '0.1',
    description = 'Post your Hamster logs into Jira',
    long_description = __doc__,
    author = u'Martín Gaitán',
    author_email = 'gaitan@gmail.com',
    url='https://github.com/mgaitan/hamster2jira',
    packages = find_packages(),
    package_data={'hamster2jira': ['local_settings.py.template']},
    license = 'GNU GENERAL PUBLIC LICENCE v3.0',
    install_requires = ['django>=1.2', 'jira-python'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
    scripts = ['scripts/hamster2jira'],
)
