# Algebraic Four Color Proof — Direct Construction Form

**Track:** B — independent of the held-out Rocq proof.  
**Status:** candidate algebraic proof program with an explicit unresolved closure theorem. No claim of a completed Four Color proof is made here.

## 1. The theorem species

For a finite planar graph `G=(V,E)`, let

\[
Q_4=\{0,1,2,3\}
\]

and let

\[
W_G(c):=\bigwedge_{uv\in E} c(u)\ne c(v)
\]

be the exact terminal edge witness. The target theorem is

\[
\forall G\in\mathrm{Planar}_{\mathrm{fin}},\quad
\exists c:V(G)\to Q_4\; W_G(c).
\]

Construction, bounded observation, and terminal decode are distinct species. Brown observation and completed-map facts are never proof authority for a construction transition.

## 2. Contract discipline

Every proposed proof transformation must retain the actual graph, the committed coloring, and the indexed edge ledger. A transformation is not admitted merely because it looks analogous to a Principia operator or because it succeeds on an isolated pentagon.

In particular:

1. local algebra may identify a candidate move but cannot erase exterior connectivity;
2. a modal transfer from another carrier is proof-relevant only after cyclic order, adjacency, operator action, and required invariants are explicitly preserved;
3. exact component swaps are valid graph morphisms and may be used as mechanical witnesses/falsifiers;
4. exhaustive computation may expose or refute a lemma but may not substitute for the missing algebraic implication;
5. a locked exterior is retained as evidence, not collapsed into a local picture.

This is the Four Color specialization of the Lipschitz Contract: expansion is admissible only when the witness boundary is preserved or explicitly enlarged.

## 3. The actual degree-five construction state

Let `v` be an uncommitted degree-five vertex after deleting it from a planar triangulation, and let its committed neighbors appear in cyclic order

\[
C=(c_0,c_1,c_2,c_3,c_4).
\]

The center has exactly

\[
A(v)=Q_4\setminus\{c_0,c_1,c_2,c_3,c_4\}
\]

as its direct admissible color set.

If the boundary uses at most three colors, `A(v)` is nonempty and the construction extends immediately. The hard case is therefore a proper `C5` boundary using all four colors.

Every saturated proper `C5` has multiplicity pattern

\[
2+1+1+1.
\]

After cyclic relabeling it has the role form

\[
A\;B\;A\;C\;D.
\]

The repeated color `A` is not an extra assumption; it is forced by five boundary positions and four terminal colors.

## 4. Direct V4 defect calculus on C5

Encode the four terminal colors by the Klein four group `V4`. For the actual boundary `C`, define the discrete derivative

\[
\delta_i=c_{i+1}-c_i\in V_4\setminus\{0\},
\qquad i\pmod 5.
\]

Because the cycle closes,

\[
\sum_{i=0}^{4}\delta_i=0.
\]

If the three nonzero `V4` modes occur with multiplicities `n_1,n_2,n_3`, closure implies

\[
n_1\equiv n_2\equiv n_3\pmod 2.
\]

Since their total is five,

\[
\boxed{(n_1,n_2,n_3)=(3,1,1)}
\]

for every proper `C5`, not merely for a fixed colored-center surrogate.

The position of the two singleton derivative modes exactly distinguishes the two boundary species:

\[
\boxed{\text{singleton derivative edges adjacent}\iff |\operatorname{im}(C)|=3}
\]

and

\[
\boxed{\text{singleton derivative edges separated}\iff |\operatorname{im}(C)|=4}.
\]

Thus the degree-five extension problem can be written as a defect-transport problem:

\[
\text{separated singleton derivative modes}
\longrightarrow
\text{adjacent singleton derivative modes}.
\]

When the singletons become adjacent, the boundary is automatically a three-color `C5`, so the center has exactly one available terminal color.

This is an algebraic reparameterization of the real hard boundary, not a completed proof of transport.

## 5. The two candidate one-step openings

For a saturated role word

\[
A\;B\;A\;C\;D,
\]

there are two distinguished two-color separations at the boundary level:

\[
\{B,C\}
\qquad\text{and}\qquad
\{B,D\}.
\]

If `B` and `C` lie in different connected components of the subgraph induced by colors `{B,C}`, swapping the component containing `B` opens the center. Likewise for `{B,D}`.

