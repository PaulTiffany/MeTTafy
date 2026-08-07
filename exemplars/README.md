# MeTTafy Exemplar Corpus

This directory contains **MeTTafy-owned manifests and annotations**, not untracked copies of upstream proof corpora.

Each exemplar records the exact upstream artifact, version/commit, license, checker, verification status, and MeTTafy strategy annotations needed to reproduce the semantic classification.

## Directory layout

```text
exemplars/
  topology/
    <exemplar-id>.toml
```

## Corpus rule

Upstream proof source remains upstream unless redistribution is technically necessary and license-compliant. Prefer pinned references and adapters to bulk copying.

An exemplar is not considered verified merely because its manifest says so. Corpus tooling must be able to replay or otherwise validate the recorded checker result against the pinned source.

## Annotation rule

Strategy annotations are explicitly separated from verified proof facts:

- `verified.*` fields describe machine-checkable facts;
- `annotation.*` fields describe MeTTafy's semantic interpretation;
- `prediction.*` fields, when present, describe learned/heuristic candidate scores.

A prediction may inform an annotation, but neither prediction nor annotation changes the proof assistant's authority over proof validity.
