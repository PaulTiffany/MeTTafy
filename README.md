# MeTTafy

**Semantic decompilation into executable MeTTa — taught through the history of computational proof.**

MeTTafy is an open-source research and teaching project for recovering the *computational strategies* inside programs and formal proofs, representing those strategies explicitly, and re-expressing them as inspectable MeTTa structures.

## Learn without installing anything

**Start with [`docs/README.md`](docs/README.md).**

The current lesson is **Sprint 01 — The Four Color Theorem**:

- [`docs/four-color.md`](docs/four-color.md) — the learner-facing historical and computational lesson;
- [`docs/auditability.md`](docs/auditability.md) — how to challenge a MeTTafy interpretation;
- [`exemplars/four_color/high_level_strategy.metta`](exemplars/four_color/high_level_strategy.metta) — the current hand-annotated MeTTa strategy target;
- [`exemplars/four_color/manifest.json`](exemplars/four_color/manifest.json) — provenance and benchmark metadata.

**You do not need to clone this repository, know Rocq/Coq, or know MeTTa to get value from the learning path.**

## The project idea

The goal is **not** ordinary source-to-source transpilation.

```text
historical / formal program
    ↓
structural program model
    ↓
semantic strategy recovery
    ↓
strategy graph / ontology
    ↓
MeTTa representation
    ↓
independent verification
```

A conventional implementation or proof may express reduction, transport, search, constraint propagation, induction, compactness, rewriting, certificate checking, or other strategies through many lines of incidental control flow. MeTTafy aims to recover those strategies as first-class objects rather than merely translating syntax.

## Historical exemplar sprints

MeTTafy develops one famous computational proof at a time.

Each sprint should produce two things from the same artifact:

```text
Learner surface:
history → intuition → mathematics → computation → formal artifact → MeTTa

Research surface:
proof/program structure → semantic recovery → strategy graph → verification
```

The historical context teaches **how computation entered mathematics**. The blind benchmark tests whether MeTTafy can actually recover the strategy without cheating from theorem names, authors, filenames, or historical reputation.

### Sprint 01 — Four Color Theorem

The Four Color Theorem is the first exemplar because its history exposes a remarkable sequence:

```text
conjecture
→ flawed human proof
→ structural reduction
→ computer-assisted finite checking
→ simplified computational proof
→ fully machine-checked formal proof
```

The maintained Rocq formalization gives us a checkable artifact whose high-level strategy already contains representation change, discretization, transport, compactness, induction/minimality, decision procedures, unavoidability, reducibility, and discharging.

Future sprints will remain scoped one historical exemplar at a time. Knot-theoretic rewriting and invariants are the natural next family after Four Color is complete.

## Human auditability is a requirement

MeTTafy treats **human interpretability as the gold standard for machine interpretability**.

Every semantic claim should support a path like:

```text
plain-language explanation
    ↓
semantic strategy claim
    ↓
structural evidence
    ↓
pinned source artifact
    ↓
checker / verification record
```

A learner should be able to ask:

- What do you think is happening?
- Why do you think that?
- Show me.
- What could you be wrong about?

If answering those questions requires understanding the entire implementation, the interpretation is not finished.

## Architecture micro-witness: Brown Goo

MeTTafy also carries a small Lean-checked architecture witness for **distinction-preserving transport**: [`examples/brown_goo/`](examples/brown_goo/).

The informal mnemonic is deliberately silly:

> **Brown goo = lost distinction disguised as knowledge.**

The formal claim is narrower. If a translation collapses two source objects that an admissible downstream continuation can still distinguish, then that continuation cannot be reproduced exactly from the translated representation.

This closes a subtle loophole in ordinary lossy abstraction: a distinction is not genuinely arbitrary merely because the **current** layer does not inspect it. A later policy, action, provenance query, verifier, reward, or composed consequence may make it operationally real. The Lean witness distinguishes **contextually arbitrary** from **pseudo-arbitrary** distinctions and proves the corresponding factorization failure.

A timely documentary example is Ben Goertzel's August 17, 2026 essay [*The Folly of Statistically Watermarking LLM-Gen Text*](https://bengoertzel.substack.com/p/the-folly-of-statistically-watermarking): lexical perturbations may be nearly irrelevant to semantic content while remaining deliberately observable to a watermark detector and consequential to governance. That is precisely why "irrelevant here" must not silently become "arbitrary everywhere." The same essay also separates statistical detection from signed provenance and from the full causal history of ideas and authorship. It is motivation, not theorem evidence; the Lean witness remains checker-authoritative for its own claims.

This micro-witness is MeTTafy-original architecture work, not part of the Four Color benchmark corpus and not evidence for Four Color theorem validity.

## Why MeTTa?

MeTTa is the programming language of OpenCog Hyperon. Its metagraph-oriented model allows facts, rules, queries, and programs themselves to participate in a common symbolic substrate. That makes it an interesting target for a semantic intermediate representation: the recovered description of *what a program is doing* can itself become available to later reasoning and transformation.

## Project principles

- **Semantics before syntax.** Recover strategies, constraints, invariants, and effects before emitting target code.
- **Evidence before confidence.** Semantic classifications retain provenance and supporting structure.
- **Verification before equivalence claims.** Learned or heuristic interpretation never replaces an exact checker.
- **Unknown is valid.** Abstention is better than a confident invented strategy.
- **Human-auditable projection.** Every machine interpretation should have a faithful path back to human intuition and source evidence.
- **Historical context without benchmark leakage.** Teaching metadata is separated from classifier input.
- **Celebrate the ecosystem.** Build with and alongside MeTTa, Hyperon, OpenCog, Rocq/Coq, Lean/mathlib, FabricPC, and community tooling rather than competing with canonical upstream work.
- **Reuse responsibly.** Prefer dependencies, adapters, and pinned upstream references over copying or silent forks. Preserve licenses and notices.

