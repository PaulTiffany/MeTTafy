# Provenance fold collapse

The mechanistic interpretability chain now crosses the recognition-to-emission seam without changing the stable public `Strategy.to_dict()` contract.

The chain is:

```text
BlindStructuralEvidence
  -> RuleTrace
  -> sibling ProvenanceEdge(authorized_by)
  -> Strategy IR
  -> emitted MeTTa Provenance atom
```

The key architectural rule is that provenance is a sibling compilation graph, not a new field in the public Strategy serialization. This preserves downstream integrator compatibility while keeping authorization causality explicit and machine-readable.

`WIT-PROVENANCE-FOLD-COLLAPSE` verifies that every promoted strategy has exactly one deterministic `authorized_by` parent in the sibling graph and that the exact edge survives MeTTa emission.

The next seam remains runtime provenance:

```text
emitted MeTTa
  -> executable/runtime trace
  -> mechanical witness
```

That seam should be closed with another typed provenance relation rather than inferred from text matching or post-hoc explanation.
