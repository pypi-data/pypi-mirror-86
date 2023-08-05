# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enumatch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enumatch',
    'version': '0.1.0',
    'description': 'Force match all possibilities of an enum',
    'long_description': None,
    'author': 'Arijit Basu',
    'author_email': 'sayanarijit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
