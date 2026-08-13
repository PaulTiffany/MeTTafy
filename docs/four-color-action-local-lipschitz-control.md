# Action-Local Lipschitz Control for the Degree-Five Four Color Construction

**Status:** proof-interface correction and mechanical contract.

The proof-relevant controller is action-local. A construction state may expose
more than one currently permitted parameter, but a realized choice is one
morphism with one affected successor:

\[
\boxed{z\xrightarrow{a}z_a,\qquad |\operatorname{Affected}(z,a)|=1.}
\]

Counterfactual siblings are audit objects, not coordinates of the realized
action.

## 1. Change direction

At zero focus slack, one already-chosen current embedding-derived dual
parameter may be realized:

\[
z_t\xrightarrow{\operatorname{turn}(p)}z_{t+1}=T_pz_t.
\]

The exact certificate preserves the fixed graph carrier and every committed
edge obligation. Further permissions are derived again from the actual
successor.

## 2. Focus color commitment is not stopping

The exact observable

\[
A_z(v)=Q_4\setminus c(N(v))
\]

has one direct Four Color meaning. If

\[
A_z(v)\neq\varnothing,
\]

a currently admissible color may be committed:

\[
z_t\xrightarrow{\operatorname{commit}(q)}z_t[v\mapsto q].
\]

That operation is represented by `CommitFocusAction`. It is **not** represented
as a stop action. The earlier `StopAction`/`realize_stop` names incorrectly
collapsed focus admissibility into the separate trajectory notion of stopping
and have been removed from the proof-relevant Four Color controller.

The distinction matters for the fixed theorem species just as the fixed
sphere/plane surface does: a torus or another mutable topology is not a legal
construction action, and neither is an unrelated stop semantics silently
inserted into a color commitment.

## 3. Bounded realization

For construction Hamming distance on one fixed carrier,

\[
d_H(z,z')=|\{u:c_z(u)\ne c_{z'}(u)\}|,
\]

one realized direction change has finite displacement bounded by the currently
committed carrier, while a focus commitment changes exactly one assignment.
This is the per-action finite-budget layer of the Lipschitz Contract.

## 4. Counterfactual search is audit-only

`cacophony_router.py`, `staged_cacophony_search.py`, and exhaustive transition
families may enumerate alternatives to try to kill a proposed law. They are not
the proof-relevant choice law.

The execution semantics remain

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

CI rejects action schemas that acquire plural/future outcome coordinates or
import the counterfactual routing layer, and now also rejects a return of the
old Four-Color `StopAction` vocabulary.
