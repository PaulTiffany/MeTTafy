# Four Color Ground Falsification

This note records Ground-layer findings downstream of the frozen ordered-state proof at `7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b`. It does not rewrite that proof.

## C1 — saturated boundary normal form

`tests/test_ground_reduction.py` exhaustively enumerates all `4^5 = 1024` Q4 assignments to a labeled five-cycle. Exactly 120 assignments are both proper and saturated (use all four colors), and every accepted assignment canonicalizes under dihedral symmetry and color-name permutation to

`0 1 0 2 3`.

The same certifier rejects nonproper and nonsaturated inputs. This is the executable Ground witness for `C1 SaturatedBoundaryNormalForm`.

## C0 — banked counterexample to the frozen wording

The frozen proof says that every vertex of degree at most four is immediately reducible by deleting it, coloring the smaller graph, and restoring the vertex with a color absent from its neighborhood.

The degree-four part of that sentence is false as written. Four neighbors can carry all four Q4 colors, leaving no missing color. `test_c0_degree_four_all_colors_refutes_immediate_missing_color_step` banks the explicit boundary color image `{0,1,2,3}` as a counterexample to that shortcut.

The executable immediate-restoration interface is therefore deliberately certified only through degree three, where the pigeonhole argument is valid. Its exhaustive witness checks all `1 + 4 + 16 + 64 = 85` neighbor-color assignments of degrees zero through three.

This does **not** refute the standard reducibility of a degree-four vertex in a plane triangulation. It refutes only the frozen proof's claim that the degree-four case is reducible by the immediate missing-color argument. A successor proof must insert the standard degree-four Kempe-chain/planarity reduction explicitly.

## Surface consequence

Until that repair is written and re-falsified:

- `C1` may be treated as mechanically covered;
- `C0` remains open and carries a banked counterexample;
- downstream novel claims are not silently rewritten;
- no theorem-level victory claim is warranted.
