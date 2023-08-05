# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oradad_file']

package_data = \
{'': ['*']}

install_requires = \
['lz4>=3.1.1,<4.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pycrypto>=2.6.1,<3.0.0',
 'rsa>=4.6,<5.0']

setup_kwargs = {
    'name': 'oradad-file',
    'version': '0.1.0',
    'description': 'Oradad File reader in python3',
    'long_description': None,
    'author': 'Léonard Moreau',
    'author_email': 'leonard@moreau.cloud',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
