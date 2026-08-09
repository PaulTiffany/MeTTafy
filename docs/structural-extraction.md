# Structural Evidence Layer (Issue #32)

This document records the first tranche of the Rocq structural extraction work.

## Purpose

Recover mechanically observable structure from the pinned formal artifact so that later semantic recognition can operate on a source-neutral, leakage-safe intermediate representation.

```text
pinned Rocq source
    → structural extractor (deterministic)
    → StructuralEvidence IR
    → blind projection
    → semantic recognizer (may abstain)
    → Strategy IR
    → MeTTa
```

Rocq remains the sole authority for theorem validity. The structural layer never promotes a semantic guess into checker authority.

## Transferability requirement

Every recovered fact must be expressible for three audiences at once:

| Audience       | Form required                                                                 |
|----------------|-------------------------------------------------------------------------------|
| Lay reader     | Plain-language sentence stating what was observed and why it is limited.      |
| Mathematician  | Ordinary mathematical observation checkable against the formal text.          |
| Machine        | Typed, deterministic, hashable data carrying full provenance.                 |

## Current extractor

- Module: `mettafy.structural`
- Version: `0.1.0-structural-bootstrap`
- Method: conservative syntax-surface analysis of Rocq/Coq vernacular
- Scope: the five primary proof-layer paths recorded in `exemplars/four_color/manifest.json`
- Non-claims: completeness, semantic labelling, proof validity

A later upgrade to SerAPI / Rocq-LSP AST dumps is explicitly anticipated once the IR contract is stable.

## First recovered structural observations

From the exact text of `theories/proof/fourcolor.v` and `combinatorial4ct.v` at commit `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2`:

### Finite high-level theorem

- **Plain language**: The body is a short composition of applications. One step obtains a hypermap together with a coloring-transport function; the next step applies a previously established combinatorial result and returns the transported coloring.
- **Mathematical**: Finite simple maps are discretized to planar hypermaps; the combinatorial four-color theorem is invoked; the resulting coloring is transported back to the original map.
- **Machine features**: `application`, `composition`.

### General high-level theorem

- **Plain language**: The general statement is obtained by applying a compactness extension to the finite result.
- **Mathematical**: Compactness extension of the finite four-color theorem yields the result for arbitrary simple maps.
- **Machine features**: `application`.

### Combinatorial core

- **Plain language**: An inductive argument on a size measure appears, together with a decision procedure for colorability and a reference to an unavoidability result.
- **Mathematical**: Proof proceeds by induction on the cardinality of the cubified hypermap; the argument relies on a colorability decision procedure and the unavoidability of a set of reducible configurations.
- **Machine features**: `induction`, `decision_call`, `application`.

These observations are structural only. Comparison against the held-out strategy annotations in `exemplars/four_color/manifest.json` occurs solely in a later evaluation layer.

## Artifacts

Running

```bash
python scripts/extract_four_color_structural.py
```

produces:

- `artifacts/witnesses/rocq-structural-fourcolor-highlevel.json` — full view + observations
- `artifacts/witnesses/rocq-structural-fourcolor-highlevel-blind.json` — classifier-safe view
- `artifacts/witnesses/rocq-structural-fourcolor-highlevel-audit.json` — human audit map

## Authority boundary

```text
Prediction may guide search; verification governs acceptance.
```

Learned or heuristic interpretation never replaces the Rocq checker.
