import examples.four_color.ReidemeisterStaging

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Adversarial quotient audit for Four Color MapMaker strategy staging.

This file formalizes only the INFERENCE experiment: pairs of projected strategy
tangles are challenged to collapse or remain distinct under an explicit normalizer.
Passing a finite corpus does not inhabit NormalFormCompleteness,
StrategyIRCompleteness, InferenceSound, or CertifiedInstantiation.
-/

namespace MeTTafy.FourColor

inductive QuotientExpectation where
  | collapse
  | split
  deriving DecidableEq, Repr

/-- One local falsifiable claim about the proposed Strategy-IR quotient. -/
structure QuotientChallenge where
  left : StrategyTangle
  right : StrategyTangle
  expectation : QuotientExpectation
  observableId : Nat
  deriving DecidableEq, Repr

abbrev StrategyNormalizer := StrategyTangle -> StrategyTangle

/-- Whether one explicit normalizer satisfies the local collapse/split claim. -/
def QuotientChallenge.satisfied
    (normalize : StrategyNormalizer)
    (challenge : QuotientChallenge) : Prop :=
  match challenge.expectation with
  | .collapse => normalize challenge.left = normalize challenge.right
  | .split => normalize challenge.left ≠ normalize challenge.right

/-- A corpus audit records only that its finite local challenges passed. -/
structure QuotientAudit (normalize : StrategyNormalizer) where
  challenges : List QuotientChallenge
  passed : ∀ challenge, challenge ∈ challenges -> challenge.satisfied normalize

/--
A collapse claim may additionally be checked against the proof-relevant interface.
This remains an inference-level property of the quotient.
-/
def CollapsePreservesInterface
    (interfaceOf : StrategyInterfaceExtractor)
    (normalize : StrategyNormalizer)
    (challenge : QuotientChallenge) : Prop :=
  challenge.expectation = .collapse ->
    interfaceOf (normalize challenge.left) = interfaceOf (normalize challenge.right)

/--
Corpus pressure is deliberately weaker than global completeness: every recorded
challenge may pass while unrepresented tangles remain unknown.
-/
def CorpusPressureSatisfied
    (normalize : StrategyNormalizer)
    (corpus : List QuotientChallenge) : Prop :=
  ∀ challenge, challenge ∈ corpus -> challenge.satisfied normalize

/-!
There is intentionally no function

  QuotientAudit -> CertifiedInstantiation

and no theorem converting `CorpusPressureSatisfied` into
`FiniteResponseCompleteNormalForms`. The adversarial corpus can falsify or refine
Strategy IR; it cannot silently acquire construction authority.
-/

end MeTTafy.FourColor
