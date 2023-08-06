# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guacapy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0', 'simplejson>=3.17.2,<4.0.0']

setup_kwargs = {
    'name': 'guacapy',
    'version': '0.10.0',
    'description': 'REST API client for Apache Guacamole',
    'long_description': None,
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
