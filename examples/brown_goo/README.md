# Brown Goo: a distinction-preservation micro-witness

This is a small **MeTTafy-original Lean witness**, not a historical proof exemplar and not part of the Four Color benchmark corpus.

It formalizes a deliberately silly phrase with a non-silly boundary condition:

> **Brown goo is collapse of a distinction that the representation still needs to support faithfully—either now, or under an admissible future continuation.**

The motivating shorthand is:

> **blob → boundary violation → semantic smearing → brown goo**

and the sharper epistemic gloss is:

> **Brown goo = lost distinction disguised as knowledge.**

The Lean theorem does **not** attempt to formalize `knowledge`, `bullshit`, intent, or aesthetic slop. It formalizes the transport conditions underneath that language.

## First-order Brown Goo

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

`ExactRecovery recover transport` says `recover` is a left inverse:

```text
recover (transport x) = x
```

for every source object `x`.

The first teethed theorem is:

```text
brownGoo_forbids_exactRecovery
```

In plain language:

> If two source objects that were required to remain distinguishable become the same target object, no exact decoder can recover every source object.

That is the irreversible part. Once the required distinction is actually gone from the transported representation, rhetoric cannot restore it.

## The pseudo-arbitrary loophole

Non-injectivity by itself is not automatically Brown Goo. Quotients, compression, abstraction, and projections may intentionally identify source objects.

But an **empty immediate contract is not enough to prove that a distinction was genuinely arbitrary**.

A distinction is genuinely arbitrary only relative to the future operations the representation is expected to support. The Lean witness therefore introduces a family of admissible continuations:

```text
contexts : (α → γ) → Prop
```

An admitted continuation can stand for a later observer, policy, action, provenance query, reward function, or a long second-/third-order causal chain summarized by its eventual observable result.

Two objects are contextually distinct when at least one admissible continuation gives different results:

```text
ContextuallyDistinct contexts x y
```

They are contextually arbitrary when **every** admissible continuation treats them identically:

```text
ContextuallyArbitrary contexts x y
```

The witness calls a pair **pseudo-arbitrary** when the immediate contract does not require the distinction, but an admissible continuation still distinguishes it.

That is the key correction:

> **A distinction is not arbitrary merely because the current layer does not care about it.**

If a later admissible behavior cares, the distinction is operationally real.

## The higher-order teeth

For an admissible continuation

```text
observe : α → γ
```

`FactorsThrough transport observe` means there is some downstream function

```text
downstream : β → γ
```

that reproduces `observe` exactly using only the transported representation:

```text
downstream (transport x) = observe x
```

for every source object.

Lean proves:

```text
contextualDifference_forbids_factorization
```

If `transport x = transport y` while `observe x ≠ observe y`, then `observe` cannot factor through `transport`.

And therefore:

```text
contextualBrownGoo_exhibits_unfactorable_context
```

> **Whenever a transport collapses a pair that some admissible future continuation can distinguish, at least one promised future behavior becomes impossible to reconstruct exactly from the transported state.**

This is the second-/third-order form of Brown Goo. The distinction may look irrelevant at the immediate boundary, yet become actual through later composition.

## Blob → goo, twice

The first concrete witness uses:

```text
BlobKind
├── binaryImage
├── text
└── receipt
```

and the bad transport

```text
smearBlobKind : BlobKind → Unit
```

which maps every kind to `()`.

Under a contract requiring different blob kinds to remain distinct, Lean proves this is ordinary first-order Brown Goo and that no exact recovery function exists.

The second witness deliberately gives `smearBlobKind` an **empty immediate contract**. First-order checking therefore accepts it as faithful.

Then we add a later admissible routing intent:

```text
routeBlob : BlobKind → Bool
```

which routes images differently from text.

Now image-vs-text is revealed as pseudo-arbitrary. Lean proves that the same total smear is `ContextualBrownGoo`, and that an admissible downstream routing behavior cannot factor through the smeared `Unit` representation.

So both statements are mechanically present at once:

```text
first-order empty contract:     accepted
future routing continuation:    impossible after collapse
```

That contrast is the point.

## Contemporary exemplar: statistical text watermarking

Ben Goertzel's August 17, 2026 essay [*The Folly of Statistically Watermarking LLM-Gen Text*](https://bengoertzel.substack.com/p/the-folly-of-statistically-watermarking) provides a useful contemporary motivation for the same distinction, without serving as proof evidence for this Lean witness.

A statistical watermark can be designed so that small lexical choices are intended to be nearly irrelevant to the text's ordinary semantic content while remaining deliberately observable to a detector. This means the same perturbation can be:

- arbitrary relative to a continuation family that asks only for semantic content or task capability; and
- non-arbitrary relative to a continuation family containing watermark detection, governance decisions, provenance inference, or later adversarial adaptation.

So "semantically incidental" does **not** imply "arbitrary in every admissible future context." The continuation family determines the claim.

Goertzel also emphasizes a separate distinction that matters here: a statistical detector may provide evidence about one generation path without recovering the full causal history of ideas, reasoning, or authorship. In Brown Goo terms, **detection signal, signed provenance, semantic content, and causal history are different objects and should not be silently flattened into one another.**

This example is intentionally documentary. The Lean theorems above stand or fall on their own checker-visible definitions and proofs.

## Why this belongs near MeTTafy

MeTTafy's architecture already depends on preserving distinctions across boundaries:

- raw structural evidence versus blind classifier input;
- observed structure versus semantic interpretation;
- verified fact versus model prediction;
- source provenance versus emitted representation;
- descriptive MeTTa atoms versus executable MeTTa;
- checker authority versus plausible explanation.

The contextual extension adds a harder requirement: a projection should not be called harmless merely because the **current** consumer cannot see what was erased. If an admissible later consumer, verifier, policy, or composition requires that distinction, the projection has already destroyed capability.

That is why this matters for semantic translation rather than only file handling.

## Checker boundary

The file uses Lean core only—no mathlib dependency—and is checked by the dedicated `Lean micro-witnesses` workflow against the exact version pinned in the repository's `lean-toolchain`.

The witness proves only the stated transport, factorization, and recoverability facts. It does not establish that every lossy abstraction is bad, that every possible future context should be admitted, or that the informal phrase "brown goo" has a unique philosophical meaning.

The scientifically important choice is therefore explicit:

> **What continuation family are we promising the representation will support?**

Once that family is declared, genuinely arbitrary and pseudo-arbitrary distinctions can be separated mechanically.
