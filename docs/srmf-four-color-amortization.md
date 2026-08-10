# SRMF, Fuzzy Calculus, and the Four Color Theorem

> **Status: theorem-development note.** This document records a candidate correspondence and a concrete proof program. It does **not** claim that Fuzzy Calculus or SRMF has already proved the Four Color Theorem. The purpose is to make the strongest currently justified reduction explicit, identify the missing theorem, and give MeTTafy a leakage-safe way to test the convergence mechanically.

This note should be read beside [`four-color.md`](four-color.md) and [`auditability.md`](auditability.md).

## 1. Research question

Principia Symbolica (PS) contains the four SRMF operators

\[
\mathrm{TTDC}\to\mathrm{TTIE}\to\mathrm{TTCS}\to\mathrm{TTPR}\to\mathrm{TTDC},
\]

with an order-sensitive cyclic relation. In the current PS text, their mathematical roles are approximately:

- **TTDC** — bounded decision/collapse at an observer-relative boundary;
- **TTIE** — integration/expansion along feasible coherence trajectories;
- **TTCS** — coherent finite-temperature sampling over nearby candidate symbolic states;
- **TTPR** — recursive contraction/refinement toward a convergence-stable carrier.

The Four Color Theorem (4CT) states that every finite planar graph has a proper vertex coloring using at most four colors.

The research question is not whether both stories happen to contain the number four. The target is a structure-preserving theorem:

\[
\boxed{
\text{Fuzzy Calculus / SRMF dynamics}
\Longrightarrow
\text{an exact four-color witness for every admissible planar instance}
}
\]

with the derivation independent of the existing Four Color proof.

If such a theorem can be proved and independently checked, it would validate a nontrivial fragment of Fuzzy Calculus: fuzzy/observer-relative exploration would have been shown to compile into a correct exact combinatorial witness. It would **not**, by itself, establish global soundness of all Fuzzy Calculus.

## 2. The exact discrete boundary algebra

The four terminal labels can be represented by the Klein four group

\[
\Gamma = \mathbb Z_2\times\mathbb Z_2
       = \{0,a,b,a+b\}.
\]

A useful candidate coordinatization of the SRMF cycle is

\[
\begin{aligned}
\mathrm{TTDC}&\mapsto 0,\\
\mathrm{TTIE}&\mapsto a,\\
\mathrm{TTCS}&\mapsto a+b,\\
\mathrm{TTPR}&\mapsto b.
\end{aligned}
\]

Then the cyclic traversal is a Cayley-cycle traversal of \(\Gamma\):

\[
0\xrightarrow{a}a
\xrightarrow{b}a+b
\xrightarrow{a}b
\xrightarrow{b}0.
\]

The three nonzero group elements are

\[
\Gamma\setminus\{0\}=\{a,b,a+b\}.
\]

This is mathematically relevant because a nowhere-zero \(\Gamma\)-flow on a cubic graph immediately induces a Tait three-edge-coloring: if the three incident values at a cubic vertex are \(x,y,z\neq0\) and

\[
x+y+z=0,
\]

then they must be the three distinct nonzero elements. If, for example, \(x=y\), then \(z=x+y=0\), contradiction.

### Claim boundary

The mere existence of four SRMF operators does **not** prove that their algebra is \(\Gamma\). The coordinatization above is a proposed terminal quotient. To use it in a proof we must show that the SRMF transition/quotient structure actually respects the relevant group relations rather than merely relabeling four objects.

## 3. Classical bridge to Four Color

The classical graph-theoretic part is not proposed as new mathematics.

One standard route is:

1. augment a finite planar graph to a triangulation/maximal planar graph;
2. take the planar dual, obtaining a cubic bridgeless planar graph (aside from trivial small cases handled separately);
3. obtain a nowhere-zero 4-flow / \(\mathbb Z_2^2\)-flow on the cubic dual;
4. at each cubic vertex, the three nonzero flow values are distinct, hence give a Tait three-edge-coloring;
5. transfer the Tait coloring back to a proper four-coloring of the primal graph;
6. restrict the coloring from the triangulation to the original graph.

