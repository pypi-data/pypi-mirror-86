enumatch
========

[![PyPI version](https://img.shields.io/pypi/v/enumatch.svg)](https://pypi.org/project/enumatch)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/enumatch.svg)](https://pypi.org/project/enumatch)
[![Test Coverage](https://api.codeclimate.com/v1/badges/36a72f1bf1a4979a765c/test_coverage)](https://codeclimate.com/github/sayanarijit/enumatch/test_coverage)

Strictly match all the possibilities of an enum.

Use case
--------

This little `match` function makes matching Python's enum fields safer by forcing
us to match all the possibilities either explicitly or by using a wildcard.

Use `...` (ellipsis) for the wildcard.


> ***TIPs***
> 
> - Avoid the use of `...` (wildcard) to make sure any modification to the enums are safe.
> - Create the matcher at compile-time to have compile-time validation and zero runtime cost.


Example: Flat matcher
---------------------

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


Example: Nested matcher
-----------------------

```python
from enum import Enum, auto
from enumatch import match, forall

class Switch(Enum):
    on = auto()
    off = auto()

# is_on[main_switch][bedroom_switch]: bool
is_on = match({
    Switch.on: match({Switch.on: True, Switch.off: False}),
    Switch.off: forall(Switch, False),
})

assert is_on[Switch.on][Switch.on] == True
assert is_on[Switch.on][Switch.off] == False
assert is_on[Switch.off][Switch.on] == False
assert is_on[Switch.off][Switch.off] == False
```
