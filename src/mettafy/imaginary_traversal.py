from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

ColorWord = tuple[int, int, int, int, int]
Permutation4 = tuple[int, int, int, int]
Dihedral5 = tuple[int, int]  # (epsilon in {+1,-1}, shift mod 5)
GroupElement = tuple[Dihedral5, Permutation4]

X3_REP: ColorWord = (0, 1, 0, 1, 2)
X4_REP: ColorWord = (0, 1, 0, 2, 3)
IDENTITY_D5: Dihedral5 = (1, 0)
IDENTITY_S4: Permutation4 = (0, 1, 2, 3)
IDENTITY_G: GroupElement = (IDENTITY_D5, IDENTITY_S4)


def d5_elements() -> tuple[Dihedral5, ...]:
    return tuple((eps, shift) for eps in (1, -1) for shift in range(5))


def s4_elements() -> tuple[Permutation4, ...]:
    return tuple(permutations(range(4)))


def group_elements() -> tuple[GroupElement, ...]:
    return tuple((d, p) for d in d5_elements() for p in s4_elements())


def d5_mul(left: Dihedral5, right: Dihedral5) -> Dihedral5:
    """Composition left after right for i -> eps*i + shift mod 5."""
    eps_l, shift_l = left
    eps_r, shift_r = right
    return (eps_l * eps_r, (eps_l * shift_r + shift_l) % 5)


def d5_inv(element: Dihedral5) -> Dihedral5:
    eps, shift = element
    return (eps, (-eps * shift) % 5)


def s4_mul(left: Permutation4, right: Permutation4) -> Permutation4:
    return tuple(left[right[i]] for i in range(4))  # type: ignore[return-value]


def s4_inv(p: Permutation4) -> Permutation4:
    out = [0, 0, 0, 0]
    for i, value in enumerate(p):
        out[value] = i
    return tuple(out)  # type: ignore[return-value]


def group_mul(left: GroupElement, right: GroupElement) -> GroupElement:
    return (d5_mul(left[0], right[0]), s4_mul(left[1], right[1]))


def group_inv(element: GroupElement) -> GroupElement:
    return (d5_inv(element[0]), s4_inv(element[1]))


def act(word: ColorWord, element: GroupElement) -> ColorWord:
    """Apply position symmetry then global palette permutation."""
    (eps, shift), palette = element
    out = [0, 0, 0, 0, 0]
    for i in range(5):
        source = (eps * (i - shift)) % 5
        out[i] = palette[word[source]]
    return tuple(out)  # type: ignore[return-value]


def stabilizer(word: ColorWord) -> frozenset[GroupElement]:
    return frozenset(g for g in group_elements() if act(word, g) == word)


def conjugate_subgroup(
    subgroup: frozenset[GroupElement], element: GroupElement
) -> frozenset[GroupElement]:
    inv = group_inv(element)
    return frozenset(group_mul(group_mul(element, h), inv) for h in subgroup)


def proper_c5(word: ColorWord) -> bool:
    return all(word[i] != word[(i + 1) % 5] for i in range(5))


def sheet(word: ColorWord) -> int:
    if not proper_c5(word):
        raise ValueError("word is not a proper C5 coloring")
    used = len(set(word))
    if used not in (3, 4):
        raise ValueError("proper Q4-coloring of C5 must use three or four colors")
    return used


def orbit(word: ColorWord) -> frozenset[ColorWord]:
    return frozenset(act(word, g) for g in group_elements())


# g0 = (rotation by 2, (0 2)(1 3)).
G0: GroupElement = ((1, 2), (2, 3, 0, 1))


@dataclass(frozen=True)
class SignedSheetState:
    word: ColorWord
    sign: int

    def __post_init__(self) -> None:
        if self.sign not in (1, -1):
            raise ValueError("sign must be +1 or -1")
        expected = 3 if self.sign == 1 else 4
        if sheet(self.word) != expected:
            raise ValueError("sign does not match chromatic sheet")


def _coset_representative(word: ColorWord, base: ColorWord) -> GroupElement:
    for g in group_elements():
        if act(base, g) == word:
            return g
    raise ValueError("word is outside the expected orbit")


def j_map(word: ColorWord) -> ColorWord:
    """Equivariant sheet switch X3 -> X4 induced by conjugate stabilizers."""
    if sheet(word) != 3:
        raise ValueError("J expects the three-color sheet")
    g = _coset_representative(word, X3_REP)
    a = group_inv(G0)
    return act(X4_REP, group_mul(g, a))


def j_inv_map(word: ColorWord) -> ColorWord:
    """Inverse sheet switch X4 -> X3."""
    if sheet(word) != 4:
        raise ValueError("J^-1 expects the four-color sheet")
    g = _coset_representative(word, X4_REP)
    return act(X3_REP, group_mul(g, G0))


def imaginary_traversal(state: SignedSheetState) -> SignedSheetState:
    """Complex-structure action: + sheet -> -, - sheet -> negative + sheet.

    The scalar minus sign is represented by the SignedSheetState sign. Applying
    twice returns the same chromatic word with sign reversed, i.e. I^2 = -id.
    """
    if state.sign == 1:
        return SignedSheetState(j_map(state.word), -1)
    return SignedSheetState(j_inv_map(state.word), 1)


def imaginary_square(word: ColorWord) -> tuple[ColorWord, int]:
    """Return the word and scalar after I^2 on a positive-sheet basis state."""
    first = j_map(word)
    second = j_inv_map(first)
    return second, -1
