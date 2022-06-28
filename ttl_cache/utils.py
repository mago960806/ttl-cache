from typing import Any, Optional, Hashable


def make_hashable(o: Any) -> Hashable:
    """
    Make any object to hashable type
    """
    match o:
        case tuple() | list():
            return tuple(map(make_hashable, o))
        case dict():
            return tuple(sorted(((k, make_hashable(v)) for k, v in o.items())))
        case object():
            if hasattr(o, "__dict__"):
                return str(vars(o))
            return str(o)


def make_key(*args: Optional[Any], **kwargs: Optional[Any]) -> int:
    """
    Make a cache key from positional and keyword arguments
    """
    return hash(make_hashable(args)) + hash(make_hashable(kwargs))
