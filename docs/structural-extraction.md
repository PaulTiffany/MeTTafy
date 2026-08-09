# Structural Evidence Layer (Issue #32)

This tranche introduces the first Rocq front end for MeTTafy and, more importantly, a mechanically enforced boundary between source/audit material and semantic recognition.

```text
pinned, hash-verified Rocq fixture bytes
    → deterministic structural extractor
    → StructuralEvidence        # raw/audit side
    → one-way blind projection
    → BlindStructuralEvidence   # classifier capability boundary
    → conservative recognizer
    → Strategy IR candidate OR abstention
    → post-hoc unit-local evaluation
```

Rocq remains the sole authority for theorem validity. This structural witness does not replay the proof and does not promote a semantic guess into checker authority.

## Current extractor

- Module: `mettafy.structural`
- Version: `0.2.0-structural-bootstrap`
- Method: conservative syntax-surface analysis of Rocq/Coq vernacular
- Current witness slice: the high-level `fourcolor.v` and `combinatorial4ct.v` fixtures from `rocq-community/fourcolor@f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`
- Fixture integrity: exact SHA-256 values are frozen in `scripts/extract_four_color_structural.py`
- Long-term parser direction: a maintained Rocq AST/machine-readable interface such as Rocq-LSP once the IR contract is stable

The bootstrap parser is intentionally incomplete. Unsupported syntax or insufficient evidence is not silently promoted into semantic knowledge.

## One-way membrane

`StructuralEvidence` may contain raw source excerpts, source identifiers, references, exact paths, exact input hashes, and the declared upstream revision. Those fields exist for reproducibility and human audit.

`blind_structural_view()` converts that object to the separate `BlindStructuralEvidence` type. The blind type contains only:

- blind ordinal unit IDs;
- blind source tokens;
- unit kind;
- bounded observable feature vocabulary;
- source-relative line coordinates;
- blind-unit dependency edges;
- MeTTafy revision, extractor version, source count, and a path-free corpus-content hash.

It cannot contain source text, original names, qualified references, source paths, the upstream repository SHA, or path-keyed input hashes. `recognize_from_structural()` rejects raw `StructuralEvidence` at runtime and is typed to the blind object.

The separate `blind_audit_map()` joins blind unit IDs back to source metadata only after recognition for human inspection and held-out evaluation.

## Comment and metadata leakage

Feature extraction runs on a comment-stripped projection of each Rocq source. The comment scanner tracks nested `(* ... *)` forms, preserves line positions, and fails closed on malformed comments.

Tests inject strategy-shaped documentary text such as `induction`, `rewrite`, and `decide_colorable` into nested comments and require recovered features to remain unchanged.

The serialized blind payload is also tested adversarially for source names, theorem names, paths, qualified references, upstream SHA, and held-out strategy vocabulary.

## Observable features versus semantic strategies

The extractor currently records bounded structural facts such as:

- `application`
- `composition`
- `induction`
- `case_split`
- `rewrite_transport`
- `decision_call`

These names describe mechanically observed syntax/structure; they are not Four Color strategy labels.

Recognition is intentionally stricter than extraction. A lone induction or decision-procedure-shaped call is **not** promoted to `Reduction` or `CertificateCheck`. Those observations currently produce an explicit abstention because the existing `StrategyKind` vocabulary would overstate what the evidence proves.

The first promoted claim is narrower: when a result bound by one proof application is mechanically observed feeding a later application in the same unit, the recognizer may emit the existing generic `Reduction` StrategyKind. It does not infer `Discretization`, `ProofByTransport`, or any other held-out Four Color label from that structure.

## Evaluation boundary

Held-out Four Color annotations are joined only after recognition. The evaluation helper compares predictions to targets **per blind unit**; it cannot award a prediction on one theorem credit for a label belonging to another theorem/layer.

Evaluation output is marked `evaluation_only: true` and is never an input to the recognizer.

## Witness artifacts

Running

```bash
python scripts/extract_four_color_structural.py
```

produces five deterministic JSON artifacts under `artifacts/witnesses/`:

- `rocq-structural-fourcolor-highlevel.json` — raw structural witness, provenance, claim and non-claims;
- `rocq-structural-fourcolor-highlevel-blind.json` — exact classifier-safe projection;
- `rocq-structural-fourcolor-highlevel-audit.json` — human/evaluation join map;
- `rocq-recognition-fourcolor-highlevel.json` — Strategy candidates and abstentions;
- `rocq-evaluation-fourcolor-highlevel.json` — unit-local post-hoc comparison.

The script records the actual MeTTafy repository SHA, verifies the frozen source fixture hashes before extraction, and records a SHA-256 digest of the canonical blind projection. It fails closed if repository provenance or fixture integrity cannot be established.

CI runs this witness twice on the same revision and requires byte-identical outputs.

## Explicit non-claims

This tranche does not establish:

- Four Color theorem validity;
- completeness of Rocq structural extraction;
- correctness of every semantic strategy annotation;
- equivalence between Rocq proof terms and emitted MeTTa;
- identity with a live upstream checkout beyond the frozen, independently reviewable fixture hashes;
- language-general semantic recovery beyond the declared structural contract.

Formal proof replay remains an independent mechanical witness (`WIT-ROCQ-REPLAY`). Differential source↔MeTTa execution remains a separate witness as well.

## Authority boundary

> Prediction may guide search; verification governs acceptance.
