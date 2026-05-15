"""High-level radio command wrapper.

Wires the protocol layer to the port and canonical state. Public verbs
(`set_*`, `snapshot`) are the only API the server layer touches.
"""
from __future__ import annotations

import asyncio
from typing import Callable

from . import protocol, state
from .port import PortClosed, RadioPort


class Radio:
    def __init__(self, factory, write_gap_s: float | None = None):
        kwargs = {"write_gap_s": write_gap_s} if write_gap_s is not None else {}
        self.port = RadioPort(factory=factory, **kwargs)
        self.state = state.RadioState()
        self._consumer: asyncio.Task | None = None
        self._subscribers: list[Callable[[dict], None]] = []

    async def start(self) -> None:
        await self.port.open()
        self._consumer = asyncio.create_task(self._consume_frames())

    async def stop(self) -> None:
        if self._consumer is not None:
            self._consumer.cancel()
            try:
                await self._consumer
            except asyncio.CancelledError:
                pass
        await self.port.close()

    def subscribe(self, callback: Callable[[dict], None]) -> None:
        self._subscribers.append(callback)

    async def _consume_frames(self) -> None:
        while True:
            try:
                frame = await self.port.next_frame()
            except PortClosed:
                return
            update = protocol.decode(frame)
            delta = self.state.apply(update)
            if delta is not None:
                for cb in list(self._subscribers):
                    try:
                        cb(delta)
                    except Exception:
                        pass

    async def set_span_khz(self, khz: int) -> None:
        frame = protocol.encode_set_span_khz(khz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_span())
