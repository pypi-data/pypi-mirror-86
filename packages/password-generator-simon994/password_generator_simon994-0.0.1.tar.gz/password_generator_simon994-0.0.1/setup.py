# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['password_generator_simon994']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'password-generator-simon994',
    'version': '0.0.1',
    'description': 'A simple lib that prints a password, of a specified length',
    'long_description': None,
    'author': 'SimonN',
    'author_email': '65023744+Simon994@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
