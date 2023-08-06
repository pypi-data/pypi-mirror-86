# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trex_imager_readfile']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'trex-imager-readfile',
    'version': '1.0.2',
    'description': 'Read functions for TREx ASI PGM raw files',
    'long_description': None,
    'author': 'Darren Chaddock',
    'author_email': 'dchaddoc@ucalgary.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
