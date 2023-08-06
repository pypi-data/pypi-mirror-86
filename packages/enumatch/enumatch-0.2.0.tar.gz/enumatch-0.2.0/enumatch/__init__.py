__version__ = "0.2.0"  # Also update pyproject.toml

from typing import Dict, TypeVar, Union, Any, Iterable
from enum import Enum

T1 = TypeVar("T1")
T2 = TypeVar("T2")
EnumType = TypeVar("EnumType", bound=Enum)

def match(cases: Dict[Union[T1, Any], T2]) -> Dict[T1, T2]:
    """Strictly match all the possibilities of an enum.

    Use `...` (ellipsis) for default.

    Example:

        >>> from enum import Enum, auto
        >>> from enumatch import match
        >>> 
        >>> class Side(Enum):
        ...     left = auto()
        ...     right = auto()
        ... 
        >>> # Define a simple matcher
        >>> matcher1 = match({Side.left: "Go left", Side.right: "Go right"})
        >>> 
        >>> assert matcher1[Side.left] == "Go left"
        >>> assert matcher1[Side.right] == "Go right"
        >>> 
        >>> # Define a matcher with a default case
        >>> matcher2 = match({Side.left: "Go left", ...: "Go right"})
        >>> 
        >>> assert matcher2[Side.left] == "Go left"
        >>> assert matcher2[Side.right] == "Go right"
        >>> 
        >>> # If all the possibilities are not handled, we get error
        >>> import pytest
        >>> with pytest.raises(ValueError, match="missing possibilities: Side.right"):
        ...     match({Side.left: "Go left"})
        ... 
        >>> 
    """

    if not isinstance(cases, dict):
        raise TypeError("expecting a dict")

    final: Dict[T1, T2] = {}

    case1 = next(iter(cases))
    case1_type = type(case1)

    if not issubclass(case1_type, Enum):
        raise TypeError("the first key of the given dict must be an enum attribute")

    possibilities: Iterable[T1] = iter(case1_type)
    for possibility in possibilities:
        if possibility in cases:
            final[possibility] = cases[possibility]
        elif ... in cases:
            final[possibility] = cases[...]
        else:
            missing = ", ".join([str(p) for p in case1_type if p not in cases])
            raise ValueError(f"missing possibilities: {missing}")

    return final


def forall(enum: Iterable[EnumType], value: T2) -> Dict[EnumType, T2]:
    """A little helper to define a common value for all the possibilities.

    Basically a shortcut to: `{e: value for e in enum}`

    Example:

        >>> from enum import Enum, auto
        >>> from enumatch import match, forall
        >>> 
        >>> class Switch(Enum):
        ...     on = auto()
        ...     off = auto()
        ... 
        >>> # is_on[main_switch][bedroom_switch]: bool
        >>> is_on = match({
        ...     Switch.on: match({Switch.on: True, Switch.off: False}),
        ...     Switch.off: forall(Switch, False),
        ... })
        >>> 
        >>> assert is_on[Switch.on][Switch.on] == True
        >>> assert is_on[Switch.on][Switch.off] == False
        >>> assert is_on[Switch.off][Switch.on] == False
        >>> assert is_on[Switch.off][Switch.off] == False
    """

    return {p: value for p in enum}
