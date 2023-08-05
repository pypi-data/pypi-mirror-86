# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seabird']

package_data = \
{'': ['*']}

install_requires = \
['betterproto>=1.2.5,<2.0.0', 'grpclib>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'python-seabird',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kaleb Elwert',
    'author_email': 'belak@coded.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
