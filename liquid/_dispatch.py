from typing import Protocol, TypeVar


__all__ = (
    "Dispatch",
)


A = TypeVar("A", contravariant=True)
R = TypeVar("R", covariant=True)


class Dispatch(Protocol[A, R]):
    async def __call__(self, action: A) -> R:
        ...
