# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fedgp']

package_data = \
{'': ['*']}

install_requires = \
['sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'fedgp',
    'version': '0.1.0.dev1',
    'description': 'A package for model agreggation in federated learning using Gaussian processes',
    'long_description': None,
    'author': 'Santiago',
    'author_email': '16252054+sssilvar@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
