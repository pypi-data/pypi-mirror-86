# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['create_django_project']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['create-django-project = create_django_project.main:main']}

setup_kwargs = {
    'name': 'create-django-project',
    'version': '0.0.1',
    'description': 'Command Line Interface (CLI) that abstract much of common pattern in creating and structuring Django project.',
    'long_description': 'Create Django Project\n=====================\nCommand Line Interface (CLI) that abstract much of common pattern in creating and structuring Django project.\n',
    'author': 'Innocent Zenda',
    'author_email': 'zendainnocent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZendaInnocent/create-django-project.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
