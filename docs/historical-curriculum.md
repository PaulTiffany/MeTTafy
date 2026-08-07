# Historical Curriculum: Computation Enters Geometry and Topology

MeTTafy's formal-proof exemplar corpus is also intended as a teaching tool for the history of computational mathematics in topology, geometry, and closely related graph-theoretic problems.

The corpus should therefore preserve more than executable proof artifacts. Each major exemplar should connect:

```text
historical mathematical problem
    -> human proof strategy
    -> computational intervention
    -> formal/checkable artifact
    -> MeTTafy semantic strategy graph
```

The goal is to let a learner see not only **that** a proof computes, but **where computation entered the proof, why it was needed, and how later formalization changed what could be trusted or inspected**.

## Curriculum principle

Prefer famous, citable proof lineages with accessible primary or authoritative secondary sources. A historical exemplar should ideally have:

- a canonical theorem/problem;
- a recognizable historical proof or algorithmic milestone;
- a documented computational component;
- a later formalization or independently checkable implementation when available;
- enough surviving source/material to reconstruct semantic proof strategies without inventing them;
- licensing that permits the intended use, or a reference-only integration when redistribution is inappropriate.

Historical annotations are not training labels unless they can be mapped to explicit proof structure. Biography and narrative provide context; source and checker evidence govern semantic claims.

## Arc 1 — Four Color Theorem

The Four Color Theorem is the natural opening exemplar.

Historical arc:

1. Francis Guthrie's 1852 conjecture;
2. Kempe's 1879 attempted proof and the later discovery of its flaw;
3. development of reducibility, unavoidable sets, and discharging methods;
4. Appel and Haken's 1976 computer-assisted proof, historically notable because a large finite case analysis was delegated to computer calculation;
5. later simplifications and reductions of the unavoidable configuration set;
6. Georges Gonthier's fully computer-checked Coq formalization, where the calculations and their mathematical justification were brought inside a proof-assistant framework.

MeTTafy teaching targets:

- minimal-counterexample reasoning;
- structural reduction;
- unavoidable-set construction;
- discharging / conserved local accounting;
- finite configuration enumeration;
- reducibility checking;
- certificate/checker separation;
- the historical distinction between *computer-assisted* and *formally checked* proof.

This is especially useful because the theorem exposes a recurring MeTTafy question: two programs can perform different low-level calculations while instantiating the same high-level proof strategy.

## Arc 2 — Knot theory and Reidemeister-style computation

Knot theory provides a complementary style of computational topology. Rather than a single enormous finite case check, the domain is rich in diagram transformations and invariant computation.

Potential exemplar families:

- Reidemeister moves as local rewrite rules preserving knot type;
- normalizing or searching over knot diagrams;
- tricolorability and other elementary invariants;
- Alexander/Jones/Kauffman-style polynomial calculations where suitable open implementations and formalizations exist;
- unknot-recognition and equivalence procedures;
- triangulation-based 3-manifold / knot-complement computations.

MeTTafy teaching targets:

- equivalence-preserving rewrite;
- local move systems;
- invariant extraction;
- normalization;
- search modulo equivalence;
- state-space explosion and heuristic guidance;
- distinction between an invariant proving non-equivalence and a transformation sequence proving equivalence.

## Arc 3 — Kepler conjecture / Flyspeck

Although primarily discrete geometry rather than topology, the Kepler conjecture belongs naturally in this historical curriculum because it is another landmark in computer-assisted mathematics.

Thomas Hales and Samuel Ferguson announced a computer-assisted proof in 1998. Concern about the difficulty of fully auditing its computational components helped motivate the Flyspeck project, which ultimately produced a formal proof using HOL Light and Isabelle.

MeTTafy teaching targets:

- decomposition of a global geometric theorem into finite/local verification problems;
- nonlinear inequality verification;
- large proof orchestration across heterogeneous methods;
- trusted-kernel boundaries;
- migration from computational evidence to machine-checked formal proof.

## Arc 4 — Algebraic and computational topology

Once the historical landmark cases establish the idea, the curriculum can move into routine algorithmic topology where computation is not controversial but constitutive of the subject.

Candidate topics:

- simplicial and cellular complexes;
- boundary operators;
- homology via kernels, images, and matrix reduction;
- Euler characteristic;
- simplicial maps and induced maps on homology;
- persistence / filtered complexes when suitable formal artifacts are available;
- discrete Morse-style reductions;
- fundamental-group presentations and rewriting where tractable.

MeTTafy teaching targets:

- algebraic reduction;
- chain-complex construction;
- quotient reasoning;
- normal forms;
- functorial transport;
- local-to-global structure;
- canonicalization and certificate production.

## Exemplar metadata for historical teaching

In addition to the formal exemplar fields in `formal-proof-exemplars.md`, landmark exemplars may include:

```text
history.problem_date
history.conjecturer_or_origin
history.key_proof_dates
history.key_authors
history.primary_citations
history.computational_milestone
history.formalization_milestone
history.teaching_notes
```

These fields are documentary metadata. They must not be passed to the strategy classifier as hidden answer keys during evaluation.

## Training/evaluation discipline

Historical context creates a leakage risk: if the classifier receives theorem names such as `four_color_theorem`, it can guess strategies from reputation instead of recovering them from proof structure.

Therefore benchmark runs should support a **blind mode** that removes theorem titles, author names, historical descriptions, filenames, and other semantic hints. The classifier receives only the proof/program structure and permitted local identifiers.

The historical layer is then joined back onto the result for teaching and interpretation.

This gives MeTTafy two complementary surfaces:

```text
learner view:    history + mathematics + computation + recovered strategies
benchmark view:  proof structure only -> recovered strategies
```

That separation is essential if the same corpus is to serve both education and research.

## Scope note

"Computational topology" is used here as a broad teaching umbrella that includes adjacent landmark problems in planar graph theory and discrete geometry when they illuminate the history of computation in geometrical reasoning. The project should identify the mathematical field of each exemplar precisely rather than retroactively relabel every example as topology.
