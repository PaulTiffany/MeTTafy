from __future__ import annotations

import pytest

from mettafy.imaginary_traversal import IDENTITY_S4
from mettafy.terminal_holonomy import (
    IDENTITY_TRANSPORT,
    MINUS_ID_TRANSPORT,
    SpinTransport,
    TransportConnection,
    planar_spin_holonomy,
)


def test_spinor_sign_is_internal_but_terminally_trivial() -> None:
    assert IDENTITY_TRANSPORT.internally_trivial
    assert IDENTITY_TRANSPORT.terminally_trivial
    assert not MINUS_ID_TRANSPORT.internally_trivial
    assert MINUS_ID_TRANSPORT.terminally_trivial


def test_odd_quarter_turn_is_not_terminally_trivial() -> None:
    traversal = SpinTransport(quarter_turns=1)
    assert not traversal.internally_trivial
    assert not traversal.terminally_trivial


def test_nonidentity_palette_holonomy_never_hides_in_decoder_kernel() -> None:
    swap01 = (1, 0, 2, 3)
    transport = SpinTransport(palette=swap01, quarter_turns=2)
    assert transport.palette != IDENTITY_S4
    assert not transport.terminally_trivial


def test_planar_spin_winding_lands_in_terminal_kernel() -> None:
    for winding in range(-5, 6):
        holonomy = planar_spin_holonomy(winding)
        assert holonomy.terminally_trivial
        assert holonomy.internally_trivial is (winding % 2 == 0)


def test_connection_accepts_minus_identity_monodromy_but_not_quarter_turn() -> None:
    edge_ab = SpinTransport(quarter_turns=1)
    edge_bc = SpinTransport(quarter_turns=1)
    edge_ca = SpinTransport()
    good = TransportConnection(
        vertices=("a", "b", "c"),
        transitions={
            ("a", "b"): edge_ab,
            ("b", "a"): edge_ab.inverse(),
            ("b", "c"): edge_bc,
            ("c", "b"): edge_bc.inverse(),
            ("c", "a"): edge_ca,
            ("a", "c"): edge_ca.inverse(),
        },
    )
    assert good.holonomy(("a", "b", "c", "a")) == MINUS_ID_TRANSPORT
    assert good.loop_terminally_trivial(("a", "b", "c", "a"))

    bad_edge_bc = SpinTransport()
    bad = TransportConnection(
        vertices=("a", "b", "c"),
        transitions={
            ("a", "b"): edge_ab,
            ("b", "a"): edge_ab.inverse(),
            ("b", "c"): bad_edge_bc,
            ("c", "b"): bad_edge_bc.inverse(),
            ("c", "a"): edge_ca,
            ("a", "c"): edge_ca.inverse(),
        },
    )
    assert not bad.loop_terminally_trivial(("a", "b", "c", "a"))


def test_terminal_path_independence_modulo_spinor_sign() -> None:
    edge_ab = SpinTransport(quarter_turns=1)
    edge_bd = SpinTransport(quarter_turns=1)
    edge_ac = SpinTransport()
    edge_cd = SpinTransport()
    connection = TransportConnection(
        vertices=("a", "b", "c", "d"),
        transitions={
            ("a", "b"): edge_ab,
            ("b", "a"): edge_ab.inverse(),
            ("b", "d"): edge_bd,
            ("d", "b"): edge_bd.inverse(),
            ("a", "c"): edge_ac,
            ("c", "a"): edge_ac.inverse(),
            ("c", "d"): edge_cd,
            ("d", "c"): edge_cd.inverse(),
        },
    )
    assert connection.terminal_paths_agree(("a", "b", "d"), ("a", "c", "d"))


def test_connection_rejects_noninverse_reverse_transition() -> None:
    with pytest.raises(ValueError, match="reverse transition"):
        TransportConnection(
            vertices=("a", "b"),
            transitions={
                ("a", "b"): SpinTransport(quarter_turns=1),
                ("b", "a"): SpinTransport(quarter_turns=1),
            },
        )
