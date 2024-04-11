from __future__ import annotations

from typing import Union

import pytest

from liquid import create_store


class Dec:
    pass


class Inc:
    pass


Action = Union[type[Inc], type[Dec]]


def reduce(state: int, action: Action) -> int:
    if action is Inc:
        return state + 1

    if action is Dec:
        return state - 1

    raise ValueError(f"Unknown action: {action}")


@pytest.mark.asyncio
async def test_counter():
    store = create_store(reduce, 0)

    assert await store.dispatch(Inc) == 1
    assert await store.dispatch(Inc) == 2
    assert await store.dispatch(Dec) == 1
    assert await store.dispatch(Dec) == 0
