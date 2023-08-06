# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sportsref', 'sportsref.nba', 'sportsref.nfl', 'sportsref.nfl.finders']

package_data = \
{'': ['*']}

install_requires = \
['mementos>=1.3.1,<2.0.0',
 'numexpr>=2.7.1,<3.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'sportsref',
    'version': '0.11.0',
    'description': '',
    'long_description': None,
    'author': 'Matt Goldberg',
    'author_email': 'matt.goldberg7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
