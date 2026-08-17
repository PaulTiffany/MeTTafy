# Zero-Point Correspondence of Four Color Control Parameterizations

**Status:** exact proof-interface discipline for the fixed genus-zero construction species. This note does not itself establish the remaining global continuation theorem.

## 1. Shared construction point

Let a Four Color construction state be

\[
z_0=s=(G,c),
\]

with the genus-zero surface species fixed and every committed edge obligation valid.
A control parameterization \(\mathcal P_\alpha(s)\) is a description of directions
available around that exact state; its parameters are not additional coordinates of
the Four Color state.

Each parameterization has a distinguished null parameter \(0_\alpha\) satisfying

\[
\rho_\alpha(s,0_\alpha)=s.
\]

Two parameterizations correspond at zero exactly when

\[
\rho_\alpha(s,0_\alpha)=s=\rho_\beta(s,0_\beta).
\]

The repository calls this a `ZeroPointCorrespondence`.

## 2. What correspondence grants

Zero-point correspondence permits a change of control description without counting
that change as a construction transition. In particular, the current Kempe-component
parameterization and the degree-five V4 dual-defect parameterization can be based at
the same exact graph/coloring state.

Thus

\[
(s,\mathcal P_{\mathrm{Kempe}},0)
\sim
(s,\mathcal P_{V_4/\mathrm{dual}},0)
\]

means only that both descriptions have the same construction origin.

It does **not** identify arbitrary nonzero parameters across the two descriptions.
A nonzero control must still be supplied and certified by the family that owns it.
For Kempe controls the repository checks current component availability and exact
ledger-preserving replay. For a V4 domain translation, an embedded cut/continuation
witness is still required before a nonzero parameter may act on the construction.

## 3. Receding-horizon interpretation

At stage \(t\), the coloration agent occupies one exact construction point \(s_t\).
Several corresponding parameterizations may be derived at that point:

\[
\mathcal P_1(s_t),\ldots,\mathcal P_k(s_t).
\]

Switching among them at their shared zero does not move the coloring. Only a certified
nonzero control produces

\[
s_t\longrightarrow s_{t+1}.
\]

The next parameterizations are then derived again from \(s_{t+1}\). This is the same
receding-horizon discipline used by immediate control access: present access is proof
authority; a predeclared future route is not.

## 4. Why this matters for the locked degree-five case

A locally exhausted Kempe description does not imply that the Four Color construction
has reached a new theorem state. The exact graph/coloring point remains the shared
zero. The retained planar witness may expose a richer corresponding parameterization
at that same point, such as the V4 dual continuation geometry.

Accordingly the proof interface is

\[
\text{control-family evidence at }z_0
\to
\text{parameter refinement at the same }z_0
\to
\text{certified nonzero control}
\to
z_1.
\]

This prevents two invalid shortcuts at once:

1. changing descriptions cannot masquerade as construction progress;
2. correspondence at zero cannot masquerade as permission to transport a nonzero
   operation between unrelated control families.

## 5. Mechanical witnesses

`src/mettafy/zero_point_correspondence.py` provides:

- exact construction-state equality at the fixed species;
- `ControlParameterization` with a distinguished identity zero;
- `ZeroPointCorrespondence` between parameterizations based at the same state;
- current Kempe-component parameterization;
- degree-five V4 dual-defect parameterization derived from the witnessed C5 boundary;
- family-specific certification for nonzero Kempe parameters.

`tests/test_zero_point_correspondence.py` checks:

- the Kempe zero parameter is exact identity;
- Kempe and dual parameterizations share the same zero for all 120 saturated proper
  C5 boundary assignments;
- reparameterization at zero leaves the persistent exterior carrier unchanged;
- a nonzero Kempe parameter requires current family-specific access and preserves the
  edge ledger;
- a stale nonzero parameter cannot be borrowed after the construction has moved;
- distinct construction points do not qualify as the same zero.

## 6. Proof boundary

The earned statement is

\[
\boxed{\text{corresponding control parameterizations may share one exact }z_0}
\]

with nonzero transport remaining certificate-specific.

The next theorem obligation is therefore sharper: derive the nonzero plane-dual
control from the retained embedding witness while keeping its zero identified with
the exact same construction state. Once that interface is graph-native, it can be
composed with receding-horizon control without introducing an external state space or
future-path oracle.
