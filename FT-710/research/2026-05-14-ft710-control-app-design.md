# FT-710 Control App — Design

Date: 2026-05-14
Status: Design, pre-implementation
Authors: jrl@infowest.com (brainstormed with Claude)

## Goal

A purpose-built local web application that exposes the FT-710's CAT command
set, including the Yaesu-specific surfaces (spectrum scope, AESS, parametric
EQ) that generic remote-control software like SimpleHRR does not expose.

V1 is local-first: the app runs on the PC the FT-710 USB cable plugs into,
and the operator uses it from that machine's browser. Remote operation is
covered for now by running the app under a remote-desktop session, so the
v1 architecture does not need to solve internet remote on its own. The
architecture must not foreclose internet remote as a v2.

## Why this exists

SimpleHRR explicitly supports the FT-710 but covers only common-denominator
controls shared with Icom radios. The Yaesu `SS` (spectrum scope) command,
the `AS` (AESS) command, and the parametric EQ menu items are not
addressable through it. Manual spectrum scope control over CAT is the
specific gap that prompted this project.

## Non-goals for v1

- Internet-accessible remote operation (deferred to v2; mitigated by
  remote desktop in the meantime)
- Audio streaming (handled separately by the OS / remote desktop)
- Multi-radio support (FT-710 only)
- Authentication / multi-user (single operator at localhost)
- Logbook, contesting, digital-mode integration (use existing tools)
- CW operating surface (deferred to v2)
- TX shaping surface (deferred to v2)
- Memory channel manager (deferred to v2)

## V1 feature scope

Three control surfaces:

1. **Spectrum scope.** Span, reference level, mode (3DSS center/cursor/fix,
   2D waterfall center/cursor/fix in normal and expanded width variants),
   sweep speed, peak level, color profile, marker on/off, AF-FFT toggle.
   Covers all sub-functions of the `SS` command.
2. **Core tuning.** VFO A/B frequency, mode, band, A/B swap, split, RIT /
   CLAR offset, fine/fast tuning, lock, memory channel select.
3. **RX DSP.** Preamp (IPO / AMP1 / AMP2), attenuator, AGC speed,
   noise blanker on/off + level, DNR on/off + level, manual notch, auto
   notch (DNF), contour, APF, IF shift, IF width.

## Architecture

### Process model

A single Python process owns the serial port and serves an HTTP + WebSocket
API on `localhost`. The browser is the only client.

```
+--------------------------+        +----------------+
| Browser (vanilla JS)     | <----> | FastAPI server | <---> /dev/ttyUSB0
|  HTML/CSS/JS, WebSocket  |  WS    |  + asyncio I/O |       (FT-710 USB)
+--------------------------+        +----------------+
```

The Python process is the single owner of the serial port. Nothing else on
the host should hold the port open while this app is running.

### Why server-side canonical state

The server maintains a typed, in-memory model of the radio's current state.
Browser clients render this state; they never read the radio directly.
This gives us two things:

- **Multi-tab consistency.** Open the UI in two browsers (desktop and
  phone, say) and both stay in sync because both render the same server
  state.
- **AI integration in one place.** The radio's Auto Information feature
  pushes state changes; we consume them once on the server, apply to the
  state model, and broadcast deltas to all connected clients.

### Why raw CAT instead of Hamlib

The whole motivation is exposing Yaesu-specific commands Hamlib does not
model (the `SS` sub-functions in particular). Since we have to talk raw
CAT for the unique features anyway, doing it for everything keeps one
protocol layer and one source of truth (the FT-710 CAT manual).

### Stack

- Python 3.11+
- FastAPI + uvicorn for HTTP and WebSocket
- pyserial-asyncio for the serial port
- Vanilla HTML / CSS / JavaScript on the frontend (no build step,
  no framework)

## Module layout

```
ft710ctl/
  ft710ctl/
    __main__.py        # entry point, argparse, starts uvicorn
    server.py          # FastAPI app, mounts routes and static files
    radio/
      port.py          # asyncio serial wrapper: write queue + line reader
      protocol.py      # CAT frame encode/decode (pure functions)
      commands.py      # ergonomic verbs (set_span_khz, set_ref_level_db)
      state.py         # canonical RadioState dataclass + broadcast channel
    api/
      ws.py            # WebSocket schema and dispatch
      rest.py          # /api/state, /api/raw, /api/debug/unknown, /health
    web/
      index.html
      style.css
      app.js
  tests/
    test_protocol.py   # round-trip tests per command
    test_commands.py   # commands + state with FakeSerial
  pyproject.toml
```

