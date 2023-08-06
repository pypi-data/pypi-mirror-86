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
    'version': '0.1.1',
    'description': 'An interactive command-line utility for downloading data from a CKAN data portal',
    'long_description': '# ckan-downloader\nAn interactive command-line utility for downloading data from a CKAN data portal.\n\nProvide a CSV with or specify some dataset IDs to start downloading all resources attached to those datasets into folders. \n\n## Installation\n```\npip install ckan-downloader\n```\n\n## Example usage\n```\n$ python -m ckan_downloader\n\nCKAN Downloader 0.1.0\n\nWhat is the data portal URL? \n> geoscience.data.qld.gov.au\n\nTest connection to https://geoscience.data.qld.gov.au/api/action/site_read was successful.\n\nDo you have a CSV with the dataset IDs to download? (y/n) \n> y\n\nWhat is the CSV file path? \n> tests/test1.csv\n\nDoes this CSV have a header row? (y/n) \n> y\n\nThe name of the field/column containing the dataset IDs is needed. The options are:\n   id, PID, Report Title\nWhich field has the IDs? \n> PID\n\nWhich directory should the downloads be saved in? \n> downloads\n\nStarting dataset cr109373\nDownloading CR109373 Report Geometry (https://geoscience.data.qld.gov.au/dataset/e2f7ae5f-e62a-403d-ba55-539074a5380c/resource/geo-doc363732-cr109373/download/%252FReport%25252f109373%25252fDocument%25252f363732%25252f109373.zip) to downloads/cr109373/109373.zip\nDownloading WHOLE REPORT (https://gsq-horizon.s3-ap-southeast-2.amazonaws.com/QDEX/109373/cr_109373_1.pdf) to downloads/cr109373/cr_109373_1.pdf\nStarting dataset cr108134\nDownloading CR108134 Report Geometry (https://geoscience.data.qld.gov.au/dataset/61d06582-c2cf-48ce-a5de-162e71f38ab3/resource/geo-doc361522-cr108134/download/%252FReport%25252f108134%25252fDocument%25252f361522%25252f108134.zip) to downloads/cr108134/108134.zip\nDownloading WHOLE REPORT (https://gsq-horizon.s3-ap-southeast-2.amazonaws.com/QDEX/108134/cr_108134_1.pdf) to downloads/cr108134/cr_108134_1.pdf\n\n```\n\n## Future improvements\n* add command line options to skip interactive mode\n* search by spatial extent\n* include or skip certain filetypes\n* use progress bars',
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
