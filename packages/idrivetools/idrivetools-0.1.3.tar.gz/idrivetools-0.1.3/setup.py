# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idrivetools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['bmwpack = idrivetools.pack:pack_files',
                     'bmwunpack = idrivetools.unpack:unpack_files']}

setup_kwargs = {
    'name': 'idrivetools',
    'version': '0.1.3',
    'description': 'iDrive tools for packing and unpacking BMW backups',
    'long_description': None,
    'author': 'Chris Read',
    'author_email': 'centurix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
