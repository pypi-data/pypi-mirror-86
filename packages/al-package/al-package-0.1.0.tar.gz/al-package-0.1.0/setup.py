# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['al_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'al-package',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alok Singh',
    'author_email': 'aloks@cvent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
