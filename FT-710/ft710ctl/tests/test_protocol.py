import pytest

from ft710ctl.radio import protocol


def test_decode_unknown_frame():
    result = protocol.decode(b"XX0;")
    assert isinstance(result, protocol.UnknownFrame)
    assert result.raw == b"XX0;"


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


AGC_SET_CASES = [
    ("OFF", "0"), ("FAST", "1"), ("MID", "2"), ("SLOW", "3"), ("AUTO", "4"),
]
AGC_REPORT_CASES = [
    ("OFF", "0"), ("FAST", "1"), ("MID", "2"), ("SLOW", "3"),
    ("AUTO_FAST", "4"), ("AUTO_MID", "5"), ("AUTO_SLOW", "6"),
]


@pytest.mark.parametrize("name,digit", AGC_SET_CASES)
def test_encode_set_agc(name, digit):
    setting = protocol.AgcSet[name]
    assert protocol.encode_set_agc(setting) == f"GT0{digit};".encode("ascii")


def test_encode_set_agc_rejects_auto_resolved():
    # AUTO_FAST/MID/SLOW are Answer-only; not members of the Set enum.
    # Attribute access on a missing Enum member raises AttributeError.
    with pytest.raises(AttributeError):
        protocol.AgcSet.AUTO_FAST  # type: ignore[attr-defined]


@pytest.mark.parametrize("name,digit", AGC_REPORT_CASES)
def test_decode_agc(name, digit):
    report = protocol.AgcReport[name]
    assert protocol.decode(f"GT0{digit};".encode("ascii")) == protocol.AgcUpdate(report=report)


def test_encode_read_agc():
    assert protocol.encode_read_agc() == b"GT0;"


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


def test_encode_set_manual_notch_on():
    assert protocol.encode_set_manual_notch(True) == b"BP00001;"


def test_encode_set_manual_notch_off():
    assert protocol.encode_set_manual_notch(False) == b"BP00000;"


def test_encode_set_manual_notch_freq():
    assert protocol.encode_set_manual_notch_freq_hz(1500) == b"BP01150;"
    assert protocol.encode_set_manual_notch_freq_hz(10) == b"BP01001;"


def test_encode_read_manual_notch_state():
    assert protocol.encode_read_manual_notch_state() == b"BP00;"


def test_encode_read_manual_notch_freq():
    assert protocol.encode_read_manual_notch_freq() == b"BP01;"


def test_decode_manual_notch_freq():
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
        protocol.encode_set_contour_freq_hz(5)
    with pytest.raises(ValueError):
        protocol.encode_set_contour_freq_hz(3201)


def test_encode_set_apf_on():
    assert protocol.encode_set_apf(True) == b"CO020001;"


def test_encode_set_apf_freq():
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


def test_encode_set_if_shift_zero():
    assert protocol.encode_set_if_shift_hz(0) == b"IS00+0000;"


def test_encode_set_if_shift_positive():
    assert protocol.encode_set_if_shift_hz(1000) == b"IS00+1000;"


def test_encode_set_if_shift_negative():
    assert protocol.encode_set_if_shift_hz(-1000) == b"IS00-1000;"


def test_encode_set_if_shift_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_if_shift_hz(1220)
    with pytest.raises(ValueError):
        protocol.encode_set_if_shift_hz(-1220)


def test_encode_set_if_shift_rejects_non_20hz_step():
    with pytest.raises(ValueError):
        protocol.encode_set_if_shift_hz(15)


def test_encode_read_if_shift():
    assert protocol.encode_read_if_shift() == b"IS0;"


def test_decode_if_shift():
    assert protocol.decode(b"IS00+1000;") == protocol.IfShiftUpdate(shift_hz=1000)


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


SCOPE_SPEED_CASES = [
    ("SLOW1", "0"), ("SLOW2", "1"), ("FAST1", "2"),
    ("FAST2", "3"), ("FAST3", "4"), ("STOP", "5"),
]


@pytest.mark.parametrize("name,digit", SCOPE_SPEED_CASES)
def test_encode_set_scope_speed(name, digit):
    speed = protocol.ScopeSpeed[name]
    assert protocol.encode_set_scope_speed(speed) == f"SS00{digit}0000;".encode("ascii")


@pytest.mark.parametrize("name,digit", SCOPE_SPEED_CASES)
def test_decode_scope_speed(name, digit):
    speed = protocol.ScopeSpeed[name]
    frame = f"SS00{digit}0000;".encode("ascii")
    assert protocol.decode(frame) == protocol.ScopeSpeedUpdate(speed=speed)


SCOPE_PEAK_CASES = [
    ("LV1", "0"), ("LV2", "1"), ("LV3", "2"), ("LV4", "3"), ("LV5", "4"),
]


@pytest.mark.parametrize("name,digit", SCOPE_PEAK_CASES)
def test_encode_set_scope_peak(name, digit):
    peak = protocol.ScopePeak[name]
    assert protocol.encode_set_scope_peak(peak) == f"SS01{digit}0000;".encode("ascii")


@pytest.mark.parametrize("name,digit", SCOPE_PEAK_CASES)
def test_decode_scope_peak(name, digit):
    peak = protocol.ScopePeak[name]
    frame = f"SS01{digit}0000;".encode("ascii")
    assert protocol.decode(frame) == protocol.ScopePeakUpdate(peak=peak)


def test_encode_set_scope_marker():
    assert protocol.encode_set_scope_marker(True) == b"SS0210000;"
    assert protocol.encode_set_scope_marker(False) == b"SS0200000;"


