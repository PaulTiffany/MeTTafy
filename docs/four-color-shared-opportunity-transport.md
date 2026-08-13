# Shared-Opportunity Transport

**Status:** exact local transport law for one selected graph-native dual action.

Fix a current singleton V4 mode `sigma`. The other two nonzero modes form one
shared opportunity class

\[
O_\sigma=\{\mu,\nu\},\qquad \nu=\mu+\sigma.
\]

The corresponding physical opportunity carrier is

\[
\mathcal O_\sigma(z)
=
\{e:\delta_z(e)\ne\sigma\}.
\]

Because every properly colored triangle contains exactly one edge of each
nonzero V4 mode, every disk triangle contains exactly two edges of
`O_sigma`. In the dual this is the already-certified local degree-two
continuation law.

Now realize one current `sigma` domain action on an exact path `P`. The pairwise
edge law gives

\[
\delta'(e)=
\begin{cases}
\delta(e)+\sigma,&e\in P,\\
\delta(e),&e\notin P.
\end{cases}
\]

Every edge of `P` already lies in `O_sigma`, so along the realized consequence
its two opportunity labels exchange:

\[
\mu\leftrightarrow\nu.
\]

No edge enters or leaves the opportunity class. Therefore

\[
\boxed{\mathcal O_\sigma(T_Pz)=\mathcal O_\sigma(z).}
\]

This is stronger than mere cardinality preservation. The retained embedding has
the same physical opportunity carrier, the same degree-two passage through
every disk triangle, the same boundary terminal pairing, and the same two exact
`sigma` continuation paths. The realized action retypes one path; it does not
consume or duplicate the shared opportunity itself.

For the degree-five boundary, the selected `sigma` edge count is also unchanged.
A current singleton `sigma` therefore remains singleton after the action,
whether the successor already has positive focus slack or remains saturated.

`SharedOpportunityTransportCertificate` verifies all of these identities from
the actual before/after colorings and retained physical embedding. The complete
154-member proper-color-preserving flip family contributes 616 current dual
transitions (four per member); every one is required to satisfy the certificate.

The proof-relevant distinction is:

\[
\boxed{
\text{one realized pairwise consequence}
\quad+\quad
\text{one physically retained shared opportunity}.
}
\]

Opportunity remains permission geometry. It is not promoted into another
realized successor or a lookahead route.
