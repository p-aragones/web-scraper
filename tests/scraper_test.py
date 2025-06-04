import time
import pytest
from app.services.scraper_service import get_posts
from typing import List

@pytest.mark.asyncio
async def test_posts_length():
    posts: List[dict] = await get_posts(1)
    assert len(posts) == 30
    posts: List[dict] = await get_posts(5)
    assert len(posts) == 30 * 5

@pytest.mark.asyncio
async def test_caching():
    posts: List[dict] = await get_posts(1)
    posts_cached: List[dict] = await get_posts(1)
    assert posts == posts_cached

@pytest.mark.asyncio
async def test_timing():
    start_time_uncached = time.perf_counter()
    await get_posts(20)
    elapsed_uncached = time.perf_counter() - start_time_uncached

    start_time_cached = time.perf_counter()
    await get_posts(20)
    elapsed_cached = time.perf_counter() - start_time_cached
    print(f"\nWithout cache took {elapsed_uncached:.6f} seconds")
    print(f"With cache took {elapsed_cached:.6f} seconds")

    assert elapsed_cached < elapsed_uncached