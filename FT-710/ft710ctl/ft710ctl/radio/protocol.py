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


@dataclass(frozen=True)
class ManualNotchUpdate:
    enabled: bool


@dataclass(frozen=True)
class ManualNotchFreqUpdate:
    freq_hz: int


@dataclass(frozen=True)
class AutoNotchUpdate:
    enabled: bool


@dataclass(frozen=True)
class ContourUpdate:
    enabled: bool


@dataclass(frozen=True)
class ContourFreqUpdate:
    freq_hz: int


@dataclass(frozen=True)
class ApfUpdate:
    enabled: bool


@dataclass(frozen=True)
class ApfFreqUpdate:
    freq_hz: int


@dataclass(frozen=True)
class IfShiftUpdate:
    shift_hz: int


@dataclass(frozen=True)
class FilterWidthUpdate:
    index: int


class ScopeSpeed(Enum):
    SLOW1 = "0"
    SLOW2 = "1"
    FAST1 = "2"
    FAST2 = "3"
    FAST3 = "4"
    STOP = "5"


@dataclass(frozen=True)
class ScopeSpeedUpdate:
    speed: "ScopeSpeed"


class ScopePeak(Enum):
    LV1 = "0"
    LV2 = "1"
    LV3 = "2"
    LV4 = "3"
    LV5 = "4"


@dataclass(frozen=True)
class ScopePeakUpdate:
    peak: "ScopePeak"


@dataclass(frozen=True)
class ScopeMarkerUpdate:
    enabled: bool


@dataclass(frozen=True)
class ScopeColorUpdate:
    color: int  # 1..11


class AfFftMode(Enum):
    AF_FFT_0DB = "0"
    AF_FFT_10DB = "1"
    AF_FFT_20DB = "2"
    OSC_0DB = "3"
    OSC_10DB = "4"
    OSC_20DB = "5"


@dataclass(frozen=True)
class SmeterUpdate:
    raw: int


@dataclass(frozen=True)
class AfGainUpdate:
    value: int


@dataclass(frozen=True)
class RfGainUpdate:
    value: int


class Band(Enum):
    M160 = "00"
    M80 = "01"
    M60 = "02"
    M40 = "03"
    M30 = "04"
    M20 = "05"
    M17 = "06"
    M15 = "07"
    M12 = "08"
    M10 = "09"
    M6 = "10"
    GEN = "11"


@dataclass(frozen=True)
class SplitUpdate:
    enabled: bool


@dataclass(frozen=True)
class ClarUpdate:
    rx_enabled: bool
    tx_enabled: bool


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
    "ManualNotchUpdate",
    "ManualNotchFreqUpdate",
    "AutoNotchUpdate",
    "ContourUpdate",
    "ContourFreqUpdate",
    "ApfUpdate",
    "ApfFreqUpdate",
    "IfShiftUpdate",
    "FilterWidthUpdate",
    "SmeterUpdate",
    "AfGainUpdate",
    "RfGainUpdate",
    "SplitUpdate",
    "ClarUpdate",
    "ScopeSpeedUpdate",
    "ScopePeakUpdate",
    "ScopeMarkerUpdate",
    "ScopeColorUpdate",
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


def encode_set_manual_notch(enabled: bool) -> bytes:
    return b"BP00001;" if enabled else b"BP00000;"


def encode_set_manual_notch_freq_hz(freq_hz: int) -> bytes:
    if not (10 <= freq_hz <= 3200):
        raise ValueError(f"manual notch freq {freq_hz} Hz out of range 10..3200")
    if freq_hz % 10 != 0:
        raise ValueError(f"manual notch freq {freq_hz} Hz not on 10 Hz grid")
    return f"BP01{freq_hz // 10:03d};".encode("ascii")


def encode_read_manual_notch_state() -> bytes:
    return b"BP00;"


def encode_read_manual_notch_freq() -> bytes:
    return b"BP01;"


def encode_set_auto_notch(enabled: bool) -> bytes:
    return b"BC01;" if enabled else b"BC00;"


def encode_read_auto_notch() -> bytes:
    return b"BC0;"


def encode_set_contour(enabled: bool) -> bytes:
    return b"CO000001;" if enabled else b"CO000000;"


def encode_set_contour_freq_hz(freq_hz: int) -> bytes:
    if not (10 <= freq_hz <= 3200):
        raise ValueError(f"contour freq {freq_hz} Hz out of range 10..3200")
    return f"CO01{freq_hz:04d};".encode("ascii")


