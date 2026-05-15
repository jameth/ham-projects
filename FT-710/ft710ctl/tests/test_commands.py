import asyncio

import pytest

from ft710ctl.radio.commands import Radio
from tests.fake_serial import FakeSerial


async def test_set_span_writes_and_reads_back():
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_span_khz(100)
    await asyncio.sleep(0.05)
    assert radio.state.scope.span_khz == 100
    await radio.stop()


async def test_set_span_invalid_raises_before_sending():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_span_khz(3)
    assert fs.writes == []  # validation happens pre-wire
    await radio.stop()


async def test_stop_awaits_consumer_cleanup():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.stop()
    assert radio._consumer.done()