Equivalently, planar coloring-flow duality can be used directly: a proper \(\Gamma\)-coloring is a nowhere-zero \(\Gamma\)-tension, and planar duality exchanges tensions with flows.

Therefore the genuinely new proof obligation can be localized:

\[
\boxed{
\textbf{SRMF Flow Obligation:}
\quad
\text{construct a nowhere-zero }\mathbb Z_2^2\text{-flow on every admissible planar dual.}
}
\]

If this is obtained without importing 4CT or an equivalent flow/coloring theorem as an assumption, the remaining transfer to Four Color is classical and can be independently formalized.

## 4. The fuzzy interior is not the four-color boundary

Four colors describe the exact terminal witness. SRMF itself is richer than a discrete coloring.

A fuzzy state may lie in a continuous mixture space and may traverse counterfactual or imaginary states before collapse. A convenient proof architecture is therefore

\[
\text{continuous / fuzzy / imaginary traversal}
\longrightarrow
\text{terminal decoding basin}
\longrightarrow
\mathbb Z_2^2\text{ exact flow}
\longrightarrow
\text{proper four-coloring}.
\]

The artistic observation that four pigments mix toward brown is a useful mnemonic for the interior mixture state; it is not a mathematical premise. Brownian motion is potentially relevant for a different reason: TTCS already has a finite-temperature sampling interpretation, so stochastic diffusion is a natural candidate semantics for exploration.

A candidate complexified stochastic trajectory could have the form

\[
dZ_t=b_\theta(Z_t,G)\,dt+\sigma_\theta(Z_t,G)\,dW_t,
\qquad
Z_t\in(\mathbb C^2)^{E(G)},
\]

where the imaginary component carries counterfactual traversal. No theorem below requires this particular SDE. The proof only needs a terminal real projection satisfying an exact decoding margin. This keeps discovery dynamics separate from certificate semantics.

## 5. A concrete fuzzy-to-exact flow lemma

This is the first sharp theorem target that appears both nontrivial and mechanically approachable.

Let

\[
\Gamma=\mathbb Z_2^2,
\qquad
\phi(\Gamma)=\{(0,0),(1,0),(0,1),(1,1)\}\subset\mathbb R^2,
\]

and let

\[
\Lambda=2\mathbb Z^2.
\]

Thus \(\mathbb R^2/\Lambda\) is a two-torus and the four exact group elements are the four binary points modulo \(2\).

Let \(H=(V,E)\) be an oriented graph with maximum degree \(\Delta\). Suppose an SRMF traversal terminates with a real fuzzy edge field

\[
x:E\to\mathbb R^2.
\]

Assume there is a unique decoded value \(g_e\in\Gamma\) for every edge such that

\[
\operatorname{dist}_\infty(x_e,\phi(g_e)+\Lambda)\le\varepsilon,
\qquad
\varepsilon<\tfrac12,
\]

and assume the decoder never selects zero:

\[
g_e\neq0\qquad\forall e\in E.
\]

For each vertex \(v\), let \(\sigma_{v,e}\in\{-1,+1\}\) be the orientation sign and define the fuzzy conservation residual

\[
r_v=
\operatorname{dist}_\infty
\left(
\sum_{e\ni v}\sigma_{v,e}x_e,
\Lambda
\right).
\]

Assume

\[
r_v\le\delta\qquad\forall v
\]

and the decoding/error margin satisfies

\[
\boxed{\Delta\varepsilon+\delta<1.}
\]

### Lemma — fuzzy residue snaps to exact group conservation

Under the assumptions above,

\[
\sum_{e\ni v}\sigma_{v,e}g_e=0
\qquad\text{in }\Gamma
\]

