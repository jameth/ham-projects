# FT-710 Control App Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python web app at `FT-710/ft710ctl/` that exposes the FT-710's Yaesu-specific CAT command set (spectrum scope, tuning, RX DSP, S-meter, gain) through a localhost browser dashboard.

**Architecture:** FastAPI process owns the serial port via a `RadioPort` with explicit open/close/reopen lifecycle. Maintains canonical radio state. Serves HTTP + WebSocket on localhost. Vanilla JS browser client renders state and sends set commands. State sync via explicit read-back-after-set (Auto Information is **disabled** in v1 for determinism).

**Tech Stack:** Python 3.11+, FastAPI, uvicorn, pyserial-asyncio, pytest, vanilla HTML/CSS/JS.

**Design doc:** `FT-710/research/2026-05-14-ft710-control-app-design.md`

**Project root:** `FT-710/ft710ctl/` (created in Task 1).

## Revision notes (incorporates two review passes, 2026-05-14)

### v3 (second Codex pass on gpt-5.4 high)

- Task 19 `CF` byte order corrected: RX CLAR ON is `CF00010000;` (P4=1, P5=0). The v2 plan had P4/P5 swapped.
- Task 13 adds `BP01;` manual-notch frequency read (was missing).
- Task 15 adds `SS07` AF-FFT / oscilloscope sub-function (was missing).
- Task 22 `RadioPort` now actually defines `reopen()`, plus a `PortClosed` exception. `send()` raises on closed port; `next_frame()` resolves with `PortClosed` instead of blocking forever. Close-cleanup test rewritten to capture task references before close.
- Task 25 invalid-argument rule explicitly tiered by verb shape (range / enum / boolean / no-arg).
- Task 26 snapshot batch adds `SS07;`, `BP01;`.
- Task 30 `/api/raw` redesigned around quiescence + drain (was: arm-next-frame, which could capture unrelated traffic).
- Task 34 actually includes the dispatcher-fallthrough test.
- Task 11 `AGC_REPORT_CASES` corrected — no plain "AUTO" on the Answer side (manual p.13 maps Answer 4/5/6 to AUTO-FAST/MID/SLOW only).

### v2 (first review pass: Codex default + Gemini)

- Five protocol-byte errors fixed against CAT manual: `GT` Set range (Task 11), `RL` frame shape (Task 12), `CO` P2 semantics + page citation (Task 13), `IS` frame shape (Task 14), `SH` frame shape (Task 14).
- AI push **disabled** in v1 — no `AI1;` on startup. Explicit read-back is the single source of state truth. Eliminates duplicate-frame race. Revisit in v2.
- Snapshot batch (Task 27) now covers every v1 read with correct frame shapes (notably `CO0P2;` per sub-function for contour/APF).
- New v1 commands: `SM` (S-meter), `AG` (AF gain), `RG` (RF gain), `BS` (band select), `SV` (swap VFO), `ST` (split), `CF` (CLAR on/off). Tunes Task 30's tuning panel scope.
- `RadioPort` now takes a connection factory and exposes `open() / close() / reopen()` so Task 40 reconnect is implementable.
- `/api/raw` (Task 30) gets explicit single-shot port reservation to avoid frame stealing.
- `stop()` semantics in Tasks 23 and 26 now `await` cancellation cleanly.
- TDD discipline made explicit for every protocol task (no more "Same TDD pattern").
- Task 26 (verb expansion) now requires invalid-argument coverage per verb.
- Task 34 (`/api/debug/unknown`) explicitly requires a dispatcher-fallthrough test.

Tasks renumbered for the inserted tasks. Mapping from v1 numbering at the bottom.

---

## Phase 1 — Skeleton

### Task 1: Create project skeleton

**Files:**
- Create: `FT-710/ft710ctl/pyproject.toml`
- Create: `FT-710/ft710ctl/.gitignore`
- Create: `FT-710/ft710ctl/ft710ctl/__init__.py`
- Create: `FT-710/ft710ctl/tests/__init__.py`
- Create: `FT-710/ft710ctl/README.md`

**Step 1: Create `pyproject.toml`**

```toml
[project]
name = "ft710ctl"
version = "0.1.0"
description = "Local web control panel for the Yaesu FT-710"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]>=0.27",
    "pyserial-asyncio>=0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.27",
]

[project.scripts]
ft710ctl = "ft710ctl.__main__:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 2: Create `.gitignore`**

```
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
*.egg-info/
dist/
build/
```

**Step 3: Create empty package files**

`ft710ctl/__init__.py` and `tests/__init__.py`: empty files.

**Step 4: Create `README.md`**

```markdown
# ft710ctl

Local web control panel for the Yaesu FT-710 transceiver.

## Quick start

    python -m venv .venv
    . .venv/bin/activate
    pip install -e ".[dev]"
    ft710ctl --port /dev/ttyUSB0

Open http://localhost:8710/ in a browser.

See `../research/2026-05-14-ft710-control-app-design.md` for design.
```

**Step 5: Initialize venv and verify install**

```bash
cd FT-710/ft710ctl
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

Expected: clean install, no errors.

**Step 6: Commit**

```bash
git add FT-710/ft710ctl/pyproject.toml FT-710/ft710ctl/.gitignore \
        FT-710/ft710ctl/ft710ctl/__init__.py FT-710/ft710ctl/tests/__init__.py \
        FT-710/ft710ctl/README.md
git commit -m "ft710ctl: project skeleton"
```

---

### Task 2: Pytest baseline runs green with zero tests

**Files:** Create `FT-710/ft710ctl/tests/test_smoke.py`

**Step 1: Smoke test**

```python
def test_smoke():
    assert True
```

**Step 2: Run pytest**

```bash
cd FT-710/ft710ctl && pytest -v
```

Expected: `1 passed`.

**Step 3: Commit**

```bash
git add FT-710/ft710ctl/tests/test_smoke.py
git commit -m "ft710ctl: pytest baseline"
```

---

## Phase 2 — Protocol layer

**Every task in this phase runs the full five-step TDD cycle:**

1. Write the failing test(s).
2. Run pytest, confirm they fail with the expected error (ImportError or AttributeError on the new symbols).
3. Implement the minimal code to make them pass.
4. Run pytest, confirm green.
5. Commit.

Tasks below show the failing-test block in full. Where the implementation is mechanically similar to earlier tasks, steps 2–5 are abbreviated as "Standard TDD cycle" — that abbreviation means *run all five steps in order*, not "batch them together." Do not commit code that hasn't been through a red phase.

### Task 3: Protocol module skeleton + UnknownFrame

**Files:**
- Create: `FT-710/ft710ctl/ft710ctl/radio/__init__.py`
- Create: `FT-710/ft710ctl/ft710ctl/radio/protocol.py`
- Create: `FT-710/ft710ctl/tests/test_protocol.py`

**Step 1: Failing test**

```python
from ft710ctl.radio import protocol

def test_decode_unknown_frame():
    result = protocol.decode(b"XX0;")
    assert isinstance(result, protocol.UnknownFrame)
    assert result.raw == b"XX0;"
```

**Step 2: Run, see fail.** Expected: ImportError.

**Step 3: Implement**

`radio/__init__.py`: empty. `radio/protocol.py`:

```python
"""FT-710 CAT protocol: pure encode/decode functions.

Every encoder returns bytes ending in b";".
Every decoder returns either a typed update or UnknownFrame.
The FT-710 CAT Operation Reference Manual is the ground truth.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class UnknownFrame:
    raw: bytes


RadioUpdate = Union["UnknownFrame"]  # widened as decoders are added


def decode(frame: bytes) -> RadioUpdate:
    return UnknownFrame(raw=frame)
```

**Step 4: Run, see pass.**

**Step 5: Commit.** `git commit -am "ft710ctl: protocol skeleton with UnknownFrame"`.

---

### Task 4: SS span encode + decode

**Manual ref:** CAT manual p.21, `SS` command, P2=5.

**Step 1: Failing tests**

```python
import pytest

SPAN_CASES = [
    (1, b"SS0500000;"), (2, b"SS0510000;"), (5, b"SS0520000;"),
    (10, b"SS0530000;"), (20, b"SS0540000;"), (50, b"SS0550000;"),
    (100, b"SS0560000;"), (200, b"SS0570000;"), (500, b"SS0580000;"),
    (1000, b"SS0590000;"),
]

@pytest.mark.parametrize("khz,frame", SPAN_CASES)
def test_encode_set_span(khz, frame):
    assert protocol.encode_set_span_khz(khz) == frame

@pytest.mark.parametrize("khz,frame", SPAN_CASES)
def test_decode_span(khz, frame):
    assert protocol.decode(frame) == protocol.ScopeSpanUpdate(span_khz=khz)

def test_encode_set_span_rejects_invalid():
    with pytest.raises(ValueError):
        protocol.encode_set_span_khz(3)

def test_encode_read_span():
    assert protocol.encode_read_span() == b"SS05;"
```

