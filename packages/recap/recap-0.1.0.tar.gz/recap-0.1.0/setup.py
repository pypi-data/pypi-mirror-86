# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recap']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0', 'yacs>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'recap',
    'version': '0.1.0',
    'description': 'Reproducible configurations for any project',
    'long_description': '# recap\n\n![build](https://github.com/georgw777/recap/workflows/build/badge.svg)\n\n**re**producible **c**onfigurations for **a**ny **p**roject\n',
    'author': 'Georg Wölflein',
    'author_email': 'georgw7777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/georgw777/recap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
