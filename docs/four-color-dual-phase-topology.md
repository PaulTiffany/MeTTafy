# Dual Phase Topology Accounting

**Status:** exact finite identity banked on the retained degree-five disk. This
tranche introduces no future target, route coordinate, or global reachability
oracle. Current control access is already derived from the current construction
state; the purpose here is to expose the topology that distinguishes available
controls.

## 1. Three complementary networks

For each nonzero V4 mode `sigma`, exclude the `sigma` matching and retain the
other two matchings. Their union is a disjoint collection of alternating
terminal paths and internal alternating cycles.

Write

\[
P = \text{total terminal-path count},
\qquad
C = \text{total internal alternating-cycle count},
\]

across the three excluded-mode networks, and let

\[
S = \text{number of terminal paths containing exactly two matching arcs}.
\]

The already-banked ordered partial involution product advances two matching
arcs at a time. On an ordinary terminal path, the two parity classes remain two
weak product fragments. The same is true on an alternating cycle. A two-edge
terminal path is the exact exceptional case: its two parity classes meet in a
single product fragment.

Therefore the phase-fragment rank satisfies the network-local accounting law

\[
\boxed{\Phi = 2P + 2C - S.}
\]

`PhaseTopologyCertificate` checks this relation separately on each of the three
complementary networks against the exact ordered involution products.

## 2. The degree-five constant

The pentagonal frontier has five physical boundary edges. Every boundary edge
has exactly one nonzero V4 mode, so it belongs to exactly two of the three
complementary networks. Hence the three networks contain exactly ten terminal
incidences.

Every terminal path has two terminal incidences, while an internal cycle has
none. Thus

\[
2P=10,
\qquad
P=5.
\]

Substitution gives the exact degree-five identity

\[
\boxed{\Phi = 10 + 2C - S.}
\]

The constant ten is therefore not fitted to the existing witness family. It is
forced by the five-edge frontier and the three complementary V4 networks.

## 3. Mechanical falsification

The certificate is exercised on the original three-interior pivot witness and
on the complete 154-member proper-color-preserving diagonal-flip family already
used to attack the phase candidate.

For every retained disk in that family the test checks

\[
\Phi = 10 + 2C - S
\]

against the independently derived ordered-involution fragment count. The family
contains carriers with nonzero internal-cycle correction and carriers with
nonzero two-edge terminal-path correction, so both terms are mechanically
active rather than decorative.

The original hard witness reads

\[
C=1,
\qquad
S=0,
\qquad
\Phi=12.
\]

Its familiar first pivot-to-pivot stage removes the internal cycle and reaches
\(\Phi=10\), making the earlier `12 -> 10` observation an instance of the exact
topological identity rather than an unexplained scalar change.

## 4. What is now banked

The finite local control geometry has the dependency chain

\[
\text{physical V4 matchings}
\to
\text{alternating path/cycle decomposition}
\to
\text{ordered partial involutions}
\to
\boxed{\Phi=10+2C-S}.
\]

No step asks the coloration agent to know a future destination. At a zero-slack
state the currently applicable controls are derived from the current retained
carrier; after one certified action the geometry is recomputed from the actual
successor.

The next useful mechanical question is correspondingly local: for each current
pivot configuration, how does each certified path switch change the pair
\((C,S)\), and which currently applicable control changes the control regime or
reduces \(2C-S\)? That is a control-selection law on present geometry, not an
`eventual reachability` object.
