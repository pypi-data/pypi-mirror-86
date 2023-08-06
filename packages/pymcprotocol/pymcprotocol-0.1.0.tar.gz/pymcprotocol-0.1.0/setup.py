# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymcprotocol']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymcprotocol',
    'version': '0.1.0',
    'description': 'MC Protocol(MELSEC Communication Protocol) implementation by Python',
    'long_description': None,
    'author': 'Yohei Osawa',
    'author_email': 'yohei.osawa.318.niko8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