**Step 2: Run, see fail.**

**Step 3: Implement**

```python
RadioUpdate = Union["ScopeSpanUpdate", "UnknownFrame"]

@dataclass(frozen=True)
class ScopeSpanUpdate:
    span_khz: int

_SPAN_KHZ_BY_DIGIT = {
    "0": 1, "1": 2, "2": 5, "3": 10, "4": 20,
    "5": 50, "6": 100, "7": 200, "8": 500, "9": 1000,
}
_SPAN_DIGIT_BY_KHZ = {v: k for k, v in _SPAN_KHZ_BY_DIGIT.items()}

def encode_set_span_khz(khz: int) -> bytes:
    if khz not in _SPAN_DIGIT_BY_KHZ:
        raise ValueError(f"invalid span {khz} kHz; legal: {sorted(_SPAN_DIGIT_BY_KHZ)}")
    return f"SS05{_SPAN_DIGIT_BY_KHZ[khz]}0000;".encode("ascii")

def encode_read_span() -> bytes:
    return b"SS05;"
```

Add `SS05` branch to `decode`.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: SS span encode/decode"`.

---

### Task 5: SS reference level encode + decode

**Manual ref:** p.21, `SS` P2=4. Range -30.0 to +30.0 dB in 0.5 dB steps. Set frame: `SS04±NN.N;` (10 bytes).

**Step 1: Failing tests**

```python
LEVEL_CASES = [
    (0.0, b"SS04+00.0;"),
    (-30.0, b"SS04-30.0;"),
    (30.0, b"SS04+30.0;"),
    (-5.5, b"SS04-05.5;"),
    (10.5, b"SS04+10.5;"),
]

@pytest.mark.parametrize("db,frame", LEVEL_CASES)
def test_encode_set_ref_level(db, frame):
    assert protocol.encode_set_ref_level_db(db) == frame

@pytest.mark.parametrize("db,frame", LEVEL_CASES)
def test_decode_ref_level(db, frame):
    assert protocol.decode(frame) == protocol.ScopeRefLevelUpdate(level_db=db)

def test_encode_set_ref_level_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_ref_level_db(31.0)
    with pytest.raises(ValueError):
        protocol.encode_set_ref_level_db(-30.5)

def test_encode_set_ref_level_rejects_non_half_step():
    with pytest.raises(ValueError):
        protocol.encode_set_ref_level_db(5.3)

def test_encode_read_ref_level():
    assert protocol.encode_read_ref_level() == b"SS04;"
```

**Step 2: Run, see fail.**

**Step 3: Implement**

```python
@dataclass(frozen=True)
class ScopeRefLevelUpdate:
    level_db: float

def encode_set_ref_level_db(db: float) -> bytes:
    if not (-30.0 <= db <= 30.0):
        raise ValueError(f"ref level {db} dB out of range -30.0..+30.0")
    if abs(round(db * 2) - db * 2) > 1e-9:
        raise ValueError(f"ref level {db} dB not on 0.5 dB grid")
    sign = "+" if db >= 0 else "-"
    mag = abs(db)
    tens = int(mag) // 10
    ones = int(mag) % 10
    tenths = int(round((mag - int(mag)) * 10))
    return f"SS04{sign}{tens}{ones}.{tenths};".encode("ascii")

def encode_read_ref_level() -> bytes:
    return b"SS04;"
```

Extend `decode` to parse `SS04±NN.N;`.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: SS reference level encode/decode"`.

---

### Task 6: SS scope mode encode + decode

**Manual ref:** p.21, `SS` P2=6.

**Step 1: Failing tests**

```python
from enum import Enum

SCOPE_MODE_CASES = [
    ("DSS_CENTER", b"SS0600000;"),
    ("DSS_CURSOR", b"SS0610000;"),
    ("DSS_FIX", b"SS0620000;"),
    ("WF_CENTER_EXPAND", b"SS0630000;"),
    ("WF_CENTER_NORMAL", b"SS0640000;"),
    ("WF_CURSOR_EXPAND", b"SS0660000;"),
    ("WF_CURSOR_NORMAL", b"SS0670000;"),
    ("WF_FIX_EXPAND", b"SS0690000;"),
    ("WF_FIX_NORMAL", b"SS06A0000;"),
]

@pytest.mark.parametrize("name,frame", SCOPE_MODE_CASES)
def test_encode_set_scope_mode(name, frame):
    mode = protocol.ScopeMode[name]
    assert protocol.encode_set_scope_mode(mode) == frame

@pytest.mark.parametrize("name,frame", SCOPE_MODE_CASES)
def test_decode_scope_mode(name, frame):
    mode = protocol.ScopeMode[name]
    assert protocol.decode(frame) == protocol.ScopeModeUpdate(mode=mode)

def test_encode_read_scope_mode():
    assert protocol.encode_read_scope_mode() == b"SS06;"
```

**Step 2: Run, see fail.**

**Step 3: Implement**

```python
class ScopeMode(Enum):
    DSS_CENTER = "0"
    DSS_CURSOR = "1"
    DSS_FIX = "2"
    WF_CENTER_EXPAND = "3"
    WF_CENTER_NORMAL = "4"
    WF_CURSOR_EXPAND = "6"
    WF_CURSOR_NORMAL = "7"
    WF_FIX_EXPAND = "9"
    WF_FIX_NORMAL = "A"

@dataclass(frozen=True)
class ScopeModeUpdate:
    mode: ScopeMode

def encode_set_scope_mode(mode: ScopeMode) -> bytes:
    return f"SS06{mode.value}0000;".encode("ascii")

def encode_read_scope_mode() -> bytes:
    return b"SS06;"
```

Extend `decode` for `SS06`.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: SS scope mode encode/decode"`.

---

### Task 7: VFO frequency (FA, FB)

**Manual ref:** p.13, `FA` and `FB`. 9-digit Hz, zero-padded. Range 30 kHz–75 MHz.

**Step 1: Failing tests**

```python
def test_encode_set_vfo_a_hz():
    assert protocol.encode_set_vfo_a_hz(14_250_000) == b"FA014250000;"

def test_encode_set_vfo_b_hz():
    assert protocol.encode_set_vfo_b_hz(7_074_000) == b"FB007074000;"

def test_decode_vfo_a():
    assert protocol.decode(b"FA014250000;") == protocol.VfoFreqUpdate(vfo="A", hz=14_250_000)

def test_decode_vfo_b():
    assert protocol.decode(b"FB007074000;") == protocol.VfoFreqUpdate(vfo="B", hz=7_074_000)

def test_encode_set_vfo_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_vfo_a_hz(20_000)
    with pytest.raises(ValueError):
        protocol.encode_set_vfo_a_hz(80_000_000)

def test_encode_read_vfo_a():
    assert protocol.encode_read_vfo_a() == b"FA;"

def test_encode_read_vfo_b():
    assert protocol.encode_read_vfo_b() == b"FB;"
```

**Step 2: Run, see fail.**

**Step 3: Implement**

```python
@dataclass(frozen=True)
class VfoFreqUpdate:
    vfo: str
    hz: int

def _encode_set_vfo(prefix: str, hz: int) -> bytes:
    if not (30_000 <= hz <= 75_000_000):
        raise ValueError(f"frequency {hz} Hz out of range 30 kHz..75 MHz")
    return f"{prefix}{hz:09d};".encode("ascii")

def encode_set_vfo_a_hz(hz: int) -> bytes:
    return _encode_set_vfo("FA", hz)

def encode_set_vfo_b_hz(hz: int) -> bytes:
    return _encode_set_vfo("FB", hz)

def encode_read_vfo_a() -> bytes:
    return b"FA;"

def encode_read_vfo_b() -> bytes:
    return b"FB;"
```

Extend `decode` for `FA`/`FB`.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: VFO frequency encode/decode"`.

---

### Task 8: Operating mode (MD)

**Manual ref:** p.15, `MD`. Set form: `MD0<digit>;`. Read: `MD0;`.

**Step 1: Failing tests**

```python
MODE_CASES = [
    ("LSB", "1"), ("USB", "2"), ("CW_U", "3"), ("FM", "4"), ("AM", "5"),
    ("RTTY_L", "6"), ("CW_L", "7"), ("DATA_L", "8"), ("RTTY_U", "9"),
    ("DATA_FM", "A"), ("FM_N", "B"), ("DATA_U", "C"), ("AM_N", "D"),
    ("PSK", "E"), ("DATA_FM_N", "F"),
]

@pytest.mark.parametrize("name,digit", MODE_CASES)
def test_encode_set_mode(name, digit):
    mode = protocol.OperatingMode[name]
    assert protocol.encode_set_mode(mode) == f"MD0{digit};".encode("ascii")

@pytest.mark.parametrize("name,digit", MODE_CASES)
def test_decode_mode(name, digit):
    mode = protocol.OperatingMode[name]
    assert protocol.decode(f"MD0{digit};".encode("ascii")) == protocol.ModeUpdate(mode=mode)

def test_encode_read_mode():
    assert protocol.encode_read_mode() == b"MD0;"
```

