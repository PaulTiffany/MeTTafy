; Four Color engineering-target search
; Flat Python exemplars are reuse candidates, not theorem witnesses.
; Generated from mettafy.engineering_targets.four_color_engineering_index().

(EngineeringNeed N-C5-PresentStateOnly C5)
(NeedConcept N-C5-PresentStateOnly temporal-locality)
(EngineeringNeed N-C6-FreshShapeProgress C6)
(NeedConcept N-C6-FreshShapeProgress identity)
(NeedConcept N-C6-FreshShapeProgress novelty)
(NeedConcept N-C6-FreshShapeProgress persistence)
(NeedConcept N-C6-FreshShapeProgress replay)
(NeedConcept N-C6-FreshShapeProgress strict-refinement)
(EngineeringNeed N-C7-FiniteClosure C7)
(NeedConcept N-C7-FiniteClosure closure)
(NeedConcept N-C7-FiniteClosure finite-order)

; --- pinned flat-Python exemplars ---
(EngineeringExemplar X-COME-DerivedOnly)
; X-COME-DerivedOnly repository: PaulTiffany/Come
; X-COME-DerivedOnly commit: c3c09334c70fb1ee812e004c35fe2deb0ef51883
; X-COME-DerivedOnly artifact: come/adapters.py
; X-COME-DerivedOnly behavior: The adapter filters Input echoes and Selected scheduling; only Derived lines count as new knowledge. An echo of an existing statement is activity but not novelty.
(ExemplarConcept X-COME-DerivedOnly novelty)
(ExemplarConcept X-COME-DerivedOnly replay)
(EngineeringExemplar X-NB-DeterminismIdentity)
; X-NB-DeterminismIdentity repository: PaulTiffany/notebook_compiler
; X-NB-DeterminismIdentity commit: 67fe52d3820fff3b2d75c974137c68efdaaffb0c
; X-NB-DeterminismIdentity artifact: scripts/check_determinism.py
; X-NB-DeterminismIdentity behavior: Compile the same input twice in separate directories, normalize volatile representation fields, hash the normalized artifacts, and require identical semantic results.
(ExemplarConcept X-NB-DeterminismIdentity identity)
(ExemplarConcept X-NB-DeterminismIdentity replay)
(EngineeringExemplar X-NB-FrozenArtifactGraph)
; X-NB-FrozenArtifactGraph repository: PaulTiffany/notebook_compiler
; X-NB-FrozenArtifactGraph commit: 67fe52d3820fff3b2d75c974137c68efdaaffb0c
; X-NB-FrozenArtifactGraph artifact: src/notebook_compiler/artifacts.py
; X-NB-FrozenArtifactGraph behavior: Frozen immutable typed artifact objects retain source SHA-256 identity, execution trace, certificate, manifest projection, and audit provenance across later renderings.
(ExemplarConcept X-NB-FrozenArtifactGraph identity)
(ExemplarConcept X-NB-FrozenArtifactGraph persistence)
(ExemplarConcept X-NB-FrozenArtifactGraph projection)
(ExemplarConcept X-NB-FrozenArtifactGraph provenance)
(EngineeringExemplar X-NB-ControlBoardTemporalLocality)
; X-NB-ControlBoardTemporalLocality repository: PaulTiffany/notebook_compiler
; X-NB-ControlBoardTemporalLocality commit: 67fe52d3820fff3b2d75c974137c68efdaaffb0c
; X-NB-ControlBoardTemporalLocality artifact: src/notebook_compiler/control_board.py
; X-NB-ControlBoardTemporalLocality behavior: The control board contains only compile-time state before the notebook is written; later verification results live in a sibling certificate rather than future information being stored in the present state.
(ExemplarConcept X-NB-ControlBoardTemporalLocality persistence)
(ExemplarConcept X-NB-ControlBoardTemporalLocality provenance)
(ExemplarConcept X-NB-ControlBoardTemporalLocality temporal-locality)
(EngineeringExemplar X-NB-OrderedVerifier)
; X-NB-OrderedVerifier repository: PaulTiffany/notebook_compiler
; X-NB-OrderedVerifier commit: 67fe52d3820fff3b2d75c974137c68efdaaffb0c
; X-NB-OrderedVerifier artifact: src/notebook_compiler/verifier.py
; X-NB-OrderedVerifier behavior: Traverse a finite ordered sequence of cells in order, stop at the first failure, retain the failed index, and declare success only when execution completes with validation and no unresolved failure remains.
(ExemplarConcept X-NB-OrderedVerifier closure)
(ExemplarConcept X-NB-OrderedVerifier finite-order)
(ExemplarConcept X-NB-OrderedVerifier persistence)

; --- fuzzy behavioral matches ---
(EngineeringMatch N-C5-PresentStateOnly X-NB-ControlBoardTemporalLocality 1.000)
(MatchConcept N-C5-PresentStateOnly X-NB-ControlBoardTemporalLocality temporal-locality)
(EngineeringMatch N-C6-FreshShapeProgress X-COME-DerivedOnly 0.400)
(MatchConcept N-C6-FreshShapeProgress X-COME-DerivedOnly novelty)
(MatchConcept N-C6-FreshShapeProgress X-COME-DerivedOnly replay)
(EngineeringMatch N-C6-FreshShapeProgress X-NB-DeterminismIdentity 0.400)
(MatchConcept N-C6-FreshShapeProgress X-NB-DeterminismIdentity identity)
(MatchConcept N-C6-FreshShapeProgress X-NB-DeterminismIdentity replay)
(EngineeringMatch N-C6-FreshShapeProgress X-NB-FrozenArtifactGraph 0.400)
(MatchConcept N-C6-FreshShapeProgress X-NB-FrozenArtifactGraph identity)
(MatchConcept N-C6-FreshShapeProgress X-NB-FrozenArtifactGraph persistence)
(EngineeringMatch N-C7-FiniteClosure X-NB-OrderedVerifier 1.000)
(MatchConcept N-C7-FiniteClosure X-NB-OrderedVerifier closure)
(MatchConcept N-C7-FiniteClosure X-NB-OrderedVerifier finite-order)

; Deliberately absent: (Covers ...) and (Witness ...).
; Retrieval proposes an implementation target; adaptation plus a mechanical test
; is required before the proof surface may claim witness coverage.
