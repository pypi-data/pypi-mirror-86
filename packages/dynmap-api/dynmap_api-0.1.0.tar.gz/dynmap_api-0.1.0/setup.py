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
    'version': '0.1.0',
    'description': 'A unified Python API wrapper for Dynmap',
    'long_description': '# dynmap_api\nA unified Python API wrapper for Dynmap\n',
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
