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
