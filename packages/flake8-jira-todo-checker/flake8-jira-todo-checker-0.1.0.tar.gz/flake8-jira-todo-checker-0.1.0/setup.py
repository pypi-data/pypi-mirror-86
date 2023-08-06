# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_jira_todo_checker']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3,<4']

entry_points = \
{'flake8.extension': ['JIR001 = flake8_jira_todo_checker:Checker']}

setup_kwargs = {
    'name': 'flake8-jira-todo-checker',
    'version': '0.1.0',
    'description': 'Flake8 plugin to check that every TODO, FIXME, QQ etc comment has a JIRA ID next to it.',
    'long_description': 'Flake8 JIRA TODO Checker\n========================\n\nFlake8 plugin to check that every `TODO`, `FIXME`, `QQ` etc comment has a JIRA ID next to it.\n',
    'author': 'Simon StJG',
    'author_email': 'Simon.StJG@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonstjg/flake8-jira-todo-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
