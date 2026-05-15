import asyncio

import pytest

from ft710ctl.radio.commands import Radio
from tests.fake_serial import FakeSerial


async def test_set_span_writes_and_reads_back():
    fs = FakeSerial()
    fs.on(b"SS05;", b"SS0560000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_span_khz(100)
    await asyncio.sleep(0.05)
    assert radio.state.scope.span_khz == 100
    await radio.stop()


async def test_set_span_invalid_raises_before_sending():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_span_khz(3)
    assert fs.writes == []  # validation happens pre-wire
    await radio.stop()


async def test_stop_awaits_consumer_cleanup():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.stop()
    assert radio._consumer.done()


# ---------- SS sub-function verbs (scope panel) ----------


async def test_set_ref_level_db_round_trip():
    fs = FakeSerial()
    fs.on(b"SS04;", b"SS04-05.5;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_ref_level_db(-5.5)
    await asyncio.sleep(0.05)
    assert radio.state.scope.ref_level_db == -5.5
    await radio.stop()


async def test_set_ref_level_db_invalid_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_ref_level_db(31.0)
    assert fs.writes == []
    await radio.stop()


async def test_set_scope_mode_round_trip():
    from ft710ctl.radio import protocol
    fs = FakeSerial()
    fs.on(b"SS06;", b"SS0640000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_scope_mode(protocol.ScopeMode.WF_CENTER_NORMAL)
    await asyncio.sleep(0.05)
    assert radio.state.scope.mode == protocol.ScopeMode.WF_CENTER_NORMAL
    await radio.stop()


async def test_set_scope_mode_non_enum_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(TypeError):
        await radio.set_scope_mode("WF_CENTER_NORMAL")
    assert fs.writes == []
    await radio.stop()


async def test_set_scope_speed_round_trip():
    from ft710ctl.radio import protocol
    fs = FakeSerial()
    fs.on(b"SS00;", b"SS0020000;")  # FAST1
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_scope_speed(protocol.ScopeSpeed.FAST1)
    await asyncio.sleep(0.05)
    assert radio.state.scope.speed == protocol.ScopeSpeed.FAST1
    await radio.stop()


async def test_set_scope_speed_non_enum_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(TypeError):
        await radio.set_scope_speed("FAST1")
    assert fs.writes == []
    await radio.stop()


async def test_set_scope_peak_round_trip():
    from ft710ctl.radio import protocol
    fs = FakeSerial()
    fs.on(b"SS01;", b"SS0120000;")  # LV3
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_scope_peak(protocol.ScopePeak.LV3)
    await asyncio.sleep(0.05)
    assert radio.state.scope.peak == protocol.ScopePeak.LV3
    await radio.stop()


async def test_set_scope_peak_non_enum_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(TypeError):
        await radio.set_scope_peak("LV3")
    assert fs.writes == []
    await radio.stop()


async def test_set_scope_marker_on_round_trip():
    fs = FakeSerial()
    fs.on(b"SS02;", b"SS0210000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_scope_marker(True)
    await asyncio.sleep(0.05)
    assert radio.state.scope.marker is True
    await radio.stop()


async def test_set_scope_marker_off_round_trip():
    fs = FakeSerial()
    fs.on(b"SS02;", b"SS0200000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_scope_marker(False)
    await asyncio.sleep(0.05)
    assert radio.state.scope.marker is False
    await radio.stop()


async def test_set_scope_color_round_trip():
    fs = FakeSerial()
    fs.on(b"SS03;", b"SS0340000;")  # color 5 (digit "4")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_scope_color(5)
    await asyncio.sleep(0.05)
    assert radio.state.scope.color == 5
    await radio.stop()


async def test_set_scope_color_invalid_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_scope_color(12)
    assert fs.writes == []
    await radio.stop()


async def test_set_af_fft_mode_round_trip():
    from ft710ctl.radio import protocol
    fs = FakeSerial()
    fs.on(b"SS07;", b"SS0730000;")  # OSC_0DB, osc_time=0
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_af_fft_mode(protocol.AfFftMode.OSC_0DB)
    await asyncio.sleep(0.05)
    assert radio.state.scope.af_fft.mode == protocol.AfFftMode.OSC_0DB
    await radio.stop()


async def test_set_af_fft_mode_non_enum_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(TypeError):
        await radio.set_af_fft_mode("OSC_0DB")
    assert fs.writes == []
    await radio.stop()


# ---------- VFO, mode, band, swap, split ----------


async def test_set_vfo_a_round_trip():
    fs = FakeSerial()
    fs.on(b"FA;", b"FA014250000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_vfo_a_hz(14_250_000)
    await asyncio.sleep(0.05)
    assert radio.state.tuning.vfo_a_hz == 14_250_000
    await radio.stop()


async def test_set_vfo_a_invalid_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_vfo_a_hz(20_000)
    assert fs.writes == []
    await radio.stop()


async def test_set_vfo_b_round_trip():
    fs = FakeSerial()
    fs.on(b"FB;", b"FB007074000;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_vfo_b_hz(7_074_000)
    await asyncio.sleep(0.05)
    assert radio.state.tuning.vfo_b_hz == 7_074_000
    await radio.stop()


async def test_set_vfo_b_invalid_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(ValueError):
        await radio.set_vfo_b_hz(80_000_000)
    assert fs.writes == []
    await radio.stop()


async def test_set_mode_round_trip():
    from ft710ctl.radio import protocol
    fs = FakeSerial()
    fs.on(b"MD0;", b"MD02;")  # USB
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_mode(protocol.OperatingMode.USB)
    await asyncio.sleep(0.05)
    assert radio.state.tuning.mode == protocol.OperatingMode.USB
    await radio.stop()


async def test_set_mode_non_enum_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(TypeError):
        await radio.set_mode("USB")
    assert fs.writes == []
    await radio.stop()


async def test_set_band_writes_bytes():
    from ft710ctl.radio import protocol
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_band(protocol.Band.M20)
    await asyncio.sleep(0.05)
    assert b"BS05;" in fs.writes
    await radio.stop()


async def test_set_band_non_enum_no_writes():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    with pytest.raises(TypeError):
        await radio.set_band("M20")
    assert fs.writes == []
    await radio.stop()


async def test_swap_vfo_writes_one_frame():
    fs = FakeSerial()
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.swap_vfo()
    await asyncio.sleep(0.05)
    assert fs.writes == [b"SV;"]
    await radio.stop()


async def test_set_split_on_round_trip():
    fs = FakeSerial()
    fs.on(b"ST;", b"ST1;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_split(True)
    await asyncio.sleep(0.05)
    assert radio.state.tuning.split is True
    await radio.stop()


async def test_set_split_off_round_trip():
    fs = FakeSerial()
    fs.on(b"ST;", b"ST0;")
    radio = Radio(factory=lambda: fs, write_gap_s=0)
    await radio.start()
    await radio.set_split(False)
    await asyncio.sleep(0.05)
    assert radio.state.tuning.split is False
    await radio.stop()
