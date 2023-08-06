# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypix']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypix',
    'version': '0.1.6',
    'description': 'Python library for generating pix codes with CRC16 validation',
    'long_description': 'Python Pix\n==========================\n\n[![pypi](https://img.shields.io/pypi/v/google-auth.svg)](https://pypi.python.org/pypi/google-auth)\n[![Build Status](https://travis-ci.com/dyohan9/python-pix.svg?branch=master)](https://travis-ci.com/dyohan9/python-pix)\n[![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)](https://www.python.org/)\n[![License GPL-3.0](https://img.shields.io/badge/license-%20GPL--3.0-yellow.svg)](https://github.com/bothub-it/bothub-engine/blob/master/LICENSE)\n\n\nThis library automates the creation of Pix keys\n\nInstalling\n----------\n\nYou can install using [pip](https://pip.pypa.io/en/stable/):\n\n    $ pip install pypix\n\n### Supported Python Versions\n\nPython \\>= 3.6\n\n### Deprecated Python Versions\n\nPython == 2.7. Python 2.7 support will be removed on January 1, 2020.\n\nCurrent Maintainers\n-------------------\n\n-   [@dyohan9](https://github.com/dyohan9) (Daniel Yohan)\n\nAuthors\n-------\n\n-   [@dyohan9](https://github.com/dyohan9) (Daniel Yohan)\n\nContributing\n------------\n\nContributions to this library are always welcome and highly encouraged.\n\nSee\n[CONTRIBUTING.md](https://github.com/dyohan9/python-pix/blob/master/CONTRIBUTING.md)\nfor more information on how to get started.\n\nLicense\n-------\n\nGPL-3.0 License - See [the\nLICENSE](https://github.com/dyohan9/python-pix/blob/master/LICENSE)\nfor more information.\n',
    'author': 'Daniel Yohan',
    'author_email': 'dyohan9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dyohan9/python-pix',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
