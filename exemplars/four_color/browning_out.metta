; Track B — independent differential color proof program
; Dependency discipline: SRMF is downstream of the continuous dynamics.
; This file must not use four SRMF operators, held-out 4CT labels, or
; NoStableFifthClass as premises for the terminal-rank theorem.

(Theory DifferentialBrowningOutColorAlgebra)

; --- foundational differential substrate ---
(: symbolic-density (-> Atom Bool))
(: drift-field (-> Atom Bool))
(: laplace-beltrami (-> Atom Bool))
(: inverse-temperature (-> Atom Bool))
(: fokker-planck-evolves (-> Atom Bool))

; Conceptual governing equation carried by the proof graph:
; d rho / ds = - div(rho D) + beta^-1 Delta_s rho

; --- graph boundary obligations ---
(: planar-conflict-object (-> Atom Bool))
(: indexed-edge-obligation (-> Atom Bool))
(: obligation-preserved (-> Atom Atom Bool))

; --- chromatic differential modes ---
(: chromatic-mode (-> Atom Bool))
(: terminal-mode (-> Atom Bool))
(: observer-discriminable (-> Atom Bool))
(: differential-persistent (-> Atom Bool))
(: diffusion-survives (-> Atom Bool))
(: contraction-survives (-> Atom Bool))
(: boundary-compatible (-> Atom Bool))
(: independent-mode (-> Atom Bool))
(: composite-residue (-> Atom Bool))

; Brown is residue, not a terminal color.
(CompositeClass brown)
(= (terminal-mode brown) False)
(= (composite-residue brown) True)

; A terminal chromatic mode must survive the upstream dynamics and all
; external boundary obligations. Naming a mode is never sufficient.
(= (admissible-terminal-mode $x)
   (and (chromatic-mode $x)
        (differential-persistent $x)
        (diffusion-survives $x)
        (contraction-survives $x)
        (observer-discriminable $x)
        (boundary-compatible $x)))

; --- central theorem surface ---
(: planar-terminal-rank-at-most-four (-> Atom Bool))
(: differential-closure-witness (-> Atom Bool))
(: excess-mode-browns-out (-> Atom Bool))

; IMPORTANT: this is a proof target, not an asserted theorem.
(= (differential-four-color-target $P)
   (and (planar-conflict-object $P)
        (differential-closure-witness $P)
        (planar-terminal-rank-at-most-four $P)))

; A nonterminal excess mode may brown out while its indexed provenance and
; edge obligations remain auditable.
(= (admissible-browning $x)
   (and (chromatic-mode $x)
        (not (admissible-terminal-mode $x))
        (excess-mode-browns-out $x)
        (composite-residue brown)))

; --- constructive falsifier ---
; A genuine fifth class is a fifth independent differential mode/basin that
; survives every upstream guard and remains boundary-compatible.
(: fifth-mode-candidate (-> Atom Bool))

(= (falsifies-differential-closure $x)
   (and (fifth-mode-candidate $x)
        (independent-mode $x)
        (admissible-terminal-mode $x)
        (not (excess-mode-browns-out $x))))

; --- downstream SRMF transport only ---
(: srmf-factorization-witness (-> Atom Bool))
(: no-stable-fifth-class (-> Atom Bool))

; NoStableFifthClass may be derived only after the differential closure proof.
(= (derived-no-stable-fifth-class $P)
   (and (differential-four-color-target $P)
        (srmf-factorization-witness $P)
        (no-stable-fifth-class $P)))

; Forbidden dependency pattern, recorded for validator implementation:
;   SRMFFourOperators -> PlanarTerminalRankAtMostFour
; Forbidden:
;   NoStableFifthClass -> PlanarTerminalRankAtMostFour
; Allowed:
;   FokkerPlanck + PlanarBoundary + DifferentialClosureWitness
;       -> PlanarTerminalRankAtMostFour
;       -> BrowningOut
;       -> SRMFFactorization
;       -> NoStableFifthClass

; Intended queries:
; !(match &self (differential-four-color-target $P) $P)
; !(match &self (falsifies-differential-closure $x) $x)
; !(match &self (derived-no-stable-fifth-class $P) $P)
