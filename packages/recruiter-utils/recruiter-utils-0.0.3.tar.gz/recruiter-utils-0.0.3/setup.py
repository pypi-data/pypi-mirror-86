# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'recruiter-utils',
    'version': '0.0.3',
    'description': 'Package with util functions for recruiter',
    'long_description': None,
    'author': 'ArcLightSlavik',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
