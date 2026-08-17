# Browning-Out Color Algebra — Differential-Dynamics Grounding

This note advances Track B of the independent Four Color proof program. It corrects an important dependency error in the first browning-out draft:

```text
WRONG:  SRMF cycle -> prove NoStableFifthClass
RIGHT:  differential dynamics -> derive chromatic closure -> SRMF witnesses/transports it
```

SRMF is not proof authority for a theorem whose operator cycle is itself a chart/factorization of the underlying continuous dynamics.

## 1. Foundational substrate

Principia Symbolica's foundational symbolic evolution is the Fokker--Planck relation

\[
\frac{\partial \rho}{\partial s}
= -\nabla\cdot(\rho D)+\beta^{-1}\Delta_s\rho,
\]

where `rho` is symbolic probability density, `D` is the drift field, `Delta_s` is the symbolic Laplace--Beltrami operator, and `beta > 0` is inverse temperature.

The continuous substrate is therefore a drift--diffusion system. The corresponding operational decomposition is:

```text
drift / advection      move symbolic density through possibility
diffusion / sampling   spread mass across coherent futures
gradient contraction   sharpen candidates toward stable forms
boundary collapse      impose decision / discontinuity / commitment
```

SRMF later exposes these phases as test-time symbolic charts:

```text
TTIE  <- advection / integration
TTCS  <- diffusion / stochastic sampling
TTPR  <- contraction / refinement
TTDC  <- boundary collapse / commitment
```

The arrows are dependency arrows, not definitions by fiat.

## 2. Brownian motion is inside the substrate

The diffusion generator `beta^{-1} Delta_s` is the mathematical home of the Brownian component. The relevant point is not that a color label performs an arbitrary random walk. Rather, unresolved microscopic symbolic trajectories are represented macroscopically by drift--diffusion evolution.

Let

\[
L^*\rho := -\nabla\cdot(\rho D)+\beta^{-1}\Delta_s\rho
\]

be the forward generator on densities. Its diffusion semigroup smooths fine distinctions while preserving total probability under the declared boundary hypotheses.

Thus a chromatic history can remain present in the underlying density while cease to be separately recoverable by a bounded terminal observation.

That is the correct location for **browning out**.

## 3. Chromatic observable and browning

Let `C` be a symbolic chromatic observable on the state manifold. Do not assume four terminal values yet.

For an observer `O`, let

\[
Q_O:C(M)\to \mathcal C_O
\]

be the finite-resolution chromatic observation map.

Two microscopic chromatic histories `h1,h2` are observationally equivalent after evolution time `s` when

\[
Q_O(P_s h_1)=Q_O(P_s h_2),
\]

where `P_s` is the semigroup induced by the underlying drift--diffusion dynamics.

A **brown state** is an equivalence/residue class produced when multiple microscopic chromatic histories remain dynamically represented but are no longer independently terminally discriminable after amortized drift--diffusion and observer projection.

Brown therefore means:

```text
retained microscopic / provenance structure
+ lost independent terminal chromatic discriminability
```

It does NOT mean:

```text
zero
cancellation
grey
fifth terminal color
forgotten obligation
```

## 4. Indexed graph obligations remain external invariants

For a finite planar graph `G=(V,E)`, each edge carries an indexed obligation

\[
O_{uv}: c(u)\ne c(v).
\]

These obligations are distinct by edge identity even when current values coincide.

Browning is admissible only on internal chromatic provenance. It may not erase an external edge obligation. A terminal collapse is valid only when every indexed edge obligation remains satisfied after observation/collapse.

Hence the forbidden move remains

```text
unsatisfied edge -> diffuse/brown -> forget edge -> declare solved.
```

The edge ledger is not part of what diffusion is permitted to erase.

## 5. Correct theorem target: differential closure first

The central novel theorem must now be stated below SRMF.

### Planar Chromatic Differential Closure (target)

For the declared Principia drift--diffusion/contraction/collapse dynamics with planar pairwise boundary constraints, every dynamically persistent, observer-discriminable terminal chromatic basin is representable using at most four mutually separating terminal classes; any putative additional chromatic distinction either

1. evolves into an existing terminal basin,
2. remains transient/nonterminal under the continuous dynamics, or
3. becomes brown residue whose provenance may persist but whose independent terminal chromatic rank does not.

Schematically,

\[
\operatorname{rank}_{\mathrm{terminal}}
\bigl(Q_O\circ P_s\bigr)\le 4
\]

