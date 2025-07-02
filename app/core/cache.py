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
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}:{v}" for k, v in kwargs.items()])
            cache_key = ":".join(key_parts)

            # Check if the result is in cache and not expired
            if cache_key in cache:
                cached_data = cache[cache_key]
                if datetime.now() < cached_data["expiry"]:
                    return cached_data["data"]

            # Execute the function and cache the result
            result = await func(*args, **kwargs)
            cache[cache_key] = {
                "data": result,
                "expiry": datetime.now() + timedelta(seconds=seconds)
            }

            return result

        return wrapper

    return decorator