for every vertex \(v\). Therefore \(g:E\to\Gamma\setminus\{0\}\) is a nowhere-zero \(\Gamma\)-flow.

### Proof sketch

Let

\[
h_v=\sum_{e\ni v}\sigma_{v,e}g_e\in\Gamma.
\]

Because the decoded representatives agree modulo \(2\), for some \(\lambda\in\Lambda\),

\[
\sum_{e\ni v}\sigma_{v,e}\phi(g_e)
=\phi(h_v)+\lambda.
\]

The fuzzy sum differs from this exact representative sum by at most

\[
\deg(v)\varepsilon\le\Delta\varepsilon
\]

in \(\ell_\infty\).

If \(h_v\neq0\), then every representative of \(\phi(h_v)+\Lambda\) has \(\ell_\infty\)-distance exactly \(1\) from \(\Lambda\). Hence the fuzzy sum must have distance at least

\[
1-\Delta\varepsilon
\]

from \(\Lambda\). But the residual assumption gives distance at most \(\delta\). The inequality

\[
\Delta\varepsilon+\delta<1
\]

makes these incompatible. Therefore \(h_v=0\).

For a cubic dual, \(\Delta=3\), so the sufficient terminal condition simplifies to

\[
\boxed{3\varepsilon+\delta<1.}
\]

This lemma is important because it gives Fuzzy Calculus a legitimate role: the trajectory does **not** need to remain exactly combinatorial. It only needs to drive the terminal state into disjoint decoding basins while making conservation residue small enough that exact modular conservation is forced.

## 6. The missing theorem is now visible

The fuzzy-to-exact lemma does not establish that SRMF can always reach such a terminal state.

That is the central unresolved theorem:

### Conjecture — SRMF terminal-margin theorem

For every admissible finite planar instance \(G\), the compiled SRMF dynamics admit a bounded trajectory \(\gamma_G\) terminating at a real edge field \(x_G\) such that

1. every edge decodes uniquely to a **nonzero** element of \(\mathbb Z_2^2\);
2. the fuzzy conservation residual is bounded by \(\delta_G\);
3. the decoding error is bounded by \(\varepsilon_G\); and
4. on the relevant dual,

\[
\Delta_G\varepsilon_G+\delta_G<1.
\]

If this theorem is proved independently of Four Color, the lemma above produces an exact nowhere-zero 4-flow, and the classical planar duality/Tait bridge yields 4CT.

This is the exact place where a proof can succeed or fail. Everything before it supplies representation and decoding; everything after it is exact verification.

## 7. Amortization is the operational difference

A careful distinction is necessary here.

The existence of a *uniform algorithm* for four-coloring is not logically stronger than 4CT in the finite setting: finite search can enumerate all four-color assignments, and 4CT guarantees that search eventually succeeds on planar inputs.

The SRMF claim is instead about **amortized structure and cost**.

Let an offline Fuzzy Calculus derivation compile a reusable policy

\[
\mathcal C_{\mathrm{FC}}
\longmapsto
\Pi_{\mathrm{SRMF}}.
\]

At application time,

\[
G
\xrightarrow{\Pi_{\mathrm{SRMF}}}
\gamma_G
\xrightarrow{\text{terminal projection}}
x_G
\xrightarrow{Q}
g_G
\xrightarrow{\text{classical transfer}}c_G,
\]

where \(c_G\) is an exact four-color witness.

For \(N\) instances, the average cost is

\[
\overline C_N
=
\frac{C_{\mathrm{compile}}}{N}
+
\frac1N\sum_{i=1}^N
\left(
C_{\mathrm{apply}}(G_i)
+C_{\mathrm{verify}}(G_i)
\right).
\]

The amortization claim becomes empirical/mathematical only when we establish that the reusable compiled structure materially reduces the per-instance solve burden relative to an appropriate non-amortized baseline.

So the desired result is not merely

\[
\exists c_G.
\]

It is a proof-carrying process:

