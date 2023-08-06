# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['config_injector', 'config_injector.config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'config-injector',
    'version': '0.1.1',
    'description': 'Simple dependency injection framework for python for easy and logical app configuration.',
    'long_description': '# config-injector\nA simple json configuration dependency injector framework.\n',
    'author': 'DustinMoriarty',
    'author_email': 'dustin.moriarty@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DustinMoriarty/config-injector',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