### Module responsibilities

- **`radio/port.py`** is the only module that imports pyserial. Exposes a
  pair of asyncio coroutines: `send_frame(bytes)` and `frames()` (an async
  iterator yielding inbound `;`-terminated frames). Internally runs one
  writer task draining an `asyncio.Queue` and one reader task accumulating
  bytes and splitting on `;`.
- **`radio/protocol.py`** translates the FT-710 CAT manual to Python.
  Pure functions: `encode_set_span(span_khz) -> bytes`,
  `decode(frame_bytes) -> RadioUpdate | UnknownFrame`. No I/O. The unit
  tests live entirely against this module.
- **`radio/commands.py`** wraps protocol + port into a `Radio` class with
  verbs like `await radio.set_span_khz(100)`, `await radio.snapshot()`.
  This is the surface the API layer calls. Validation lives here:
  invalid arguments raise `ValueError` *before* anything hits the wire.
- **`radio/state.py`** holds a `RadioState` dataclass and a broadcast
  channel. When the port reader emits a `RadioUpdate`, state is updated
  and a JSON-Patch-style delta is published to all subscribers.
- **`api/ws.py`** is the WebSocket protocol: messages are JSON
  `{op, field, value}`. Validates field names against a whitelist,
  dispatches to `radio.set_<field>(value)`. Per-client errors return
  only to the originating socket; state deltas broadcast to all.
- **`api/rest.py`** carries:
  - `GET /api/state` — full snapshot for non-WebSocket clients
  - `POST /api/raw` — body is a `;`-terminated CAT frame, response is
    whatever the radio sends within 1 s. Escape hatch for anything the
    UI does not yet wrap.
  - `GET /api/debug/unknown` — recent unparseable frames, ring of 100
  - `GET /health` — port state, last reader-task error, uptime

## Data flow

### Outbound (UI to radio)

1. User adjusts a control. JS sends
   `{"op":"set","field":"scope.span_khz","value":100}` over the WebSocket.
2. `api/ws.py` validates the field against a whitelist, looks up the
   verb, calls `radio.set_span_khz(100)`.
3. `commands.py` validates the argument (legal span values are
   1/2/5/10/20/50/100/200/500/1000 kHz), calls
   `protocol.encode_set_span(100)`, enqueues the resulting `SS0560000;`
   bytes for the writer task.
4. `port.py` writes the bytes with a 20 ms inter-frame gap. We do not
   wait for an ack (set frames do not generate one). We immediately
   enqueue the matching read (`SS05;`) to close the loop.

### Inbound (radio to all clients)

1. `port.py` reader emits each `;`-terminated frame.
2. `protocol.decode(frame)` returns a typed `RadioUpdate` or
   `UnknownFrame`.
3. `state.apply(update)` mutates the canonical state and publishes a
   JSON-Patch delta.
4. Every WebSocket subscriber receives
   `{"op":"patch","field":"scope.span_khz","value":100}`.

### Startup sequence

1. Open serial port (`--port` argument, default `/dev/ttyUSB0`).
2. Send `AI1;` to enable Auto Information push.
3. Send the snapshot batch — one read per tracked field
   (`FA;`, `FB;`, `MD0;`, `SS05;`, `SS04;`, `SS06;`, `PA0;`, `RA0;`,
   `GT0;`, `NB0;`, `NR0;`, `BC0;`, `BP00;`, `IS0;`, `SH0;`, `CO0;`).
4. Once the snapshot completes, start uvicorn.

### Client connect

The server immediately sends the full current state as the first
WebSocket frame. From then on, only deltas. Reconnecting clients get a
fresh full snapshot.

### AI as optimization, not guarantee

Not every command triggers an AI push, and AI clears on radio power-off.
So for every Set we send, we also enqueue the read-back. AI buys us low
latency on physical front-panel changes; the read-back guarantees
correctness either way.

