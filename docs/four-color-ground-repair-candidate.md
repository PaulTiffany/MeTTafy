# Four Color Ground Repair Candidate — Degree Four

This is a successor-proof repair candidate downstream of the frozen ordered-state proof at `7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b`. It does not edit that frozen artifact.

## Repair target

The frozen C0 reduction says that every vertex of degree at most four is immediately reducible because a color is absent from its neighborhood. The mechanical falsifier shows the degree-four part of that sentence is false: four neighbors may use all four colors.

The standard repair is local and precedes the novel degree-five construction.

## Corrected low-degree reduction

Assume a minimum counterexample has been triangulated without changing its vertex set, and let `v` be a vertex of degree at most five supplied by Euler's formula.

For `deg(v) <= 3`, delete `v`, four-color the smaller graph by minimality, and restore `v` with a color absent from its neighborhood. The executable interface in `ground_reduction.py` exhaustively certifies this immediate argument for all neighbor-color assignments through degree three.

For `deg(v) = 4`, delete `v` and four-color `G-v`. Let its neighbors occur in cyclic order `a b c d`.

If those neighbors use at most three colors, restore `v` immediately. Otherwise rename the four colors so the boundary is `A B C D`.

Consider the `{A,C}` Kempe component containing `a`.

- If it does not contain `c`, interchange `A` and `C` on that complete component. Color `A` disappears from `N(v)`, so `v` can be restored with `A`.
- If it does contain `c`, choose a simple `a--c` path in that component. In the plane embedding this path is a crosscut between opposite vertices of the exposed quadrilateral. It separates `b` from `d`. Therefore the disjoint-color `{B,D}` subgraph cannot also contain a `b--d` path. Interchange `B` and `D` on the component containing `b`; color `B` disappears from `N(v)`, so `v` can be restored with `B`.

Thus degree four is reducible by one exact whole-component Kempe interchange, but not necessarily by the immediate missing-color shortcut.

Consequently, after this repair, the minimum-counterexample reduction may proceed to a degree-five vertex, where the ordered-state construction begins.

## Mechanical interface

`src/mettafy/degree_four_reduction.py` implements only the executable interface of the standard lemma:

1. preserve the ordered four-cycle frontier;
2. return immediately when a color is already available;
3. test the first opposite Kempe pair from the actual current state;
4. if it is connected, test the complementary pair;
5. reject a state in which both opposite pairs are connected rather than silently assuming the planar crosscut premise;
6. certify that the selected complete-component interchange opens a color at `v`.

`tests/test_degree_four_reduction.py` exercises both valid Kempe branches, the already-open case, and explicit rejection when the planar crosscut premise is not satisfied.

This repair candidate is not theorem authority. It becomes a successor proof only after its mathematical wording, mechanical interface, and downstream dependency surface are all re-audited.