for the planar admissible terminal regime.

This inequality is the theorem to derive. It must not be inserted as an SRMF rule.

## 6. SRMF result becomes a corollary

Only after Planar Chromatic Differential Closure is established may we transport the result upward:

```text
Fokker--Planck / differential closure
  -> operator-phase factorization
  -> TTIE / TTCS / TTPR / TTDC witness trace
  -> NoStableFifthClass as an SRMF corollary
  -> exact terminal coloring certificate
```

The SRMF statement is therefore:

### NoStableFifthClass (derived form)

No admissible SRMF trace may terminate in a fifth independently chromatic class if the underlying differential trajectory lies in the planar closure regime proved above.

This is not an independent premise.

## 7. Why the four-operator cycle cannot prove fourness by itself

The SRMF cycle has four named charts, but that cardinality is downstream structure. Using

```text
four SRMF operators -> four colors
```

would be numerology/circular pattern matching unless the four-channel decomposition itself is derived as the relevant minimal factorization of the underlying chromatic differential dynamics.

The proof must instead show that the continuous planar system has only four terminally independent chromatic degrees/basins under the declared constraints. SRMF may then expose those modes.

## 8. Brownian / browning-out proof handle

The foundational Fokker--Planck equation gives a precise handle absent from the earlier draft:

\[
\partial_s\rho
= -\nabla\cdot(\rho D)+\beta^{-1}\Delta_s\rho.
\]

The second-order term is smoothing. Principia's associated H-theorem/free-energy machinery supplies monotone relaxation structure. Therefore the browning question can be made spectral:

> Which chromatic modes survive the drift--diffusion semigroup and subsequent admissible contraction as independent terminal observables, and which modes decay into composite residue?

A putative fifth color must be represented by a fifth independent mode that survives all of:

```text
planar boundary constraints
+ drift
+ diffusion
+ contraction
+ bounded observation
+ terminal collapse
```

If its mode decays, merges, or becomes observationally dependent, it browns out.

This is a differential/spectral statement, not an SRMF naming statement.

## 9. Mechanical proof obligations

The MeTTa validator should now track the following dependency graph:

```text
PrincipiaFokkerPlanck                    [premise / existing theorem]
PlanarBoundaryEncoding                   [prove]
ChromaticModeDefinition                  [define]
DiffusionModeEvolution                   [derive]
ObligationPreservation                   [prove]
PlanarTerminalRankBound                  [OPEN — central theorem]
BrowningOutOfNonterminalModes            [derive from rank/mode theorem]
SRMFFactorization                        [existing/derived transport]
NoStableFifthClass                       [corollary]
ExactColoringCertificate                 [downstream]
```

MeTTa must reject any proof graph in which `NoStableFifthClass` or four SRMF chart names are used to establish `PlanarTerminalRankBound`.

## 10. Constructive falsifier

A counterexample to this proof route is not merely a fifth symbolic name. It is a planar boundary-compatible fifth chromatic mode/basin `x5` satisfying all of:

```text
independent of four existing terminal modes
persistent under the underlying differential evolution
not killed/merged by diffusion
stable under admissible contraction
observer-discriminable at terminal resolution
preserves every indexed adjacency obligation
survives terminal collapse as a genuinely new chromatic class
```

Such a witness would falsify Planar Chromatic Differential Closure and therefore the browning-out proof route.

## 11. Relation to the classical downstream algebra

If the differential theorem yields an exact four-class coloring, `V4 = Z2 x Z2`, nowhere-zero flow, and Tait decoding remain available as downstream representations/checks. They are not the source of fourness.

Likewise, the held-out Rocq Four Color development remains comparison/validation material, not a Track-B premise.

## 12. Current proof spine

```text
planar adjacency / indexed edge obligations
  -> Principia symbolic manifold + chromatic observable
  -> symbolic Fokker--Planck drift--diffusion
  -> spectral / variational evolution of chromatic modes
  -> planar terminal-rank theorem                 [CENTRAL OPEN STEP]
  -> nonterminal excess modes brown out
  -> SRMF factorization witnesses the trajectory
  -> NoStableFifthClass                           [COROLLARY]
  -> <= 4 exact terminal colors
  -> mechanically checked coloring certificate
```

The correction is load-bearing: **the differential-equation loop is upstream of SRMF.** The proof of fourness belongs there.