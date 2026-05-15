"""Test double for serial-asyncio.

Records every write. Replies to specific frames with canned answers.
Used by command-layer tests so they never need real hardware.
"""
from __future__ import annotations
import asyncio


class FakeSerial:
    def __init__(self):
        self.writes: list[bytes] = []
        self._response_rules: dict[bytes, bytes] = {}
        self._inbound: asyncio.Queue[bytes] = asyncio.Queue()
        self.is_open = True
        self.raise_on_next_write: Exception | None = None

    def on(self, request: bytes, response: bytes) -> None:
        self._response_rules[request] = response

    async def write(self, data: bytes) -> None:
        if self.raise_on_next_write is not None:
            exc, self.raise_on_next_write = self.raise_on_next_write, None
            raise exc
        self.writes.append(data)
        if data in self._response_rules:
            await self._inbound.put(self._response_rules[data])

    async def push(self, frame: bytes) -> None:
        await self._inbound.put(frame)

    async def read_frame(self) -> bytes:
        return await self._inbound.get()

    def close(self) -> None:
        self.is_open = False
