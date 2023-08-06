# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydevice42']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'pydevice42',
    'version': '0.1.0',
    'description': 'Enhancements to the Sync scripts for Device42',
    'long_description': None,
    'author': 'Joaquim Esteves',
    'author_email': 'joaquimbve@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
