# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['config_injector', 'config_injector.config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'config-injector',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DustinMoriarty',
    'author_email': 'dustin.moriarty@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