Therefore the one-step branch is exact:

- if at least one candidate pair is exterior-disconnected, there is a ledger-preserving opening component traversal;
- if both candidate pairs are exterior-connected, the local pentagon is **locked** against every one-step opening of this type.

The repository contains both positive and negative mechanical witnesses for this distinction.

## 6. Genuine planar lock and why local flattening is invalid

A planar saturated degree-five construction can realize both required exterior continuations simultaneously. In that state the center has no direct color and no one-step two-color component swap opens one.

This matters mathematically. It refutes the flat claim that cyclic order around the pentagon alone forces defect coalescence.

The exterior connectivity is part of the proof witness. When both candidate continuations exist, the admissible proof state must expand from the five-edge boundary to include the continuation paths that certify the lock.

This is the constructive meaning of bounded witness expansion:

\[
\boxed{\text{local lock}\Rightarrow\text{enlarge the retained boundary witness}.}
\]

A proof that discards those paths and reasons only on the pentagon violates the contract.

## 7. Principia machinery that survives direct transfer

The relevant Principia structure is directional transformation followed by bounded refinement:

\[
E_\lambda=R_\lambda\circ D_\lambda.
\]

For Four Color construction this can only be used as an architecture, not as imported theorem authority:

- `D` corresponds to extending a currently legal continuation of the retained coloring relation;
- `R` corresponds to a refinement forced when continuation meets an already retained planar relation;
- the refinement must preserve the graph ledger and cyclic incidence exactly.

Principia's chromatic transference result is useful only for its explicit invariant discipline: cyclic order and adjacency must survive carrier changes. Its imaginary traversal and observer-bounded curvature remain heuristic/research machinery unless an exact map to graph construction states is supplied.

Accordingly, the fixed-colored-region model is retained only as a red-team visualization. It is not a premise of the hard degree-five proof.

## 8. The remaining theorem: Witness-Expansion Closure

The missing theorem is now more exact than the earlier desaturation or coalescence slogans.

### Witness-Expansion Closure

Let `K` be a saturated degree-five construction state with boundary role word `A B A C D`.

Either:

1. one of the two candidate exterior separations `{B,C}` or `{B,D}` is disconnected, yielding an exact one-step opening; or
2. both are connected, yielding a retained planar lock witness.

In the locked branch, there must exist a finite sequence of witness expansions and exact ledger-preserving construction transformations

\[
(K,W_0)\to(K_1,W_1)\to\cdots\to(K_m,W_m)
\]

such that:

- every `W_i` contains the boundary and every continuation relation used to justify the next step;
- no step removes an inherited edge obligation;
- no step imports a completed four-coloring as authority;
- expansion is finite and bounded by an explicit planar/algebraic measure;
- the terminal construction state has a three-color neighbor image at the original focus vertex.

This theorem is **not yet proved**.

Its hard content is the locked branch. The problem is no longer to invent a local recoloring; it is to identify the planar/algebraic quantity that makes indefinite witness expansion impossible.

## 9. What a successful algebraic proof still needs

A completed Track-B proof requires all of the following:

1. the direct `V4` C5 calculus above;
2. the exact one-step opening criterion;
3. a classification of the retained continuation structure in the locked branch;
4. a monotone or nilpotent quantity on witness expansion that cannot cycle forever;
5. a proof that termination opens the original center rather than merely moving the obstruction;
6. global minimal-counterexample induction once Witness-Expansion Closure is established;
7. a no-hidden-4CT dependency audit.

The index-four nilpotent construction algebra remains a candidate for item 4, but it is not promoted until its action on the **expanded planar witness**, rather than on a four-state toy module, is explicitly defined.

## 10. Certification boundary

The repository may currently certify:

- exact construction-state edge preservation;
- direct admissible-color complement;
- direct proper-C5 `V4` derivative closure;
- the `3,1,1` derivative law;
- exact X3/X4 classification by singleton-defect adjacency;
- the two candidate one-step opening pairs;
- positive opening witnesses;
- a genuinely planar one-step locked negative witness;
- observer/terminal/dependency separation.

It may **not** yet certify a Four Color proof.

A full theorem certificate begins only when Witness-Expansion Closure is proved for the locked branch without erasing the exterior continuation witness.
