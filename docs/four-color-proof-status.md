# Four Color Proof Program — Current Status

**Repository:** `PaulTiffany/MeTTafy`  
**Branch:** `agent/ordered-state-construction`  
**Status:** active independent proof program; not yet a closed proof of the Four Color Theorem

## 1. Canonical simplification

The current Track-B proof object is **ordered state construction**.

The four states do not inspect simultaneous futures and do not alternate through
a micro-action game.  A state gets its turn, continues until the planar shape
relevant to the construction is determined, and that realized shape becomes a
constraint inherited by later states.

```text
state 1 establishes shape
-> state 2 inherits shape 1 and establishes shape 2
-> state 3 inherits shapes 1,2 and establishes shape 3
-> state 4 inherits shapes 1,2,3 and establishes shape 4
```

Length is irrelevant.  The proof-relevant data are incidence, cyclic order,
side relation, permitted shared boundary contact, and forbidden crossing or
alteration of an already established continuation.

The detailed definition is in `docs/four-color-ordered-state-construction.md`.

## 2. Fixed theorem species

The construction remains on one fixed finite closed genus-zero planar carrier.
The graph, indexed edge obligations, and terminal palette

\[
Q_4=\{0,1,2,3\}
\]

are fixed.  No future route, theorem verdict, opening/closure flag, observer
state, or held-out Four Color label is a construction coordinate.

A proper coloring still means only

\[
uv\in E\Longrightarrow c(u)\neq c(v).
\]

Thus every primitive conflict is pairwise and indexed by one edge.

## 3. Easy mathematics now kept easy

### 3.1 Pairwise interaction

No higher-order primitive is required to represent graph coloring.  Apparent
higher-order difficulty comes from composition of inherited pairwise planar
constraints.

Principia quadratic sufficiency may witness that fact, but it is not proof
authority for fourness.

### 3.2 Degree-five reduction

For a minimum planar counterexample, elementary reduction leaves the only local
nontrivial focus at degree five.  The five incident edges are five separately
indexed obligations.

### 3.3 Four states, five indexed obligations

By the fifth indexed obligation, reuse of one of four state classes is
unavoidable.  This is pigeonhole arithmetic, not the Four Color theorem.

The hard issue is whether the reused state can continue lawfully in the already
constricted planar geometry.

## 4. Central theorem gap

The canonical open target is now:

### Sequential Planar Reuse Lemma — OPEN

On a fixed closed genus-zero planar construction, after predecessor state shapes
have been established turn by turn with their incidence and cyclic order
retained, a fifth degree-five obligation admits reuse of at least one of the
four existing states without forcing a forbidden crossing or alteration of an
earlier established relation.

A valid falsifier must therefore exhibit all of:

1. a finite genus-zero carrier;
2. four lawfully established predecessor state shapes;
3. a fifth indexed obligation;
4. and proof that every reuse continuation violates retained planarity.

This is the theorem to prove or kill.

## 5. What existing machinery is for

The repository contains substantially more machinery than the canonical proof
now assumes.  It remains useful as a falsifier/witness bank.

- `ConstructionState` — fixed graph, partial commitments, exact edge ledger.
- C5/V4 derivative calculus — exact local differences on the degree-five ring.
- plane-dual continuation — graph-native physical continuation witnesses.
- locked planar C5 witnesses — prevent us from flattening away exterior shape.
- graph-native nonreplay history — prevents reversible symmetry from being
  mislabeled as progress.
- staged and handoff experiments — evidence about what happens when the simple
  reuse claim is sliced into micro-actions.
- held-out Rocq extraction — post-hoc comparison only; never Track-B authority.

Bellman values, scalar phase ranks, holonomy, SRMF, browning-out, observer
quotients, V4-flow decoding, and similar layers are **not premises of the
central theorem**.  They are retained only if the direct planar argument later
requires them.

## 6. Existing exact local facts retained

The following remain banked and useful:

- adjacency is definitionally the conflict relation;
- a saturated proper degree-five C5 boundary using Q4 has role form
  `A B A C D` up to symmetry;
- its V4 derivative has multiplicity pattern `(3,1,1)`;
- exterior connectivity can genuinely lock naive one-step Kempe openings;
- actual dual path switches preserve the fixed graph and exact edge ledger;
- a legal local move need not monotonically decrease any scalar;
- future controls must be derived from the realized successor, not imported as
  counterfactual coordinates.

These facts constrain a proof.  They do not replace Sequential Planar Reuse.

## 7. Immediate research program

```text
fixed planar carrier
-> identify one predecessor state shape exactly
-> anchor its incidence/cyclic-order data
-> derive the next state only inside the inherited admissible geometry
-> repeat through four states
-> present the fifth indexed obligation
-> prove lawful state reuse OR bank the exact planar falsifier
```

The next mechanical work should therefore test ordered predecessor shapes
directly on the existing hard planar witnesses, rather than inventing another
global progress potential.

## 8. Trust boundary

Track A remains the pinned held-out Rocq Four Color development and may be used
only after Track-B claims are frozen for structural comparison.

Track B may use ordinary graph theory and planar topology, but it may not import
an equivalent Four Color existence theorem under another name.

## 9. Bottom line

We do **not** yet have a new proof of the Four Color Theorem.

We have reduced the independent proof attempt to a substantially smaller
question:

\[
\boxed{
\text{Does ordered planar state formation force a lawful reuse among four
states at the degree-five fifth obligation?}
}
\]

Everything else is secondary until that statement is proved or falsified.