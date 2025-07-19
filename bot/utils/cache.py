"""
This module provides a simple asynchronous in-memory cache
with timestamping for each cached item.
"""

import asyncio
from typing import Any, Dict, Tuple, Optional
from datetime import datetime, timezone


class SimpleCache:
    """
    A thread-safe asynchronous cache that stores values along with
    their insertion timestamps.
    """

    def __init__(self):
        """
        Initializes the cache dictionary and an asyncio lock
        to ensure safe concurrent access.
        """
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Tuple[Any, datetime]]:
        """
        Retrieve a cached value and its timestamp by key.

        Args:
            key (str): The key to look up in the cache.

        Returns:
            Optional[Tuple[Any, datetime]]: The cached value and its timestamp,
            or None if the key is not found.
        """
        async with self._lock:
            return self._cache.get(key)

    async def set(self, key: str, value: Any) -> None:
        """
        Set a cache entry with the given key and value, timestamping it.

        Args:
            key (str): The key for the cache entry.
            value (Any): The value to cache.
        """
        async with self._lock:
            self._cache[key] = (value, datetime.now(timezone.utc))
