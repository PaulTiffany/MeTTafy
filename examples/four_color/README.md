# Four Color Lean micro-witnesses

These files are deliberately bounded formal witnesses for the independent Four Color research lane.

- `FourColorCore.lean` — V4 palette algebra, fixed-region and hard-frontier separation, degree-five frontier facts, and atomic bichromatic turn preservation.
- `C2ContactVoid.lean` — contact/void semantics, the coarse Brown projection, canonical `A B A C D` carrier incidence, and the reduction of C2 clean-carrier existence to one explicit planar crosscut-intersection premise.
- `C2ForcedThird.lean` — the red-team forced-third law: fixing one lower/reference state leaves three nontrivial upward states, and any two distinct upward states uniquely determine the third by `r + x + y`.
- `BrownAffordance.lean` — observer-relative playability: direct color contact determines the local legal-move profile, while Brown can distinguish occupancy (`void` versus `colored`) but cannot factor the color-dependent affordance profile through its coarse observation.
- `RedTeamComposition.lean` — one-turn composition for the hard degree-five game: a proper one-site frontier rewrite either re-enters the same hard/A-B-A red-team normal form or removes the old seed color from the frontier and thereby opens a concrete focus-color opportunity. A successor that remains blocked therefore re-enters the same normal form. The same file also banks the finite stop condition: relative to one fixed reference there are exactly three upward states, and once all three have acted, a void rule that makes acted states unavailable leaves no upward action on that local surface; any later action must be a fresh start/restart elsewhere.

These files do not claim a new proof of the Four Color Theorem. In particular, `crosscut_meets_opposite` remains an open planar-topology obligation. The red-team composition witness does not require or claim a monotone ranking function, a global non-replay theorem, or a proof that every restart policy over an arbitrary map eventually exhausts all voids.
