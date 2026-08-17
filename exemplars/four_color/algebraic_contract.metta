; Track B — algebraic Four Color proof contract
; Held-out Rocq Four Color labels are forbidden as premises here.

(Theory FourColorAlgebraicContract)

; --- theorem species ---
(TerminalColor q0)
(TerminalColor q1)
(TerminalColor q2)
(TerminalColor q3)
(CompositeColor brown)
(= (Terminal brown) False)

; Indexed obligations are external witnesses, never aggregate aliases.
(: edge-obligation (-> Atom Atom Atom))
(: obligation-preserved (-> Atom Bool))
(: new-obligation-satisfied (-> Atom Bool))
(: terminal-in-q4 (-> Atom Bool))
(: budget-bounded (-> Atom Bool))
(: certificate-composes (-> Atom Bool))

; A local planar expansion witness must satisfy the fixed contract.
(: local-expansion (-> Atom Bool))
(= (admissible-local-expansion $t)
   (and (local-expansion $t)
        (obligation-preserved $t)
        (new-obligation-satisfied $t)
        (terminal-in-q4 $t)
        (budget-bounded $t)
        (certificate-composes $t)))

; Brown can exist internally but cannot be terminal.
(: brown-residue (-> Atom Bool))
(: unresolved-external-conflict (-> Atom Bool))
(: reexpanded-before-commit (-> Atom Bool))
(= (admissible-brown-state $x)
   (and (brown-residue $x)
        (or (not (unresolved-external-conflict $x))
            (reexpanded-before-commit $x))))

; --- dependency hygiene ---
(: upstream-of-closure (-> Atom Bool))
(ForbiddenClosurePremise FourColorTheorem)
(ForbiddenClosurePremise HeldOutRocqAuthority)
(ForbiddenClosurePremise SRMFFourCharts)
(ForbiddenClosurePremise NoStableFifthClass)

(= (dependency-violation $x)
   (and (ForbiddenClosurePremise $x)
        (upstream-of-closure $x)))

; --- global closure interface ---
(: planar-generator (-> Atom Bool))
(: generator-complete (-> Atom Bool))
(: has-local-witness (-> Atom Bool))
(: composes-terminating (-> Atom Bool))

(= (contract-expansion-closure $E)
   (and (generator-complete $E)
        (has-local-witness $E)
        (composes-terminating $E)))

; Final theorem promotion is permitted only through the closure interface.
(= (four-color-contract-certified $E)
   (and (contract-expansion-closure $E)
        (not (dependency-violation FourColorTheorem))
        (not (dependency-violation HeldOutRocqAuthority))
        (not (dependency-violation SRMFFourCharts))
        (not (dependency-violation NoStableFifthClass))))

; Intended mechanical queries:
; !(match &self (dependency-violation $x) $x)
; !(match &self (admissible-local-expansion $t) $t)
; !(match &self (four-color-contract-certified $E) $E)
;
; A successful theorem query requires actual generator-completeness,
; local-witness, and termination facts supplied elsewhere. This file does not
; assert them by fiat.
