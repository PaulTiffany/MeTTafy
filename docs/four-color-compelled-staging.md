# Compelled Staging for Witness Expansion

**Status:** mechanical progress law for finite declared stage universes. This note does not claim Witness-Expansion Closure or the Four Color Theorem.

## 1. Why staging is the next object

The locked degree-five branch already shows that a boundary-only recoloring can be reversible. A legal planar cut can toggle the boundary and the same cut can toggle it back. Therefore the boundary word alone cannot support a strict descent argument.

The proof state must retain more than the current boundary. When an obstruction exposes a new continuation relation, that relation must be added to the state rather than discarded. This is compelled staging:

\[
(K,W,h) \longrightarrow (K',W',h')
\]

with

\[
W \subsetneq W'.
\]

The strict inclusion is not aesthetic decoration. It records that the next admissible move became available only after the proof retained information that the earlier representation could not safely omit.

## 2. Finite declared stage universe

For one fixed construction object, let `S` be a finite set of concrete stage certificates supplied by the embedding/construction layer. Examples could eventually be content-addressed dual paths, Jordan cuts, local retriangulations, or other graph-native certificates. This tranche does **not** claim which certificates are sufficient for Four Color closure.

A staging state records:

\[
(W,S,h)
\]

where `W` is the retained witness set and `h` is the ordered history of already consumed stages.

The mechanical rank is

\[
\mu(W,S,h)=|S\setminus h|.
\]

A compelled stage is admissible as a progress step only when:

1. its stage certificate lies in `S`;
2. it has not already been consumed;
3. it strictly enlarges the retained witness;
4. the inherited witness is preserved exactly.

Then

\[
\mu_{i+1}=\mu_i-1.
\]

This gives a well-founded rank **conditional on the supplied finite stage universe**.

## 3. What this blocks

The known locked boundary involution cannot masquerade as progress by replaying the same cut twice. The first traversal consumes the concrete stage certificate and retains its witness. The inverse traversal across the same certificate is therefore rejected as a second progress step.

This is deliberately weaker than saying the inverse recoloring is mathematically impossible. It says only that an already-consumed reversible move cannot be counted twice in a monotone construction proof.

That distinction is essential: the theorem must not manufacture irreversibility by denying a real graph symmetry.

## 4. Beauty as compelled staging

The research principle motivating this tranche is:

> when direct closure would violate retained invariants, enlarge the representation by the minimum witness needed for lawful continuation.

Each stage therefore has two simultaneous monotonicities:

\[
W_i \subsetneq W_{i+1}
\]

and

\[
\mu_{i+1}<\mu_i.
\]

The first says the proof does not obtain simplicity by forgetting. The second says a declared finite construction budget is actually being consumed.

This is the exact sense in which staging can be both complexity-increasing in representation and well-founded in construction.

## 5. The theorem gap remains visible

Finite stage exhaustion is **not** Witness-Expansion Closure.

If

\[
\mu=0
\]

while the original center remains locked, the correct result is `exhausted`, not `proved`.

A full Four Color closure theorem must still establish, from planar structure rather than by declaration, that:

1. the chosen stage universe is complete for every locked construction state;
2. every nonterminal locked state has an admissible fresh compelled stage;
3. consuming stages cannot strand the construction before the original focus opens;
4. the terminal state preserves the full indexed edge ledger and uses only `Q4`;
5. the stage universe and progress law do not depend on hidden Four Color authority.

The current mechanical witness certifies only the progress law once a finite stage universe is supplied.

## 6. Why this matters for the next theorem

The earlier question was "find a scalar that decreases on every locked C5 recoloring." The planar-dual counterexample showed that this is too flat.

The sharper question is now:

> what finite graph-native stage universe is compelled by the expanding planar witness, and why must one fresh stage remain available until the original obstruction opens?

That is a stronger and more faithful target for Witness-Expansion Closure.
