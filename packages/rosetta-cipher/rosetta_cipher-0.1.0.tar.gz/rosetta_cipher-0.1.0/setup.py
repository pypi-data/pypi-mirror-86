# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rosetta_cipher']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'cityhash>=0.2.3,<0.3.0',
 'click>=7.1.2,<8.0.0',
 'gunicorn>=20.0.4,<21.0.0']

entry_points = \
{'console_scripts': ['rosetta-cipher = rosetta_cipher.cli:process']}

setup_kwargs = {
    'name': 'rosetta-cipher',
    'version': '0.1.0',
    'description': 'A package to generate human readable names from hashs, datetime/timestamp, versions (Comes from the great name generatory of https://github.com/moby/moby)',
    'long_description': None,
    'author': 'purplebabar',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
