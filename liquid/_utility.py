from typing import TypeVar


__all__ = (
    "identity",
)


T = TypeVar("T")


def identity(x: T) -> T:
    return x
