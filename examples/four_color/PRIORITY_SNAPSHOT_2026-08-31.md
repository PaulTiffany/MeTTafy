# Four Color Theorem Research — Priority Snapshot

**Author:** Paul Carver Tiffany III  
**Snapshot date:** 31 August 2026  
**Repository:** `PaulTiffany/MeTTafy`  
**Frozen base commit:** `767a305cc2b26e5068eddd57209b80b268ede4ea`  
**Base commit time:** 2026-08-31T03:04:20Z

## Purpose

This document records the state of the independent Four Color Theorem research lane as it existed at the frozen base commit above.

The base commit was already public before this archival note was added. This file is therefore an annotation of that pre-existing Git history, not a retroactive replacement for it.

The purpose of this snapshot is priority and provenance: to make the mathematical and computational state at this point in the research easy to identify, cite, archive, and compare with later revisions.

## State recorded at the snapshot

At the frozen base commit, the repository records a MapMaker formulation with the operational order

```text
Do:Observe
-> Imagine:Observe
-> Imagine:Act*
-> Do:Act
```

and a formal Four Color development in which:

- the ordered MapMaker product fixes phases 1, 2, and 4 while reducing repeatable strategic variation to phase 3;
- relative to a fixed reference color, the phase-3 decision surface is represented by the three nonidentity directions of the Klein four-group `V4`;
- proper boundary-edge differences lie on that same nonzero `V4` surface rather than creating an additional decision dimension;
- arbitrary retained imaginary traversal has a small algebraic normal form: identity or one of the three nonidentity directions;
- two distinct upward states determine the unique forced third, and the three upward states exhaust the local phase-3 surface;
- the acted/void-blocked rule supplies a local stopping condition once that surface is exhausted;
- realized construction authority remains separate from imaginary traversal and requires a sound actual-map instantiation;
- Reidemeister-style staging and uncrossing machinery are present in the Four Color research lane as representation-changing witnesses around the construction strategy.

The commits immediately preceding the frozen base include the explicit proof-frontier reduction and phase-3 constraint-collapse witnesses.

## Status discipline

This snapshot records a research frontier. It does **not**, merely by being timestamped or archived, assert that a complete proof of the Four Color Theorem has been established.

In particular, any global realization, projection, geometric, construction, or other proof obligation that remained open or explicitly separated at the frozen base commit remains an obligation here.

Later work may close, revise, refute, or reframe parts of this program. Such later work should cite this snapshot rather than altering the historical claim about what existed on 31 August 2026.

## Priority semantics

For priority questions, the authoritative technical record is the Git history rooted at the frozen base commit, including its ancestors. This note exists to identify that record in human-readable form.

A later archival release or DOI should preserve this commit ancestry and identify the frozen base commit explicitly.
