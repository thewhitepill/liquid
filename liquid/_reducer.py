from typing import Protocol, TypeVar


__all__ = (
    "Reducer",
)


S = TypeVar("S")
A = TypeVar("A", contravariant=True)


class Reducer(Protocol[S, A]):
    def __call__(self, state: S, action: A) -> S:
        ...
