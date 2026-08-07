# Mechanical witnesses

MeTTafy treats a green check as evidence for a proposition, not as generic confidence.

The canonical registry is [`certification/witness-registry-v1.json`](../certification/witness-registry-v1.json). Every witness declares what it can establish, what it cannot establish, its authority source, replayability, and evidentiary strength.

## Composition rule

> Independent witnesses accumulate evidence; no witness inherits the authority of another.

A Rocq kernel replay can certify that a pinned formal artifact checks. It cannot certify that MeTTafy's semantic interpretation of that artifact is correct. A differential execution test can show behavioral agreement over a certified domain. It cannot by itself establish intensional strategy identity. An automated accessibility engine can detect mechanically testable WCAG failures. It cannot certify full WCAG conformance.

This is deliberate. Product certification should look like a lattice of bounded witnesses, not one confidence score.

## Witness strengths

The registry uses five coarse strength classes. These are descriptive, not a total ranking:

- `diagnostic`: exposes defects or test weakness without establishing correctness;
- `bounded`: proves or checks an enumerated local property;
- `behavioral`: observes execution over a declared domain/environment;
- `artifact`: establishes provenance, integrity, or reproducibility properties of bytes;
- `formal`: delegates a formal proposition to a proof checker/kernel under pinned assumptions.

A stronger class in one dimension does not subsume another class. Formal theorem replay does not replace accessibility testing; accessibility testing does not replace semantic benchmarks.

## Automated WCAG witness

`WIT-WCAG-AUTO` uses pinned Deque `axe-core` 4.12.1. The npm tarball is fetched at an exact version and verified against its published SHA-512 integrity before its browser engine is executed.

The witness scans every primary Pages route using WCAG 2.0/2.1/2.2 Level A/AA rule tags. Its release threshold is zero automated violations.

The evidence artifact separately records `incomplete` findings that require human/manual review. Therefore the passing proposition is:

> axe-core found zero automatically detectable A/AA violations in the configured product pages.

It is **not**:

> MeTTafy fully conforms to WCAG 2.2 AA.

Full conformance requires criteria that automation cannot decide, including manual and assistive-technology evaluation.

## Expansion path

The registry already reserves independent witnesses for:

- pinned Rocq proof replay;
- differential source/MeTTa execution;
- metamorphic semantic perturbation;
- mutation-test sensitivity;
- fuzz/parser resilience;
- reproducibility;
- supply-chain SBOM/provenance;
- performance and resource budgets.

A planned witness becomes implemented only when its executable harness and evidence artifact exist and pass on the same repository commit being certified.