**Step 2: Run, see fail.**

**Step 3: Implement** `OperatingMode` enum + `ModeUpdate` dataclass + encode/read functions + `decode` branch.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: operating mode encode/decode"`.

---

### Task 9: Preamp (PA)

**Manual ref:** p.17, `PA`. Set: `PA0<digit>;`. P2: 0=IPO, 1=AMP1, 2=AMP2. Read: `PA0;`.

**Step 1: Failing tests**

```python
PREAMP_CASES = [
    ("IPO", "0"), ("AMP1", "1"), ("AMP2", "2"),
]

@pytest.mark.parametrize("name,digit", PREAMP_CASES)
def test_encode_set_preamp(name, digit):
    setting = protocol.Preamp[name]
    assert protocol.encode_set_preamp(setting) == f"PA0{digit};".encode("ascii")

@pytest.mark.parametrize("name,digit", PREAMP_CASES)
def test_decode_preamp(name, digit):
    setting = protocol.Preamp[name]
    assert protocol.decode(f"PA0{digit};".encode("ascii")) == protocol.PreampUpdate(setting=setting)

def test_encode_read_preamp():
    assert protocol.encode_read_preamp() == b"PA0;"
```

**Step 2: Run, see fail.** **Step 3: Implement.** **Step 4: Run, see pass.**

**Step 5: Commit.** `git commit -am "ft710ctl: preamp encode/decode"`.

---

### Task 10: Attenuator (RA)

**Manual ref:** p.18, `RA`. Set: `RA0<digit>;`. P2: 0=OFF, 1=6dB, 2=12dB, 3=18dB. Read: `RA0;`.

**Step 1: Failing tests**

```python
ATT_CASES = [
    ("OFF", "0"), ("DB6", "1"), ("DB12", "2"), ("DB18", "3"),
]

@pytest.mark.parametrize("name,digit", ATT_CASES)
def test_encode_set_attenuator(name, digit):
    setting = protocol.Attenuator[name]
    assert protocol.encode_set_attenuator(setting) == f"RA0{digit};".encode("ascii")

@pytest.mark.parametrize("name,digit", ATT_CASES)
def test_decode_attenuator(name, digit):
    setting = protocol.Attenuator[name]
    assert protocol.decode(f"RA0{digit};".encode("ascii")) == protocol.AttenuatorUpdate(setting=setting)

def test_encode_read_attenuator():
    assert protocol.encode_read_attenuator() == b"RA0;"
```

**Step 2–5:** Standard TDD cycle. Commit: `git commit -am "ft710ctl: attenuator encode/decode"`.

---

### Task 11: AGC (GT) — Set and Answer have different value spaces

**Manual ref:** p.13, `GT`. *Set* P2 = 0..4 only (OFF/FAST/MID/SLOW/AUTO). *Answer* P3 = 0..6 (the AUTO-FAST/MID/SLOW variants are *reported* values when AUTO resolves). Decoder must accept the wider Answer range.

**Step 1: Failing tests**

```python
AGC_SET_CASES = [
    ("OFF", "0"), ("FAST", "1"), ("MID", "2"), ("SLOW", "3"), ("AUTO", "4"),
]
# Answer P3 mapping per manual p.13: 0=OFF, 1=FAST, 2=MID, 3=SLOW,
# 4=AUTO-FAST, 5=AUTO-MID, 6=AUTO-SLOW. There is no plain "AUTO" on the
# Answer side — when Set is AUTO, the radio reports which auto-tier it
# resolved to via 4/5/6.
AGC_REPORT_CASES = [
    ("OFF", "0"), ("FAST", "1"), ("MID", "2"), ("SLOW", "3"),
    ("AUTO_FAST", "4"), ("AUTO_MID", "5"), ("AUTO_SLOW", "6"),
]

@pytest.mark.parametrize("name,digit", AGC_SET_CASES)
def test_encode_set_agc(name, digit):
    setting = protocol.AgcSet[name]
    assert protocol.encode_set_agc(setting) == f"GT0{digit};".encode("ascii")

def test_encode_set_agc_rejects_auto_resolved():
    # Set form does not accept AUTO_FAST/MID/SLOW — those are Answer-only.
    with pytest.raises(AttributeError):
        protocol.AgcSet["AUTO_FAST"]

@pytest.mark.parametrize("name,digit", AGC_REPORT_CASES)
def test_decode_agc(name, digit):
    report = protocol.AgcReport[name]
    assert protocol.decode(f"GT0{digit};".encode("ascii")) == protocol.AgcUpdate(report=report)

def test_encode_read_agc():
    assert protocol.encode_read_agc() == b"GT0;"
```

**Step 2: Run, see fail.**

**Step 3: Implement** two enums (`AgcSet` for outbound, `AgcReport` for inbound), the encoder, and the decoder branch.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: AGC encode/decode with Set/Report split"`.

---

### Task 12: Noise blanker + reduction (NB, NL, NR, RL)

**Manual ref:** `NB` p.17, `NL` p.17, `NR` p.17, `RL` p.20. **RL frame is `RL0xx;` (mandatory P1=0 byte)**.

**Step 1: Failing tests**

```python
def test_encode_set_nb_on():
    assert protocol.encode_set_nb(True) == b"NB01;"

def test_encode_set_nb_off():
    assert protocol.encode_set_nb(False) == b"NB00;"

def test_encode_read_nb():
    assert protocol.encode_read_nb() == b"NB0;"

def test_encode_set_nb_level():
    assert protocol.encode_set_nb_level(0) == b"NL0000;"
    assert protocol.encode_set_nb_level(10) == b"NL0010;"

def test_encode_set_nb_level_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_nb_level(11)

def test_encode_set_nr_on():
    assert protocol.encode_set_nr(True) == b"NR01;"

def test_encode_set_nr_level():
    assert protocol.encode_set_nr_level(1) == b"RL001;"
    assert protocol.encode_set_nr_level(15) == b"RL015;"

def test_encode_set_nr_level_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_nr_level(0)
    with pytest.raises(ValueError):
        protocol.encode_set_nr_level(16)

def test_encode_read_nr_level():
    assert protocol.encode_read_nr_level() == b"RL0;"

def test_decode_nr_level():
    assert protocol.decode(b"RL015;") == protocol.NrLevelUpdate(level=15)
```

**Step 2–5:** Standard TDD cycle. Commit: `git commit -am "ft710ctl: NB/NL/NR/RL encode/decode"`.

---

### Task 13: Notch + DNF + Contour/APF (BP, BC, CO)

**Manual ref:** `BP` p.7, `BC` p.7, `CO` p.9 (*not* p.8). **CO P2=0 is on/off, P2=1 is freq, P2=2 is APF on/off, P2=3 is APF freq.** Set frame: `CO0<P2><P3 4 digits>;` (9 bytes). Read frame: `CO0<P2>;` (5 bytes).

**Step 1: Failing tests**

```python
def test_encode_set_manual_notch_on():
    assert protocol.encode_set_manual_notch(True) == b"BP00001;"

def test_encode_set_manual_notch_off():
    assert protocol.encode_set_manual_notch(False) == b"BP00000;"

def test_encode_set_manual_notch_freq():
    # P3 = freq / 10 Hz, three digits, range 001-320 -> 10 Hz to 3200 Hz
    assert protocol.encode_set_manual_notch_freq_hz(1500) == b"BP01150;"
    assert protocol.encode_set_manual_notch_freq_hz(10) == b"BP01001;"

def test_encode_read_manual_notch_state():
    assert protocol.encode_read_manual_notch_state() == b"BP00;"

def test_encode_read_manual_notch_freq():
    assert protocol.encode_read_manual_notch_freq() == b"BP01;"

def test_decode_manual_notch_freq():
    # BP P1 P2 P3 P3 P3 ; — P3 is freq/10 Hz, three digits
    assert protocol.decode(b"BP01150;") == protocol.ManualNotchFreqUpdate(freq_hz=1500)

def test_encode_set_auto_notch_on():
    assert protocol.encode_set_auto_notch(True) == b"BC01;"

def test_encode_read_auto_notch():
    assert protocol.encode_read_auto_notch() == b"BC0;"

def test_encode_set_contour_on():
    assert protocol.encode_set_contour(True) == b"CO000001;"

def test_encode_set_contour_off():
    assert protocol.encode_set_contour(False) == b"CO000000;"

def test_encode_set_contour_freq():
    assert protocol.encode_set_contour_freq_hz(1500) == b"CO011500;"

def test_encode_set_contour_freq_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_contour_freq_hz(5)  # below 10 Hz
    with pytest.raises(ValueError):
        protocol.encode_set_contour_freq_hz(3201)  # above 3200 Hz

def test_encode_set_apf_on():
    assert protocol.encode_set_apf(True) == b"CO020001;"

def test_encode_set_apf_freq():
    # P3 = 0000-0050, representing -250..+250 Hz in 10 Hz steps
    assert protocol.encode_set_apf_freq_hz(-250) == b"CO030000;"
    assert protocol.encode_set_apf_freq_hz(0) == b"CO030025;"
    assert protocol.encode_set_apf_freq_hz(250) == b"CO030050;"

def test_encode_read_contour_state():
    assert protocol.encode_read_contour_state() == b"CO00;"

def test_encode_read_contour_freq():
    assert protocol.encode_read_contour_freq() == b"CO01;"

def test_encode_read_apf_state():
    assert protocol.encode_read_apf_state() == b"CO02;"

def test_encode_read_apf_freq():
    assert protocol.encode_read_apf_freq() == b"CO03;"
```

