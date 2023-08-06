# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['column_diff']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.5,<4.0.0', 'pandas>=1.1.4,<2.0.0', 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'column-diff',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
