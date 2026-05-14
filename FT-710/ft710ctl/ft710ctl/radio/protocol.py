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


RadioUpdate = Union["UnknownFrame"]


def decode(frame: bytes) -> RadioUpdate:
    return UnknownFrame(raw=frame)
