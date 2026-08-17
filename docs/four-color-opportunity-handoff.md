# Cross-Direction Opportunity Handoff

**Status:** exact local transport certificate; no lookahead router.

Fix a saturated degree-five state and one currently applicable singleton V4
direction \(\sigma\).  Let the other two nonzero modes be

\[
O_\sigma=\{\tau,\rho\}.
\]

A chosen \(\sigma\)-domain action realizes exactly one physical dual path
\(P\).  The source opportunity carrier is

\[
\mathcal O_\sigma(z)=\{e:\delta_z(e)\neq\sigma\}.
\]

The already-certified local consequence law gives

\[
\boxed{\mathcal O_\sigma(T_Pz)=\mathcal O_\sigma(z)}
\]

and, for either complementary direction \(\mu\in O_\sigma\),

\[
\boxed{
\mathcal O_\mu(T_Pz)
=
\mathcal O_\mu(z)\triangle P.
}
\]

Thus continuing in the same direction preserves the physical opportunity
carrier.  Changing direction does not inspect several future states: the one
realized consequence \(P\) retypes the newly selected directional carrier by
symmetric difference with that same physical path.

## Stop or handoff

After the action there are only two proof-relevant cases.

If

\[
A_{T_Pz}(v)\neq\varnothing,
\]

the focus has a currently admissible color and the local traversal may stop.
No successor direction is asserted or required.

If instead

\[
A_{T_Pz}(v)=\varnothing,
\]

the successor boundary is again a saturated proper C5.  The source mode
\(\sigma\) remains singleton, and exactly one member

\[
\eta\in O_\sigma
\]

is the other singleton mode at the actual successor.  `OpportunityHandoffCertificate`
derives \(\eta\) from that successor and then mechanically reconstructs its
embedding-derived dual continuation there.  This is a present permission, not
a future-route coordinate.

The other singleton may be the same mode as before or the other member of the
shared opportunity pair.  The certificate does not impose a preferred branch.
It records only the consequence that actually occurred and the permission
surface that actually exists afterward.

## Discrete control calculus

The local operations can therefore be stated without counterfactual fan-out:

\[
\boxed{
\begin{array}{lll}
\text{continue in }\sigma
&:& \mathcal O_\sigma' = \mathcal O_\sigma,\\[1mm]
\text{change to }\mu\neq\sigma
&:& \mathcal O_\mu' = \mathcal O_\mu\triangle P,\\[1mm]
\text{stop}
&:& A(v)\neq\varnothing.
\end{array}}
\]

Every line is evaluated from the one realized current action and the actual
successor state.
