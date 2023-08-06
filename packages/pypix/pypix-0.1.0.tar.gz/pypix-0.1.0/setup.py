# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypix']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypix',
    'version': '0.1.0',
    'description': 'Python library for generating pix codes with CRC16 validation',
    'long_description': None,
    'author': 'Daniel Yohan',
    'author_email': 'dyohan9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
