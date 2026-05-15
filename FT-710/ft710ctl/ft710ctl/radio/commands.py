"""High-level radio command wrapper.

Wires the protocol layer to the port and canonical state. Public verbs
(`set_*`, `snapshot`) are the only API the server layer touches.
"""
from __future__ import annotations

import asyncio
from typing import Callable

from . import protocol, state
from .port import PortClosed, RadioPort


class Radio:
    def __init__(self, factory, write_gap_s: float | None = None):
        kwargs = {"write_gap_s": write_gap_s} if write_gap_s is not None else {}
        self.port = RadioPort(factory=factory, **kwargs)
        self.state = state.RadioState()
        self._consumer: asyncio.Task | None = None
        self._subscribers: list[Callable[[dict], None]] = []

    async def start(self) -> None:
        await self.port.open()
        self._consumer = asyncio.create_task(self._consume_frames())

    async def stop(self) -> None:
        if self._consumer is not None:
            self._consumer.cancel()
            try:
                await self._consumer
            except asyncio.CancelledError:
                pass
        await self.port.close()

    def subscribe(self, callback: Callable[[dict], None]) -> None:
        self._subscribers.append(callback)

    async def _consume_frames(self) -> None:
        while True:
            try:
                frame = await self.port.next_frame()
            except PortClosed:
                return
            update = protocol.decode(frame)
            delta = self.state.apply(update)
            if delta is not None:
                for cb in list(self._subscribers):
                    try:
                        cb(delta)
                    except Exception:
                        pass

    async def set_span_khz(self, khz: int) -> None:
        frame = protocol.encode_set_span_khz(khz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_span())

    async def set_ref_level_db(self, db: float) -> None:
        frame = protocol.encode_set_ref_level_db(db)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_ref_level())

    async def set_scope_mode(self, mode: protocol.ScopeMode) -> None:
        _require_enum(mode, protocol.ScopeMode)
        await self.port.send(protocol.encode_set_scope_mode(mode))
        await self.port.send(protocol.encode_read_scope_mode())

    async def set_scope_speed(self, speed: protocol.ScopeSpeed) -> None:
        _require_enum(speed, protocol.ScopeSpeed)
        await self.port.send(protocol.encode_set_scope_speed(speed))
        await self.port.send(b"SS00;")

    async def set_scope_peak(self, peak: protocol.ScopePeak) -> None:
        _require_enum(peak, protocol.ScopePeak)
        await self.port.send(protocol.encode_set_scope_peak(peak))
        await self.port.send(b"SS01;")

    async def set_scope_marker(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_scope_marker(enabled))
        await self.port.send(b"SS02;")

    async def set_scope_color(self, color: int) -> None:
        frame = protocol.encode_set_scope_color(color)
        await self.port.send(frame)
        await self.port.send(b"SS03;")

    async def set_af_fft_mode(
        self, mode: protocol.AfFftMode, osc_time_index: int = 0
    ) -> None:
        _require_enum(mode, protocol.AfFftMode)
        await self.port.send(
            protocol.encode_set_af_fft_mode(mode, osc_time_index=osc_time_index)
        )
        await self.port.send(protocol.encode_read_af_fft())

    async def set_vfo_a_hz(self, hz: int) -> None:
        frame = protocol.encode_set_vfo_a_hz(hz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_vfo_a())

    async def set_vfo_b_hz(self, hz: int) -> None:
        frame = protocol.encode_set_vfo_b_hz(hz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_vfo_b())

    async def set_mode(self, mode: protocol.OperatingMode) -> None:
        _require_enum(mode, protocol.OperatingMode)
        await self.port.send(protocol.encode_set_mode(mode))
        await self.port.send(protocol.encode_read_mode())

    async def set_band(self, band: protocol.Band) -> None:
        _require_enum(band, protocol.Band)
        # BS has no Read form per manual; band change is reflected through
        # VFO/mode reads that snapshot will pick up. Send the Set frame only.
        await self.port.send(protocol.encode_set_band(band))

    async def swap_vfo(self) -> None:
        # No Read form. The post-swap state surface refreshes via snapshot.
        await self.port.send(protocol.encode_swap_vfo())

    async def set_split(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_split(enabled))
        await self.port.send(protocol.encode_read_split())

    # ---------- RX DSP ----------

    async def set_preamp(self, setting: protocol.Preamp) -> None:
        _require_enum(setting, protocol.Preamp)
        await self.port.send(protocol.encode_set_preamp(setting))
        await self.port.send(protocol.encode_read_preamp())

    async def set_attenuator(self, setting: protocol.Attenuator) -> None:
        _require_enum(setting, protocol.Attenuator)
        await self.port.send(protocol.encode_set_attenuator(setting))
        await self.port.send(protocol.encode_read_attenuator())

    async def set_agc(self, setting: protocol.AgcSet) -> None:
        _require_enum(setting, protocol.AgcSet)
        await self.port.send(protocol.encode_set_agc(setting))
        await self.port.send(protocol.encode_read_agc())

    async def set_nb(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_nb(enabled))
        await self.port.send(protocol.encode_read_nb())

    async def set_nb_level(self, level: int) -> None:
        frame = protocol.encode_set_nb_level(level)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_nb_level())

    async def set_nr(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_nr(enabled))
        await self.port.send(protocol.encode_read_nr())

    async def set_nr_level(self, level: int) -> None:
        frame = protocol.encode_set_nr_level(level)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_nr_level())

    async def set_manual_notch(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_manual_notch(enabled))
        await self.port.send(protocol.encode_read_manual_notch_state())

    async def set_manual_notch_freq_hz(self, freq_hz: int) -> None:
        frame = protocol.encode_set_manual_notch_freq_hz(freq_hz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_manual_notch_freq())

    async def set_auto_notch(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_auto_notch(enabled))
        await self.port.send(protocol.encode_read_auto_notch())

    async def set_contour(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_contour(enabled))
        await self.port.send(protocol.encode_read_contour_state())

    async def set_contour_freq_hz(self, freq_hz: int) -> None:
        frame = protocol.encode_set_contour_freq_hz(freq_hz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_contour_freq())

    async def set_apf(self, enabled: bool) -> None:
        await self.port.send(protocol.encode_set_apf(enabled))
        await self.port.send(protocol.encode_read_apf_state())

    async def set_apf_freq_hz(self, freq_hz: int) -> None:
        frame = protocol.encode_set_apf_freq_hz(freq_hz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_apf_freq())

    async def set_if_shift_hz(self, shift_hz: int) -> None:
        frame = protocol.encode_set_if_shift_hz(shift_hz)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_if_shift())

    async def set_filter_width(self, index: int) -> None:
        frame = protocol.encode_set_filter_width(index)
        await self.port.send(frame)
        await self.port.send(protocol.encode_read_filter_width())


def _require_enum(value, cls) -> None:
    if not isinstance(value, cls):
        raise TypeError(f"expected {cls.__name__}, got {type(value).__name__}")