def test_decode_scope_marker():
    assert protocol.decode(b"SS0210000;") == protocol.ScopeMarkerUpdate(enabled=True)
    assert protocol.decode(b"SS0200000;") == protocol.ScopeMarkerUpdate(enabled=False)


SCOPE_COLOR_CASES = [
    (1, "0"), (2, "1"), (10, "9"), (11, "A"),
]


@pytest.mark.parametrize("color,digit", SCOPE_COLOR_CASES)
def test_encode_set_scope_color(color, digit):
    assert protocol.encode_set_scope_color(color) == f"SS03{digit}0000;".encode("ascii")


@pytest.mark.parametrize("color,digit", SCOPE_COLOR_CASES)
def test_decode_scope_color(color, digit):
    frame = f"SS03{digit}0000;".encode("ascii")
    assert protocol.decode(frame) == protocol.ScopeColorUpdate(color=color)


def test_encode_set_scope_color_rejects_out_of_range():
    with pytest.raises(ValueError):
        protocol.encode_set_scope_color(12)


# SS07 byte layout per CAT manual p.21:
#   SS 0 7 P3 P4 P5 P6 P7 ;     (10 bytes total)
#   P3       = AF-FFT/OSC level mode digit (0..5)
#   P4 - P5  = 2-digit OSC time index "00".."05" (1/3/10/30/100/300 ms)
#   P6 - P7  = fixed "00"
AF_FFT_CASES = [
    ("AF_FFT_0DB", 0), ("AF_FFT_10DB", 1), ("AF_FFT_20DB", 2),
    ("OSC_0DB", 3), ("OSC_10DB", 4), ("OSC_20DB", 5),
]


@pytest.mark.parametrize("name,digit", AF_FFT_CASES)
def test_encode_set_af_fft_mode(name, digit):
    mode = protocol.AfFftMode[name]
    assert protocol.encode_set_af_fft_mode(mode) == f"SS07{digit}0000;".encode("ascii")


def test_encode_set_af_fft_mode_with_osc_time():
    # OSC_0DB mode (digit "3") at osc_time_index=2 → b"SS0730200;" (10 bytes)
    assert protocol.encode_set_af_fft_mode(protocol.AfFftMode.OSC_0DB, osc_time_index=2) == b"SS0730200;"


def test_encode_set_af_fft_mode_rejects_invalid_osc_time():
    with pytest.raises(ValueError):
        protocol.encode_set_af_fft_mode(protocol.AfFftMode.AF_FFT_0DB, osc_time_index=6)


def test_encode_read_af_fft():
    assert protocol.encode_read_af_fft() == b"SS07;"


@pytest.mark.parametrize("name,digit", AF_FFT_CASES)
def test_decode_af_fft(name, digit):
    mode = protocol.AfFftMode[name]
    frame = f"SS07{digit}0000;".encode("ascii")
    assert protocol.decode(frame) == protocol.AfFftUpdate(mode=mode, osc_time_index=0)


def test_decode_af_fft_with_osc_time():
    # Round-trip OSC_0DB with osc_time_index=3 confirms the 2-byte field.
    assert protocol.decode(b"SS0730300;") == protocol.AfFftUpdate(
        mode=protocol.AfFftMode.OSC_0DB, osc_time_index=3
    )


def test_decode_af_fft_rejects_old_11_byte_form():
    # The pre-fix encoder produced 11-byte frames; they must fall through.
    raw = b"SS07000000;"
    assert protocol.decode(raw) == protocol.UnknownFrame(raw=raw)


def test_encode_read_smeter():
    assert protocol.encode_read_smeter() == b"SM0;"


def test_decode_smeter():
    assert protocol.decode(b"SM0123;") == protocol.SmeterUpdate(raw=123)
    assert protocol.decode(b"SM0000;") == protocol.SmeterUpdate(raw=0)
    assert protocol.decode(b"SM0255;") == protocol.SmeterUpdate(raw=255)


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


def test_encode_set_rf_gain():
    assert protocol.encode_set_rf_gain(128) == b"RG0128;"


def test_encode_read_rf_gain():
    assert protocol.encode_read_rf_gain() == b"RG0;"


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


def test_encode_set_rx_clar_on():
    # CF byte layout (manual p.8): C F P1 P2 P3 P4 P5 P6 P7 P8 ;
    #   P1=0 (main band), P2=0 (fixed), P3=0 (CLAR setting mode),
    #   P4=RX CLAR (0=OFF, 1=ON), P5=TX CLAR (0=OFF, 1=ON), P6-P8=0.
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
    # SS00 Answer needs 10 bytes; this 9-byte frame must fall through
    assert protocol.decode(b"SS00000;") == protocol.UnknownFrame(raw=b"SS00000;")
    # SS01 Answer with wrong padding (5 chars after sub-id instead of 5 with trailing 0000) → unknown
    assert protocol.decode(b"SS0100001;") == protocol.UnknownFrame(raw=b"SS0100001;")
    # SS02 with P3 not 0/1 → unknown (digit "2" is not a valid marker state)
    assert protocol.decode(b"SS0220000;") == protocol.UnknownFrame(raw=b"SS0220000;")
    # SS03 with P3 outside 0..9/A → unknown (digit "B" is past Color-11)
    assert protocol.decode(b"SS03B0000;") == protocol.UnknownFrame(raw=b"SS03B0000;")
