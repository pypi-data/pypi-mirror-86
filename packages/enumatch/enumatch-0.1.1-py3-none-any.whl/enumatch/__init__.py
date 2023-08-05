__version__ = "0.1.1"

from typing import Dict, TypeVar, Union, List, Any
from enum import Enum

T1 = TypeVar("T1")
T2 = TypeVar("T2")

def match(cases: Dict[Union[T1, Any], T2]) -> Dict[T1, T2]:  # type: ignore
    """Match all the possibilities of an enum

    Use ... (ellipsis) for default.

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
        >>> assert matcher2[Side.left] == "Go left"
        >>> assert matcher2[Side.right] == "Go right"
        >>> 
        >>> # If all the possibilities are not handled, we get error
        >>> import pytest
        >>> with pytest.raises(ValueError, match="missing possibility"):
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

    possibilities: List[T1] = list(case1_type)

    for possibility in possibilities:
        if possibility not in cases:
            if ... not in cases:
                raise ValueError(f"missing possibility: {possibility}")
            else:
                final[possibility] = cases[...]
        else:
            final[possibility] = cases[possibility]

    return final
