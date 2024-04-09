from __future__ import annotations

from typing import Union

import pytest

from liquid import create_store
from pydantic import BaseModel


class Dec(BaseModel):
    pass


class Inc(BaseModel):
    pass


Action = Union[Inc, Dec]


class State(BaseModel):
    value: int

    def decrement(self) -> State:
        return State(value=self.value - 1)

    def increment(self) -> State:
        return State(value=self.value + 1)


def reduce(state: State, action: Action) -> State:
    match action:
        case Inc():
            return state.increment()
        case Dec():
            return state.decrement()
        case _:
            raise TypeError


@pytest.mark.asyncio
async def test_counter():
    store = create_store(reduce, State(value=0))

    assert await store.dispatch(Inc()) == State(value=1)
    assert await store.dispatch(Inc()) == State(value=2)
    assert await store.dispatch(Dec()) == State(value=1)
    assert await store.dispatch(Dec()) == State(value=0)