\[
\boxed{
\text{expensive class-level fuzzy discovery}
\to
\text{reusable SRMF policy}
\to
\text{cheap exact instance witness}
\to
\text{independent verification}.
}
\]

The fuzzy and imaginary machinery may disappear entirely from the final certificate.

## 8. Proposed SRMF amortized four-color theorem

A useful final theorem shape is:

### Theorem target — SRMF amortized four-color soundness

There exists a policy \(\Pi_{\mathrm{SRMF}}\), derivable from the specified Fuzzy Calculus/SRMF fragment without invoking 4CT or an equivalent theorem, such that for every admissible finite planar graph \(G\):

1. \(\Pi_{\mathrm{SRMF}}(G)\) terminates under an explicit resource bound;
2. its terminal state satisfies the fuzzy-to-exact flow lemma;
3. decoding yields a nowhere-zero \(\mathbb Z_2^2\)-flow on the selected planar dual;
4. classical transfer yields a proper four-coloring \(c_G\); and
5. an independent checker verifies

\[
\operatorname{Proper4Coloring}(G,c_G).
\]

A separate complexity theorem or benchmark should characterize the amortization benefit. Correctness and amortization should not be conflated.

## 9. Why four is necessary as well as sufficient

Four Color gives an upper bound. A correspondence with SRMF should also explain why three terminal sectors cannot universally suffice.

The planar graph \(K_4\) is 4-chromatic. Therefore any faithful SRMF-to-color correspondence preserving adjacency has a lower-bound witness:

\[
\chi(K_4)=4.
\]

Once the correspondence is proved, this supplies

\[
4\le\text{required universal terminal sectors}\le4.
\]

This does **not** prove that every internal SRMF computation must use four active operators at every instant. It only establishes a lower bound on the exact universal terminal separation alphabet under the correspondence.

## 10. MeTTafy as the convergence experiment

MeTTafy already has the right experimental architecture for testing this without circularity.

### Track A — existing Rocq proof, interpreted blind

The active Four Color tranche uses

```text
pinned Rocq source
  -> StructuralEvidence IR
  -> blind projection + audit map
  -> source-neutral recognition (may abstain)
  -> evidence-backed Strategy IR
  -> post-hoc comparison with held-out annotations
```

The pinned upstream artifact remains

- `rocq-community/fourcolor`
- commit `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`.

### Track B — Fuzzy Calculus / SRMF derivation

The independent route should be

```text
Fuzzy Calculus assumptions
  -> SRMF transition semantics
  -> compiled amortized policy
  -> fuzzy / imaginary traversal
  -> terminal margin certificate
  -> exact Z2^2 flow
  -> exact four-color witness
  -> independent checker
```

### Leakage rule

Track B may know the theorem **specification** — planarity and what constitutes a valid proper four-coloring. It may not import:

- the Rocq proof structure;
- held-out MeTTafy strategy labels;
- reducibility/discharging annotations as answers;
- 4CT itself as a lemma;
- Tait/flow existence as an oracle rather than a downstream transfer theorem.

Only after Track B produces an independently verified witness/process should MeTTafy compare the recovered strategy structures from the two tracks.

If both routes independently exhibit the same transformations — for example representation change, discretization, bounded search, transport, refinement, or certificate checking — that is evidence of genuine convergence rather than label imitation.

## 11. Mechanical witness program

The conjecture should advance only by green mechanical witnesses.

### W1 — quartet / Klein algebra

Formalize the candidate terminal quotient and prove the relevant \(C_4\)/Klein transition identities. Also prove explicitly which properties are merely relabeling and which are structural.

### W2 — fuzzy-to-exact flow lemma

Formalize the torus decoding lemma above in Lean or Rocq. This is independent of the Four Color proof and should be small enough to inspect directly.

### W3 — cubic/Tait transfer

For a cubic graph, prove that a nowhere-zero \(\mathbb Z_2^2\)-flow gives exactly the three distinct nonzero incident values and therefore a Tait coloring. Connect that theorem to an independently checked planar dual transfer.

