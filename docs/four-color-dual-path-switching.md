# Alternating Dual-Path Switching

**Status:** exact graph-level switch identity for every certified plane-dual domain translation, plus an exhaustive pivot-to-direct switching theorem for the complete boundary-only triangulated pentagon class. The remaining proof obligation is to lift the pivot-to-direct implication from that finite class to arbitrary triangulated pentagonal disks.

## 1. The dual path is an alternating V4 switch

Let the three nonzero V4 modes be

\[
\{\sigma,\tau,\rho\}.
\]

For a saturated degree-five boundary, choose singleton translation mode \(\sigma\). The retained triangulated embedding derives an actual path \(P\) in the two-mode dual network

\[
F_\sigma=\{e:m(e)\neq\sigma\}.
\]

Every crossed primal edge of \(P\) therefore has mode \(\tau\) or \(\rho\). Translating one side of the cut by \(\sigma\) adds \(\sigma\) to each crossed edge mode. In the Klein four group,

\[
\tau+\sigma=\rho,
\qquad
\rho+\sigma=\tau.
\]

Thus the graph-native domain translation is exactly an alternating switch of the two non-\(\sigma\) modes along the physical path carrier \(P\). No disk edge outside \(P\) changes mode.

## 2. Symmetric-difference law

For each nonzero mode \(\mu\), let

\[
F_\mu(z)=\{e\text{ in the retained disk}:m_z(e)\neq\mu\}.
\]

After a certified \(\sigma\)-translation along \(P\), the exact edge-set identities are

\[
\boxed{F_\sigma(z')=F_\sigma(z)}
\]

and, for each \(\mu\neq\sigma\),

\[
\boxed{F_\mu(z')=F_\mu(z)\triangle P}.
\]

This is not a boundary analogy. `AlternatingPathSwitchCertificate` checks the identity on the complete retained triangulated disk: every crossed physical edge toggles by \(+\sigma\), every noncrossed edge is unchanged, and the two complementary selected-mode carriers are exactly symmetric-differenced by the path.

## 3. Pairing signature

For each of the two singleton modes of a saturated C5, the actual embedded continuation gives one physical noncrossing terminal pairing. Its current control consequence is classified as:

- **direct** when either path of that actual pairing yields positive focus palette slack;
- **pivot** when both paths preserve zero focus slack.

The two singleton records form the `DualPairingSignature`. A construction is in the direct regime if at least one singleton continuation family is direct; otherwise it is in the pivot regime.

These labels are derived control metadata. They are not coordinates of `ConstructionState`.

## 4. Complete boundary-only switching theorem

The five labelled Catalan triangulations of a pentagonal disk with no interior vertices admit exactly 360 compatible saturated labelled colorings under the exact committed-edge ledger. Their pairing signatures split as

\[
240\text{ direct},\qquad 120\text{ pivot}.
\]

The stronger switching test now examines **every current dual stage** from every pivot construction. There are

\[
120\times4=480
\]

such exact first-stage controls: two singleton modes and two physical paths for each mode.

Every one satisfies

\[
\boxed{
\operatorname{Pivot}(z)
\xrightarrow{\text{any current certified dual stage}}
\operatorname{Direct}(z').
}
\]

The test also certifies the alternating-path symmetric-difference law on all

\[
360\times4=1440
\]

current dual controls in the complete boundary-only class.

The persistent-double-lock carrier is one member of the pivot class, and all four of its current graph-native dual stages move it into direct control geometry.

## 5. Cost-of-Cacophony interpretation

This sharpens the staged-routing picture. Direct and pivot states can have the same number of lawful current controls. What differs is their **ordered consequence** for the focus observable.

A pivot is therefore not a failed action. It is a lawful transformation that changes the control geometry so that the next receding-horizon decision becomes direct. In the boundary-only theorem,

\[
\operatorname{Pivot}\to\operatorname{Direct}\to A(v)\neq\varnothing,
\]

so the entire additional cost of interference is one stage.

The alternating-switch identity identifies the mechanism behind that geometry change: the first path preserves its own selected-mode network while performing symmetric-difference surgery on each of the other two dual networks.

## 6. Remaining topological lemma

The algebraic part no longer depends on the number of interior triangles. For an arbitrary retained triangulated pentagonal disk, every certified domain translation already satisfies

\[
F_\mu(z')=F_\mu(z)\triangle P
\]

for \(\mu\neq\sigma\).

The remaining theorem-specific content is therefore topological:

> **Planar Dual Pivot-Switching Lemma.** If both singleton continuation families at a saturated degree-five construction have pivot terminal pairings, then symmetric-difference surgery by an actual path of either family forces the successor saturated construction into the direct pairing regime.

Equivalently,

\[
\boxed{
\operatorname{Pivot}(z)
\Longrightarrow
\forall P\in\mathcal P_{\mathrm{dual}}(z),
\operatorname{Direct}(T_Pz)
}
\]

would match the stronger finite theorem already observed on all boundary-only cases. A weaker existential form would still suffice for the Four Color continuation argument.

The next derivation should prove this from planar path surgery/Jordan separation in the trivalent dual disk, taking account of the fact that the two selected-mode networks may share physical edges of their common V4 mode.
