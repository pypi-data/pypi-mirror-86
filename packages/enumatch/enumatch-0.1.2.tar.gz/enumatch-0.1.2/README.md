enumatch
========

[![PyPI version](https://img.shields.io/pypi/v/enumatch.svg)](https://pypi.org/project/enumatch)
[![codecov](https://codecov.io/gh/sayanarijit/enumatch/branch/master/graph/badge.svg)](https://codecov.io/gh/sayanarijit/enumatch)

Strictly match all the possibilities of an enum

Use case
--------

This little `match` function makes matching Python's enum fields safer by forcing
us to match all the possibilities either explicitely or by using a default value.

Use `...` (ellipsis) for default.

> TIP: Create the matcher at compile-time to have zero runtime cost.


Example
-------

```python
from enum import Enum, auto
from enumatch import match

class Side(Enum):
    left = auto()
    right = auto()

# Define a simple matcher
matcher1 = match({Side.left: "Go left", Side.right: "Go right"})

assert matcher1[Side.left] == "Go left"
assert matcher1[Side.right] == "Go right"

# Define a matcher with a default case
matcher2 = match({Side.left: "Go left", ...: "Go right"})

assert matcher2[Side.left] == "Go left"
assert matcher2[Side.right] == "Go right"

# If all the possibilities are not handled, we get error
with pytest.raises(ValueError, match="missing possibilities: Side.right"):
    match({Side.left: "Go left"})
```
