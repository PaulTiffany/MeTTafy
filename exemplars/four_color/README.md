# Sprint 01 — Four Color Theorem

The Four Color Theorem is MeTTafy's first historical exemplar because it exposes several distinct moments in the history of computational proof:

1. a famous human conjecture;
2. a plausible but flawed human proof strategy;
3. a computer-assisted proof whose finite case analysis became part of the mathematical controversy;
4. a later simplified computational proof with released programs/checking data;
5. a fully machine-checked formal proof.

The pedagogical objective is not merely to explain the theorem. It is to show **where computation enters mathematical reasoning**, how trust boundaries changed over time, and how MeTTafy can recover reusable semantic proof strategies from the resulting proof programs.

## Canonical formal artifact

MeTTafy pins the maintained Rocq community formalization:

- repository: `rocq-community/fourcolor`
- commit: `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`
- license: CeCILL-B

No upstream proof source is vendored here. `manifest.json` records the files and proof layers we study.

## What the top-level formal proof actually does

The pinned `theories/proof/fourcolor.v` makes the high-level architecture unusually explicit.

For a finite simple map, it:

```text
finite simple map
    -> discretize to a planar hypermap
    -> prove the combinatorial four-color theorem there
    -> transport the resulting coloring back to the map
```

For an arbitrary simple map, it applies a compactness extension to the finite result.

This gives MeTTafy an initial semantic decomposition:

```text
FiniteReduction
    -> Discretization
    -> RepresentationChange
    -> StructuralReduction / CombinatorialCore
    -> ProofByTransport
    -> CompactnessExtension
```

The combinatorial theorem in `combinatorial4ct.v` then reveals another layer: reduction to a cubic structure, induction/minimal-counterexample reasoning, an explicit colorability decision, and the unavoidability/reducibility machinery. The underlying repository separates substantial pieces of this machinery into files such as `unavoidability.v`, `reducibility.v`, and `discharge.v`.

`high_level_strategy.metta` is our first hand-annotated target strategy graph. It is **not** a new proof of the theorem; it is a semantic representation derived from the pinned proof artifact.

## Historical reading path

The intended learner path is:

```text
Guthrie (1852)
    -> Kempe (1879)
    -> reducibility / unavoidable configurations / discharging
    -> Appel & Haken computer-assisted proof (1976/1977)
    -> Robertson, Sanders, Seymour & Thomas simplification (1996/1997)
    -> Gonthier computer-checked Coq proof (2005)
    -> maintained Rocq formal artifact
    -> MeTTafy strategy graph
```

Useful starting references:

- Kenneth Appel and Wolfgang Haken, *Every planar map is four colorable. Part I: Discharging*, Illinois Journal of Mathematics 21 (1977), 429–490.
- Kenneth Appel, Wolfgang Haken, and John Koch, *Every planar map is four colorable. Part II: Reducibility*, Illinois Journal of Mathematics 21 (1977), 491–567.
- Neil Robertson, Daniel P. Sanders, Paul Seymour, and Robin Thomas, *The four-colour theorem*, Journal of Combinatorial Theory, Series B 70 (1997), 2–44.
- Georges Gonthier, *Formal Proof — The Four-Color Theorem*, Notices of the AMS 55(11) (2008), 1382–1393, describing the computer-checked proof project.
- Robin Thomas's Georgia Tech Four Color Theorem pages preserve a useful explanation of the Robertson–Sanders–Seymour–Thomas proof and links to the associated computational material.

## Benchmark separation

The learner-facing record contains names, dates, theorem names, source paths, and historical explanations.

The classifier-facing benchmark must not.

`mettafy.exemplars.blind_exemplar_view()` strips documentary and answer-key fields, while `exemplar_strategy_targets()` extracts the held-out semantic labels separately. This prevents a recognizer from scoring well merely by recognizing the phrase "Four Color Theorem."

## Sprint completion target

Sprint 01 is complete when MeTTafy can reproducibly:

1. resolve and verify the pinned formal artifact;
2. extract structural evidence from the selected proof layers;
3. produce a strategy graph without historical/name leakage;
4. compare that graph to the held-out annotations;
5. emit an inspectable MeTTa representation; and
6. present the result as a coherent historical/computational lesson.