**Step 2–5:** Standard TDD cycle. Commit: `git commit -am "ft710ctl: notch/DNF/contour/APF encode/decode"`.

---

### Task 14: IF shift + filter width (IS, SH)

**Manual ref:** `IS` p.15 (Set: `IS00±xxxx;`, 10 bytes; Read: `IS0;`). `SH` p.21 (Set: `SH00xx;`, 7 bytes; Read: `SH0;`). Manual page 5 highlights `IS00+1000;` as the correct shape and `IS00+100;` as a malformed example.

**Step 1: Failing tests**

```python
def test_encode_set_if_shift_zero():
    assert protocol.encode_set_if_shift_hz(0) == b"IS00+0000;"

def test_encode_set_if_shift_positive():
    assert protocol.encode_set_if_shift_hz(1000) == b"IS00+1000;"

def test_encode_set_if_shift_negative():
    assert protocol.encode_set_if_shift_hz(-1000) == b"IS00-1000;"

def test_encode_set_if_shift_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_if_shift_hz(1220)  # above 1200
    with pytest.raises(ValueError):
        protocol.encode_set_if_shift_hz(-1220)

def test_encode_set_if_shift_rejects_non_20hz_step():
    with pytest.raises(ValueError):
        protocol.encode_set_if_shift_hz(15)

def test_encode_read_if_shift():
    assert protocol.encode_read_if_shift() == b"IS0;"

def test_decode_if_shift():
    assert protocol.decode(b"IS00+1000;") == protocol.IfShiftUpdate(shift_hz=1000)

# SH filter width — P3 is mode-dependent; decoder returns raw P3 index,
# command layer maps to Hz against the current mode (per design doc).
SH_CASES = [
    (0, b"SH0000;"), (1, b"SH0001;"), (15, b"SH0015;"), (23, b"SH0023;"),
]

@pytest.mark.parametrize("idx,frame", SH_CASES)
def test_encode_set_filter_width(idx, frame):
    assert protocol.encode_set_filter_width(idx) == frame

def test_encode_set_filter_width_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_filter_width(24)
    with pytest.raises(ValueError):
        protocol.encode_set_filter_width(-1)

def test_encode_read_filter_width():
    assert protocol.encode_read_filter_width() == b"SH0;"
```

**Step 2–5:** Standard TDD cycle. Commit: `git commit -am "ft710ctl: IS + SH encode/decode"`.

---

### Task 15: Remaining SS sub-functions (speed, peak, color, marker)

**Manual ref:** p.21, `SS` P2=0/1/2/3.

**Step 1: Failing tests**

```python
SCOPE_SPEED_CASES = [
    ("SLOW1", "0"), ("SLOW2", "1"), ("FAST1", "2"),
    ("FAST2", "3"), ("FAST3", "4"), ("STOP", "5"),
]

@pytest.mark.parametrize("name,digit", SCOPE_SPEED_CASES)
def test_encode_set_scope_speed(name, digit):
    speed = protocol.ScopeSpeed[name]
    assert protocol.encode_set_scope_speed(speed) == f"SS00{digit}0000;".encode("ascii")

SCOPE_PEAK_CASES = [
    ("LV1", "0"), ("LV2", "1"), ("LV3", "2"), ("LV4", "3"), ("LV5", "4"),
]

@pytest.mark.parametrize("name,digit", SCOPE_PEAK_CASES)
def test_encode_set_scope_peak(name, digit):
    peak = protocol.ScopePeak[name]
    assert protocol.encode_set_scope_peak(peak) == f"SS01{digit}0000;".encode("ascii")

def test_encode_set_scope_marker():
    assert protocol.encode_set_scope_marker(True) == b"SS0210000;"
    assert protocol.encode_set_scope_marker(False) == b"SS0200000;"

# P3 = 0..A for Color-1..Color-11
SCOPE_COLOR_CASES = [
    (1, "0"), (2, "1"), (10, "9"), (11, "A"),
]

@pytest.mark.parametrize("color,digit", SCOPE_COLOR_CASES)
def test_encode_set_scope_color(color, digit):
    assert protocol.encode_set_scope_color(color) == f"SS03{digit}0000;".encode("ascii")

def test_encode_set_scope_color_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_scope_color(12)

# SS07 — AF-FFT / oscilloscope mode (manual p.21)
# P3 0 = AF-FFT (ATT=0dB), 1 = AF-FFT (ATT=10dB), 2 = AF-FFT (ATT=20dB),
#    3 = OSC Level (ATT=0dB), 4 = OSC Level (ATT=10dB), 5 = OSC Level (ATT=20dB)
# P4 0 = OSC Time 1 ms, 1 = 3 ms, 2 = 10 ms, 3 = 30 ms, 4 = 100 ms, 5 = 300 ms
AF_FFT_CASES = [
    ("AF_FFT_0DB", 0), ("AF_FFT_10DB", 1), ("AF_FFT_20DB", 2),
    ("OSC_0DB", 3), ("OSC_10DB", 4), ("OSC_20DB", 5),
]

@pytest.mark.parametrize("name,digit", AF_FFT_CASES)
def test_encode_set_af_fft_mode(name, digit):
    mode = protocol.AfFftMode[name]
    # P3 = digit, P4 = 0 default oscilloscope time, P5-P7 fixed 0
    assert protocol.encode_set_af_fft_mode(mode) == f"SS07{digit}00000;".encode("ascii")

def test_encode_read_af_fft():
    assert protocol.encode_read_af_fft() == b"SS07;"
```

**Step 2–5:** Standard TDD cycle. Commit: `git commit -am "ft710ctl: SS speed/peak/color/marker/AF-FFT encode/decode"`.

---

### Task 16: S-meter (SM)

**Manual ref:** p.21, `SM`. Set is rare; we primarily read. Read: `SM0;`. Answer: `SM0xxx;` where P2 = 000-255.

**Step 1: Failing tests**

```python
def test_encode_read_smeter():
    assert protocol.encode_read_smeter() == b"SM0;"

def test_decode_smeter():
    assert protocol.decode(b"SM0123;") == protocol.SmeterUpdate(raw=123)
    assert protocol.decode(b"SM0000;") == protocol.SmeterUpdate(raw=0)
    assert protocol.decode(b"SM0255;") == protocol.SmeterUpdate(raw=255)
```

**Step 2–5:** TDD. Commit: `git commit -am "ft710ctl: SM read/decode"`.

---

### Task 17: AF gain + RF gain (AG, RG)

**Manual ref:** `AG` p.6 (Set: `AG0xxx;`, P2 = 000-255). `RG` p.20 (Set: `RG0xxx;`, P2 = 000-255).

**Step 1: Failing tests**

```python
def test_encode_set_af_gain():
    assert protocol.encode_set_af_gain(0) == b"AG0000;"
    assert protocol.encode_set_af_gain(128) == b"AG0128;"
    assert protocol.encode_set_af_gain(255) == b"AG0255;"

def test_encode_set_af_gain_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_af_gain(256)

def test_encode_read_af_gain():
    assert protocol.encode_read_af_gain() == b"AG0;"

def test_decode_af_gain():
    assert protocol.decode(b"AG0128;") == protocol.AfGainUpdate(value=128)

# RG mirrors AG
def test_encode_set_rf_gain():
    assert protocol.encode_set_rf_gain(128) == b"RG0128;"

def test_encode_read_rf_gain():
    assert protocol.encode_read_rf_gain() == b"RG0;"
```

**Step 2–5:** TDD. Commit: `git commit -am "ft710ctl: AG + RG encode/decode"`.

---

### Task 18: Band select + swap VFO + split (BS, SV, ST)

**Manual ref:** `BS` p.7 (Set: `BSxx;`, 5 bytes, P1 = two-digit band index — see manual for band table). `SV` p.21 (Set: `SV;` — toggle, no parameters, no Read). `ST` p.21 (Set: `ST<digit>;`, P1 = 0 OFF / 1 ON; Read: `ST;`).

