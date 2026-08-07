# Learn MeTTafy

**No clone, install, proof assistant, or MeTTa setup is required to start here.**

MeTTafy is being developed in historical exemplar sprints. Each sprint uses a famous computational proof to teach two things at once:

1. how computation entered a piece of mathematics; and
2. how MeTTa can represent the reusable reasoning strategies inside that computation.

The repository is the source of truth, but the learning path is meant to work directly in GitHub's rendered documentation.

## Start here

### Sprint 01 — Four Color Theorem

Read [`four-color.md`](four-color.md).

You will learn:

- why the Four Color Theorem became a landmark in computer-assisted mathematics;
- how the modern formal proof changes representations before solving the finite combinatorial core;
- what MeTTafy means by strategies such as `Discretization`, `ProofByTransport`, and `CompactnessExtension`;
- why MeTTafy's semantic interpretation is not itself the proof;
- how to drill from a plain-language explanation to exact source evidence.

## How to audit MeTTafy

Read [`auditability.md`](auditability.md).

Every claimed interpretation should support four questions:

1. **What do you think is happening?**
2. **Why do you think that?**
3. **Show me.**
4. **What could you be wrong about?**

That path from explanation back to evidence is a core design requirement, not optional documentation polish.

## Two views of the same exemplar

Each sprint has two deliberately different surfaces.

### Learner view

```text
history
→ intuition
→ mathematical strategy
→ computational intervention
→ formal proof artifact
→ MeTTa representation
```

Names, dates, diagrams, citations, and explanatory language belong here.

### Benchmark view

```text
proof/program structure
→ MeTTafy
→ predicted/recovered strategy graph
→ compare with held-out annotations
```

Historical metadata and answer labels are stripped so the system cannot succeed merely by recognizing a famous theorem name.

## Current curriculum

| Sprint | Historical exemplar | Status |
| --- | --- | --- |
| 01 | Four Color Theorem | Active |
| 02 | Knot-theoretic rewriting / invariants | Planned after Sprint 01 |
| Later | Algebraic/computational topology, Flyspeck/Kepler, other landmark computational proofs | Candidate curriculum |

The rule is simple: **finish the current historical exemplar before expanding the curriculum.**

## For contributors

The learner-facing docs should remain readable without local setup. Reproduction, testing, proof-assistant setup, and development instructions can live deeper in the repository and be linked from the relevant lesson.

A good contribution should improve at least one of these paths:

```text
story → intuition
intuition → semantic strategy
strategy → source evidence
source evidence → verification
```

If a learner has to clone the repository merely to understand the central idea, we have put the explanation at the wrong layer.