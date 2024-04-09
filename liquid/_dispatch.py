from typing import Protocol, TypeVar

from pydantic import BaseModel


__all__ = (
    "Dispatch",
)


A = TypeVar("A", contravariant=True, bound=BaseModel)
R = TypeVar("R", covariant=True)


class Dispatch(Protocol[A, R]):
    async def __call__(self, action: A) -> R:
        ...
