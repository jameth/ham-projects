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

    async def set_ref_level_db(self, db: float) -> None:
        frame = protocol.encode_set_ref_level_db(db)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_ref_level())

    async def set_scope_mode(self, mode: protocol.ScopeMode) -> None:
        _require_enum(mode, protocol.ScopeMode)
        await self.port.send(protocol.encode_set_scope_mode(mode))
        await self.port.send(protocol.encode_read_scope_mode())

    async def set_scope_speed(self, speed: protocol.ScopeSpeed) -> None:
        _require_enum(speed, protocol.ScopeSpeed)
        await self.port.send(protocol.encode_set_scope_speed(speed))
        await self.port.send(b"SS00;")

    async def set_scope_peak(self, peak: protocol.ScopePeak) -> None:
        _require_enum(peak, protocol.ScopePeak)
        await self.port.send(protocol.encode_set_scope_peak(peak))
        await self.port.send(b"SS01;")

    async def set_scope_marker(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_scope_marker(enabled))
        await self.port.send(b"SS02;")

    async def set_scope_color(self, color: int) -> None:
        frame = protocol.encode_set_scope_color(color)
        await self.port.send(frame)
        await self.port.send(b"SS03;")

    async def set_af_fft_mode(
        self, mode: protocol.AfFftMode, osc_time_index: int = 0
    ) -> None:
        _require_enum(mode, protocol.AfFftMode)
        await self.port.send(
            protocol.encode_set_af_fft_mode(mode, osc_time_index=osc_time_index)
        )
        await self.port.send(protocol.encode_read_af_fft())


def _require_enum(value, cls) -> None:
    if not isinstance(value, cls):
        raise TypeError(f"expected {cls.__name__}, got {type(value).__name__}")