## Error handling and resilience

### Serial port failures

- On write error or read timeout, mark port disconnected and broadcast
  `{"op":"port","state":"disconnected"}`. UI greys out controls.
- Background task retries `open()` every 2 seconds.
- On reconnect, resend the snapshot batch and broadcast
  `{"op":"port","state":"connected"}`.
- The app does not chase `ttyUSB` renumbering. Operator restarts with
  the right `--port` if the kernel reassigns.

### Malformed CAT responses

- Decoders return either a typed update or `UnknownFrame(raw_bytes)`.
- Unknown frames go into a 100-deep ring buffer at
  `/api/debug/unknown` and log at DEBUG.
- Truncated or non-ASCII frames receive the same treatment.
- Nothing here crashes the server or mutates state.

### Command rejection

- The FT-710 silently ignores invalid Set frames.
- `commands.py` validates *before* enqueue. Invalid argument raises
  `ValueError` that the WebSocket layer turns into a per-client
  `{"op":"error","reason":"..."}` reply. No broadcast.

### Concurrent writers

- One asyncio task drains the write queue, so writes serialize by
  construction.
- 20 ms inter-frame gap to be polite to the radio's CAT parser. The
  manual is silent on minimum spacing; community reports suggest the
  radio drops frames under sustained back-to-back writes.

## Testing strategy

Three layers:

1. **Protocol unit tests.** `protocol.py` is pure functions, so a
   round-trip test per command is cheap. One assertion that
   `encode_set_span(100) == b"SS0560000;"`, one that
   `decode(b"SS0560000;") == ScopeSpanUpdate(span_khz=100)`. ~15
   commands in v1 means ~30 tests. Goal: protocol layer is provably
   correct before any UI work.
2. **Command-layer tests with a fake port.** `port.py` accepts a
   serial-like object via injection. Tests inject `FakeSerial`,
   capture writes, replay canned responses. Verifies the integration
   of `commands.py` and `state.py` without hardware.
3. **Manual smoke tests against the real radio.** Pre-release
   checklist:
   - Change span across all 10 legal values, verify radio display
     and read-back.
   - Set reference level to `+00.0`, `-30.0`, `+30.0`, `-15.5`.
   - Switch scope mode across every variant (3DSS center/cursor/fix,
     W/F center/cursor/fix in normal and expanded).
   - Toggle each RX DSP control, verify radio panel and read-back.
   - Open the UI in two browser tabs, change a setting in one,
     confirm the other updates within ~100 ms.

No Selenium tests in v1. The frontend is small enough that smoke
testing plus WebSocket dev tools is enough.

## Delivery plan

Six commits, each independently usable:

1. **Skeleton.** `pyproject.toml`, package layout, README with run
   instructions, dev-environment notes.
2. **Protocol layer + tests.** Full v1 command coverage in
   `protocol.py`. Tests pass. *Milestone: provably correct frames.*
3. **Port + state + commands layer.** `port.py`, `state.py`,
   `commands.py`. Fake-port tests pass.
4. **HTTP + WebSocket API.** `server.py`, `api/ws.py`,
   `api/rest.py`, including `/api/raw`. Verify with `curl` and a
   WebSocket REPL. *Milestone: full backend, no UI.*
5. **Frontend.** Static dashboard with scope, tuning, and RX DSP
   panels. *Milestone: v1 feature complete.*
6. **Resilience polish.** Reconnect logic, unknown-frame ring buffer,
   snapshot-on-startup hardening, error-broadcast formatting.

Each milestone is a clean stopping point.

## Open questions for implementation time

- 20 ms inter-frame gap is a guess. Tighten or loosen based on
  observed behavior under load.
- AI push coverage is empirical. Build a small harness that logs
  which `Set` operations produce AI pushes vs. require explicit
  read-back. Inform future timing/heuristics.
- WebSocket reconnect strategy on the client: simple fixed-interval
  retry vs. exponential backoff. Probably doesn't matter for
  localhost; revisit when v2 introduces network remote.

## Out of scope for this doc

The matching implementation plan (the step-by-step build checklist
with verification commands) will be written with
`superpowers:writing-plans` against this design before implementation
starts.
