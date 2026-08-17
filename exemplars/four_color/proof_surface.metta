; Four Color ordered-construction proof surface
; Generated from mettafy.proof_surface.four_color_ordered_surface().
; Mechanical witnesses are falsifiers; they are not theorem premises.

(ProofSurface FourColorOrderedV1)
(FrozenProof FourColorOrderedV1 sha-7a5c5a0735108d2bdc4fff57f7ed9a0c300af28b)
; frozen proof artifact: docs/four-color-ordered-construction-proof.md

; --- typed claims ---
(Claim C0 MinimalCounterexampleReduction Ground)
; C0 artifact: docs/four-color-ordered-construction-proof.md#1-minimal-counterexample-reduction
(Claim C1 SaturatedBoundaryNormalForm Ground)
; C1 artifact: docs/four-color-ordered-construction-proof.md#1-minimal-counterexample-reduction
(Claim C2 CleanFrontierTurnExistence Frontier)
; C2 artifact: docs/four-color-clean-turn-lemma.md
(Claim C3 SingletonCleanTurnFinishes Flow)
; C3 artifact: docs/four-color-ordered-construction-proof.md#4-singleton-turns-finish
(Claim C4 RepeatedTurnPairLemma Frontier)
; C4 artifact: docs/four-color-clean-turn-dynamics.md
(Claim C5 PresentStateNoninverseContinuation Flow)
; C5 artifact: docs/four-color-ordered-construction-proof.md#6-ordered-state-continuation
(Claim C6 OrderedShapeProgress Frontier)
; C6 artifact: docs/four-color-ordered-construction-proof.md#6-ordered-state-continuation
(Claim C7 FiniteConstructionClosure Closure)
; C7 artifact: docs/four-color-ordered-construction-proof.md#7-closure
(Claim C8 DegreeFiveExtension Closure)
; C8 artifact: docs/four-color-ordered-construction-proof.md#7-closure

; --- dependency surface ---
(DependsOn C1 C0)
(DependsOn C2 C1)
(DependsOn C3 C2)
(DependsOn C4 C1)
(DependsOn C4 C2)
(DependsOn C5 C4)
(DependsOn C6 C5)
(DependsOn C7 C2)
(DependsOn C7 C4)
(DependsOn C7 C5)
(DependsOn C7 C6)
(DependsOn C8 C0)
(DependsOn C8 C3)
(DependsOn C8 C7)

; --- evidence fibers ---
(EvidenceFiber E0 C0 Mathematical)
; E0 artifact: docs/four-color-ordered-construction-proof.md#1-minimal-counterexample-reduction
(EvidenceFiber E1 C1 Mathematical)
; E1 artifact: docs/four-color-ordered-construction-proof.md#1-minimal-counterexample-reduction
(EvidenceFiber E2 C2 Mathematical)
; E2 artifact: docs/four-color-clean-turn-lemma.md
(EvidenceFiber E3 C3 Mathematical)
; E3 artifact: docs/four-color-ordered-construction-proof.md#4-singleton-turns-finish
(EvidenceFiber E4 C4 Mathematical)
; E4 artifact: docs/four-color-clean-turn-dynamics.md
(EvidenceFiber E5 C5 Mathematical)
; E5 artifact: docs/four-color-ordered-construction-proof.md#6-ordered-state-continuation
(EvidenceFiber E6 C6 Mathematical)
; E6 artifact: docs/four-color-ordered-construction-proof.md#6-ordered-state-continuation
(EvidenceFiber E7 C7 Mathematical)
; E7 artifact: docs/four-color-ordered-construction-proof.md#7-closure
(EvidenceFiber E8 C8 Mathematical)
; E8 artifact: docs/four-color-ordered-construction-proof.md#7-closure

; --- mechanical witnesses ---
(Witness W-SequentialFrontier ci-passed)
; W-SequentialFrontier artifact: tests/test_sequential_frontier.py
(Covers W-SequentialFrontier C2)
(Covers W-SequentialFrontier C3)
(Covers W-SequentialFrontier C4)
(Covers W-SequentialFrontier C5)
(Witness W-FlipFamily4620 ci-passed)
; W-FlipFamily4620 artifact: tests/test_ordered_construction_closure.py
(Covers W-FlipFamily4620 C2)
(Covers W-FlipFamily4620 C3)
(Covers W-FlipFamily4620 C4)
(Covers W-FlipFamily4620 C5)
(Covers W-FlipFamily4620 C7)
(Covers W-FlipFamily4620 C8)
(Witness W-TheseusShapeOrder ci-passed)
; W-TheseusShapeOrder artifact: tests/test_ordered_shape_progress.py
(Covers W-TheseusShapeOrder C6)
(Witness W-GeneratedDisks5000 local-passed)
; W-GeneratedDisks5000 artifact: docs/four-color-proof-status.md#5-mechanical-red-team
(Covers W-GeneratedDisks5000 C2)
(Covers W-GeneratedDisks5000 C4)
(Covers W-GeneratedDisks5000 C5)
(Covers W-GeneratedDisks5000 C7)

; --- destructive mutation program ---
(Mutation M0-DropMinimality C0 ExpectedFailure planned)
; M0-DropMinimality: Remove the smaller-counterexample induction premise and require the reduction to fail.
(Mutation M1-BreakBoundaryNormalForm C1 ExpectedFailure planned)
; M1-BreakBoundaryNormalForm: Feed a nonproper or nonsaturated five-cycle and require normal-form certification to fail.
(Mutation M2-AllowPlanarCrossing C2 ExpectedFailure planned)
; M2-AllowPlanarCrossing: Permit complementary bichromatic paths to cross without incidence and require the clean-turn lemma witness to fail.
(Mutation M3-DirtyFrontierTurn C3 ExpectedFailure planned)
; M3-DirtyFrontierTurn: Allow a purported clean component to hit two frontier vertices and require turn certification to fail.
(Mutation M4-BreakRepeatedPair C4 ExpectedFailure planned)
; M4-BreakRepeatedPair: Force one repeated occurrence into the complementary locked component and require pair certification to fail.
(Mutation M5-StoreFutureRoute C5 ExpectedFailure planned)
; M5-StoreFutureRoute: Inject future-route information into present-state continuation and require ontology/flow certification to fail.
(Mutation M6-ReplayResolvedShape C6 ExpectedFailure implemented)
; M6-ReplayResolvedShape: Count an exact inverse replay of an already resolved physical component as fresh construction progress and require progress certification to fail.
; M6-ReplayResolvedShape artifact: tests/test_ordered_shape_progress.py::test_m6_exact_inverse_replay_is_an_inconsequential_label_change
(Mutation M7-AllowSaturatedExhaustion C7 ExpectedFailure planned)
; M7-AllowSaturatedExhaustion: Declare termination at a saturated frontier while a clean unresolved continuation remains and require closure certification to fail.
(Mutation M8-CorruptRestoredEdge C8 ExpectedFailure planned)
; M8-CorruptRestoredEdge: Restore the degree-five focus with a color present in its neighborhood and require the edge ledger to reject the extension.

; Intended surface queries:
; !(match &self (EvidenceFiber $e $claim $kind) ($claim $e $kind))
; !(match &self (Covers $w $claim) ($claim $w))
; !(match &self (Mutation $m $claim $expected $status) ($claim $m $status))
