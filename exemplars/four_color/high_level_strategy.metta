; MeTTafy Sprint 01 — Four Color Theorem
; Hand-annotated semantic strategy graph derived from the pinned Rocq proof.
; This is an exemplar/target representation, not a replacement proof.

(Exemplar FourColorSprint01)
(SourceRepo FourColorSprint01 rocq-community/fourcolor)
(SourceCommit FourColorSprint01 f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2)
(CheckerAuthority FourColorSprint01 Rocq)

; High-level finite theorem:
; finite simple map -> discretize to a finite planar hypermap -> solve the
; combinatorial theorem -> transport the coloring back to the original map.

(Strategy SFiniteReduction FiniteReduction)
(Strategy SDiscretize Discretization)
(Strategy SRepresent RepresentationChange)
(Strategy SCombinatorialCore StructuralReduction)
(Strategy STransport ProofByTransport)
(Strategy SCompactness CompactnessExtension)

(Then SFiniteReduction SDiscretize)
(Then SDiscretize SRepresent)
(Then SRepresent SCombinatorialCore)
(Then SCombinatorialCore STransport)
(Then STransport SCompactness)

; Finite combinatorial core:

(Strategy SCubicReduction StructuralReduction)
(Strategy SInduction Induction)
(Strategy SMinimal MinimalCounterexample)
(Strategy SDecide DecisionProcedure)
(Strategy SUnavoidable Unavoidability)
(Strategy SReducible Reducibility)
(Strategy SDischarge Discharging)

(Contains SCombinatorialCore SCubicReduction)
(Contains SCombinatorialCore SInduction)
(Contains SCombinatorialCore SMinimal)
(Contains SCombinatorialCore SDecide)
(Contains SCombinatorialCore SUnavoidable)
(Contains SCombinatorialCore SReducible)
(Contains SCombinatorialCore SDischarge)

(DependsOn SUnavoidable SDischarge)
(DependsOn SCombinatorialCore SUnavoidable)
(DependsOn SCombinatorialCore SReducible)

; Tranch7 / authority boundary:

(Role LearnedModel CandidateStrategyRanking)
(Role Rocq ExactProofChecking)
(NotAuthority LearnedModel ProofValidity)
(Authority Rocq ProofValidity)
