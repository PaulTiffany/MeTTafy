# Brown Goo: a distinction-preservation micro-witness

This is a small **MeTTafy-original Lean witness**, not a historical proof exemplar and not part of the Four Color benchmark corpus.

It formalizes a deliberately silly phrase with a non-silly boundary condition:

> **Brown goo is undeclared collapse of a distinction the transport contract required us to preserve.**

The motivating shorthand is:

> **blob → boundary violation → semantic smearing → brown goo**

and the sharper epistemic gloss is:

> **Brown goo = lost distinction disguised as knowledge.**

The Lean theorem does **not** attempt to formalize `knowledge`, `bullshit`, or aesthetic slop. It formalizes the mechanical core underneath that language.

## The contract

A source type `α` carries a `DistinctionContract α`. The contract identifies pairs `x, y` that must remain distinguishable after transport.

For a transport

```text
transport : α → β
```

MeTTafy calls it faithful to the contract when every required pair remains unequal in `β`.

`BrownGoo contract transport` is an explicit collision witness:

```text
∃ x y,
  contract.Required x y
  ∧ transport x = transport y
```

So brown goo is **not the same thing as non-injectivity**.

A quotient, compression, abstraction, or projection may intentionally identify source objects. That can be honest if the declared transport contract does not promise to preserve the erased distinction. The failure is collapsing a distinction while still claiming a fidelity level that requires it.

## The teeth

`ExactRecovery recover transport` says `recover` is a left inverse:

```text
recover (transport x) = x
```

for every source object `x`.

The main theorem is:

```text
brownGoo_forbids_exactRecovery
```

In plain language:

> If two source objects that were required to remain distinguishable become the same target object, no exact decoder can recover every source object.

That is the irreversible part. Once the required distinction is actually gone from the transported representation, rhetoric cannot restore it.

## Why this belongs near MeTTafy

MeTTafy's architecture already depends on preserving distinctions across boundaries:

- raw structural evidence versus blind classifier input;
- observed structure versus semantic interpretation;
- verified fact versus model prediction;
- source provenance versus emitted representation;
- descriptive MeTTa atoms versus executable MeTTa;
- checker authority versus plausible explanation.

Flattening any distinction that the declared verification/audit contract still relies on is exactly the failure represented here.

The tiny `BlobKind` example makes the joke literal. `binaryImage`, `text`, and `receipt` are distinct at the boundary. `smearBlobKind` maps all of them to `Unit`. Lean proves that this witnessed collapse admits no exact recovery function.

## Checker boundary

The file uses Lean core only—no mathlib dependency—and is checked by the dedicated `Lean micro-witnesses` workflow against the exact version pinned in the repository's `lean-toolchain`.

The witness proves only the stated transport/recoverability facts. It does not establish that every lossy abstraction is bad, that every non-injective mapping is misleading, or that the informal phrase "brown goo" has a unique philosophical meaning.
