# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ckan_downloader']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'tqdm>=4.51.0,<5.0.0']

setup_kwargs = {
    'name': 'ckan-downloader',
    'version': '0.1.0',
    'description': 'An interactive command-line utility for downloading data from a CKAN data portal',
    'long_description': None,
    'author': 'Eric McCowan',
    'author_email': 'eric.mccowan@servian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
