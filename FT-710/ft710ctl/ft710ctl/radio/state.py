"""Canonical radio state + apply() dispatch.

State is updated only by feeding protocol updates to apply().
apply() returns a delta dict {field: dotted-path, value: new-value} for
WebSocket broadcast, or None if the update is unknown / not applicable.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum

from . import protocol


@dataclass
class AfFftState:
    mode: protocol.AfFftMode | None = None
    osc_time_index: int = 0


@dataclass
class ScopeState:
    span_khz: int | None = None
    ref_level_db: float | None = None
    mode: protocol.ScopeMode | None = None
    speed: protocol.ScopeSpeed | None = None
    peak: protocol.ScopePeak | None = None
    color: int | None = None
    marker: bool | None = None
    af_fft: AfFftState = field(default_factory=AfFftState)


@dataclass
class TuningState:
    vfo_a_hz: int | None = None
    vfo_b_hz: int | None = None
    mode: protocol.OperatingMode | None = None
    split: bool | None = None
    clar_rx_enabled: bool | None = None
    clar_tx_enabled: bool | None = None


@dataclass
class RxDspState:
    preamp: protocol.Preamp | None = None
    attenuator: protocol.Attenuator | None = None
    agc: protocol.AgcReport | None = None
    nb_enabled: bool | None = None
    nb_level: int | None = None
    nr_enabled: bool | None = None
    nr_level: int | None = None
    manual_notch_enabled: bool | None = None
    manual_notch_freq_hz: int | None = None
    auto_notch_enabled: bool | None = None
    contour_enabled: bool | None = None
    contour_freq_hz: int | None = None
    apf_enabled: bool | None = None
    apf_freq_hz: int | None = None
    if_shift_hz: int | None = None
    filter_width_index: int | None = None


@dataclass
class MetersState:
    smeter_raw: int | None = None
    af_gain: int | None = None
    rf_gain: int | None = None


@dataclass
class RadioState:
    scope: ScopeState = field(default_factory=ScopeState)
    tuning: TuningState = field(default_factory=TuningState)
    rx: RxDspState = field(default_factory=RxDspState)
    meters: MetersState = field(default_factory=MetersState)

    def apply(self, update) -> dict | None:
        path, value = _apply_update(self, update)
        if path is None:
            return None
        return {"field": path, "value": value}


def to_jsonable(value):
    """Convert a state value (or nested dataclass / enum) to JSON-safe primitives."""
    if isinstance(value, Enum):
        return value.name
    if is_dataclass(value):
        return {f.name: to_jsonable(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return value


def _apply_update(rs: RadioState, update):
    # Scope
    if isinstance(update, protocol.ScopeSpanUpdate):
        rs.scope.span_khz = update.span_khz
        return "scope.span_khz", update.span_khz
    if isinstance(update, protocol.ScopeRefLevelUpdate):
        rs.scope.ref_level_db = update.level_db
        return "scope.ref_level_db", update.level_db
    if isinstance(update, protocol.ScopeModeUpdate):
        rs.scope.mode = update.mode
        return "scope.mode", update.mode
    if isinstance(update, protocol.ScopeSpeedUpdate):
        rs.scope.speed = update.speed
        return "scope.speed", update.speed
    if isinstance(update, protocol.ScopePeakUpdate):
        rs.scope.peak = update.peak
        return "scope.peak", update.peak
    if isinstance(update, protocol.ScopeMarkerUpdate):
        rs.scope.marker = update.enabled
        return "scope.marker", update.enabled
    if isinstance(update, protocol.ScopeColorUpdate):
        rs.scope.color = update.color
        return "scope.color", update.color
    if isinstance(update, protocol.AfFftUpdate):
        rs.scope.af_fft.mode = update.mode
        rs.scope.af_fft.osc_time_index = update.osc_time_index
        return "scope.af_fft", rs.scope.af_fft
    # Tuning
    if isinstance(update, protocol.VfoFreqUpdate):
        if update.vfo == "A":
            rs.tuning.vfo_a_hz = update.hz
            return "tuning.vfo_a_hz", update.hz
        rs.tuning.vfo_b_hz = update.hz
        return "tuning.vfo_b_hz", update.hz
    if isinstance(update, protocol.ModeUpdate):
        rs.tuning.mode = update.mode
        return "tuning.mode", update.mode
    if isinstance(update, protocol.SplitUpdate):
        rs.tuning.split = update.enabled
        return "tuning.split", update.enabled
    if isinstance(update, protocol.ClarUpdate):
        rs.tuning.clar_rx_enabled = update.rx_enabled
        rs.tuning.clar_tx_enabled = update.tx_enabled
        return "tuning.clar", {"rx": update.rx_enabled, "tx": update.tx_enabled}
    # RX DSP
    if isinstance(update, protocol.PreampUpdate):
        rs.rx.preamp = update.setting
        return "rx.preamp", update.setting
    if isinstance(update, protocol.AttenuatorUpdate):
        rs.rx.attenuator = update.setting
        return "rx.attenuator", update.setting
    if isinstance(update, protocol.AgcUpdate):
        rs.rx.agc = update.report
        return "rx.agc", update.report
    if isinstance(update, protocol.NbUpdate):
        rs.rx.nb_enabled = update.enabled
        return "rx.nb_enabled", update.enabled
    if isinstance(update, protocol.NbLevelUpdate):
        rs.rx.nb_level = update.level
        return "rx.nb_level", update.level
    if isinstance(update, protocol.NrUpdate):
        rs.rx.nr_enabled = update.enabled
        return "rx.nr_enabled", update.enabled
    if isinstance(update, protocol.NrLevelUpdate):
        rs.rx.nr_level = update.level
        return "rx.nr_level", update.level
    if isinstance(update, protocol.ManualNotchUpdate):
        rs.rx.manual_notch_enabled = update.enabled
        return "rx.manual_notch_enabled", update.enabled
    if isinstance(update, protocol.ManualNotchFreqUpdate):
        rs.rx.manual_notch_freq_hz = update.freq_hz
        return "rx.manual_notch_freq_hz", update.freq_hz
    if isinstance(update, protocol.AutoNotchUpdate):
        rs.rx.auto_notch_enabled = update.enabled
        return "rx.auto_notch_enabled", update.enabled
    if isinstance(update, protocol.ContourUpdate):
        rs.rx.contour_enabled = update.enabled
        return "rx.contour_enabled", update.enabled
    if isinstance(update, protocol.ContourFreqUpdate):
        rs.rx.contour_freq_hz = update.freq_hz
        return "rx.contour_freq_hz", update.freq_hz
    if isinstance(update, protocol.ApfUpdate):
        rs.rx.apf_enabled = update.enabled
        return "rx.apf_enabled", update.enabled
    if isinstance(update, protocol.ApfFreqUpdate):
        rs.rx.apf_freq_hz = update.freq_hz
        return "rx.apf_freq_hz", update.freq_hz
    if isinstance(update, protocol.IfShiftUpdate):
        rs.rx.if_shift_hz = update.shift_hz
        return "rx.if_shift_hz", update.shift_hz
    if isinstance(update, protocol.FilterWidthUpdate):
        rs.rx.filter_width_index = update.index
        return "rx.filter_width_index", update.index
    # Meters + gain
    if isinstance(update, protocol.SmeterUpdate):
        rs.meters.smeter_raw = update.raw
        return "meters.smeter_raw", update.raw
    if isinstance(update, protocol.AfGainUpdate):
        rs.meters.af_gain = update.value
        return "meters.af_gain", update.value
    if isinstance(update, protocol.RfGainUpdate):
        rs.meters.rf_gain = update.value
        return "meters.rf_gain", update.value
    return None, None
