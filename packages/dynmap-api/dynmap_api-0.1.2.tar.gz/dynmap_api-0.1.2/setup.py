# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynmap_api', 'dynmap_api.datastructures', 'dynmap_api.net']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'dynmap-api',
    'version': '0.1.2',
    'description': 'A unified Python API wrapper for Dynmap',
    'long_description': '# Minecraft Dynamic Map API Wrapper ![Poetry Build Suite](https://github.com/Ewpratten/dynmap_api/workflows/Poetry%20Build%20Suite/badge.svg) [![PyPI version](https://img.shields.io/pypi/v/dynmap_api.svg)](https://pypi.python.org/pypi/dynmap_api/)\n\n`dynmap_api` is a Python library for querying data from Minecraft servers running the [Dynmap](https://github.com/webbukkit/dynmap) plugin.\n\n## Installation\n\nTo install, ensure your system has `python3` and `python3-pip`, then run:\n\n```sh\npython3 -m pip install dynmap_api\n```\n\n## Documentation\n\nAPI documentation can be found [here](https://ewpratten.retrylife.ca/dynmap_api/)',
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
