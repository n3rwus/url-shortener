import pytest
import asyncio
from app.core.cache import timed_cache


def test_sync_cache_within_expiry(monkeypatch):
    call_count = {"count": 0}

    @timed_cache(seconds=1)
    def add(a, b):
        call_count["count"] += 1
        return a + b

    # First call, should compute result
    result1 = add(2, 3)
    # Second call, should return cached result
    result2 = add(2, 3)

    assert result1 == result2 == 5
    assert call_count["count"] == 1  # Cached on second call


def test_sync_cache_after_expiry():
    call_count = {"count": 0}

    @timed_cache(seconds=0)  # Cache instantly expires
    def multiply(x, y):
        call_count["count"] += 1
        return x * y

    result1 = multiply(4, 5)
    result2 = multiply(4, 5)

    assert result1 == result2 == 20
    assert call_count["count"] == 2  # No cache reuse


@pytest.mark.asyncio
async def test_async_cache(monkeypatch):
    call_count = {"count": 0}

    @timed_cache(seconds=2)
    async def fetch_data():
        call_count["count"] += 1
        return {"key": "value"}

    result1 = await fetch_data()
    result2 = await fetch_data()

    assert result1 == result2
    assert call_count["count"] == 1


@pytest.mark.asyncio
async def test_async_cache_expiry():
    call_count = {"count": 0}

    @timed_cache(seconds=1)
    async def delayed_response():
        call_count["count"] += 1
        return "done"

    await delayed_response()
    await asyncio.sleep(1.5)
    await delayed_response()

    assert call_count["count"] == 2
