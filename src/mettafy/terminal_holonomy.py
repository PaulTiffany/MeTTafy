from __future__ import annotations

from dataclasses import dataclass

from mettafy.imaginary_traversal import (
    IDENTITY_S4,
    Permutation4,
    s4_inv,
    s4_mul,
)


@dataclass(frozen=True)
class SpinTransport:
    """Internal chromatic transport with a spinor phase coordinate.

    ``quarter_turns`` is measured modulo four.  A value of 2 is the internal
    spinor sign ``-1`` after a 2pi rotation; it is invisible to the terminal
    scalar decoder.  Odd values remain traversal states and are not terminal.
    """

    palette: Permutation4 = IDENTITY_S4
    quarter_turns: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "quarter_turns", self.quarter_turns % 4)

    def after(self, earlier: SpinTransport) -> SpinTransport:
        """Compose ``self`` after ``earlier``."""
        return SpinTransport(
            palette=s4_mul(self.palette, earlier.palette),
            quarter_turns=self.quarter_turns + earlier.quarter_turns,
        )

    def inverse(self) -> SpinTransport:
        return SpinTransport(
            palette=s4_inv(self.palette),
            quarter_turns=-self.quarter_turns,
        )

    @property
    def internally_trivial(self) -> bool:
        return self.palette == IDENTITY_S4 and self.quarter_turns == 0

    @property
    def terminally_trivial(self) -> bool:
        """The scalar decoder forgets the central spinor sign only.

        This kernel is exactly {+id, -id}: the palette frame must close and the
        spinor phase must be even.  Odd quarter-turns change traversal sheet;
        nonidentity palette holonomy is not silently declared observer-null.
        """
        return self.palette == IDENTITY_S4 and self.quarter_turns % 2 == 0


IDENTITY_TRANSPORT = SpinTransport()
MINUS_ID_TRANSPORT = SpinTransport(quarter_turns=2)


@dataclass(frozen=True)
class TransportConnection:
    """A discrete connection on a chart graph.

    Every oriented edge carries an invertible transport.  The reverse edge
    must be present and equal to the inverse transport.  This object does not
    assume planarity; it exposes monodromy exactly so planarity-specific
    arguments cannot be hidden in the implementation.
    """

    vertices: tuple[str, ...]
    transitions: dict[tuple[str, str], SpinTransport]

    def __post_init__(self) -> None:
        vertex_set = set(self.vertices)
        if len(vertex_set) != len(self.vertices):
            raise ValueError("connection vertices must be unique")
        for (u, v), transport in self.transitions.items():
            if u not in vertex_set or v not in vertex_set:
                raise ValueError("transition endpoint is outside the connection")
            reverse = self.transitions.get((v, u))
            if reverse is None:
                raise ValueError("every transition requires an explicit reverse")
            if reverse != transport.inverse():
                raise ValueError("reverse transition must equal the inverse")

    def holonomy(self, path: tuple[str, ...]) -> SpinTransport:
        if len(path) < 1:
            raise ValueError("path must contain at least one vertex")
        if path[0] not in self.vertices:
            raise ValueError("path begins outside the connection")
        result = IDENTITY_TRANSPORT
        for u, v in zip(path, path[1:]):
            try:
                step = self.transitions[(u, v)]
            except KeyError as exc:
                raise ValueError(f"missing transition {u}->{v}") from exc
            result = step.after(result)
        return result

    def loop_terminally_trivial(self, loop: tuple[str, ...]) -> bool:
        if len(loop) < 2 or loop[0] != loop[-1]:
            raise ValueError("loop must be explicitly closed")
        return self.holonomy(loop).terminally_trivial

    def terminal_paths_agree(
        self, path_a: tuple[str, ...], path_b: tuple[str, ...]
    ) -> bool:
        """Check path independence after terminal projection.

        If two root-to-target transports differ only by an element of the
        decoder kernel {+id,-id}, their terminal observations agree even when
        the internal spinor states differ.
        """
        if not path_a or not path_b:
            raise ValueError("paths must be non-empty")
        if path_a[0] != path_b[0] or path_a[-1] != path_b[-1]:
            raise ValueError("paths must share endpoints")
        hol_a = self.holonomy(path_a)
        hol_b = self.holonomy(path_b)
        relative = hol_a.after(hol_b.inverse())
        return relative.terminally_trivial


def planar_spin_holonomy(winding_number: int) -> SpinTransport:
    """Spinor holonomy of a closed planar frame traversal.

    A full 2pi turn contributes the central sign -1, represented by two
    quarter-turns.  Therefore any integer winding produces holonomy in the
    terminal decoder kernel, although odd winding is internally nontrivial.
    """
    return SpinTransport(quarter_turns=2 * winding_number)
