from typing import Callable, TypeVar

from pydantic import BaseModel


__all__ = (
    "Reducer",
)


S = TypeVar("S", bound=BaseModel)
A = TypeVar("A", bound=BaseModel)

Reducer = Callable[[S, A], S]