## Verification boundary

Learned components may propose or rank strategy interpretations. They do not decide theorem validity.

> **Prediction may guide search; verification governs acceptance.**

The checker or independently verifiable artifact remains authoritative.

## Implementation status

MeTTafy now has a mechanically witnessed research pipeline rather than only a bootstrap analyzer. The current Sprint 01 surface includes:

- **Pinned formal authority.** `formal_artifact_green` replays the exact `rocq-community/fourcolor` artifact under a pinned immutable checker/toolchain. This certifies checker acceptance of that upstream artifact only; it does not certify MeTTafy's interpretation.
- **Leakage-safe structural recovery.** Rocq structure is extracted into a blind, source-neutral view before semantic recognition; held-out Four Color labels are joined only after recognition for evaluation.
- **Mechanistic recognition traces.** Promotions and abstentions expose their observed premises, missing premises, confidence gate, and typed provenance rather than post-hoc explanation.
- **Provenance through emission.** Promoted RuleTrace → Strategy relations survive as typed MeTTa provenance atoms and are separately checked at the deterministic artifact boundary.
- **Fail-closed reducibility contracts.** Stronger reduction claims require explicit boundary preservation, strict descent, and a verified lift; the Four Color admissible-traversal gate can stop at `certificate_required` rather than inventing missing evidence.
- **A falsification-preserving Four Color genealogy.** The earlier independent Track-B proof attempt is retained as a frozen hypothesis. Its degree-four C0 shortcut is explicitly falsified; a successor Kempe repair can pass its own mechanical checks without silently upgrading the failed ancestor or promoting a new theorem.
- **Actual Hyperon execution witnesses.** A pinned Hyperon 0.2.10 lane records query results, final Atomspace state, and per-form state deltas from one witnessed execution sequence.
- **Operational-liveness probes.** MeTTafy can derive a probe from a recovered `authorized_by` dependency, execute a separately hashed instrumented artifact, and distinguish `live`, `not_demonstrated`, `inconsistent`, `insufficient`, and `unavailable` without calling a failed perturbation "dead semantics."
- **Bounded source-distinction correspondence.** One current witness removes the source-side `composition` distinction, observes the recovered dependency disappear in executable MeTTa, restores the source exactly, and observes the byte-identical target behavior return.
- **Bounded differential execution.** The frozen finite graph corpus runs independently through the checked-in Python implementation and pinned MeTTaScript runtime, with zero tolerated colorability mismatches and independent validation of returned colorings.
- **Brown Goo micro-witness.** Lean checks the narrower architecture theorem that collapsing a source distinction needed by an admissible future continuation can prevent exact downstream factorization.
- **Four Color V4 micro-core.** Lean checks the fixed global proof-frame algebra for the Klein-four palette, cyclic five-frontier closure/parity, and the saturated proper degree-five `3,1,1` mode law. This banks only those local statements; it is not a new Four Color proof claim.

These witness classes are intentionally not flattened into one success flag:

```text
valid target ≠ executed target ≠ live target ≠ faithful transcode
```

The current open research problem is the last relation: **general source-to-target strategy faithfulness remains unproved.** Existing witnesses certify only their declared bounded claims. Likewise, the repository does **not** claim a new proof of the Four Color Theorem; the independent Track-B proof genealogy remains unresolved where its frozen claim was falsified.

See [`certification/witness-registry-v1.json`](certification/witness-registry-v1.json) for the machine-readable witness ledger, [`docs/four-color-proof-surface.md`](docs/four-color-proof-surface.md) for the current Four Color falsification/research surface, and [`docs/four-color-proof-status.md`](docs/four-color-proof-status.md) for the preserved historical Track-B claim surface.

## Prior art and community

MeTTafy exists because there is already a rich open-source ecosystem worth building on.

- **OpenCog Hyperon / MeTTa** — target language and execution substrate: https://github.com/trueagi-io/hyperon-experimental
- **MeTTaScript by MesTTo** — TypeScript MeTTa runtime/tooling and interoperability ecosystem: https://github.com/MesTTo/MeTTaScript
- **LogicMOO metta-src-conversions** — directly relevant source/MeTTa conversion prior art: https://github.com/logicmoo/metta-src-conversions
- **Rocq community Four Color formalization** — canonical Sprint 01 proof artifact: https://github.com/rocq-community/fourcolor
- **Lean mathlib4** — candidate source of later machine-checkable exemplars: https://github.com/leanprover-community/mathlib4
- **FabricPC** — possible optional predictive recognizer over verified proof traces: https://github.com/trueagi-io/FabricPC
- **Joern / Code Property Graphs** — possible future multi-language structural front end: https://github.com/joernio/joern

See [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md), [`docs/prior-art.md`](docs/prior-art.md), and [`docs/historical-curriculum.md`](docs/historical-curriculum.md).

**MeTTafy is an independent community project. It is not an official project of SingularityNET, OpenCog, Hyperon, Rocq, MesTTo, LogicMOO, or their contributors.**

## Licensing

MeTTafy-original code and documentation are released under the MIT License. Copyright © 2026 Paul Carver Tiffany III.

Third-party projects retain their own copyrights and licenses. Acknowledgment does not imply that their code has been copied into this repository. Any dependency, derived work, vendored component, or submodule is documented with its upstream source and license.

## Contributing

Collaboration is welcome from the MeTTa/Hyperon, formal-methods, mathematics, history-of-computation, program-analysis, and educational communities.

Corrections to attribution, historical claims, proof interpretation, terminology, or teaching explanations are substantive contributions.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).