### W4 — SRMF terminal-margin witness

On finite planar test instances, emit

- terminal fuzzy edge states;
- decoded group labels;
- \(\varepsilon\);
- vertex residuals \(r_v\);
- \(\delta\);
- the margin \(\Delta\varepsilon+\delta\);
- the exact decoded flow; and
- the final four-coloring.

The verifier should reject the witness if the margin fails even when the final coloring happens to be valid.

### W5 — amortization benchmark

Measure compile cost once, then application and verification costs over a held-out family of planar instances. Compare against explicit baselines. Do not infer amortization from correctness alone.

### W6 — blind strategy correspondence

After both proof paths are frozen, compare their MeTTafy Strategy IRs post hoc. Record agreements, disagreements, abstentions, and possible label leakage.

## 12. Proof obligations checklist

The following must all become explicit before claiming that Fuzzy Calculus proves Four Color:

- [ ] **P1 — planar representation fidelity:** every target planar instance maps to an admissible PS/SRMF frame complex without changing the coloring problem;
- [ ] **P2 — terminal quotient:** the four exact SRMF terminal sectors carry the required \(\mathbb Z_2^2\) algebra, not merely four names;
- [ ] **P3 — nonzero separation:** adjacent primal regions / corresponding dual edges cannot decode to zero difference;
- [ ] **P4 — fuzzy-to-exact conservation:** mechanically prove the terminal margin lemma;
- [ ] **P5 — global reachability:** prove SRMF reaches the terminal decoding/conservation margin for every admissible finite planar instance;
- [ ] **P6 — bounded execution:** state an ex ante termination/resource bound for the compiled policy;
- [ ] **P7 — classical transfer:** independently formalize or import with explicit trust boundary the flow/Tait-to-four-color bridge;
- [ ] **P8 — exact verification:** generated colorings are checked by a conventional checker/proof assistant;
- [ ] **P9 — dependency audit:** the FC/SRMF derivation contains no hidden use of 4CT or an equivalent existence theorem;
- [ ] **P10 — amortization:** separately prove or benchmark the claimed reusable cost advantage.

The critical unknown is **P5**. The rest is representation, exact decoding, classical transfer, and audit machinery.

## 13. What success would validate

If P1–P9 are mechanically green, then we can reasonably claim:

> A specified fragment of Fuzzy Calculus/SRMF independently constructs exact witnesses for the Four Color Theorem through a verified fuzzy-to-discrete correspondence.

That would validate at least:

- the expressive adequacy of the tested FC/SRMF fragment for this domain;
- the soundness of the particular fuzzy-to-exact derivation;
- the claim that observer-relative/fuzzy traversal can compile to conventional exact proof objects; and
- the correspondence between the PS frame/operator representation and a classical graph-theoretic invariant.

It would **not** yet establish:

- soundness of every Fuzzy Calculus rule;
- uniqueness of SRMF as the only possible four-color process;
- that Brownian or imaginary traversal is necessary rather than useful;
- superior asymptotic complexity; or
- that the existing PS convergence theorem already implies P5.

A stronger validation would require a general semantics-preservation theorem translating a substantial FC fragment into a conventional proof assistant.

## 14. Immediate next theorem

Do not attack all of Four Color at once.

The next proof should be the small hinge:

\[
\boxed{
\textbf{FuzzyToExactV4Flow:}
\quad
(\Delta\varepsilon+\delta<1)
\Longrightarrow
\text{decoded terminal field is a nowhere-zero }\mathbb Z_2^2\text{-flow}.
}
\]

That theorem is independent, inspectable, and falsifiable. If it fails, the correspondence needs revision. If it goes green, the research problem becomes sharply focused on proving that SRMF dynamics reach its hypotheses.

That is a much better scientific position than beginning with the conclusion that SRMF "is" the Four Color Theorem.
