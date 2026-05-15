"""FastAPI app factory.

`radio` may be None for shell / health-only tests; routes that need a
live Radio guard for that explicitly.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .radio.state import to_jsonable


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

    app.mount("/", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")
    return app
