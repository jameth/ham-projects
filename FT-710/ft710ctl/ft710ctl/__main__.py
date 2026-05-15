"""Entry point: parse args, build serial factory, run uvicorn."""
from __future__ import annotations

import argparse
import asyncio
import logging

import uvicorn

from .radio.commands import Radio
from .server import create_app


class _DeadFakeSerial:
    """SerialLike that never produces frames. Used by --no-radio for frontend dev."""

    def __init__(self):
        self._inbound: asyncio.Queue[bytes] = asyncio.Queue()
        self.is_open = True

    async def write(self, data: bytes) -> None:
        # Drop writes silently; no answers will arrive.
        return

    async def read_frame(self) -> bytes:
        # Block forever; nothing is coming.
        return await self._inbound.get()

    def close(self) -> None:
        self.is_open = False


def _make_dead_factory():
    return _DeadFakeSerial


def _make_serial_factory(device: str, baud: int):
    """Build a SerialLike factory backed by pyserial-asyncio."""
    import serial_asyncio  # imported lazily so unit tests don't need it

    class _AsyncSerial:
        def __init__(self):
            self._transport = None
            self._protocol = None
            self._reader: asyncio.StreamReader | None = None
            self._writer: asyncio.StreamWriter | None = None
            self._inbound: asyncio.Queue[bytes] = asyncio.Queue()
            self._reader_task: asyncio.Task | None = None

        async def _ensure_open(self) -> None:
            if self._writer is not None:
                return
            reader, writer = await serial_asyncio.open_serial_connection(
                url=device, baudrate=baud
            )
            self._reader = reader
            self._writer = writer
            self._reader_task = asyncio.create_task(self._read_loop())

        async def _read_loop(self) -> None:
            assert self._reader is not None
            buf = bytearray()
            while True:
                chunk = await self._reader.read(64)
                if not chunk:
                    return
                for b in chunk:
                    buf.append(b)
                    if b == ord(";"):
                        await self._inbound.put(bytes(buf))
                        buf = bytearray()

        async def write(self, data: bytes) -> None:
            await self._ensure_open()
            assert self._writer is not None
            self._writer.write(data)
            await self._writer.drain()

        async def read_frame(self) -> bytes:
            await self._ensure_open()
            return await self._inbound.get()

        def close(self) -> None:
            if self._reader_task is not None:
                self._reader_task.cancel()
            if self._writer is not None:
                self._writer.close()

    return _AsyncSerial


def main() -> None:
    parser = argparse.ArgumentParser(prog="ft710ctl")
    parser.add_argument(
        "--port",
        help="serial device, e.g. /dev/ttyUSB0 (required unless --no-radio)",
    )
    parser.add_argument("--baud", type=int, default=38400)
    parser.add_argument("--http-port", type=int, default=8710)
    parser.add_argument(
        "--no-radio",
        action="store_true",
        help="run with a stub serial that never replies (for frontend development)",
    )
    args = parser.parse_args()

    if not args.no_radio and not args.port:
        parser.error("--port is required (or pass --no-radio for frontend dev)")

    logging.basicConfig(level=logging.INFO)

    factory = _make_dead_factory() if args.no_radio else _make_serial_factory(args.port, args.baud)
    radio = Radio(factory=factory)
    on_startup = None if args.no_radio else radio.snapshot
    app = create_app(radio=radio, manage_radio_lifecycle=True, on_startup=on_startup)

    uvicorn.run(app, host="127.0.0.1", port=args.http_port, log_level="info")


if __name__ == "__main__":
    main()