**Step 1: Failing tests**

```python
BAND_CASES = [
    ("M160", "00"), ("M80", "01"), ("M60", "02"), ("M40", "03"),
    ("M30", "04"), ("M20", "05"), ("M17", "06"), ("M15", "07"),
    ("M12", "08"), ("M10", "09"), ("M6", "10"), ("GEN", "11"),
]

@pytest.mark.parametrize("name,digits", BAND_CASES)
def test_encode_set_band(name, digits):
    band = protocol.Band[name]
    assert protocol.encode_set_band(band) == f"BS{digits};".encode("ascii")

def test_encode_swap_vfo():
    assert protocol.encode_swap_vfo() == b"SV;"

def test_encode_set_split_on():
    assert protocol.encode_set_split(True) == b"ST1;"

def test_encode_set_split_off():
    assert protocol.encode_set_split(False) == b"ST0;"

def test_encode_read_split():
    assert protocol.encode_read_split() == b"ST;"

def test_decode_split():
    assert protocol.decode(b"ST1;") == protocol.SplitUpdate(enabled=True)
    assert protocol.decode(b"ST0;") == protocol.SplitUpdate(enabled=False)
```

**Step 2–5:** TDD. Commit: `git commit -am "ft710ctl: BS + SV + ST encode/decode"`.

---

### Task 19: CLAR on/off (CF, simplified)

**Manual ref:** `CF` p.8. The full `CF` Set frame carries multiple parameters (RX/TX CLAR enable, CLAR offset frequency). For v1 we expose only the RX CLAR on/off toggle. Full CLAR control is deferred.

**Step 1: Failing tests**

```python
def test_encode_set_rx_clar_on():
    # CF byte layout (manual p.8): C F P1 P2 P3 P4 P5 P6 P7 P8 ;
    #   P1=0 (main band), P2=0 (fixed), P3=0 (CLAR setting mode),
    #   P4=RX CLAR (0=OFF, 1=ON), P5=TX CLAR (0=OFF, 1=ON), P6-P8=0
    # RX CLAR ON, TX CLAR OFF -> P4=1, P5=0 -> CF00010000;
    assert protocol.encode_set_rx_clar(True) == b"CF00010000;"

def test_encode_set_rx_clar_off():
    # RX CLAR OFF, TX CLAR OFF -> P4=0, P5=0 -> CF00000000;
    assert protocol.encode_set_rx_clar(False) == b"CF00000000;"

def test_encode_read_clar():
    # CF read: C F P1 P2 P3 ;
    assert protocol.encode_read_clar() == b"CF000;"

def test_decode_clar_rx_on_tx_off():
    update = protocol.decode(b"CF00010000;")
    assert update.rx_enabled is True
    assert update.tx_enabled is False

def test_decode_clar_rx_off_tx_off():
    update = protocol.decode(b"CF00000000;")
    assert update.rx_enabled is False
    assert update.tx_enabled is False
```

**Step 2–5:** TDD. Commit: `git commit -am "ft710ctl: CF RX CLAR on/off (simplified)"`.

---

### Task 20: Dispatcher robustness

We are *not* enabling `AI` for v1 (see revision notes), but we still want the decoder to be robust against malformed inbound bytes.

**Step 1: Failing tests**

```python
def test_decode_truncated_frame():
    assert protocol.decode(b"FA01") == protocol.UnknownFrame(raw=b"FA01")

def test_decode_empty():
    assert protocol.decode(b"") == protocol.UnknownFrame(raw=b"")

def test_decode_non_ascii():
    assert protocol.decode(b"\xff\xfe;") == protocol.UnknownFrame(raw=b"\xff\xfe;")

def test_decode_unknown_two_letter_prefix():
    assert protocol.decode(b"ZZ0;") == protocol.UnknownFrame(raw=b"ZZ0;")

def test_decode_known_prefix_wrong_length():
    # FA needs exactly 12 bytes
    assert protocol.decode(b"FA12345;") == protocol.UnknownFrame(raw=b"FA12345;")
```

**Step 2–5:** TDD. Confirm `decode` falls through to `UnknownFrame` for every bad shape. Commit: `git commit -am "ft710ctl: dispatcher robustness"`.

---

## Phase 3 — Port, state, commands

### Task 21: FakeSerial test double

**Files:** Create `FT-710/ft710ctl/tests/fake_serial.py`.

**Step 1: Write the helper**

```python
"""Test double for serial-asyncio.

Records every write. Replies to specific frames with canned answers.
Used by command-layer tests so they never need real hardware.
"""
from __future__ import annotations
import asyncio


class FakeSerial:
    def __init__(self):
        self.writes: list[bytes] = []
        self._response_rules: dict[bytes, bytes] = {}
        self._inbound: asyncio.Queue[bytes] = asyncio.Queue()
        self.is_open = True
        self.raise_on_next_write: Exception | None = None

    def on(self, request: bytes, response: bytes) -> None:
        self._response_rules[request] = response

    async def write(self, data: bytes) -> None:
        if self.raise_on_next_write is not None:
            exc, self.raise_on_next_write = self.raise_on_next_write, None
            raise exc
        self.writes.append(data)
        if data in self._response_rules:
            await self._inbound.put(self._response_rules[data])

    async def push(self, frame: bytes) -> None:
        await self._inbound.put(frame)

    async def read_frame(self) -> bytes:
        return await self._inbound.get()

    def close(self) -> None:
        self.is_open = False
```

**Step 2: Smoke test it**

`tests/test_fake_serial.py`:
```python
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
```

**Step 3: Run, see pass.** **Step 4: Commit.** `git commit -am "ft710ctl: FakeSerial test double"`.

---

### Task 22: RadioPort with connection factory + lifecycle

**Files:** Create `FT-710/ft710ctl/ft710ctl/radio/port.py`, `FT-710/ft710ctl/tests/test_port.py`.

**Step 1: Failing tests**

```python
import asyncio
import pytest
from tests.fake_serial import FakeSerial
from ft710ctl.radio.port import RadioPort, PortClosed

async def test_open_and_send_receive():
    fs = FakeSerial()
    fs.on(b"FA;", b"FA014250000;")
    port = RadioPort(factory=lambda: fs)
    await port.open()
    await port.send(b"FA;")
    frame = await asyncio.wait_for(port.next_frame(), timeout=1.0)
    assert frame == b"FA014250000;"
    await port.close()

async def test_close_awaits_task_cleanup():
    fs = FakeSerial()
    port = RadioPort(factory=lambda: fs)
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
    port = RadioPort(factory=lambda: next(serials))
    await port.open()
    await port.reopen()  # closes fs1, opens fs2
    await port.send(b"FA;")
    await asyncio.sleep(0.05)
    assert fs2.writes == [b"FA;"]
    assert fs1.writes == []
    await port.close()

async def test_send_after_close_raises():
    fs = FakeSerial()
    port = RadioPort(factory=lambda: fs)
    await port.open()
    await port.close()
    with pytest.raises(PortClosed):
        await port.send(b"FA;")

async def test_pending_next_frame_resolves_on_close():
    """A consumer awaiting next_frame() must not block forever after close()."""
    fs = FakeSerial()
    port = RadioPort(factory=lambda: fs)
    await port.open()
    pending = asyncio.create_task(port.next_frame())
    await asyncio.sleep(0)  # let the task park
    await port.close()
    with pytest.raises(PortClosed):
        await asyncio.wait_for(pending, timeout=1.0)
```

**Step 2: Run, see fail.**

**Step 3: Implement**

