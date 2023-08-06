# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['password_generator_simon994']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['generate-pw = password_generator_simon994.password_generator_simon994:generate_password']}

setup_kwargs = {
    'name': 'password-generator-simon994',
    'version': '0.0.4',
    'description': 'A simple password generator. Generates, prints and copies a password to the clipboard',
    'long_description': None,
    'author': 'SimonN',
    'author_email': '65023744+Simon994@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
