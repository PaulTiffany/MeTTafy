# Sprint 01 — The Four Color Theorem

> **Goal:** understand one famous computational proof without needing to know Rocq, Coq, or MeTTa first.

## 1. The question

Can every map drawn on a plane be colored with at most four colors so that regions sharing a boundary have different colors?

The statement is easy to picture. The proof is not.

That mismatch is exactly why the Four Color Theorem is such a good first MeTTafy exemplar.

## 2. Why this theorem matters computationally

The theorem became famous not only because of the mathematics, but because the accepted proof required computer-assisted checking of a large finite family of configurations.

The historical arc matters:

```text
conjecture
  -> plausible human proof
  -> flaw discovered
  -> structural reduction
  -> computer-assisted finite checking
  -> simplified computational proof
  -> fully machine-checked formal proof
```

The important lesson is not simply "computers proved a theorem." It is that the **trust boundary moved** over time.

## 3. The human version of the modern formal strategy

The maintained Rocq formalization makes the highest-level proof surprisingly readable once we ignore syntax.

For a finite map, the proof does roughly this:

```text
ordinary planar map
    ↓
turn it into a finite combinatorial object
    ↓
solve the coloring problem there
    ↓
carry the answer back to the original map
```

Then a compactness argument extends the finite result to the general theorem.

In MeTTafy vocabulary, we currently describe that as:

```text
FiniteReduction
→ Discretization
→ RepresentationChange
→ StructuralReduction
→ ProofByTransport
→ CompactnessExtension
```

These names are **interpretations of proof structure**, not replacements for the proof.

## 4. What MeTTafy is trying to learn

MeTTafy should eventually look at the proof program and recover moves like these on its own.

For example:

- **Discretization** — replace a continuous/geometric object with a finite combinatorial representation.
- **Representation change** — move the problem into a different formal language where the desired operation is easier to perform.
- **Structural reduction** — simplify the problem while preserving the property we care about.
- **Proof by transport** — solve the problem in one representation and carry the result back.
- **Compactness extension** — establish all finite cases in the right way, then lift to the general setting.

The deeper combinatorial proof adds more moves:

```text
StructuralReduction
→ Induction / MinimalCounterexample
→ DecisionProcedure
→ Unavoidability
→ Reducibility
→ Discharging
```

## 5. Why does MeTTafy think that?

This is the critical audit question.

The top-level formal source states the finite theorem by:

1. calling a construction that **discretizes a finite simple map to a hypermap**;
2. invoking the finite combinatorial Four Color theorem on that hypermap;
3. applying the returned coloring map back to the original object.

The general theorem then invokes a **compactness extension** of the finite theorem.

So our first annotations are not guesses based on the theorem's reputation; they correspond to visible proof structure in the pinned formal artifact.

## 6. What could MeTTafy be wrong about?

Several things.

- `Discretization` and `RepresentationChange` overlap here; their exact boundary is an interpretation.
- `MinimalCounterexample` is a semantic reading of the induction structure and should be justified from local evidence rather than theorem history.
- `Discharging`, `Unavoidability`, and `Reducibility` are historically famous words in this proof, which creates a label-leakage risk.
- A future learned model may rank the right strategy for the wrong reason.

For that reason MeTTafy keeps **benchmark input separate from answer labels**. Historical names, theorem titles, filenames, and annotations are removed from classifier input.

## 7. What is actually trusted?

The formal proof checker, not MeTTafy.

```text
proof artifact ──checked by──> Rocq
      │
      └──interpreted by──> MeTTafy
```

A green MeTTafy label does **not** establish the theorem.

MeTTafy is trying to explain the computational strategy inside an already checkable proof.

Our standing rule is:

> **Prediction may guide search; verification governs acceptance.**

## 8. Show me the machine-readable version

The current hand-annotated strategy target is here:

- [`../exemplars/four_color/high_level_strategy.metta`](../exemplars/four_color/high_level_strategy.metta)

The provenance/benchmark manifest is here:

- [`../exemplars/four_color/manifest.json`](../exemplars/four_color/manifest.json)

The pinned upstream formalization is referenced, not copied wholesale:

- `rocq-community/fourcolor`
- commit `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`
- license: CeCILL-B

## 9. The historical reading path

A useful sequence is:

```text
Guthrie (1852)
→ Kempe (1879)
→ flaw in Kempe's proof
→ reducibility / unavoidable configurations / discharging
→ Appel & Haken computer-assisted proof
→ Robertson–Sanders–Seymour–Thomas simplification
→ Gonthier formal proof
→ maintained Rocq artifact
→ MeTTafy semantic strategy graph
```

This sprint will gradually attach primary or authoritative citations to each step rather than relying on folklore summaries.

## 10. What should I understand before leaving this page?

You do **not** need to understand the formal proof yet.

If you can explain these four things, the lesson worked:

1. why the Four Color Theorem became a landmark in computer-assisted mathematics;
2. that the modern formal proof changes representations before solving the finite combinatorial core;
3. that MeTTafy is trying to recover those reusable reasoning moves;
4. that MeTTafy's interpretation remains subordinate to independently checkable proof evidence.

Next: [`auditability.md`](auditability.md) explains how to challenge any MeTTafy interpretation without reading the whole codebase.