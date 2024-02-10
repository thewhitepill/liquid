from typing import Awaitable, Callable, TypeVar

from pydantic import BaseModel


__all__ = (
    "Dispatch",
)


A = TypeVar("A", bound=BaseModel)
R = TypeVar("R")


Dispatch = Callable[[A], Awaitable[R]]
