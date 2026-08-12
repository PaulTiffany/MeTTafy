# Dual Involution Phase Algebra

**Status:** exact graph-native partial-involution representation of the trivalent
V4 disk dual, with ordered-product inverse laws and a finite phase-fragment rank
candidate. The rank candidate survives the current three-interior-vertex
pivot-to-pivot kill witness, but no universal descent theorem is claimed.

## 1. From three matchings to three partial involutions

For a retained properly colored triangulated pentagonal disk, every disk
triangle has exactly one edge of each nonzero Klein-four mode

\[
Q^\times=\{10,01,11\}.
\]

The dual carrier therefore has three physical matchings

\[
M_{10},\qquad M_{01},\qquad M_{11}.
\]

Each matching defines a fixed-point-free partial involution

\[
\iota_\mu:U_\mu\rightharpoonup U_\mu,
\qquad
\iota_\mu^2=\mathrm{id}
\]

on dual face nodes together with the boundary half-edge nodes carrying mode
\(\mu\). Every disk-face node lies in the domain of all three involutions.
A boundary terminal lies in exactly the involution matching its physical
boundary-edge mode.

This representation retains the physical splice at every triangle rather than
remembering only terminal pairing or alternating-component counts.

## 2. Ordered two-step products retain phase

For distinct modes \(\mu,\nu\), define the partial product

\[
\phi_{\mu,\nu}=\iota_\mu\circ\iota_\nu.
\]

It advances two matching edges through the dual splice. Reversing the order is
the exact partial inverse:

\[
\boxed{
\phi_{\mu,\nu}^{-1}=\phi_{\nu,\mu}.
}
\]

For a disk with \(f\) triangular faces, every ordered product has exactly \(f\)
defined source-target steps. Boundary loss on face sources is exactly balanced
by boundary-terminal sources of the same matching.

The six ordered relations form `phase_relation_key`. They retain information
that the previous projections lose: on the three-interior pivot witness, the
successive zero-slack states have distinct ordered phase keys even after the
internal alternating-cycle count has already fallen to zero.

## 3. A finite phase-fragment rank candidate

For one orientation of each unordered mode pair, let

\[
\kappa_{\mu\nu}(z)
\]

be the number of weak connected fragments in the graph of the partial
two-step relation \(\phi_{\mu,\nu}\). Reverse products have the same fragment
count because their relations are inverse. Define

\[
\boxed{
\Phi(z)=
\kappa_{10,01}(z)
+\kappa_{10,11}(z)
+\kappa_{01,11}(z).
}
\]

This is a graph-native nonnegative integer. Since each product has exactly
\(f\) steps,

\[
0<\Phi(z)\le 3f.
\]

No future route or theorem-status coordinate is encoded in the construction
state.

## 4. First kill test: the three-interior pivot witness

The exact three-interior-vertex witness that killed the universal one-pivot
claim begins with

\[
\operatorname{regime}(z_0)=\mathrm{pivot},
\qquad
\Phi(z_0)=12.
\]

It has four current embedding-derived dual controls. Every one remains
zero-slack and pivot-type, but every one satisfies

\[
\boxed{
\Phi(Tz_0)=10<12.
}
\]

Thus the candidate scalar detects progress where terminal pairing alone reports

\[
\mathrm{pivot}\to\mathrm{pivot}.
\]

For each of those four successor states, nonreplay history leaves three fresh
current controls. Their consequences are not interchangeable: one fresh
choice returns to a pivot state with \(\Phi=12\), while fresh alternatives
produce direct control geometry with \(\Phi=10\).

So **freshness alone is still not the router**. The stronger candidate is an
existential staged dichotomy.

## 5. Candidate descent statement

The theorem interface now worth attacking is

\[
\boxed{
\operatorname{Pivot}(z,h)
\Longrightarrow
\exists T\in\mathcal A_{\mathrm{fresh}}(z,h):
\left[
\operatorname{Direct}(Tz)
\ \lor\
\Phi(Tz)<\Phi(z)
\right].
}
\]

Here \(h\) is retained graph-native nonreplay history and every admissible
control is derived from the current exact embedding.

On the known three-stage witness the certified trajectory has

\[
(\mathrm{pivot},12)
\to
(\mathrm{pivot},10)
\to
(\mathrm{direct},10)
\to
A(v)\ne\varnothing.
\]

Strict rank descent is required only while the successor remains pivot. Once
direct geometry is reached, the existing current-control machinery supplies the
focus-slack stage.

The candidate survives this first adversarial witness. It is **not yet a
general planar theorem**. The next work is to derive or kill the boxed
existential statement on arbitrary trivalent dual disks, using how a matching
path switch conjugates/rewires the ordered partial involutions.

## 6. Proper-color-preserving flip-family falsifier

To attack the candidate beyond a single hand-selected carrier, the mechanical
suite now traverses the complete color-preserving diagonal-flip component of
the three-interior witness coloring.

The flips are used **only to generate distinct planar theorem instances**.
They are not coloration construction controls and do not enlarge the allowed
state transition vocabulary.

That component contains exactly

\[
154
\]

valid triangulated pentagonal disks with the same committed coloring. Their
current control regimes split as

\[
128\text{ direct},\qquad 26\text{ pivot}.
\]

The 26 pivot instances have phase-fragment ranks

\[
\{9^{\times 12},\,
  11^{\times 6},\,
  12^{\times 3},\,
  13^{\times 2},\,
  10^{\times 2},\,
  14^{\times 1}\}.
\]

For every one of those 26 pivot instances, exhaustive evaluation of all four
current graph-derived dual parameters found at least one certified successor
satisfying

\[
\operatorname{Direct}(Tz)
\quad\text{or}\quad
\Phi(Tz)<\Phi(z).
\]

Thus the candidate survives an entire nontrivial flip-connected family that
includes the original pivot-to-pivot counterexample. This is stronger
falsification evidence, not a substitute for the universal planar derivation.
