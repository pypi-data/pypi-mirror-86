# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enumatch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enumatch',
    'version': '0.2.0',
    'description': 'Strictly match all the possibilities of an enum',
    'long_description': 'enumatch\n========\n\n[![PyPI version](https://img.shields.io/pypi/v/enumatch.svg)](https://pypi.org/project/enumatch)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/enumatch.svg)](https://pypi.org/project/enumatch)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/36a72f1bf1a4979a765c/test_coverage)](https://codeclimate.com/github/sayanarijit/enumatch/test_coverage)\n\nStrictly match all the possibilities of an enum.\n\nUse case\n--------\n\nThis little `match` function makes matching Python\'s enum fields safer by forcing\nus to match all the possibilities either explicitly or by using a wildcard.\n\nUse `...` (ellipsis) for the wildcard.\n\n\n> ***TIPs***\n> \n> - Avoid the use of `...` (wildcard) to make sure any modification to the enums are safe.\n> - Create the matcher at compile-time to have compile-time validation and zero runtime cost.\n\n\nExample: Flat matcher\n---------------------\n\n```python\nfrom enum import Enum, auto\nfrom enumatch import match\n\nclass Side(Enum):\n    left = auto()\n    right = auto()\n\n# Define a simple matcher\nmatcher1 = match({Side.left: "Go left", Side.right: "Go right"})\n\nassert matcher1[Side.left] == "Go left"\nassert matcher1[Side.right] == "Go right"\n\n# Define a matcher with a default case\nmatcher2 = match({Side.left: "Go left", ...: "Go right"})\n\nassert matcher2[Side.left] == "Go left"\nassert matcher2[Side.right] == "Go right"\n\n# If all the possibilities are not handled, we get error\nwith pytest.raises(ValueError, match="missing possibilities: Side.right"):\n    match({Side.left: "Go left"})\n```\n\n\nExample: Nested matcher\n-----------------------\n\n```python\nfrom enum import Enum, auto\nfrom enumatch import match, forall\n\nclass Switch(Enum):\n    on = auto()\n    off = auto()\n\n# is_on[main_switch][bedroom_switch]: bool\nis_on = match({\n    Switch.on: match({Switch.on: True, Switch.off: False}),\n    Switch.off: forall(Switch, False),\n})\n\nassert is_on[Switch.on][Switch.on] == True\nassert is_on[Switch.on][Switch.off] == False\nassert is_on[Switch.off][Switch.on] == False\nassert is_on[Switch.off][Switch.off] == False\n```\n',
    'author': 'Arijit Basu',
    'author_email': 'sayanarijit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sayanarijit/enumatch',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
