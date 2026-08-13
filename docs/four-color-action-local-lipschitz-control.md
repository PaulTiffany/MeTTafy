# Action-Local Lipschitz Control for the Degree-Five Four Color Construction

**Status:** proof-interface correction and mechanical contract.

The proof-relevant controller is action-local.  A construction state may expose
more than one currently permitted parameter, but a realized choice is one
morphism with one affected successor:

\[
\boxed{z\xrightarrow{a}z_a,\qquad |\operatorname{Affected}(z,a)|=1.}
\]

Counterfactual siblings are not coordinates of the realized action.  They may
be enumerated by an offline falsifier, but the state does not inspect several
successor states and then authorize one by comparing their outcomes.

This is the same bounded interaction discipline as the simple trajectory
red-team model: continuing a trajectory does not grant authority over every
other trajectory; when a state changes direction or stops, the realized action
has one corresponding affected state.  Composition happens one action at a
time.

## 1. Change direction

When the degree-five focus has zero palette slack, one already-chosen current
embedding-derived dual parameter `p` may be realized:

\[
z_t\xrightarrow{\operatorname{turn}(p)}z_{t+1}=T_p z_t.
\]

`ChangeDirectionAction` carries only:

```text
chosen DualDomainParameter
current graph-native history
one certified realized stage
```

The action does **not** contain alternatives, candidate successors, outcome
arrays, routes, or a future destination.  The exact dual-domain certificate
preserves the fixed graph carrier and every committed edge obligation.  After
the action, any further parameterization is derived again from the actual
successor `z_(t+1)`.

## 2. Stop

When the exact observable

\[
A_z(v)=Q_4\setminus c(N(v))
\]

is nonempty, the local traversal may stop by committing one chosen admissible
color `q`:

\[
z_t\xrightarrow{\operatorname{stop}(q)}z_{t+1}=z_t[v\mapsto q].
\]

This again has exactly one affected successor.  The stop action changes one
committed assignment and mechanically rechecks the complete indexed edge
ledger.

## 3. Bounded realization

For the construction Hamming metric on one fixed carrier,

\[
d_H(z,z')=|\{u:c_z(u)\ne c_{z'}(u)\}|,
\]

one realized direction change has finite displacement bounded by the number of
currently committed vertices, while a stop action has displacement exactly one.
This is the per-action finite-budget layer of the Lipschitz Contract.  It does
not replace the stronger transformation-neighborhood inequality

\[
d(Tz,Tz')\le Ld(z,z'),
\]

when that comparison is required; it prevents a more basic breach first: one
choice may not co-realize or causally consult a fan-out of sibling successor
states.

## 4. Counterfactual search is audit-only

`cacophony_router.py`, `staged_cacophony_search.py`, and exhaustive transition
families remain useful mechanical falsifiers.  They can ask whether a proposed
law survives many possible controls.  They are **not** the proof-relevant
choice law.

In particular, the previously tested relation

\[
\operatorname{Direct}(Tz)\lor\Delta\Phi(T)<0
\]

across all four current controls is retained as counterfactual evidence about
the transition algebra.  It must not be interpreted as a state looking at four
future outcomes and choosing the favorable one.

The proof-relevant execution semantics are instead:

\[
\boxed{
\text{derive permissions at }z_t
\to
\text{choose one action}
\to
\text{realize one }z_{t+1}
\to
\text{derive again at }z_{t+1}.
}
\]

## 5. CI boundary

`scripts/validate_action_local_control.py` rejects proof-relevant action schemas
that acquire plural/future outcome coordinates or import the counterfactual
routing/search layer.  CI therefore guards the distinction between:

- **permission surface:** controls currently available at the shared zero-point;
- **realized action:** one selected control and one affected successor;
- **audit surface:** optional exhaustive counterfactual enumeration used only to
  try to falsify algebraic claims.

This action-local boundary is now part of the mechanical Four Color proof
contract.
