from typing import Iterable


def is_sliceable(obj: object) -> bool:
    """
    Checks if an object is an iterable that supports slicing.

    Args:
        obj: The object to check.

    Returns:
        True if the object is an iterable that supports slicing, False otherwise.
    """
    return isinstance(obj, Iterable) and hasattr(obj, "__getitem__")
