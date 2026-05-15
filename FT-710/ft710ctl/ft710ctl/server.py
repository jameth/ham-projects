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

from .radio.state import to_jsonable


class RawRequest(BaseModel):
    frame: str
    timeout_s: float = Field(default=1.0, ge=0.05, le=10.0)


_WEB_DIR = Path(__file__).parent / "web"


def create_app(radio=None) -> FastAPI:
    app = FastAPI(title="ft710ctl")
    app.state.radio = radio

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
        try:
            while True:
                # Phase 4 follow-up tasks fill in set / patch / port handling.
                await websocket.receive_text()
        except WebSocketDisconnect:
            return

    app.mount("/", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")
    return app
