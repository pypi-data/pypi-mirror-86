# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcdiscovery', 'mcdiscovery.types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcdiscovery',
    'version': '0.1.1',
    'description': 'A library for discovering Minecraft LAN servers on a network',
    'long_description': "# Minecraft LAN Server Discovery ![Poetry Test Suite](https://github.com/Ewpratten/mcdiscovery/workflows/Poetry%20Test%20Suite/badge.svg) ![Poetry Build Suite](https://github.com/Ewpratten/mcdiscovery/workflows/Poetry%20Build%20Suite/badge.svg) [![PyPI version](https://img.shields.io/pypi/v/mcdiscovery.svg)](https://pypi.python.org/pypi/mcdiscovery/)\n\n`mcdiscovery` is a Python library and CLI tool for discovering Minecraft LAN worlds / servers on your local network. This works in accordance to [@tomsik68](https://github.com/tomsik68)'s protocol description [here](https://github.com/tomsik68/mclauncher-api/wiki/LAN-Server-Discovery).\n\n## Installation\n\nTo install, ensure your system has `python3` and `python3-pip`, then run:\n\n```sh\npython3 -m pip install mcdiscovery\n```\n\n## Usage\n\n`mcdiscovery` can be used as a CLI tool by running `python3 -m mcdiscovery`, or as a library with `import mcdiscovery`. API documentation can be found [here](https://ewpratten.retrylife.ca/mcdiscovery/mcdiscovery.net.LANServerFinder.html). ",
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
