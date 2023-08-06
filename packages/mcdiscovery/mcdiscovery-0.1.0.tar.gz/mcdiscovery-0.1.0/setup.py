# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcdiscovery', 'mcdiscovery.types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcdiscovery',
    'version': '0.1.0',
    'description': 'A library for discovering Minecraft LAN servers on a network',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
