from typing import Any, Callable, Protocol, TypeVar

from ._dispatch import Dispatch
from ._reducer import Reducer
from ._utility import identity


__all__ = (
    "DefaultStore",
    "Store",
    "StoreEnhancer",
    "StoreFactory",

    "create_store",
    "default_store_factory"
)


A = TypeVar("A")
R = TypeVar("R")
S = TypeVar("S")
S_co = TypeVar("S_co", covariant=True)


class Store(Protocol[S_co, A, R]):
    dispatch: Dispatch[A, R]

    async def get_state(self) -> S_co:
        ...


StoreEnhancer = Callable[[Store[Any, Any, Any]], Store[Any, Any, Any]]


class StoreFactory(Protocol[S, A, R]):
    def __call__(
        self,
        reducer: Reducer[S, A],
        initial_state: S
    ) -> Store[S, A, R]:
        ...


class DefaultStore(Store[S, A, S]):
    def __init__(self, reducer: Reducer[S, A], initial_state: S) -> None:
        self._reducer = reducer
        self._state = initial_state

    async def dispatch(self, action: A) -> S: # type: ignore[override]
        self._state = self._reducer(self._state, action)

        return self._state

    async def get_state(self) -> S:
        return self._state


def default_store_factory(
    reducer: Reducer[S, A],
    initial_state: S
) -> Store[S, A, S]:
    return DefaultStore(reducer, initial_state)


def create_store(
    reducer: Reducer[S, A],
    initial_state: S,
    factory: StoreFactory[S, A, R] = default_store_factory, # type: ignore[assignment]
    enhancer: StoreEnhancer = identity # type: ignore[assignment]
) -> Store[Any, Any, Any]:
    return enhancer(factory(reducer, initial_state))
