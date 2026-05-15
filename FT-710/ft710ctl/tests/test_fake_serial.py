import pytest

from tests.fake_serial import FakeSerial


async def test_records_writes():
    fs = FakeSerial()
    await fs.write(b"SS05;")
    assert fs.writes == [b"SS05;"]


async def test_canned_response():
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    await fs.write(b"SS05;")
    assert await fs.read_frame() == b"SS0560000;"


async def test_raises_on_demand():
    fs = FakeSerial()
    fs.raise_on_next_write = IOError("simulated")
    with pytest.raises(IOError):
        await fs.write(b"SS05;")
    # Subsequent writes succeed
    await fs.write(b"FA;")
    assert fs.writes == [b"FA;"]
