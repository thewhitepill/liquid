from typing import Any, Callable

from ._store import Store, StoreEnhancer
from ._dispatch import Dispatch
from ._utility import compose, extend


__all__ = (
    "Middleware",
    "Next",

    "apply_middleware"
)


Next = Dispatch[Any, Any]
Middleware = Callable[[Store[Any, Any, Any]], Callable[[Next], Callable[[Any], Any]]]


def apply_middleware(*chain: list[Middleware]) -> StoreEnhancer[Any, Any, Any, Any]:
    def enhance(original_store: Store[Any, Any, Any]) -> Store[Any, Any, Any]:
        nonlocal chain

        enhanced_store = extend(original_store)
        partial = [middleware(enhanced_store) for middleware in chain]
        enhanced_store.dispatch = compose(*partial)(original_store.dispatch)

        return enhanced_store

    return enhance
