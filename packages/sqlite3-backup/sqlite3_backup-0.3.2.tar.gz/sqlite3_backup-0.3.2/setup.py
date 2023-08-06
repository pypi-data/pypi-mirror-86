# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite3_backup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlite3-backup',
    'version': '0.3.2',
    'description': 'implements missing backup functionality in sqlite3 module',
    'long_description': '# README\n\n`sqlite3` from the standard library does not support the backup\nfunctionality provided by the original `sqlite3` C implementation.\n\nThis package fixes this by providing a simple backup function.\n\nTypical use case is to write an in-memory sqlite3-db to disk.\n\nThis package uses the `ctypes` module and does not require a\nworking c compiler setup.\n',
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
