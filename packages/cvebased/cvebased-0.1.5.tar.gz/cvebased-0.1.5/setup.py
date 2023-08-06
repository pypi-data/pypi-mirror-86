# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvebased']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'cvebased',
    'version': '0.1.5',
    'description': 'A utility library to ease interactions with cvebase.com data',
    'long_description': '# cvebased',
    'author': 'cvebase',
    'author_email': 'hello@cvebase.com',
    'maintainer': 'cvebase',
    'maintainer_email': 'hello@cvebase.com',
    'url': 'https://www.cvebase.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
