# Trivalent Dual Splice State

**Status:** exact carrier representation banked as the next proof language after the one-pivot descent conjecture was killed.  It retains the information boundary pairing forgets, but it does **not** yet supply a global descent theorem.

## 1. Why boundary pairing was too coarse

Every properly colored triangle in the retained disk has exactly one edge of each nonzero V4 mode.  Passing to the dual therefore gives a trivalent graph whose three incident edges at every face node have the three distinct modes.

For mode \(\mu\), let

\[
M_\mu=\{e:m(e)=\mu\}.
\]

Each \(M_\mu\) is a physical matching in the trivalent dual.  The two-mode network used by the existing continuation calculus is

\[
F_\mu=M_\nu\cup M_\rho,
\qquad
\{\mu,\nu,\rho\}=V_4\setminus\{0\}.
\]

A boundary terminal pairing records only the components of \(F_\mu\) that reach the pentagonal frontier.  It forgets internal alternating cycles and, more generally, which physical matching edges perform the splicing at each triangle.

`TrivalentDualSpliceSignature` therefore retains all three physical matchings and derives the complete path/cycle decomposition of every \(F_\mu\).

## 2. Exact matching surgery

A certified `sigma` domain translation along physical path \(P\) swaps the two complementary modes on that path.  At the matching level the exact identities are

\[
\boxed{M_\sigma'=M_\sigma}
\]

and

\[
\boxed{
M_\mu'=M_\mu\triangle P,
\qquad \mu\neq\sigma.
}
\]

`MatchingPathSwitchCertificate` checks these identities on the actual physical carrier.  This is the trivalent-dual form of the previously banked alternating-path surgery law.

## 3. What the three-interior-vertex kill witness teaches us

The pivot-to-pivot witness from `four-color-jordan-mod2-surgery.md` contains one internal alternating cycle in the network excluding its repeated boundary mode.  Its complete initial cycle profile is:

\[
(1,0,0)
\]

across the three excluded-mode networks, up to the fixed V4 mode ordering.

Every one of its four current pivot controls performs an exact matching switch and removes that internal cycle.  Nevertheless **every successor is still pivot-type**.

Thus internal cycle count contains real information that boundary pairing discarded, but

\[
\boxed{
\text{alternating-cycle count is not itself a sufficient descent rank.}
}
\]

The exact three-stage route makes the failure sharper:

\[
\begin{array}{c|c|c}
\text{construction} & \text{pairing regime} & \text{total alternating cycles}\\
\hline
z_0 & \text{pivot} & 1\\
z_1 & \text{pivot} & 0\\
z_2 & \text{direct} & 0
\end{array}
\]

So the second geometry-changing stage occurs entirely inside the zero-cycle stratum.

## 4. The correct finite object

The retained local control geometry can now be written as the three-matching object

\[
\boxed{
\mathfrak S(z)=
\bigl(D;M_{10},M_{01},M_{11};\partial D\bigr),
}
\]

where \(D\) is the fixed trivalent dual disk and the three matchings are content-addressed by their physical primal-edge carriers.

The previous F2 identities are immediate projections:

\[
F_\alpha=M_\beta\cup M_\gamma,
\]

\[
F_\alpha\triangle F_\beta=F_\gamma,
\]

and

\[
F_\alpha\cap F_\beta=M_\gamma.
\]

This object is finite on a fixed carrier and is changed by certified path switches rather than by arbitrary relabeling.

## 5. New theorem frontier

The proof obligation has moved again.  We now seek a finite quotient or rank of \(\mathfrak S(z)\) that is:

1. sensitive to trivalent splice structure, not merely frontier pairing;
2. compatible with the exact matching switch
   \(M_\mu\mapsto M_\mu\triangle P\);
3. insensitive to pure color-language gauge where appropriate;
4. strong enough that a zero-focus-slack construction always has a fresh certified control decreasing the rank or reaches positive focus slack.

The three-stage witness is now the first mandatory falsifier for any proposed rank: it must distinguish both pivot strata even though the second has no alternating cycles.

A promising next representation is to encode the three physical matchings as partial involutions on dual face/boundary nodes.  The products of pairs of these involutions recover the alternating path/cycle components, while their ordered composition retains the splice phase that component counts lose.

That is the next derivation target; no monotonicity claim is banked yet.
