# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hush']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pycryptodome>=3.9.4,<4.0.0']

entry_points = \
{'console_scripts': ['hush = hush:cli']}

setup_kwargs = {
    'name': 'hush',
    'version': '2.0.0',
    'description': 'Minimalistic command line secret management',
    'long_description': None,
    'author': 'Lech Gudalewicz',
    'author_email': 'lechgu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lechgu/hush',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
