# Four Color Proof — Ordered State Construction

**Track:** B, independent construction route  
**Status:** canonical simplification; one planar reuse theorem remains open

## 1. Construction rule

The proof object is not a simultaneous choice tree.

There are four state classes

\[
Q_4=\{q_0,q_1,q_2,q_3\}.
\]

They are realized **in turns** on one fixed closed genus-zero planar carrier.
A turn establishes the actual shape needed by one state under the constraints
already present.  Once that shape is established, later turns inherit it as
part of their admissibility boundary.

Schematically,

\[
z_0\xrightarrow{q_0}z_1
\xrightarrow{q_1}z_2
\xrightarrow{q_2}z_3
\xrightarrow{q_3}z_4.
\]

The essential direction is one-way:

\[
\boxed{\text{realized earlier shape}\;\Longrightarrow\;\text{constraint on later continuation}.}
\]

A later state is not allowed to obtain feasibility by silently changing the
incidence or cyclic order already established by an earlier state.

## 2. What `shape` means

Length is irrelevant.  A state may continue arbitrarily far while nothing
forces it to interact with another established state.

For proof purposes its shape is only the finite topological data that becomes
relevant when another continuation encounters it:

- incidence;
- cyclic order;
- which side of an established planar continuation a later continuation lies on;
- permitted shared boundary contact, when explicitly part of the carrier;
- forbidden crossing or alteration of an already established continuation.

Thus free continuation carries no proof cost merely because it is long.  A new
proof obligation appears only at an interaction.

## 3. Sequential admissibility

Let \(\Gamma_i\) be the retained shapes after turn \(i\).  For a candidate next
continuation \(\gamma\), write

\[
\gamma\perp_{\!P}\Gamma_i
\]

when \(\gamma\) preserves every established planar incidence and cyclic-order
relation and introduces no forbidden crossing.

The next admissible set is

\[
\mathcal A_{i+1}
=
\{\gamma:\gamma\text{ satisfies its own indexed obligation and }
\gamma\perp_{\!P}\Gamma_i\}.
\]

After realizing \(\gamma_{i+1}\),

\[
\Gamma_{i+1}=\Gamma_i\cup\{\gamma_{i+1}\}.
\]

Therefore admissibility is inherited monotonically:

\[
\boxed{\mathcal A_{i+2}\subseteq\mathcal A_{i+1}}
\]

with respect to the accumulated predecessor constraints.  This is the simple
turn-based content: each realized state constricts the next.

No future route is a state variable.  The next admissible continuation is
derived only after the preceding shape is known.

## 4. Pairwise primitive interaction

The primitive obstruction is pairwise:

\[
\text{new continuation}\quad\text{vs.}\quad\text{one established continuation}.
\]

A violation occurs when the new continuation would cross, alter, or reverse the
retained incidence/cyclic order of an established one.

Higher apparent complexity comes from composition of these pairwise inherited
constraints.  It is not a new primitive interaction order.

This is the only role currently needed from the Principia quadratic-sufficiency
observation.

## 5. Degree-five specialization

In a minimum-counterexample presentation, the only local nontrivial focus has
five separately indexed incident obligations.

Process those obligations on the fixed planar carrier.  There are only four
state classes.  Therefore by the fifth indexed obligation at least one state
class must be reused.

That cardinality statement is trivial and is **not** the Four Color theorem.
The theorem-specific question is geometric:

> when a state class is reused, can its required continuation be realized
> without violating the shapes established on earlier turns?

This separates the easy part from the hard part cleanly:

\[
\boxed{
5\text{ indexed obligations}+4\text{ states}
\Longrightarrow
\text{reuse is unavoidable}
}
\]

but

\[
\boxed{
\text{planarity}
\Longrightarrow
\text{at least one lawful reuse continuation}
}
\]

is the remaining theorem.

## 6. The one theorem to attack

### Sequential Planar Reuse Lemma — OPEN

On a fixed closed genus-zero planar construction, suppose four state classes
have been realized turn by turn with all inherited incidence and cyclic-order
constraints retained.  At a degree-five focus, the fifth indexed obligation
cannot require a genuinely new state class: at least one existing state admits
a continuation satisfying the fifth obligation while preserving every earlier
retained planar relation.

Equivalently, a proposed counterexample must provide:

1. a finite genus-zero carrier;
2. four lawfully established predecessor state shapes;
3. a fifth indexed obligation;
4. and a proof that **every** reuse of the four existing states would force a
   forbidden crossing or alteration of an established predecessor.

That is the falsifier.  Nothing weaker refutes the lemma.

## 7. Relation to the existing machinery

The existing MeTTafy machinery should now be read as witnesses and falsifiers
for this small theorem, not as the theorem itself.

- `ConstructionState` keeps the fixed graph and exact committed edge ledger.
- the C5/V4 derivative calculus records local state differences after a shape
  has been realized;
- plane-dual paths expose actual planar continuations;
- nonreplay history prevents a reversible move from being misreported as new
  construction progress;
- witness expansion is justified only when the currently retained predecessor
  shapes are insufficient to decide the next lawful continuation.

V4 does **not** explain why there are four states.  Bellman values, scalar phase
ranks, holonomy, SRMF, and browning-out are not premises of Sequential Planar
Reuse.  They may be useful later only if the direct planar reuse lemma genuinely
needs them.

## 8. Immediate proof program

The next work is deliberately small:

1. encode the predecessor shapes used by the existing degree-five planar
   witnesses as an ordered retained set;
2. derive each later admissible continuation only from those already realized
   shapes;
3. search specifically for a four-predecessor/fifth-obligation falsifier;
4. if no falsifier survives, isolate the exact Jordan/noncrossing identity that
   blocks it and prove that identity directly.

The intended proof is therefore no longer

```text
invent a global progress scalar
-> prove descent
-> decode four colors
```

but

```text
first state establishes shape
-> second inherits it
-> third inherits both
-> fourth inherits all three
-> fifth indexed obligation must lawfully reuse one established state
```

Only the final arrow is theorem-specific.