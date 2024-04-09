from typing import Protocol, TypeVar

from pydantic import BaseModel


__all__ = (
    "Reducer",
)


S = TypeVar("S", bound=BaseModel)
A = TypeVar("A", contravariant=True, bound=BaseModel)


class Reducer(Protocol[S, A]):
    def __call__(self, state: S, action: A) -> S:
        ...
