# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idrivetools']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bmwbackup = idrivetools.backup:backup',
                     'bmwrestore = idrivetools.restore:restore']}

setup_kwargs = {
    'name': 'idrivetools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Read',
    'author_email': 'centurix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
