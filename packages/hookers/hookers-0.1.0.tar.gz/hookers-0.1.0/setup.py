# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hookers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hookers',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '林玮 (Jade Lin)',
    'author_email': 'linw1995@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
