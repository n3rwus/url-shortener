import inspect
from functools import wraps
from typing import Dict, List, Any, Callable
from datetime import datetime, timedelta

"""
This module provides caching functionality for the application.
"""

# Simple in-memory cache implementation
cache: Dict[str, Dict[str, Any]] = {}


def timed_cache(seconds: int = 300):
    """
    Decorator to cache function results for a specified time period.

    Args:
        seconds (int): Cache expiration time in seconds

    Returns:
        Callable: Decorated function with caching capability
    """

    def decorator(func: Callable):
        is_async = inspect.iscoroutinefunction(func)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            if cache_key in cache:
                cached = cache[cache_key]
                if datetime.now() < cached["expiry"]:
                    return cached["data"]

            result = await func(*args, **kwargs)
            cache[cache_key] = {
                "data": result,
                "expiry": datetime.now() + timedelta(seconds=seconds),
            }
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            if cache_key in cache:
                cached = cache[cache_key]
                if datetime.now() < cached["expiry"]:
                    return cached["data"]

            result = func(*args, **kwargs)
            cache[cache_key] = {
                "data": result,
                "expiry": datetime.now() + timedelta(seconds=seconds),
            }
            return result

        return async_wrapper if is_async else sync_wrapper

    return decorator