# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enumatch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enumatch',
    'version': '0.1.1',
    'description': 'Force match all possibilities of an enum',
    'long_description': 'enumatch\n========\n\n[![PyPI version](https://img.shields.io/pypi/v/enumatch.svg)](https://pypi.org/project/enumatch)\n[![codecov](https://codecov.io/gh/sayanarijit/enumatch/branch/master/graph/badge.svg)](https://codecov.io/gh/sayanarijit/enumatch)\n\nMatch all the possibilities of an enum\n\nUse case\n--------\n\nThis little `match` function makes matching Python\'s enum fields safer by forcing\nus to match all the possibilities either explicitely or by using a default value.\n\nUse ... (ellipsis) for default.\n\n\nExample\n-------\n\n```python\nfrom enum import Enum, auto\nfrom enumatch import match\n\nclass Side(Enum):\n    left = auto()\n    right = auto()\n\n# Define a simple matcher\nmatcher1 = match({Side.left: "Go left", Side.right: "Go right"})\n\nassert matcher1[Side.left] == "Go left"\nassert matcher1[Side.right] == "Go right"\n\n# Define a matcher with a default case\nmatcher2 = match({Side.left: "Go left", ...: "Go right"})\nassert matcher2[Side.left] == "Go left"\nassert matcher2[Side.right] == "Go right"\n\n# If all the possibilities are not handled, we get error\nimport pytest\nwith pytest.raises(ValueError, match="missing possibility"):\n    match({Side.left: "Go left"})\n```\n',
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
