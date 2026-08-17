# Fresh-Stage Routing as a Cost-of-Cacophony Problem

**Status:** exact graph-native one/two-stage router plus an exhaustive theorem for the labelled boundary-only triangulated pentagon class. The arbitrary-interior planar switching lemma remains to be derived; this note does not promote the full Four Color Theorem.

## 1. Freshness is necessary but not a routing rule

At a saturated degree-five construction point

\[
z_0=(G,c),\qquad A_c(v)=\varnothing,
\]

the retained embedding exposes a finite set of current nonzero plane-dual controls. Graph-native stage history tells us which physical mode/cut identities have already been consumed as proof progress.

That history solves replay, but it does not by itself solve **selection**. Two controls can both be fresh and exact while having different consequences for the focus observable. Treating all simultaneously available controls as interchangeable is precisely the staged-interference problem addressed here.

The router therefore distinguishes two current regimes without adding either regime to `ConstructionState`:

- **direct:** at least one fresh current dual control yields \(A(v)\neq\varnothing\);
- **pivot:** fresh current controls exist, but none yields focus slack at the present zero-point.

The classification is recomputed from the current embedding and history. It is control metadata, not a theorem-state coordinate.

## 2. Receding-horizon router

The exact controller is

\[
R(z_t,h_t).
\]

If a current fresh control \(T\) already satisfies

\[
A_{Tz_t}(v)\neq\varnothing,
\]

it is taken immediately. This is the one-stage/direct regime and carries zero extra staging cost.

If every current fresh control preserves zero focus slack, the controller may take one lawful pivot

\[
z_t\xrightarrow{T_1}z_{t+1},
\]

retain its content-addressed physical witness, and rebase all control parameterizations at the exact successor zero-point. Only then are the next controls derived. If a fresh successor control \(T_2\) yields focus slack,

\[
z_t\xrightarrow{T_1}z_{t+1}\xrightarrow{T_2}z_{t+2},
\qquad A_{z_{t+2}}(v)\neq\varnothing,
\]

the route carries one unit of extra staging cost.

Nothing about this procedure inserts a future path into the Four Color construction state. The second-stage access is certified from the successor actually induced by the first stage.

## 3. Exact boundary-only theorem

Consider a triangulated pentagonal disk with **no interior vertices**. There are exactly five labelled Catalan triangulations of the five-cycle. For each triangulation, retain only saturated proper four-color boundary assignments that also satisfy its two diagonal edge obligations.

`tests/test_cacophony_router.py` exhausts this complete labelled class:

\[
\boxed{360\text{ compatible saturated embedded constructions}.}
\]

Every one has an exact graph-native route to positive focus slack in at most two stages:

\[
\boxed{240\text{ direct one-stage instances}}
\]

and

\[
\boxed{120\text{ pivot two-stage instances}.}
\]

Thus on the entire boundary-only class,

\[
\boxed{
A(v)=\varnothing
\Longrightarrow
\text{direct focus slack or one pivot followed by direct focus slack}.
}
\]

The persistent-double-lock carrier is in the pivot class. The router derives a zero-slack first stage, rebases at the exact successor, and mechanically observes that the successor is in the direct regime before applying the second stage.

## 4. Cost of cacophony

The key distinction is now concrete: **freshness is not routing**.

The exhaustive class contains direct-regime states with both kinds of fresh current controls at once:

\[
T_a:z_0\mapsto z_a,\quad A_{z_a}(v)\neq\varnothing,
\]

while another equally fresh legal control satisfies

\[
T_b:z_0\mapsto z_b,\quad A_{z_b}(v)=\varnothing.
\]

A controller that merely consumes unused stages can therefore pay unnecessary staging cost or enter avoidable interference. The proof-relevant quantity is not the number of available controls but their ordered consequence under the present geometry.

This is the Four Color realization of the same structural lesson as staged multi-constraint control: simultaneous admissibility does not imply simultaneous usefulness; a pivot changes the geometry in which the next decision is made.

For the boundary-only theorem the exact extra-stage cost is

\[
C_{\mathrm{stage}}=m-1\in\{0,1\},
\]

where \(m\) is the certified number of dual stages required to obtain positive focus slack.

## 5. Sharpened arbitrary-interior obligation

The finite theorem isolates a stronger and cleaner candidate than unrestricted fresh-stage existence.

Let the two singleton V4 modes of a saturated C5 be \(\sigma\) and \(\tau\). Their retained embedding determines two alternating two-mode continuation networks. Call the current geometry **dual-pivot** when neither singleton-mode network supplies a focus-slack-producing domain translation.

The next universal target is the **planar dual pivot-switching lemma**:

> For an arbitrary properly colored triangulated pentagonal disk, if both current singleton-mode continuation families are pivot-type, then a certified domain translation along an actual current dual path produces a successor whose freshly derived dual parameterization contains a direct focus-slack control.

A sufficient form is

\[
\boxed{
\operatorname{Pivot}(z)
\Longrightarrow
\exists T_1\in\mathcal A_{\mathrm{dual}}(z):
\operatorname{Direct}(T_1z).
}
\]

Together with the already exact direct case this would give

\[
A(v)=\varnothing
\Longrightarrow
\text{positive focus slack in at most two graph-native dual stages}
\]

for arbitrary retained triangulated disks, with each stage preserving the fixed genus-zero species and complete edge ledger.

The boundary-only exhaustive theorem is evidence for this switching law, not a substitute for its arbitrary-interior proof. The next derivation should work on the alternating dual path systems themselves, where a domain translation swaps the two selected V4 edge modes along one embedded path and thereby changes the successor pairing geometry.
