# Audience Interface Certification

MeTTafy does not treat every external user as asking the same question of the product.

`certification/audience-interface-v1.json` defines five independent stakeholder witnesses. The grade `audience_green` is earned only when all five executable witnesses pass on the same candidate revision.

| Audience | Witness | Question answered |
| --- | --- | --- |
| MeTTa ecosystem integrator | `WIT-METTA-RUNTIME` | Does the checked MeTTa artifact actually parse, and does the executable teaching projection reduce, in the pinned MeTTaScript runtime? |
| Downstream software integrator | `WIT-DOWNSTREAM-CONTRACT` | Is the CLI surface deterministic and bounded for the interface we declare today? |
| Security / production operator | `WIT-OPERATOR-RESILIENCE` | Do malformed inputs in the certified corpus terminate and reject within declared resource/error bounds? |
| Research reviewer / reproducibility auditor | `WIT-REVIEWER-TRACEABILITY` | Can the Four Color teaching artifact be traced consistently to one pinned source/checker authority boundary? |
| Keyboard / low-vision / human-audit user | `WIT-HUMAN-OPERABILITY` | Can a keyboard user reach meaningful controls, and does the lesson reflow without horizontal overflow at 320 CSS pixels? |

## Composition

The five witnesses are conjunctive for `audience_green`: 5/5 are required.

Audience green does **not** imply overall product green. In particular, it does not close the planned semantic benchmark gates, the separate manual WCAG/assistive-technology review, or formal proof replay unless those independent witnesses are also green.

The important discipline is that each audience gets the strongest mechanical witness we can honestly provide for its own interface, without borrowing authority from a sibling witness.

## Failure history

The first grading cycle caught two witness-design defects before promotion:

- an adversarial Python case contained a lone surrogate that could not cross the subprocess argument encoding boundary, so it was replaced with an ASCII-transportable invalid Python escape that reaches the analyzer;
- the first human-operability check incorrectly combined a 320 CSS-pixel viewport with CSS `zoom: 2`, effectively demanding a much narrower layout than the WCAG 1.4.10 reflow endpoint. The promoted witness tests the 320 CSS-pixel endpoint mechanically; real browser zoom and assistive-technology behavior remain in the manual accessibility gate.

Those failures are part of the evidence that the witnesses themselves are subject to challenge and correction.
