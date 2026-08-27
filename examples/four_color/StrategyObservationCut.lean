import examples.four_color.StrategyQuotientAudit

/-
Copyright (c) 2026 Paul Carver Tiffany III.
Released under the MIT License; see LICENSE.

Bounded-observer suffix cutting for Strategy-IR adversarial pressure.

This file formalizes only an INFERENCE-level observation boundary. A caller may
name one probe as response-complete for a local quotient experiment, after which
a serialized suffix is ignored. The cut does not produce a construction step or
certify a color.
-/

namespace MeTTafy.FourColor

/-- One serialized observation identifier in an imaginary MapMaker trace. -/
abbrev ObservationId := Nat

/-- Explicit local permission to stop comparing a trace after one probe. -/
structure ResponseCompleteCut where
  probeId : ObservationId
  deriving DecidableEq, Repr

/--
Keep the trace through the first named response-complete observation and discard
only the later suffix.
-/
def cutAfterObservation
    (cut : ResponseCompleteCut) : List ObservationId -> List ObservationId
  | [] => []
  | head :: tail =>
      if head = cut.probeId then
        [head]
      else
        head :: cutAfterObservation cut tail

/-- Extra quotient permissions used only by the ugly adversarial corpus. -/
structure UglyQuotientPolicy where
  responseCut : Option ResponseCompleteCut := none
  commuteDisjointNonObservational : Bool := false
  deriving DecidableEq, Repr

/-- Finite evidence that one ugly corpus passed under an explicit policy. -/
structure UglyQuotientAuditEvidence where
  policy : UglyQuotientPolicy
  challenges : List QuotientChallenge
  passed : Nat
  total : Nat
  passedLeTotal : passed <= total

/-!
There is intentionally no function

  UglyQuotientAuditEvidence -> CertifiedInstantiation

and no theorem converting a response-complete suffix cut into
`StrategySafeContinuation`, `InferenceSound`, or
`FiniteResponseCompleteNormalForms`.

The observer may stop looking at an imaginary suffix. Construction authority
still requires the independent bridge already defined elsewhere.
-/

end MeTTafy.FourColor
