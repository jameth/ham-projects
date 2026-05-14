# ft710ctl

Local web control panel for the Yaesu FT-710 transceiver.

## Quick start

    python -m venv .venv
    . .venv/bin/activate
    pip install -e ".[dev]"
    ft710ctl --port /dev/ttyUSB0

Open http://localhost:8710/ in a browser.

See `../research/2026-05-14-ft710-control-app-design.md` for design.
