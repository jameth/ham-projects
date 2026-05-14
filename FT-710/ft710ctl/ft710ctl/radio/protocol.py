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


@dataclass(frozen=True)
class ScopeSpanUpdate:
    span_khz: int


@dataclass(frozen=True)
class ScopeRefLevelUpdate:
    level_db: float


RadioUpdate = Union["ScopeSpanUpdate", "ScopeRefLevelUpdate", "UnknownFrame"]


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
    return UnknownFrame(raw=frame)
