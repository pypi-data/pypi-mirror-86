# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite3_backup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlite3-backup',
    'version': '0.3.1',
    'description': 'implements missing backup functionality in sqlite3 module',
    'long_description': None,
    'author': 'Uwe Schmitt',
    'author_email': 'uwe.schmitt@id.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sissource.ethz.ch/schmittu/sqlite3_backup',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
