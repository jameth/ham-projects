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


RadioUpdate = Union["ScopeSpanUpdate", "UnknownFrame"]


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


def decode(frame: bytes) -> RadioUpdate:
    if len(frame) == 10 and frame[:4] == b"SS05" and frame[-1:] == b";":
        digit = chr(frame[4])
        if digit in _SPAN_KHZ_BY_DIGIT and frame[5:9] == b"0000":
            return ScopeSpanUpdate(span_khz=_SPAN_KHZ_BY_DIGIT[digit])
    return UnknownFrame(raw=frame)
