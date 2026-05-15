"""FastAPI app factory.

`radio` may be None for shell / health-only tests; routes that need a
live Radio guard for that explicitly.
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .radio import protocol
from .radio.state import to_jsonable


class RawRequest(BaseModel):
    frame: str
    timeout_s: float = Field(default=1.0, ge=0.05, le=10.0)


# Whitelisted (field path → (Radio method name, enum class or None)).
# enum class is used to coerce a string `.name` from the WebSocket payload
# back to the actual enum member before calling the verb.
_SET_DISPATCH: dict[str, tuple[str, type | None]] = {
    # Scope
    "scope.span_khz": ("set_span_khz", None),
    "scope.ref_level_db": ("set_ref_level_db", None),
    "scope.mode": ("set_scope_mode", protocol.ScopeMode),
    "scope.speed": ("set_scope_speed", protocol.ScopeSpeed),
    "scope.peak": ("set_scope_peak", protocol.ScopePeak),
    "scope.marker": ("set_scope_marker", None),
    "scope.color": ("set_scope_color", None),
    "scope.af_fft.mode": ("set_af_fft_mode", protocol.AfFftMode),
    # Tuning
    "tuning.vfo_a_hz": ("set_vfo_a_hz", None),
    "tuning.vfo_b_hz": ("set_vfo_b_hz", None),
    "tuning.mode": ("set_mode", protocol.OperatingMode),
    "tuning.band": ("set_band", protocol.Band),
    "tuning.swap_vfo": ("swap_vfo", None),  # no value
    "tuning.split": ("set_split", None),
    "tuning.clar_rx_enabled": ("set_rx_clar", None),
    # RX DSP
    "rx.preamp": ("set_preamp", protocol.Preamp),
    "rx.attenuator": ("set_attenuator", protocol.Attenuator),
    "rx.agc": ("set_agc", protocol.AgcSet),
    "rx.nb_enabled": ("set_nb", None),
    "rx.nb_level": ("set_nb_level", None),
    "rx.nr_enabled": ("set_nr", None),
    "rx.nr_level": ("set_nr_level", None),
    "rx.manual_notch_enabled": ("set_manual_notch", None),
    "rx.manual_notch_freq_hz": ("set_manual_notch_freq_hz", None),
    "rx.auto_notch_enabled": ("set_auto_notch", None),
    "rx.contour_enabled": ("set_contour", None),
    "rx.contour_freq_hz": ("set_contour_freq_hz", None),
    "rx.apf_enabled": ("set_apf", None),
    "rx.apf_freq_hz": ("set_apf_freq_hz", None),
    "rx.if_shift_hz": ("set_if_shift_hz", None),
    "rx.filter_width_index": ("set_filter_width", None),
    # Meters / gain
    "meters.af_gain": ("set_af_gain", None),
    "meters.rf_gain": ("set_rf_gain", None),
}


async def _send_safe(websocket: WebSocket, payload: dict) -> None:
    """Send a JSON payload; swallow connection errors so dead sockets unhook cleanly."""
    try:
        await websocket.send_json(payload)
    except Exception:
        pass


async def _dispatch_set(radio, field: str, value) -> None:
    entry = _SET_DISPATCH.get(field)
    if entry is None:
        raise ValueError(f"unknown field {field!r}")
    method_name, enum_cls = entry
    method = getattr(radio, method_name)
    if method_name == "swap_vfo":
        await method()
        return
    if enum_cls is not None:
        try:
            value = enum_cls[value]
        except (KeyError, TypeError):
            raise ValueError(f"invalid enum value {value!r} for {field}")
    await method(value)


_WEB_DIR = Path(__file__).parent / "web"


def create_app(radio=None, manage_radio_lifecycle: bool = False) -> FastAPI:
    app = FastAPI(title="ft710ctl")
    app.state.radio = radio

    if manage_radio_lifecycle and radio is not None:
        @app.on_event("startup")
        async def _radio_startup() -> None:
            await radio.start()

        @app.on_event("shutdown")
        async def _radio_shutdown() -> None:
            await radio.stop()

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/state")
    async def get_state() -> dict:
        if radio is None:
            raise HTTPException(status_code=503, detail="radio not initialized")
        return to_jsonable(radio.state)

    @app.post("/api/raw")
    async def post_raw(req: RawRequest) -> dict:
        if radio is None:
            raise HTTPException(status_code=503, detail="radio not initialized")
        # Frame validation: ASCII-only, must end with ";".
        try:
            frame_bytes = req.frame.encode("ascii")
        except UnicodeEncodeError:
            raise HTTPException(status_code=400, detail="frame must be ASCII")
        if not frame_bytes.endswith(b";"):
            raise HTTPException(status_code=400, detail="frame must end with ';'")
        try:
            answer = await radio.single_shot(frame_bytes, timeout=req.timeout_s)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail="radio did not respond in time")
        return {"response": answer.decode("ascii", errors="replace")}

    @app.websocket("/ws")
    async def ws(websocket: WebSocket) -> None:
        await websocket.accept()
        if radio is None:
            await websocket.send_json({"op": "error", "reason": "radio not initialized"})
            await websocket.close()
            return
        await websocket.send_json({"op": "snapshot", "state": to_jsonable(radio.state)})
        # Initial port state so the UI can render the banner immediately.
        await websocket.send_json({"op": "port", "state": radio.port_state})

        loop = asyncio.get_event_loop()

        def _on_delta(delta: dict) -> None:
            # Fired from the consumer task. Schedule send on the same loop.
            payload = {
                "op": "patch",
                "field": delta["field"],
                "value": to_jsonable(delta["value"]),
            }
            loop.create_task(_send_safe(websocket, payload))

        def _on_port(state: str) -> None:
            loop.create_task(_send_safe(websocket, {"op": "port", "state": state}))

        radio.subscribe(_on_delta)
        radio.add_port_listener(_on_port)
        try:
            while True:
                msg = await websocket.receive_json()
                op = msg.get("op")
                request_id = msg.get("request_id")
                if op == "set":
                    try:
                        await _dispatch_set(radio, msg["field"], msg.get("value"))
                    except (ValueError, TypeError) as exc:
                        await websocket.send_json(
                            {"op": "error", "reason": str(exc), "request_id": request_id}
                        )
                        continue
                    await websocket.send_json({"op": "ack", "request_id": request_id})
                else:
                    await websocket.send_json(
                        {"op": "error", "reason": f"unknown op {op!r}", "request_id": request_id}
                    )
        except WebSocketDisconnect:
            return
        finally:
            radio.unsubscribe(_on_delta)
            radio.remove_port_listener(_on_port)

    app.mount("/", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")
    return app
