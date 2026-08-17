# Formal Artifact Certification

`formal_artifact_green` answers one narrow question:

> Does the pinned Four Color formal artifact replay successfully under the pinned checker/toolchain?

The production witness is `WIT-ROCQ-REPLAY`.

## Pinned boundary

- upstream artifact: `rocq-community/fourcolor`
- source commit: `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`
- license: CeCILL-B
- checker image: `coqorg/coq@sha256:e50d77c4c5a9aa0d76ae1b343d79c5f922da3a75054b79c5dc635895438e4674`
- Coq: 8.20.1
- OCaml: 4.13.1
- opam: 2.3.0

The witness follows the upstream package boundary: install `coq-fourcolor-reals` from the pinned source, then install `coq-fourcolor` from the same checkout. The resolved dependency table and full replay log are retained as evidence and hashed.

## Authority boundary

A passing replay is **formal evidence about the upstream proof artifact**. It does not certify MeTTafy's semantic interpretation, extracted dependency graph, historical account, or the equivalence of the teaching MeTTa artifact to the Rocq proof.

Those are separate propositions and require separate witnesses.

This separation is deliberate:

```text
pinned formal artifact
        ↓
   Rocq checker
        ↓
formal_artifact_green

semantic extraction ──X── formal authority
```

The `X` is important. Formal authority does not leak sideways into semantic claims.

## Evidence

Each replay writes:

- `artifacts/witnesses/rocq-four-color-replay.json`
- `artifacts/witnesses/rocq-four-color-replay.log`
- `artifacts/witnesses/rocq-four-color-packages.txt`

The JSON records the pinned source, immutable checker image, tool versions, build contract, elapsed time, exit status, evidence hashes, MeTTafy commit, and workflow run ID.

`certification/formal-artifact-v1.json` defines the grade. `scripts/validate_formal_artifact_program.py` prevents the policy, central witness registry, and executable replay boundary from silently drifting apart.
