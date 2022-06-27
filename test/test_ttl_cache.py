import asyncio
import uuid
from typing import Callable

import pytest_asyncio
from aiomock import AIOMock

from asyncio_ttl_cache.asyncio_ttl_cache import ttl_cache, cache_map

TTL = int | float  # 过期时间 单位(秒)


@pytest_asyncio.fixture
async def mock_func():
    sum_func = AIOMock()
    sum_func.async_return_value = 1
    return sum_func


async def test_ttl_cache_ttl_setting(mock_func: Callable):

    @ttl_cache(ttl=4)
    async def calculators():
        return await mock_func()

    await calculators()
    await asyncio.sleep(1)
    await calculators()
    await asyncio.sleep(1)
    await calculators()
    await asyncio.sleep(1)
    await calculators()
    await asyncio.sleep(1)
    await calculators()
    await asyncio.sleep(1)
    await calculators()
    await asyncio.sleep(1)

    assert mock_func.call_count == 2


async def test_ttl_cache_key_setting(mock_func: Callable):
    @ttl_cache(key=lambda args, kwargs: "test_key", ttl=4)
    async def calculators():
        return await mock_func()

    await calculators()

    assert "test_key" in cache_map
    assert mock_func.call_count == 1


async def test_single_flight():
    cost = 0.1
    ttl = 0.1

    @ttl_cache(ttl=0.1)
    async def foo(a) -> uuid.UUID:
        await asyncio.sleep(cost)
        return uuid.uuid1()

    task = asyncio.create_task(foo(0))
    assert await foo(0) == await task
    assert isinstance(await task, uuid.UUID)

    await asyncio.sleep(ttl)
    assert await foo(0) != await task