```python
"""Asyncio wrapper around the serial port with explicit lifecycle."""
from __future__ import annotations
import asyncio
from typing import Callable, Protocol


WRITE_GAP_S = 0.020  # 20 ms between writes


class PortClosed(Exception):
    """Raised by send() or pending next_frame() when the port is closed."""


class SerialLike(Protocol):
    async def write(self, data: bytes) -> None: ...
    async def read_frame(self) -> bytes: ...
    def close(self) -> None: ...


# Sentinel pushed into the inbound queue on close() to wake pending readers.
_CLOSE_SENTINEL: object = object()


class RadioPort:
    def __init__(self, factory: Callable[[], SerialLike], write_gap_s: float = WRITE_GAP_S):
        self._factory = factory
        self._write_gap_s = write_gap_s
        self._serial: SerialLike | None = None
        self._outbound: asyncio.Queue[bytes] = asyncio.Queue()
        self._inbound: asyncio.Queue = asyncio.Queue()
        self._writer_task: asyncio.Task | None = None
        self._reader_task: asyncio.Task | None = None
        self._open: bool = False

    async def open(self) -> None:
        if self._open:
            raise RuntimeError("port already open")
        self._serial = self._factory()
        self._outbound = asyncio.Queue()
        self._inbound = asyncio.Queue()
        self._open = True
        self._writer_task = asyncio.create_task(self._writer())
        self._reader_task = asyncio.create_task(self._reader())

    async def close(self) -> None:
        if not self._open:
            return
        self._open = False
        # Wake any consumer parked in next_frame().
        await self._inbound.put(_CLOSE_SENTINEL)
        for t in (self._writer_task, self._reader_task):
            if t is None:
                continue
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass
        if self._serial is not None:
            self._serial.close()
        self._serial = None
        self._writer_task = None
        self._reader_task = None

    async def reopen(self) -> None:
        """Close (if open) then open. Used by reconnect (Task 41)."""
        await self.close()
        await self.open()

    async def send(self, frame: bytes) -> None:
        if not self._open:
            raise PortClosed("port is closed")
        await self._outbound.put(frame)

    async def next_frame(self) -> bytes:
        item = await self._inbound.get()
        if item is _CLOSE_SENTINEL:
            # Re-arm sentinel for any other waiters, then raise.
            await self._inbound.put(_CLOSE_SENTINEL)
            raise PortClosed("port closed while waiting for frame")
        return item

    async def _writer(self) -> None:
        while True:
            frame = await self._outbound.get()
            await self._serial.write(frame)
            await asyncio.sleep(self._write_gap_s)

    async def _reader(self) -> None:
        while True:
            frame = await self._serial.read_frame()
            await self._inbound.put(frame)
```

**Step 4: Run, see pass.** Override `write_gap_s=0` in tests via constructor or monkeypatch to keep them quick. **Step 5: Commit.** `git commit -am "ft710ctl: RadioPort with open/close lifecycle"`.

---

### Task 23: RadioState + apply dispatch

**Files:** Create `FT-710/ft710ctl/ft710ctl/radio/state.py`, `FT-710/ft710ctl/tests/test_state.py`.

**Step 1: Failing tests** (start with scope.span — add cases for each update type as you add decoder branches)

```python
from ft710ctl.radio import state, protocol

def test_apply_span_update():
    rs = state.RadioState()
    delta = rs.apply(protocol.ScopeSpanUpdate(span_khz=100))
    assert rs.scope.span_khz == 100
    assert delta == {"field": "scope.span_khz", "value": 100}

def test_apply_smeter_update():
    rs = state.RadioState()
    delta = rs.apply(protocol.SmeterUpdate(raw=128))
    assert rs.meters.smeter_raw == 128
    assert delta == {"field": "meters.smeter_raw", "value": 128}

def test_apply_unknown_returns_none():
    rs = state.RadioState()
    assert rs.apply(protocol.UnknownFrame(raw=b"XX0;")) is None

def test_apply_is_idempotent():
    rs = state.RadioState()
    delta1 = rs.apply(protocol.ScopeSpanUpdate(span_khz=100))
    delta2 = rs.apply(protocol.ScopeSpanUpdate(span_khz=100))
    assert delta1 == delta2
    assert rs.scope.span_khz == 100
```

**Step 2: Run, see fail.**

