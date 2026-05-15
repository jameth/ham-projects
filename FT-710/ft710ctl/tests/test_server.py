from types import SimpleNamespace

from fastapi.testclient import TestClient

from ft710ctl.radio.state import RadioState
from ft710ctl.server import create_app


def _stub_radio() -> SimpleNamespace:
    return SimpleNamespace(state=RadioState())


def test_health():
    app = create_app(radio=None)
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_api_state_initial():
    radio = _stub_radio()
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.get("/api/state")
    assert r.status_code == 200
    body = r.json()
    assert "scope" in body and "tuning" in body and "rx" in body and "meters" in body


def test_api_state_serializes_enums_as_names():
    from ft710ctl.radio import protocol
    radio = _stub_radio()
    radio.state.scope.mode = protocol.ScopeMode.WF_CENTER_NORMAL
    app = create_app(radio=radio)
    client = TestClient(app)
    body = client.get("/api/state").json()
    assert body["scope"]["mode"] == "WF_CENTER_NORMAL"


def test_ws_initial_state():
    radio = _stub_radio()
    app = create_app(radio=radio)
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        first = ws.receive_json()
        assert first["op"] == "snapshot"
        assert "state" in first
        assert "scope" in first["state"]


# ---------- /api/raw ----------


import asyncio  # noqa: E402

import httpx  # noqa: E402

from ft710ctl.radio.commands import Radio  # noqa: E402
from tests.fake_serial import FakeSerial  # noqa: E402


def _async_client(app):
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    )


async def test_api_raw_returns_response():
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    app = create_app(radio=radio)
    async with _async_client(app) as ac:
        r = await ac.post("/api/raw", json={"frame": "SS05;"})
    await radio.stop()
    assert r.status_code == 200
    assert r.json() == {"response": "SS0560000;"}


async def test_api_raw_waits_for_quiescence():
    """A raw request issued while a read is in flight waits for it to settle."""
    fs = FakeSerial()
    fs.on(b"FA;", b"FA014250000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    radio._outstanding_reads = 1
    raw_task = asyncio.create_task(radio.single_shot(b"FA;", timeout=1.0))
    await asyncio.sleep(0.05)
    assert not raw_task.done()  # blocked on quiescence
    radio._outstanding_reads = 0
    result = await asyncio.wait_for(raw_task, timeout=1.0)
    await radio.stop()
    assert result == b"FA014250000;"


async def test_api_raw_rejects_non_ascii():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    app = create_app(radio=radio)
    async with _async_client(app) as ac:
        r = await ac.post("/api/raw", json={"frame": "ÿ;"})
    await radio.stop()
    assert r.status_code == 400


async def test_api_raw_rejects_missing_terminator():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    app = create_app(radio=radio)
    async with _async_client(app) as ac:
        r = await ac.post("/api/raw", json={"frame": "SS05"})
    await radio.stop()
    assert r.status_code == 400


async def test_api_raw_timeout_returns_408():
    fs = FakeSerial()  # no canned response → no reply
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    app = create_app(radio=radio)
    async with _async_client(app) as ac:
        r = await ac.post("/api/raw", json={"frame": "SS05;", "timeout_s": 0.1})
    await radio.stop()
    assert r.status_code == 408
