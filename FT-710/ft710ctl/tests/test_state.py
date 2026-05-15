from ft710ctl.radio import protocol, state


def test_apply_span_update():
    rs = state.RadioState()
    delta = rs.apply(protocol.ScopeSpanUpdate(span_khz=100))
    assert rs.scope.span_khz == 100
    assert delta == {"field": "scope.span_khz", "value": 100}


def test_apply_smeter_update():
    rs = state.RadioState()
    delta = rs.apply(protocol.SmeterUpdate(raw=128))
    assert rs.meters.smeter_raw == 128
    assert delta == {"field": "meters.smeter_raw", "value": 128}


def test_apply_unknown_returns_none():
    rs = state.RadioState()
    assert rs.apply(protocol.UnknownFrame(raw=b"XX0;")) is None


def test_apply_is_idempotent():
    rs = state.RadioState()
    delta1 = rs.apply(protocol.ScopeSpanUpdate(span_khz=100))
    delta2 = rs.apply(protocol.ScopeSpanUpdate(span_khz=100))
    assert delta1 == delta2
    assert rs.scope.span_khz == 100