**Step 3: Implement** the dataclass hierarchy: `ScopeState`, `TuningState`, `RxDspState`, `MetersState`, `RadioState`, plus an `apply()` method with one `isinstance` branch per update type. (Use a registry dict if you'd rather avoid a long if-chain.)

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: RadioState + apply dispatch"`.

---

### Task 24: Radio command wrapper (set_span_khz only)

**Files:** Create `FT-710/ft710ctl/ft710ctl/radio/commands.py`, `FT-710/ft710ctl/tests/test_commands.py`.

**Step 1: Failing tests**

```python
import asyncio
import pytest
from tests.fake_serial import FakeSerial
from ft710ctl.radio.commands import Radio

async def test_set_span_writes_and_reads_back():
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    radio = Radio(factory=lambda: fs)
    await radio.start()
    await radio.set_span_khz(100)
    await asyncio.sleep(0.05)
    assert radio.state.scope.span_khz == 100
    await radio.stop()

async def test_set_span_invalid_raises_before_sending():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_span_khz(3)
    assert fs.writes == []  # validation happens pre-wire
    await radio.stop()

async def test_stop_awaits_consumer_cleanup():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs)
    await radio.start()
    await radio.stop()
    assert radio._consumer.done()
```

**Step 2: Run, see fail.**

**Step 3: Implement**

```python
from __future__ import annotations
import asyncio
from . import protocol, state
from .port import RadioPort


class Radio:
    def __init__(self, factory, write_gap_s: float | None = None):
        kwargs = {"write_gap_s": write_gap_s} if write_gap_s is not None else {}
        self.port = RadioPort(factory=factory, **kwargs)
        self.state = state.RadioState()
        self._consumer: asyncio.Task | None = None
        self._subscribers: list = []

    async def start(self) -> None:
        await self.port.open()
        self._consumer = asyncio.create_task(self._consume_frames())

    async def stop(self) -> None:
        if self._consumer:
            self._consumer.cancel()
            try:
                await self._consumer
            except asyncio.CancelledError:
                pass
        await self.port.close()

    def subscribe(self, callback) -> None:
        self._subscribers.append(callback)

    async def _consume_frames(self) -> None:
        while True:
            frame = await self.port.next_frame()
            update = protocol.decode(frame)
            delta = self.state.apply(update)
            if delta is not None:
                for cb in list(self._subscribers):
                    try:
                        cb(delta)
                    except Exception:
                        pass  # never let a bad subscriber kill the consumer

    async def set_span_khz(self, khz: int) -> None:
        frame = protocol.encode_set_span_khz(khz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_span())
```

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: Radio wrapper with set_span_khz"`.

---

### Task 25: Expand Radio with every v1 verb (with invalid-argument coverage)

Add a `Radio.set_*` method for each command from Phase 2. Coverage rule depends on the verb's argument shape:

- **Range-checked numeric setters** (e.g. `set_span_khz`, `set_ref_level_db`, `set_vfo_a_hz`, `set_nb_level`, `set_nr_level`, `set_manual_notch_freq_hz`, `set_contour_freq_hz`, `set_apf_freq_hz`, `set_if_shift_hz`, `set_filter_width`, `set_af_gain`, `set_rf_gain`, `set_scope_color`):
  - Test 1: happy-path round-trip.
  - Test 2: invalid argument → `ValueError`, `fs.writes == []` (validation runs pre-wire).
- **Enum setters** (e.g. `set_scope_mode`, `set_mode`, `set_preamp`, `set_attenuator`, `set_agc`, `set_scope_speed`, `set_scope_peak`, `set_band`, `set_af_fft_mode`):
  - Test 1: happy-path round-trip on a representative value.
  - Test 2: passing a non-enum value (e.g. a plain string) raises `TypeError` and `fs.writes == []`.
- **Boolean toggles** (e.g. `set_scope_marker`, `set_nb`, `set_nr`, `set_manual_notch`, `set_auto_notch`, `set_contour`, `set_apf`, `set_split`, `set_rx_clar`):
  - Test 1: happy-path round-trip on True.
  - Test 2: happy-path round-trip on False.
  - No invalid-argument test (the type system covers it; the verb signature is `bool`).
- **No-argument actions** (e.g. `swap_vfo`):
  - Test 1: calling the verb writes exactly the expected bytes (e.g. `b"SV;"`).
  - No second test.

Verbs to add:

- `set_ref_level_db`
- `set_scope_mode`
- `set_scope_speed`
- `set_scope_peak`
- `set_scope_marker`
- `set_scope_color`
- `set_af_fft_mode`
- `set_vfo_a_hz`, `set_vfo_b_hz`
- `set_mode`
- `set_preamp`, `set_attenuator`, `set_agc`
- `set_nb`, `set_nb_level`, `set_nr`, `set_nr_level`
- `set_manual_notch`, `set_manual_notch_freq_hz`
- `set_auto_notch`
- `set_contour`, `set_contour_freq_hz`, `set_apf`, `set_apf_freq_hz`
- `set_if_shift_hz`, `set_filter_width`
- `set_af_gain`, `set_rf_gain`
- `set_band`, `swap_vfo`, `set_split`, `set_rx_clar`

Commit in coherent groups, e.g.:
- `git commit -am "ft710ctl: Radio verbs for SS sub-functions"`
- `git commit -am "ft710ctl: Radio verbs for VFO, mode, band, swap, split"`
- `git commit -am "ft710ctl: Radio verbs for RX DSP"`
- `git commit -am "ft710ctl: Radio verbs for AG/RG/CF"`

Roughly 4-6 commits for this slice instead of 24 individual ones.

---

### Task 26: Snapshot routine with sequenced reads

**Step 1: Failing tests**

```python
async def test_snapshot_issues_every_v1_read():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs)
    await radio.start()
    await radio.snapshot()
    expected = [
        # Scope
        b"SS05;", b"SS04;", b"SS06;", b"SS00;", b"SS01;", b"SS02;", b"SS03;", b"SS07;",
        # Tuning
        b"FA;", b"FB;", b"MD0;", b"ST;",
        # RX DSP
        b"PA0;", b"RA0;", b"GT0;",
        b"NB0;", b"NL0;", b"NR0;", b"RL0;",
        b"BP00;", b"BP01;",              # manual notch state + freq
        b"BC0;",                         # auto notch
        b"CO00;", b"CO01;", b"CO02;", b"CO03;",  # contour state/freq, APF state/freq
        b"IS0;", b"SH0;",
        # Meters + gain
        b"SM0;", b"AG0;", b"RG0;",
        # CLAR
        b"CF000;",
    ]
    for frame in expected:
        assert frame in fs.writes, f"snapshot missing read: {frame}"
    await radio.stop()

async def test_snapshot_is_sequenced_not_parallel():
    """Each read is sent in order; the writer's 20 ms gap is honored."""
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0.005)
    await radio.start()
    await radio.snapshot()
    # writes recorded in the order they were drained by the writer
    assert fs.writes[0] == b"SS05;"  # first in the snapshot list
    await radio.stop()

async def test_state_change_publishes_to_subscriber():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs)
    received: list[dict] = []
    radio.subscribe(received.append)
    await radio.start()
    await fs.push(b"SS0560000;")
    await asyncio.sleep(0.05)
    assert received == [{"field": "scope.span_khz", "value": 100}]
    await radio.stop()
```

**Step 2: Run, see fail.**

**Step 3: Implement** `Radio.snapshot()` that enqueues every read in order. The writer task's existing 20 ms gap naturally sequences them.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: snapshot routine + state broadcast"`.

---

## Phase 4 — HTTP + WebSocket API

### Task 27: FastAPI app + /health + static file serving

**Files:** Create `FT-710/ft710ctl/ft710ctl/server.py`, `FT-710/ft710ctl/ft710ctl/__main__.py`, `FT-710/ft710ctl/ft710ctl/web/index.html` (placeholder), `FT-710/ft710ctl/tests/test_server.py`.

**Step 1: Failing test**

```python
from fastapi.testclient import TestClient
from ft710ctl.server import create_app

def test_health():
    app = create_app(radio=None)
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
```

**Step 2: Run, see fail.**

**Step 3: Implement** `create_app(radio)` returning a `FastAPI` with `/health`, static file mount at `/`, placeholder `index.html`. Add `__main__.py:main()` parsing `--port` (serial) and `--http-port` (default 8710), constructing a real `pyserial-asyncio` factory, building `Radio`, and running uvicorn.

**Step 4: Run, see pass.** **Step 5: Commit.** `git commit -am "ft710ctl: FastAPI app shell + health"`.

---

### Task 28: GET /api/state

**Step 1: Failing test**

```python
def test_api_state_initial():
    radio = ...  # stub with radio.state = RadioState()
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.get("/api/state")
    assert r.status_code == 200
    body = r.json()
    assert "scope" in body and "tuning" in body and "rx" in body and "meters" in body
```

**Step 2–5:** Serialize `radio.state` with `dataclasses.asdict`, converting Enum values to `.name`. Commit: `git commit -am "ft710ctl: GET /api/state"`.

---

### Task 29: WebSocket /ws (connection + initial snapshot)

**Step 1: Failing test**

```python
def test_ws_initial_state():
    radio = ...
    app = create_app(radio=radio)
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        first = ws.receive_json()
        assert first["op"] == "snapshot"
        assert "state" in first
```

**Step 2–5:** Implement `/ws` route in `api/ws.py`. On connection, send `{"op": "snapshot", "state": ...}`. Commit: `git commit -am "ft710ctl: WebSocket /ws with initial snapshot"`.

---

### Task 30: POST /api/raw with quiescence + drain

The escape hatch must not race with the normal frame consumer, which
would let `/api/raw` capture (or worse, return) an unrelated state-change
frame.

**Design — quiescence + drain pattern:**

1. The `Radio` keeps an `outstanding_reads` counter, incremented by every
   `Radio.set_*` verb when it enqueues its read-back, decremented when a
   matching frame is consumed (or after a 2 s timeout per outstanding
   read — defensive).
2. `Radio.single_shot(frame, timeout)`:
   a. Acquire an `asyncio.Lock` so only one raw call runs at a time.
   b. Wait until `outstanding_reads == 0` (with timeout). This is the
      "quiescence" step — no read-backs in flight, no unsolicited
      frames expected (AI is off in v1).
   c. **Pause the consumer**: set a flag and capture the next inbound
      frame to a Future instead of dispatching to state.
   d. Send the raw frame via the port.
   e. Await the Future with the caller's timeout.
   f. Resume the consumer.
   g. Release the lock.

The quiescence guarantee plus consumer-pause guarantees the captured
frame is the response to *this* raw send, not a leftover.

**Step 1: Failing tests**

```python
async def test_api_raw_returns_response():
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    radio = Radio(factory=lambda: fs)
    await radio.start()
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.post("/api/raw", json={"frame": "SS05;"})
    assert r.status_code == 200
    assert r.json() == {"response": "SS0560000;"}
    await radio.stop()

async def test_api_raw_waits_for_quiescence():
    """A raw request issued while a set is in flight waits for the read-back
    to be consumed before sending."""
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    fs.on(b"FA;", b"FA014250000;")
    radio = Radio(factory=lambda: fs)
    await radio.start()
    # Inflate outstanding_reads to simulate a pending read-back.
    radio._outstanding_reads = 1
    raw_task = asyncio.create_task(radio.single_shot(b"FA;", timeout=1.0))
    await asyncio.sleep(0.05)
    assert not raw_task.done()  # blocked on quiescence
    radio._outstanding_reads = 0  # simulate read-back consumed
    result = await asyncio.wait_for(raw_task, timeout=1.0)
    assert result == b"FA014250000;"
    await radio.stop()

def test_api_raw_rejects_non_ascii():
    radio = make_stub_radio()
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.post("/api/raw", json={"frame": "ÿ;"})
    assert r.status_code == 400

def test_api_raw_rejects_missing_terminator():
    radio = make_stub_radio()
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.post("/api/raw", json={"frame": "SS05"})
    assert r.status_code == 400

async def test_api_raw_timeout_returns_408():
    fs = FakeSerial()  # no canned response → no reply
    radio = Radio(factory=lambda: fs)
    await radio.start()
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.post("/api/raw", json={"frame": "SS05;", "timeout_s": 0.1})
    assert r.status_code == 408
    await radio.stop()
```

**Step 2–5:** Implement the `outstanding_reads` counter, lock, consumer
pause flag, and Future capture. Validate frames are ASCII + end with `;`.
Returns 408 on timeout. Commit: `git commit -am "ft710ctl: /api/raw with quiescence + drain"`.

---

### Task 31: WebSocket — client set messages

Dispatch table mapping field-path string to `Radio.set_*` method. Whitelist of fields. Errors return only to the originating socket with `{"op": "error", "reason": ..., "request_id": ...}`.

**Step 1: Failing test**

```python
def test_ws_set_dispatches_to_radio():
    radio = StubRadio()  # records every set_* call
    app = create_app(radio=radio)
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.receive_json()  # snapshot
        ws.send_json({"op": "set", "field": "scope.span_khz", "value": 100, "request_id": "r1"})
        # Wait for ack or absence of error
    assert radio.calls == [("set_span_khz", (100,), {})]

def test_ws_set_unknown_field_returns_error():
    radio = StubRadio()
    app = create_app(radio=radio)
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.receive_json()
        ws.send_json({"op": "set", "field": "scope.bogus", "value": 1, "request_id": "r1"})
        msg = ws.receive_json()
        assert msg["op"] == "error"
        assert msg["request_id"] == "r1"
```

**Step 2–5:** TDD. Commit: `git commit -am "ft710ctl: WebSocket set dispatch"`.

---

### Task 32: WebSocket — broadcast deltas

Hook `Radio.subscribe()` to push every delta to every connected socket as `{"op": "patch", "field": ..., "value": ...}`. Disconnected sockets get removed from the subscriber set.

**Test** with two simulated clients receiving the same patch after `fs.push()`.

Commit: `git commit -am "ft710ctl: WebSocket delta broadcast"`.

---

### Task 33: Port state messages (`{"op": "port", "state": ...}`)

Broadcast `{"op": "port", "state": "connected"}` on successful open, `{"op": "port", "state": "disconnected"}` on close/failure. UI uses this for the banner.

**Test** by triggering open/close and asserting the messages arrive at connected clients.

Commit: `git commit -am "ft710ctl: WebSocket port state broadcast"`.

---

### Task 34: GET /api/debug/unknown (ring buffer + dispatcher-fallthrough test)

100-deep ring of unknown frames seen by `decode`. Entry: timestamp + raw hex.

**Step 1: Failing tests**

```python
async def test_unknown_ring_records_unparseable_frames():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs)
    await radio.start()
    await fs.push(b"ZZ0;")
    await fs.push(b"\xff\xfe;")
    await asyncio.sleep(0.05)
    assert len(radio.unknown_frames) == 2
    await radio.stop()

def test_unknown_ring_exposed_at_endpoint():
    radio = make_stub_radio_with_unknowns([b"ZZ0;", b"\xff\xfe;"])
    app = create_app(radio=radio)
    client = TestClient(app)
    r = client.get("/api/debug/unknown")
    assert r.status_code == 200
    assert len(r.json()["frames"]) == 2

def test_decode_dispatcher_falls_through_for_every_known_prefix_with_bad_shape():
    """Every prefix that has a known decoder branch must still return
    UnknownFrame when the body doesn't match the manual's frame shape.
    This guards against an `if` branch silently accepting malformed input."""
    bad_frames = [
        b"SS0500000",      # missing terminator
        b"SS05;",          # too short (looks like a read frame, not an answer)
        b"FA;",            # too short to be a frequency answer
        b"FA12345678;",    # wrong digit count
        b"MD;",            # missing P1+P2
        b"GT;",            # missing P1+P2
        b"BP00;",          # 5 bytes — looks like read, not answer
        b"CO00;",          # 5 bytes — looks like read, not answer
        b"IS00+;",         # missing 4-digit Hz
        b"SH00;",          # missing P3
        b"AG0;",           # missing 3-digit gain
        b"SM0;",           # missing 3-digit S-meter value
    ]
    for frame in bad_frames:
        result = protocol.decode(frame)
        assert isinstance(result, protocol.UnknownFrame), (
            f"decoder accepted malformed {frame!r}"
        )
```

**Step 2–5:** TDD. Commit: `git commit -am "ft710ctl: /api/debug/unknown ring + dispatcher fallthrough"`.

---

## Phase 5 — Frontend

### Task 35: index.html shell + style.css + app.js scaffolding

Three panels (Scope / Tuning / RX DSP) + Meters strip + status banner. Each control widget has `id` and `data-field`. `app.js` opens `/ws`, handles `snapshot` / `patch` / `error` / `port`, renders state into DOM.

Manual smoke: start server with `--no-radio` mode (stub Radio); open `http://localhost:8710/`; verify the page loads and WebSocket connects.

Commit: `git commit -am "ft710ctl: frontend shell + WebSocket plumbing"`.

---

### Task 36: Scope panel widgets

Span (10-position selector), reference level (slider -30.0 to +30.0 step 0.5), mode (dropdown), speed (6-position), color (1-11 dropdown), marker (toggle), AF-FFT mode (6-option dropdown: AF-FFT 0/10/20 dB, OSC 0/10/20 dB).

Commit: `git commit -am "ft710ctl: scope panel widgets"`.

---

### Task 37: Tuning panel widgets

VFO A/B frequency (accept MHz or Hz), mode dropdown, band selector (12 entries), A/B swap button, split toggle, CLAR toggle.

Commit: `git commit -am "ft710ctl: tuning panel widgets"`.

---

### Task 38: RX DSP panel widgets

Preamp (radio buttons), attenuator (radio buttons), AGC (radio buttons), NB toggle + level, NR toggle + level, auto-notch toggle, manual-notch toggle + freq, contour toggle + freq, APF toggle + freq, IF shift slider, filter width dropdown.

Commit: `git commit -am "ft710ctl: RX DSP panel widgets"`.

---

### Task 39: Meters strip (S-meter + AF/RF gain)

Bar graph for S-meter (subscribes to fast `meters.smeter_raw` updates), AF gain slider, RF gain slider.

Commit: `git commit -am "ft710ctl: meters + gain widgets"`.

---

### Task 40: Connection status banner

Three states: `connected` (green dot), `disconnected` (red, retrying...), `connecting` (yellow). Responds to `{"op": "port", "state": ...}` messages.

Commit: `git commit -am "ft710ctl: connection status banner"`.

---

## Phase 6 — Resilience polish

### Task 41: Serial port reconnect

Now feasible thanks to `RadioPort.open()` / `close()` / `reopen()` from Task 22. On serial error, mark port disconnected (broadcast), retry `reopen()` every 2 s, on success re-run snapshot and broadcast connected.

**Test** with `FakeSerial.raise_on_next_write` to trigger the error path.

Commit: `git commit -am "ft710ctl: serial port reconnect"`.

---

### Task 42: Manual smoke test against real radio

Run the checklist from the design doc plus the new commands:

- `/dev/ttyUSB0` and `/dev/ttyUSB1` appear after plugging in.
- `ft710ctl --port /dev/ttyUSB0` starts cleanly. `http://localhost:8710/` loads.
- All 10 scope spans set + verify on radio.
- Reference level: `+00.0`, `-30.0`, `+30.0`, `-15.5`.
- All ScopeMode variants.
- Preamp through IPO / AMP1 / AMP2.
- Attenuator through OFF / 6dB / 12dB / 18dB.
- AGC: OFF / FAST / MID / SLOW / AUTO. Confirm Answer side reports AUTO_FAST/MID/SLOW correctly.
- VFO A 14.250 MHz, VFO B 7.074 MHz, swap VFOs, split on/off, CLAR on/off.
- Band cycle: 160m → 10m via UI.
- Mode: USB / LSB / CW-U / CW-L / FM / AM / DATA-U.
- Open the UI in a second browser tab. Change span in tab 1. Verify tab 2 updates within ~200 ms.
- Disconnect USB. Red banner within 5 s. Reconnect. Green banner returns and current radio state mirrors in UI.
- S-meter updates while tuning across an HF signal.

Record results in `FT-710/ft710ctl/SMOKE.md`. Commit: `git commit -am "ft710ctl: v1 smoke test results"`.

---

## Task renumbering map (v1 → v2)

| v1 | v2 | Note |
| --- | --- | --- |
| 1 | 1 | skeleton |
| 2 | 2 | pytest baseline |
| 3 | 3 | protocol skeleton |
| 4 | 4 | SS span |
| 5 | 5 | SS ref level |
| 6 | 6 | SS mode |
| 7 | 7 | VFO freq |
| 8 | 8 | MD mode |
| 9 (PA+RA+GT) | 9, 10, 11 | split per command; GT corrected |
| 10 (NB+NL+NR+RL) | 12 | RL frame corrected |
| 11 (BP+BC+CO) | 13 | CO inversion + multi-byte corrected |
| 12 (IS+SH) | 14 | both frame shapes corrected |
| 13 (SS sub-fns) | 15 | unchanged |
| 14 (AI + robustness) | 20 | AI removed; robustness only |
| — | 16, 17, 18, 19 | SM / AG+RG / BS+SV+ST / CF — new |
| 15 (FakeSerial) | 21 | + raise-on-write helper |
| 16 (port) | 22 | factory + lifecycle |
| 17 (state) | 23 | + idempotency test |
| 18 (commands skeleton) | 24 | + stop-cleanup test |
| 19 (verb expansion) | 25 | + invalid-arg coverage required |
| 20 (snapshot) | 26 | + expanded read list + sequencing |
| 21 (server) | 27 | unchanged |
| 22 (/api/state) | 28 | + meters in payload |
| 23 (/api/raw) | 30 | + single-shot lock |
| 24 (WS snapshot) | 29 | unchanged |
| 25 (WS set) | 31 | unchanged |
| 26 (WS broadcast) | 32 | unchanged |
| — | 33 | new: WS port state |
| 27 (debug ring) | 34 | + explicit fallthrough test |
| 28 (frontend shell) | 35 | unchanged |
| 29 (scope panel) | 36 | unchanged |
| 30 (tuning panel) | 37 | now wired to existing verbs |
| 31 (RX DSP panel) | 38 | unchanged |
| — | 39 | new: meters strip |
| 32 (status banner) | 40 | unchanged |
| 33 (reconnect) | 41 | now implementable |
| 34 (smoke) | 42 | + new commands in checklist |

---

## Out of scope (deferred)

- CW operating surface (BI, SD, KP, KS, KR, KY, CS, ZI)
- TX shaping (PC, MG, PR, PL, parametric EQ menu items via `EX`)
- Memory channel manager (MR, MW, MT, MA, MB, MC, CH)
- Full `CF` CLAR control (frequency offset, RX/TX independence)
- Raw CAT terminal UI (have the `/api/raw` endpoint; UI deferred)
- Auto Information (`AI1;`) push-based state sync — v2
- LAN/internet remote access — v2
- Authentication — v2
- Audio routing (handled by remote desktop in v1)
- Multi-radio support (FT-710 only in v1)
