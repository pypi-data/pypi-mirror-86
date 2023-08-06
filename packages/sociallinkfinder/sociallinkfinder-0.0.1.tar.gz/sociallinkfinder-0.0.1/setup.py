# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sociallinkfinder']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'google>=3.0.0,<4.0.0',
 'rapidfuzz>=0.13.3,<0.14.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'sociallinkfinder',
    'version': '0.0.1',
    'description': "input: company's website url  , output: company's facebook, linkedin, twitter, instagram links in a dictionary",
    'long_description': None,
    'author': 'Priyank Mishra',
    'author_email': 'priyank.m9320@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
