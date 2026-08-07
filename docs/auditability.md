# Auditing a MeTTafy Interpretation

MeTTafy treats **human interpretability as the gold standard for machine interpretability**.

That does not mean every internal detail must be simplified away. It means every semantic claim must have an inspectable path back to evidence.

For any claimed strategy, a learner or reviewer should be able to ask four questions.

## What do you think is happening?

Example:

> This proof performs a representation change from a planar map to a finite hypermap.

## Why do you think that?

MeTTafy should identify the structural evidence: source location, transformation call, input/output objects, dependencies, or proof-state transition supporting the claim.

## Show me

The learner should be able to descend from the explanation to the exact pinned source evidence without cloning the repository.

The ideal ladder is:

```text
plain-language explanation
    ↓
semantic strategy
    ↓
structural evidence
    ↓
pinned upstream source
    ↓
checker / verification record
```

## What could you be wrong about?

Every interpretive claim should expose ambiguity when it exists.

Examples:

- two strategy labels may overlap;
- a strategy boundary may be annotation rather than theorem;
- an LLM or predictive model may recognize a familiar pattern for the wrong reason;
- the chosen abstraction may intentionally erase implementation details;
- a formally valid proof may still be poorly described by our strategy ontology.

## Evidence classes

MeTTafy should visually and mechanically distinguish at least these categories:

- **Verified fact** — established by an exact checker or deterministic source observation.
- **Derived structure** — mechanically extracted from the artifact.
- **Human annotation** — a semantic interpretation supplied by a curator.
- **Model prediction** — a learned or heuristic proposal with uncertainty.
- **Historical context** — documentary material used for teaching, not as proof evidence.

No lower-confidence class is silently promoted into a stronger one.

## Human-in-the-loop acceptance test

A sprint is not pedagogically complete unless a curious reader can answer, without installing the toolchain:

1. What mathematical problem is this?
2. Why was it historically important?
3. Where did computation enter?
4. What strategies does MeTTafy claim to see?
5. What source evidence supports those claims?
6. Which claims are exact and which are interpretive?
7. What independently verifies the formal result?
8. Where might MeTTafy be mistaken?

If those answers require reading the whole implementation, the documentation has failed.

## Progressive disclosure

The docs should work from intuition downward:

```text
picture / story
→ mathematical intuition
→ semantic move
→ proof-program evidence
→ MeTTa representation
→ raw machine artifact
```

Experts can descend as far as they want. Newcomers should not be forced to begin at the bottom.

This is not a decorative UX principle. It is part of the research methodology: a machine interpretation that cannot be projected into a faithful human-auditable account is not yet a satisfactory interpretation.