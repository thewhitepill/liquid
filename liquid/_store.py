from typing import Callable, Generic, TypeVar

from pydantic import BaseModel

from ._dispatch import Dispatch
from ._reducer import Reducer
from ._utility import identity


__all__ = (
    "DefaultStore",
    "GetState",
    "Store",
    "StoreEnhancer",
    "StoreFactory",

    "create_store",
    "default_store_factory"
)


S = TypeVar("S", bound=BaseModel)
A = TypeVar("A", bound=BaseModel)
R1 = TypeVar("R1")
R2 = TypeVar("R2")


GetState = Callable[[], S]


class Store(Generic[S, A, R1]):
    dispatch: Dispatch[A, R1]
    get_state: GetState[S]


StoreEnhancer = Callable[[Store[S, A, R1]], Store[S, A, R2]]
StoreFactory = Callable[[Reducer[S, A], S], Store[S, A, R1]]


class DefaultStore(Store[S, A, S]):
    def __init__(self, reducer: Reducer[S, A], initial_state: S) -> None:
        self._reducer = reducer
        self._state = initial_state

    async def dispatch(self, action: A) -> S:
        self._state = self._reducer(self._state, action)

        return self._state

    def get_state(self) -> S:
        return self._state


def default_store_factory(
    reducer: Reducer[S, A],
    initial_state: S
) -> Store[S, A, S]:
    return DefaultStore(reducer, initial_state)


def create_store(
    reducer: Reducer[S, A],
    initial_state: S,
    factory: StoreFactory[S, A, R1] = default_store_factory, # type: ignore[assignment]
    enchancer: StoreEnhancer[S, A, R1, R2] = identity # type: ignore[assignment]
) -> Store[S, A, R2]:
    return enchancer(factory(reducer, initial_state))
