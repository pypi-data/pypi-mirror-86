# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secmgr']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.25,<2.0.0']

setup_kwargs = {
    'name': 'secmgr',
    'version': '1.0.3',
    'description': 'Utility for working with AWS Secrets Manager',
    'long_description': None,
    'author': 'Naveed Khan',
    'author_email': 'naveed@kinoo.family',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
