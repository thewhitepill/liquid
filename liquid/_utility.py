from functools import reduce
from typing import Any, Callable, TypeVar
from types import SimpleNamespace


__all__ = (
    "compose",
    "extend",
    "identity"
)


T = TypeVar("T")


def compose(*functions: list[Callable]) -> Callable:
    if len(functions) == 0:
        return identity

    if len(functions) == 1:
        return functions[0]

    return reduce(lambda f, g: lambda *args: f(g(*args)), functions)


def extend(source: Any, **kwargs: dict[str, Any]) -> Any:
    props = {k: getattr(k) for k in source.__dir__() if not k.startswith("_")}
    props = {**props, **kwargs}

    return SimpleNamespace(**props)


def identity(x: T) -> T:
    return x
