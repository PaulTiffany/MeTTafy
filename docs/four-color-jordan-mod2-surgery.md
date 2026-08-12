# Jordan / mod-2 Dual Surgery

**Status:** the shared-edge-aware mod-2 carrier algebra is exact and graph-native.  The previously proposed universal one-pivot-to-direct lemma is **false**.  A three-interior-vertex planar witness now kills both its universal and existential one-stage forms while retaining an exact three-stage route to positive focus palette slack.

## 1. Three two-mode networks form an F2 triangle

For a retained properly colored triangulated pentagonal disk and each nonzero V4 mode `mu`, define

\[
F_\mu=\{e:m(e)\neq \mu\}.
\]

If the three nonzero modes are \(\alpha,\beta,\gamma\), then edgewise

\[
\boxed{F_\alpha\triangle F_\beta=F_\gamma}
\]

and cyclically.  More importantly, the two networks are **not disjoint**.  Their physical overlap is exactly the carrier of their common mode:

\[
\boxed{F_\alpha\cap F_\beta=E_\gamma},
\]

where \(E_\gamma=\{e:m(e)=\gamma\}\).

`ModeNetworkTriangleCertificate` checks all three symmetric-difference identities and all three shared-carrier identities on the actual retained disk.  This is the correct mod-2 object for Jordan reasoning: shared physical edges are retained rather than perturbed away by assumption.

## 2. Exact path surgery

Let \(P\) be one actual embedded path of the `sigma` two-mode continuation family.  Translation of one primal side by \(\sigma\) preserves the `sigma` network and toggles the same physical path carrier into each complementary network:

\[
F_\sigma' = F_\sigma,
\qquad
F_\mu'=F_\mu\triangle P\quad(\mu\neq\sigma).
\]

The boundary endpoints of a pivot path fall into exactly two saturated-C5 Jordan patterns:

1. **endpoint slide:** one endpoint has the repeated mode and one has the other singleton mode; the two boundary terminals are cyclically adjacent;
2. **interlaced pair:** both endpoints have the repeated mode; the path endpoints alternate around the boundary with the two terminals of the repeated-mode complement network.

`JordanMod2SurgeryCertificate` certifies these boundary parity facts together with the full physical symmetric-difference surgery.  It deliberately records the successor pairing instead of defining it to be direct.

## 3. Kill witness for one-pivot-to-direct

The following triangulated disk has three interior vertices `x0,x1,x2`:

```text
(b,x0,x1)   (x1,x2,x0)   (e,x2,d)
(a,x0,b)    (x1,d,x2)    (e,x0,a)
(e,x0,x2)   (c,x1,b)     (c,x1,d)
```

with exact committed coloring

```text
a=0, b=1, c=0, d=2, e=3,
x0=2, x1=3, x2=1.
```

The focus boundary is the familiar saturated word

\[
(0,1,0,2,3).
\]

Both current singleton continuation families are pivot-type.  There are four current graph-native dual controls: two singleton modes times two actual embedded paths.

The decisive mechanical result is

\[
\boxed{
\text{all four immediate certified stages are pivot}\to\text{pivot}.
}
\]

Every one of those four transitions still satisfies the exact F2 triangle, shared-carrier identities, Jordan endpoint pattern, and alternating-path surgery law.

Therefore both conjectures are falsified:

\[
\operatorname{Pivot}(z)
\not\Rightarrow
\forall P\;\operatorname{Direct}(T_Pz),
\]

and even

\[
\operatorname{Pivot}(z)
\not\Rightarrow
\exists P\;\operatorname{Direct}(T_Pz)
\]

for a single immediate stage.

This is not a failure of the dual algebra.  It is evidence that Jordan endpoint separation plus mod-2 carrier surgery does not, by itself, determine the successor control pairing once shared trivalent carrier structure is retained.

## 4. Cost of Cacophony becomes genuinely staged

The same kill witness has no certified route within two stages under the current graph-native dual controller.  A breadth-first receding-horizon audit with nonreplay history finds an exact route in three stages:

\[
\boxed{
\text{pivot}\to\text{pivot}\to\text{direct action}\to A(v)\neq\varnothing.
}
\]

The route therefore has

\[
C_{\mathrm{extra}}=3-1=2.
\]

That is a sharper realization of the Cost-of-Cacophony picture than the boundary-only `0/1` staging split.  Interference cost is not merely whether a pivot is required; it can be the number of lawful geometry-changing stages required before the current control basis exposes positive focus slack.

`CertifiedStagedFocusSlackRoute` and `route_focus_slack_bounded` mechanize this without future-state coordinates.  At every search node the controls are re-derived from the exact current embedding and filtered through content-addressed nonreplay history.

## 5. What survives and what changes

The following pieces are now banked:

\[
\boxed{F_\alpha\triangle F_\beta=F_\gamma}
\]

\[
\boxed{F_\alpha\cap F_\beta=E_\gamma}
\]

\[
\boxed{F_\sigma'=F_\sigma,
\quad F_\mu'=F_\mu\triangle P}
\]

and the two exact Jordan endpoint patterns above.

What is killed is the claim that one such surgery must immediately change the pairing regime.

The new proof obligation is therefore not `pivot -> direct in one stage`.  It is a **finite staged descent law** strong enough to show that repeated fresh graph-native surgery cannot remain in zero focus slack forever.

The next invariant must see more than boundary terminal pairing.  It must retain the trivalent shared-carrier interaction -- equivalently, how the three F2 networks are spliced through common-mode physical edges -- while remaining finite and nonrepeating on the fixed planar carrier.

That is the next theorem target.
