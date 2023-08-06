# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demux', 'demux.cli', 'demux.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'cglims>=1.3.4,<2.0.0',
 'click>=6.7.0,<7.0.0',
 'path.py>=12.5.0,<13.0.0',
 'psutil>=5.7.3,<6.0.0',
 'six>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'demux',
    'version': '0.1.0',
    'description': 'Application for demultiplexing sequence data',
    'long_description': None,
    'author': 'henrikstranneheim',
    'author_email': 'henrik.stranneheim@scilifelab.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
