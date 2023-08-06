# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_goodreads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio-goodreads',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mykola Solodukha',
    'author_email': 'mykola.soloduha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.4,<4.0.0',
}


setup(**setup_kwargs)
