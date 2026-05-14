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
