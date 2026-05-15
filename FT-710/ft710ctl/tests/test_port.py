import asyncio

import pytest

from ft710ctl.radio.port import PortClosed, RadioPort
from tests.fake_serial import FakeSerial


async def test_open_and_send_receive():
    fs = FakeSerial()
    fs.on(b"FA;", b"FA014250000;")
    port = RadioPort(factory=lambda: fs, write_gap_s=0)
    await port.open()
    await port.send(b"FA;")
    frame = await asyncio.wait_for(port.next_frame(), timeout=1.0)
    assert frame == b"FA014250000;"
    await port.close()


async def test_close_awaits_task_cleanup():
    fs = FakeSerial()
    port = RadioPort(factory=lambda: fs, write_gap_s=0)
    await port.open()
    # Capture task references *before* close() nulls them.
    writer = port._writer_task
    reader = port._reader_task
    await port.close()
    assert writer.done()
    assert reader.done()
    assert port._writer_task is None
    assert port._reader_task is None


async def test_reopen_pulls_fresh_serial():
    fs1 = FakeSerial()
    fs2 = FakeSerial()
    serials = iter([fs1, fs2])
    port = RadioPort(factory=lambda: next(serials), write_gap_s=0)
    await port.open()
    await port.reopen()  # closes fs1, opens fs2
    await port.send(b"FA;")
    await asyncio.sleep(0.05)
    assert fs2.writes == [b"FA;"]
    assert fs1.writes == []
    await port.close()


async def test_send_after_close_raises():
    fs = FakeSerial()
    port = RadioPort(factory=lambda: fs, write_gap_s=0)
    await port.open()
    await port.close()
    with pytest.raises(PortClosed):
        await port.send(b"FA;")


async def test_pending_next_frame_resolves_on_close():
    """A consumer awaiting next_frame() must not block forever after close()."""
    fs = FakeSerial()
    port = RadioPort(factory=lambda: fs, write_gap_s=0)
    await port.open()
    pending = asyncio.create_task(port.next_frame())
    await asyncio.sleep(0)  # let the task park
    await port.close()
    with pytest.raises(PortClosed):
        await asyncio.wait_for(pending, timeout=1.0)
