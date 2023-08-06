# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['title_setter']

package_data = \
{'': ['*']}

install_requires = \
['pathlib>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'title-setter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'azartoosa',
    'author_email': 'azartoosa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
