# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benzema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'benzema',
    'version': '0.1.0',
    'description': 'A straight forward and easy to use bencoding library written in Python 3',
    'long_description': None,
    'author': 'fishr',
    'author_email': 'karim@fishr.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
