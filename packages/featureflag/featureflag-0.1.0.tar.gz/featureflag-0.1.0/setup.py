# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['featureflag', 'featureflag.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.3,<4.0.0']

setup_kwargs = {
    'name': 'featureflag',
    'version': '0.1.0',
    'description': 'Object based feature flags for django',
    'long_description': None,
    'author': 'Winston Ferreira',
    'author_email': 'winstonf88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