def encode_set_apf(enabled: bool) -> bytes:
    return b"CO020001;" if enabled else b"CO020000;"


def encode_set_apf_freq_hz(freq_hz: int) -> bytes:
    if not (-250 <= freq_hz <= 250):
        raise ValueError(f"APF freq {freq_hz} Hz out of range -250..+250")
    if freq_hz % 10 != 0:
        raise ValueError(f"APF freq {freq_hz} Hz not on 10 Hz grid")
    value = (freq_hz // 10) + 25
    return f"CO03{value:04d};".encode("ascii")


def encode_read_contour_state() -> bytes:
    return b"CO00;"


def encode_read_contour_freq() -> bytes:
    return b"CO01;"


def encode_read_apf_state() -> bytes:
    return b"CO02;"


def encode_read_apf_freq() -> bytes:
    return b"CO03;"


def encode_set_if_shift_hz(shift_hz: int) -> bytes:
    if not (-1200 <= shift_hz <= 1200):
        raise ValueError(f"IF shift {shift_hz} Hz out of range -1200..+1200")
    if shift_hz % 20 != 0:
        raise ValueError(f"IF shift {shift_hz} Hz not on 20 Hz grid")
    sign = "+" if shift_hz >= 0 else "-"
    return f"IS00{sign}{abs(shift_hz):04d};".encode("ascii")


def encode_read_if_shift() -> bytes:
    return b"IS0;"


def encode_set_filter_width(index: int) -> bytes:
    if not (0 <= index <= 23):
        raise ValueError(f"filter width index {index} out of range 0..23")
    return f"SH00{index:02d};".encode("ascii")


def encode_read_filter_width() -> bytes:
    return b"SH0;"


def encode_set_scope_speed(speed: ScopeSpeed) -> bytes:
    return f"SS00{speed.value}0000;".encode("ascii")


def encode_set_scope_peak(peak: ScopePeak) -> bytes:
    return f"SS01{peak.value}0000;".encode("ascii")


def encode_set_scope_marker(enabled: bool) -> bytes:
    return b"SS0210000;" if enabled else b"SS0200000;"


def encode_set_scope_color(color: int) -> bytes:
    if not (1 <= color <= 11):
        raise ValueError(f"scope color {color} out of range 1..11")
    digit = "0123456789A"[color - 1]
    return f"SS03{digit}0000;".encode("ascii")


def encode_set_af_fft_mode(mode: AfFftMode, osc_time_index: int = 0) -> bytes:
    # SS07 10-byte frame: SS 0 7 P3 P4 P5 P6 P7 ;
    #   P3       = mode digit (AF-FFT/OSC level)
    #   P4 - P5  = 2-digit OSC time index "00".."05" (1/3/10/30/100/300 ms)
    #   P6 - P7  = fixed "00"
    if not (0 <= osc_time_index <= 5):
        raise ValueError(f"osc_time_index {osc_time_index} out of range 0..5")
    return f"SS07{mode.value}{osc_time_index:02d}00;".encode("ascii")


def encode_read_af_fft() -> bytes:
    return b"SS07;"


def encode_read_smeter() -> bytes:
    return b"SM0;"


def encode_set_af_gain(value: int) -> bytes:
    if not (0 <= value <= 255):
        raise ValueError(f"AF gain {value} out of range 0..255")
    return f"AG0{value:03d};".encode("ascii")


def encode_read_af_gain() -> bytes:
    return b"AG0;"


def encode_set_rf_gain(value: int) -> bytes:
    if not (0 <= value <= 255):
        raise ValueError(f"RF gain {value} out of range 0..255")
    return f"RG0{value:03d};".encode("ascii")


def encode_read_rf_gain() -> bytes:
    return b"RG0;"


def encode_set_band(band: Band) -> bytes:
    return f"BS{band.value};".encode("ascii")


def encode_swap_vfo() -> bytes:
    return b"SV;"


def encode_set_split(enabled: bool) -> bytes:
    return b"ST1;" if enabled else b"ST0;"


def encode_read_split() -> bytes:
    return b"ST;"


def encode_set_rx_clar(enabled: bool) -> bytes:
    # P1=0 main band, P2=0, P3=0 CLAR setting mode, P4=RX, P5=TX (always 0 in v1), P6-P8=0.
    p4 = "1" if enabled else "0"
    return f"CF000{p4}0000;".encode("ascii")


def encode_read_clar() -> bytes:
    return b"CF000;"


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
    if len(frame) == 10 and frame[:2] == b"SS" and frame[-1:] == b";" and frame[5:9] == b"0000":
        sub = frame[2:4]
        digit = chr(frame[4])
        if sub == b"00":
            try:
                return ScopeSpeedUpdate(speed=ScopeSpeed(digit))
            except ValueError:
                pass
        if sub == b"01":
            try:
                return ScopePeakUpdate(peak=ScopePeak(digit))
            except ValueError:
                pass
        if sub == b"02" and digit in ("0", "1"):
            return ScopeMarkerUpdate(enabled=(digit == "1"))
        if sub == b"03" and digit in "0123456789A":
            return ScopeColorUpdate(color="0123456789A".index(digit) + 1)
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
    if len(frame) == 8 and frame[:4] == b"BP00" and frame[-1:] == b";" and frame[4:7] in (b"000", b"001"):
        return ManualNotchUpdate(enabled=(frame[4:7] == b"001"))
    if len(frame) == 8 and frame[:4] == b"BP01" and frame[-1:] == b";" and frame[4:7].isdigit():
        units = int(frame[4:7])
        if 1 <= units <= 320:
            return ManualNotchFreqUpdate(freq_hz=units * 10)
    if len(frame) == 5 and frame[:3] == b"BC0" and frame[-1:] == b";" and frame[3:4] in (b"0", b"1"):
        return AutoNotchUpdate(enabled=(frame[3:4] == b"1"))
    if len(frame) == 9 and frame[:4] == b"CO00" and frame[-1:] == b";" and frame[4:8] in (b"0000", b"0001"):
        return ContourUpdate(enabled=(frame[4:8] == b"0001"))
    if len(frame) == 9 and frame[:4] == b"CO01" and frame[-1:] == b";" and frame[4:8].isdigit():
        hz = int(frame[4:8])
        if 10 <= hz <= 3200:
            return ContourFreqUpdate(freq_hz=hz)
    if len(frame) == 9 and frame[:4] == b"CO02" and frame[-1:] == b";" and frame[4:8] in (b"0000", b"0001"):
        return ApfUpdate(enabled=(frame[4:8] == b"0001"))
    if len(frame) == 9 and frame[:4] == b"CO03" and frame[-1:] == b";" and frame[4:8].isdigit():
        v = int(frame[4:8])
        if 0 <= v <= 50:
            return ApfFreqUpdate(freq_hz=(v - 25) * 10)
    if len(frame) == 10 and frame[:4] == b"IS00" and frame[-1:] == b";" and frame[4:5] in (b"+", b"-") and frame[5:9].isdigit():
        mag = int(frame[5:9])
        if 0 <= mag <= 1200 and mag % 20 == 0:
            sign = 1 if frame[4:5] == b"+" else -1
            return IfShiftUpdate(shift_hz=sign * mag)
    if len(frame) == 7 and frame[:4] == b"SH00" and frame[-1:] == b";" and frame[4:6].isdigit():
        idx = int(frame[4:6])
        if 0 <= idx <= 23:
            return FilterWidthUpdate(index=idx)
    if len(frame) == 7 and frame[:3] == b"SM0" and frame[-1:] == b";" and frame[3:6].isdigit():
        raw = int(frame[3:6])
        if 0 <= raw <= 255:
            return SmeterUpdate(raw=raw)
    if len(frame) == 7 and frame[:3] == b"AG0" and frame[-1:] == b";" and frame[3:6].isdigit():
        v = int(frame[3:6])
        if 0 <= v <= 255:
            return AfGainUpdate(value=v)
    if len(frame) == 7 and frame[:3] == b"RG0" and frame[-1:] == b";" and frame[3:6].isdigit():
        v = int(frame[3:6])
        if 0 <= v <= 255:
            return RfGainUpdate(value=v)
    if len(frame) == 4 and frame[:2] == b"ST" and frame[-1:] == b";" and frame[2:3] in (b"0", b"1"):
        return SplitUpdate(enabled=(frame[2:3] == b"1"))
    if (
        len(frame) == 11
        and frame[:5] == b"CF000"
        and frame[-1:] == b";"
        and frame[5:6] in (b"0", b"1")
        and frame[6:7] in (b"0", b"1")
        and frame[7:10] == b"000"
    ):
        return ClarUpdate(
            rx_enabled=(frame[5:6] == b"1"),
            tx_enabled=(frame[6:7] == b"1"),
        )
    return UnknownFrame(raw=frame)
