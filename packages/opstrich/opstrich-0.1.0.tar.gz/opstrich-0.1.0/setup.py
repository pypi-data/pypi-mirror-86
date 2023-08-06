# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opstrich', 'opstrich.invoke']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'invoke>=1.4.1,<2.0.0',
 'isort>=5.6.4,<6.0.0',
 'pyupgrade>=2.7.4,<3.0.0']

setup_kwargs = {
    'name': 'opstrich',
    'version': '0.1.0',
    'description': 'DevOps tooling, various scripts, etc.',
    'long_description': '# Opstrich\n#### DevOps tooling, various scripts, etc.\n\n[![Build Status](https://travis-ci.com/RevolutionTech/opstrich.svg?branch=main)](https://travis-ci.com/RevolutionTech/opstrich)\n',
    'author': 'Lucas Connors',
    'author_email': 'lucas@revolutiontech.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RevolutionTech/opstrich',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
