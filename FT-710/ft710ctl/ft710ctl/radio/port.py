"""Asyncio wrapper around the serial port with explicit lifecycle."""
from __future__ import annotations

import asyncio
from typing import Callable, Protocol


WRITE_GAP_S = 0.020  # 20 ms between writes


class PortClosed(Exception):
    """Raised by send() or pending next_frame() when the port is closed."""


class SerialLike(Protocol):
    async def write(self, data: bytes) -> None: ...
    async def read_frame(self) -> bytes: ...
    def close(self) -> None: ...


# Sentinel pushed into the inbound queue on close() to wake pending readers.
_CLOSE_SENTINEL: object = object()


class RadioPort:
    def __init__(
        self,
        factory: Callable[[], SerialLike],
        write_gap_s: float = WRITE_GAP_S,
        on_fault: Callable[[Exception], None] | None = None,
    ):
        self._factory = factory
        self._write_gap_s = write_gap_s
        self._on_fault = on_fault
        self._serial: SerialLike | None = None
        self._outbound: asyncio.Queue[bytes] = asyncio.Queue()
        self._inbound: asyncio.Queue = asyncio.Queue()
        self._writer_task: asyncio.Task | None = None
        self._reader_task: asyncio.Task | None = None
        self._open: bool = False

    async def open(self) -> None:
        if self._open:
            raise RuntimeError("port already open")
        self._serial = self._factory()
        self._outbound = asyncio.Queue()
        self._inbound = asyncio.Queue()
        self._open = True
        self._writer_task = asyncio.create_task(self._writer())
        self._reader_task = asyncio.create_task(self._reader())

    async def close(self) -> None:
        if not self._open:
            return
        self._open = False
        # Wake any consumer parked in next_frame().
        await self._inbound.put(_CLOSE_SENTINEL)
        for t in (self._writer_task, self._reader_task):
            if t is None:
                continue
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass
        if self._serial is not None:
            self._serial.close()
        self._serial = None
        self._writer_task = None
        self._reader_task = None

    async def reopen(self) -> None:
        await self.close()
        await self.open()

    async def send(self, frame: bytes) -> None:
        if not self._open:
            raise PortClosed("port is closed")
        await self._outbound.put(frame)

    async def next_frame(self) -> bytes:
        item = await self._inbound.get()
        if item is _CLOSE_SENTINEL:
            # Re-arm sentinel for any other waiters, then raise.
            await self._inbound.put(_CLOSE_SENTINEL)
            raise PortClosed("port closed while waiting for frame")
        return item

    async def _writer(self) -> None:
        assert self._serial is not None
        try:
            while True:
                frame = await self._outbound.get()
                await self._serial.write(frame)
                if self._write_gap_s > 0:
                    await asyncio.sleep(self._write_gap_s)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if self._on_fault is not None:
                self._on_fault(exc)

    async def _reader(self) -> None:
        assert self._serial is not None
        try:
            while True:
                frame = await self._serial.read_frame()
                await self._inbound.put(frame)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if self._on_fault is not None:
                self._on_fault(exc)
