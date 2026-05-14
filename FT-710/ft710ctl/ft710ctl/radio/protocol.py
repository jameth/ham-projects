"""FT-710 CAT protocol: pure encode/decode functions.

Every encoder returns bytes ending in b";".
Every decoder returns either a typed update or UnknownFrame.
The FT-710 CAT Operation Reference Manual is the ground truth.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Union


@dataclass(frozen=True)
class UnknownFrame:
    raw: bytes


@dataclass(frozen=True)
class ScopeSpanUpdate:
    span_khz: int


@dataclass(frozen=True)
class ScopeRefLevelUpdate:
    level_db: float


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


@dataclass(frozen=True)
class VfoFreqUpdate:
    vfo: str
    hz: int


class OperatingMode(Enum):
    LSB = "1"
    USB = "2"
    CW_U = "3"
    FM = "4"
    AM = "5"
    RTTY_L = "6"
    CW_L = "7"
    DATA_L = "8"
    RTTY_U = "9"
    DATA_FM = "A"
    FM_N = "B"
    DATA_U = "C"
    AM_N = "D"
    PSK = "E"
    DATA_FM_N = "F"


@dataclass(frozen=True)
class ModeUpdate:
    mode: OperatingMode


class Preamp(Enum):
    IPO = "0"
    AMP1 = "1"
    AMP2 = "2"


@dataclass(frozen=True)
class PreampUpdate:
    setting: Preamp


class Attenuator(Enum):
    OFF = "0"
    DB6 = "1"
    DB12 = "2"
    DB18 = "3"


@dataclass(frozen=True)
class AttenuatorUpdate:
    setting: Attenuator


class AgcSet(Enum):
    OFF = "0"
    FAST = "1"
    MID = "2"
    SLOW = "3"
    AUTO = "4"


class AgcReport(Enum):
    OFF = "0"
    FAST = "1"
    MID = "2"
    SLOW = "3"
    AUTO_FAST = "4"
    AUTO_MID = "5"
    AUTO_SLOW = "6"


@dataclass(frozen=True)
class AgcUpdate:
    report: AgcReport


@dataclass(frozen=True)
class NbUpdate:
    enabled: bool


@dataclass(frozen=True)
class NbLevelUpdate:
    level: int


@dataclass(frozen=True)
class NrUpdate:
    enabled: bool


@dataclass(frozen=True)
class NrLevelUpdate:
    level: int


RadioUpdate = Union[
    "ScopeSpanUpdate",
    "ScopeRefLevelUpdate",
    "ScopeModeUpdate",
    "VfoFreqUpdate",
    "ModeUpdate",
    "PreampUpdate",
    "AttenuatorUpdate",
    "AgcUpdate",
    "NbUpdate",
    "NbLevelUpdate",
    "NrUpdate",
    "NrLevelUpdate",
    "UnknownFrame",
]


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


def encode_set_scope_mode(mode: ScopeMode) -> bytes:
    return f"SS06{mode.value}0000;".encode("ascii")


def encode_read_scope_mode() -> bytes:
    return b"SS06;"


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


def encode_set_mode(mode: OperatingMode) -> bytes:
    return f"MD0{mode.value};".encode("ascii")


def encode_read_mode() -> bytes:
    return b"MD0;"


def encode_set_preamp(setting: Preamp) -> bytes:
    return f"PA0{setting.value};".encode("ascii")


def encode_read_preamp() -> bytes:
    return b"PA0;"


def encode_set_attenuator(setting: Attenuator) -> bytes:
    return f"RA0{setting.value};".encode("ascii")


def encode_read_attenuator() -> bytes:
    return b"RA0;"


def encode_set_agc(setting: AgcSet) -> bytes:
    return f"GT0{setting.value};".encode("ascii")


def encode_read_agc() -> bytes:
    return b"GT0;"


def encode_set_nb(enabled: bool) -> bytes:
    return b"NB01;" if enabled else b"NB00;"


def encode_read_nb() -> bytes:
    return b"NB0;"


def encode_set_nb_level(level: int) -> bytes:
    if not (0 <= level <= 10):
        raise ValueError(f"NB level {level} out of range 0..10")
    return f"NL00{level:02d};".encode("ascii")


def encode_read_nb_level() -> bytes:
    return b"NL0;"


def encode_set_nr(enabled: bool) -> bytes:
    return b"NR01;" if enabled else b"NR00;"


def encode_read_nr() -> bytes:
    return b"NR0;"


def encode_set_nr_level(level: int) -> bytes:
    if not (1 <= level <= 15):
        raise ValueError(f"NR level {level} out of range 1..15")
    return f"RL0{level:02d};".encode("ascii")


def encode_read_nr_level() -> bytes:
    return b"RL0;"


def _parse_vfo(frame: bytes) -> "VfoFreqUpdate | None":
    if len(frame) != 12 or frame[-1:] != b";":
        return None
    prefix = frame[:2]
    if prefix not in (b"FA", b"FB"):
        return None
    digits = frame[2:11]
    if not digits.isdigit():
        return None
    hz = int(digits)
    vfo = "A" if prefix == b"FA" else "B"
    return VfoFreqUpdate(vfo=vfo, hz=hz)


def _parse_ref_level(frame: bytes) -> "ScopeRefLevelUpdate | None":
    if len(frame) != 10 or frame[:4] != b"SS04" or frame[-1:] != b";":
        return None
    body = frame[4:9].decode("ascii", errors="replace")
    if len(body) != 5 or body[0] not in "+-" or body[3] != ".":
        return None
    if not (body[1:3].isdigit() and body[4].isdigit()):
        return None
    mag = int(body[1:3]) + int(body[4]) / 10.0
    db = mag if body[0] == "+" else -mag
    if not (-30.0 <= db <= 30.0):
        return None
    return ScopeRefLevelUpdate(level_db=db)


def decode(frame: bytes) -> RadioUpdate:
    if len(frame) == 10 and frame[:4] == b"SS05" and frame[-1:] == b";":
        digit = chr(frame[4])
        if digit in _SPAN_KHZ_BY_DIGIT and frame[5:9] == b"0000":
            return ScopeSpanUpdate(span_khz=_SPAN_KHZ_BY_DIGIT[digit])
    ref = _parse_ref_level(frame)
    if ref is not None:
        return ref
    if len(frame) == 10 and frame[:4] == b"SS06" and frame[-1:] == b";" and frame[5:9] == b"0000":
        digit = chr(frame[4])
        try:
            return ScopeModeUpdate(mode=ScopeMode(digit))
        except ValueError:
            pass
    vfo = _parse_vfo(frame)
    if vfo is not None:
        return vfo
    if len(frame) == 5 and frame[:3] == b"MD0" and frame[-1:] == b";":
        digit = chr(frame[3])
        try:
            return ModeUpdate(mode=OperatingMode(digit))
        except ValueError:
            pass
    if len(frame) == 5 and frame[:3] == b"PA0" and frame[-1:] == b";":
        digit = chr(frame[3])
        try:
            return PreampUpdate(setting=Preamp(digit))
        except ValueError:
            pass
    if len(frame) == 5 and frame[:3] == b"RA0" and frame[-1:] == b";":
        digit = chr(frame[3])
        try:
            return AttenuatorUpdate(setting=Attenuator(digit))
        except ValueError:
            pass
    if len(frame) == 5 and frame[:3] == b"GT0" and frame[-1:] == b";":
        digit = chr(frame[3])
        try:
            return AgcUpdate(report=AgcReport(digit))
        except ValueError:
            pass
    if len(frame) == 5 and frame[:3] == b"NB0" and frame[-1:] == b";" and frame[3:4] in (b"0", b"1"):
        return NbUpdate(enabled=(frame[3:4] == b"1"))
    if len(frame) == 7 and frame[:3] == b"NL0" and frame[-1:] == b";" and frame[3:4] == b"0" and frame[4:6].isdigit():
        level = int(frame[4:6])
        if 0 <= level <= 10:
            return NbLevelUpdate(level=level)
    if len(frame) == 5 and frame[:3] == b"NR0" and frame[-1:] == b";" and frame[3:4] in (b"0", b"1"):
        return NrUpdate(enabled=(frame[3:4] == b"1"))
    if len(frame) == 6 and frame[:3] == b"RL0" and frame[-1:] == b";" and frame[3:5].isdigit():
        level = int(frame[3:5])
        if 1 <= level <= 15:
            return NrLevelUpdate(level=level)
    return UnknownFrame(raw=frame)
