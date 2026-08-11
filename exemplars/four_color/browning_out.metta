; Track B — independent symbolic color proof program
; This file must not import held-out Four Color proof labels as premises.

(Theory BrowningOutColorAlgebra)

; --- sorts / terminal classes ---
(TerminalClass q1)
(TerminalClass q2)
(TerminalClass q3)
(TerminalClass q4)
(CompositeClass brown)

; Brown is explicitly nonterminal.
(= (Terminal brown) False)
(= (Composite brown) True)

; --- indexed obligations ---
; Obligations remain distinct by identity even when endpoint values coincide.
(: obligation-distinct (-> Atom Atom Bool))
(= (obligation-distinct $o1 $o2) (not (== $o1 $o2)))

; --- browning operator ---
(: brown-step (-> Atom Atom))

; Terminal idempotence.
(= (brown-step q1) q1)
(= (brown-step q2) q2)
(= (brown-step q3) q3)
(= (brown-step q4) q4)
(= (brown-step brown) brown)

; Candidate fifth classes are not licensed merely by naming them.
; They must exhibit a novel invariant stable under the full SRMF cycle.
(: fifth-candidate (-> Atom Bool))
(: novel-invariant (-> Atom Bool))
(: observer-stable (-> Atom Bool))
(: obligations-preserved (-> Atom Bool))
(: terminal-independent (-> Atom Bool))

(= (stable-fifth $x)
   (and (fifth-candidate $x)
        (novel-invariant $x)
        (observer-stable $x)
        (obligations-preserved $x)
        (terminal-independent $x)))

; --- SRMF routing predicates ---
(: ttcs-explores (-> Atom Bool))
(: ttpr-refines (-> Atom Bool))
(: ttie-reexpands (-> Atom Bool))
(: ttdc-commits (-> Atom Bool))
(: unresolved-external-conflict (-> Atom Bool))

; Brown cannot mask unresolved external conflict.
(= (admissible-brown $x)
   (and (== (brown-step $x) brown)
        (obligations-preserved $x)
        (or (not (unresolved-external-conflict $x))
            (ttie-reexpands $x))))

; --- proof target ---
; The target rule is intentionally conditional on an algebraic closure witness.
; MeTTa must not assert closure by fiat.
(: contracts-to-existing (-> Atom Bool))
(: contracts-to-brown (-> Atom Bool))
(: algebraic-closure-witness (-> Atom Bool))

(= (no-stable-fifth-class $x)
   (and (fifth-candidate $x)
        (algebraic-closure-witness $x)
        (or (contracts-to-existing $x)
            (and (contracts-to-brown $x)
                 (admissible-brown $x)))))

; A genuine counterexample to this proof route must survive every guard.
(= (falsifies-browning-proof $x)
   (and (stable-fifth $x)
        (not (contracts-to-existing $x))
        (not (contracts-to-brown $x))))

; Intended queries:
; !(match &self (no-stable-fifth-class $x) $x)
; !(match &self (falsifies-browning-proof $x) $x)
;
; The current file defines the proof surface. Subsequent tranches must supply
; planar conflict instances and algebraic closure witnesses rather than
; importing the Four Color conclusion.
