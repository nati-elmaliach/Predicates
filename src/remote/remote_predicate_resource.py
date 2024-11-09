from __future__ import annotations

import asyncio
import logging
import os
from typing import Optional

import aiohttp
from data import test_user

from src import Predicate

logger = logging.getLogger(__name__)


class RemotePredicateResource:
    """A resource that periodically fetches a predicate from a remote service."""

    def __init__(self, url: str, interval_in_sec: int):
        self._url = url
        self.interval_in_sec = interval_in_sec
        self._current_predicate: Optional[Predicate] = None
        self._etag: Optional[str] = None
        self._update_task: Optional[asyncio.Task] = None

    @classmethod
    async def from_env(cls, interval_in_sec=120) -> RemotePredicateResource:
        url = os.getenv("PREDICATE_SERVICE_URL")
        if not url:
            raise EnvironmentError(
                "PREDICATE_SERVICE_URL environment variable is not set"
            )

        resource = cls(url, interval_in_sec)
        # Initial fetch
        await resource._fetch_predicate()
        # Start background updates
        resource._start_background_task()

        return resource

    async def _fetch_predicate(self) -> None:
        headers = {"If-None-Match": self._etag} if self._etag else {}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self._url}/api/v1/predicate", headers=headers
            ) as response:
                if response.status == 304:  # Not Modified
                    print("Not modified")
                    return

                response.raise_for_status()
                data = await response.text()
                print(data)
                self._current_predicate = Predicate.from_json(data)
                self._etag = response.headers.get("ETag")
                self.log()

    async def _update_loop(self) -> None:
        while True:
            try:
                await asyncio.sleep(self.interval_in_sec)  # Wait for interval
                await self._fetch_predicate()
            except Exception as e:
                logger.error(f"Error updating predicate: {e}")

    def _start_background_task(self) -> None:
        self._update_task = asyncio.create_task(self._update_loop())

    def log(self):
        print(self._current_predicate.evaluate(test_user))

    @property
    def predicate(self) -> Predicate:
        if self._current_predicate is None:
            raise RuntimeError("No predicate has been fetched yet")
        return self._current_predicate
