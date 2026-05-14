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
