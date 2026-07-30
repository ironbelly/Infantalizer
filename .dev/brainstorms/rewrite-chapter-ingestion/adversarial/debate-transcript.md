# Debate Transcript — RQ1 Crux + Strictness Gradient

> Step 2 of the adversarial pipeline. Steelman debate: each position is argued at full strength, then
> rebutted. Depth: deep. Convergence threshold: 0.75.

## Round 1 — Steelmen

### Steelman for the 4th-entry position (A+B, argued at full strength)

The manifest is **the authoritative descriptor of the chapter set** — prep paid a 5-signal evidence process to
compute order, titles, split/order confidence, provenance, normalization events, and a per-chapter hash.
`rewrite_phase_reads` is the *enumerated, hardcoded, frozen set of files rewrite consumes as input.* The manifest
is precisely such an input. Three independent reasons force it in:

1. **A real authoritative artifact that its sole consumer ignores is dead documentation.** Under
   convention-discovery, every manifest field except `file` is write-only — prep emits it, nothing reads it,
   it drifts from reality. (architect Arg 1.)
2. **Convention-discovery creates two sources of truth** for the same concept (prep's manifest vs rewrite's
   glob), and two code paths producing "the chapter set" will diverge — a prologue sorted as ch-00 by one and
   attached to ch-01 by the other. (architect Arg 2.)
3. **Integrity properties are only reachable through the manifest.** Source-drift detection (`output_sha256`),
   partial-set detection (`chapter_count`), per-chapter review gating (`needs_human_review`). The analyzer adds
   the decisive framing: `chronicler`'s per-tier `continuity.md` is **cumulative state across chapters**, so a
   silent source error at chapter N compounds and surfaces chapters later as an unattributable `disclosure_leak`
   or `meaning_diff`. prep §12's default was written *without weighing canon cumativity* — rational for a
   stateless rewrite, unsafe where rewrite writes cumulative canon. (analyzer core.)

**The C5 bar is met:** the justification is concrete (the three silent-corruption → loud-halt conversions), and
unachievable by convention-discovery. This is not "convenience"; it is correctness.

### Steelman for the frozen-with-NOTE position (C, argued at full strength)

`rewrite_phase_reads` is defined in path-contract §4 as a list of **prep-package files** — files physically under
`work/prep/<slug>/`. The manifest lives at `source/<slug>/chapter-manifest.yaml`. These are **different
categories** of input: work-level prep context vs source-side enumeration. The analyst already reads
`source/<slug>/ch-NN.txt` at step 1, today, and nobody counts that against the frozen read-set — because
`source/` reads are a separate surface. C concedes **the manifest must be read** (S5 drift requires it) and
disputes only *where it's declared*. Adding it to `rewrite_phase_reads` is a **category error**: it would imply
the manifest is a prep-package member (it isn't) and create a new hash-pinning expectation on a source-side file
(check_boundary.py scope creep, against ADR-006's spirit). A §4 NOTE — "the manifest + chapter files are the
source-enumeration read surface, consumed by chapter-iterate, not prep-package members" — resolves the seam
without touching the frozen contract. **Smallest moving part, and honest about provenance.**

C's secondary point: the 4th entry is *additive*, so if a later decision wants hash-pinning, it can be added on
top. Starting frozen is the reversible default.

## Round 2 — Rebuttals

### Rebut C (from the 4th-entry camp)

C's category distinction is **correct as provenance** but **insufficient as a contract.** The freeze's *purpose*
is not "list of files under work/prep/" — it is "the enumerated, minimal, hardcoded set of inputs rewrite
depends on, so that a change to the input contract is visible and reviewable." The manifest is *exactly that
kind of dependency*, regardless of which directory it lives in. The category error is actually C's: it treats the
freeze as a *location index* when it functions as a *dependency contract*. A §4 NOTE that says "rewrite also
reads the manifest" without listing it in the read-set is the worst of both worlds — it documents a real
dependency as an informal aside, invisible to any tooling that reads `rewrite_phase_reads` as the dependency
list. (Concretely: which file does a maintainer edit to know "what does rewrite read"? They read §4. A NOTE they
might skim is a weaker contract than a list entry.)

Moreover, C's "source-side reads are already a separate surface" claim is **not symmetric**: the analyst reads
*one chapter at a time* (an unbounded, per-iteration read). The manifest is a **fixed, single, structural input**
— the chapter set itself. It is not analogous to a per-chapter source read; it is analogous to `30-mapping.yaml`
(a single fixed structural input). Fixed structural inputs belong in the read-set.

### Rebut the 4th-entry camp (from C)

The rebuttal's "location index vs dependency contract" reframing is fair, but it **proves too much.** If the
freeze's purpose is "the enumerated set of structural inputs," then by parity the per-chapter `ch-NN.txt` files
are *also* structural inputs — yet A, B, and C all agree those stay out of `rewrite_phase_reads` (correctly,
because they're source-side and unbounded). So the freeze already tolerates structural inputs outside the list
when they're source-side. The manifest is source-side. The distinction C draws is not contrived — it's the same
distinction the existing read-set already applies to every `ch-NN.txt`.

And the "a maintainer reads §4 to know dependencies" argument cuts both ways: a §4 NOTE *is* in §4. If §4 says
"rewrite reads these 3 prep files [list]; the source-side manifest and chapter files are enumerated by
chapter-iterate [note]," the maintainer has the complete picture. The information is not hidden; it is
*categorized*. The 4th entry buys no discoverability a NOTE doesn't already provide.

## Round 3 — Resolution probe (convergence)

The camps agree on **every operational consequence**: the manifest is read; drift/partial/PENDING are detected;
analyst is inline; resume is filesystem-derived; tier fan-out is inner-loop. The *only* remaining disagreement is
whether the manifest is listed in `rewrite_phase_reads` or noted in §4 as a separate source-side surface.

Two convergence observations:

1. **C's deepest concern is real and must be honored:** a 4th entry that implies "the manifest is a prep-package
   file" would be a provenance lie, and would create a check_boundary.py hash-pinning expectation the
   source-side location was designed to avoid. Any 4th-entry resolution must therefore (a) live in a *sub-list*
   or *clearly-labeled category* that distinguishes prep-package members from source-side inputs, and (b) carry
   an explicit note that the manifest is **not** hash-pinned by Rule F (it's outside the glob), so check_boundary
   behavior is unchanged. That neutralizes C's scope-creep objection.

2. **A/B's deepest concern is real and must be honored:** a NOTE that leaves the manifest out of the enumerated
   read-set under-states a genuine dependency. The merge should list the manifest as a structural input *and*
   categorize it as source-side, satisfying both the discoverability (A/B) and provenance-accuracy (C) demands.

**Convergent resolution (this is the merge seam):** §4 becomes two labeled groups — **(a) prep-package reads**
(the frozen 3, byte-unchanged) and **(b) source-side enumeration reads** (`chapter-manifest.yaml` + the
`ch-<NN>.txt` set, consumed by the new chapter driver skill). The manifest is a declared structural input
(A/B satisfied) that is explicitly *not* a prep-package member and *not* Rule-F hash-pinned (C satisfied). This
is not a compromise that weakens either side — it is the contract making explicit a distinction (prep-package
vs source-side) that was always true but only informal.

## Round 4 — Strictness gradient adjudication (Axis 2)

With RQ1 resolved, pick a point on the drift-strictness gradient (B strictest → A → C most permissive):

- **Adopt B's uncertainty-propagation as the unifying mechanism.** B's key insight — that a missing manifest or
  accepted drift should **force `analyst` to PARTIAL access (facts ≤ PROBABLE), propagating visible lower
  confidence** rather than silently proceeding — is strictly better than C's silent convention-fallback and
  A's NOTICE-only degrade. It converts "no manifest" from a silent-fallback into a *loud, confidence-tagged*
  degrade without halting the pilot. This honors the analyzer's core principle (loud > silent) **and** C's
  operational requirement (the pilot must run today).
- **Soften B's D3 hard-halt on partial sets to A/C's intersection-with-warning by default**, but keep B's
  `scope: partial (4 of 17)` stamping downstream. narnia's 4-of-17 is the live pilot; a hard halt unless
  `--chapters 1-4` is passed would block day-one use for a scope decision that is the operator's to make.
  Compromise: **WARN + intersect by default; HALT only when the operator explicitly requests a chapter that the
  manifest declares but is absent on disk** (so `--chapter 9` on 4 files halts, but bare `/laf:rewrite` warns and
  runs what exists). Best of A (warn) and B (the explicit-request-halts rule), keeping C's runnability.
- **Adopt B's formal three-way AND done-predicate + false-positive analysis**, including the T4/T5-safety-SKIP
  discovery (do NOT require a t5 safety report as a done-marker). This is the most rigorous and the only variant
  that validated against the live filesystem.
- **Keep C's minimal command surface as the default**, grafting B's accept-flags as *optional escape hatches*
  (not required for normal runs). Normal use: `--work <slug> [--chapter N | --chapters range]`. Escape:
  `--allow-no-manifest`, `--accept-source-drift ch-NN`, `--accept-review-flag ch-NN`, `--force`. This satisfies
  C's "smallest defensible thing" for the common case while preserving B's auditable, per-chapter escape valves.
- **Adopt the loop-entry pre-flight (A+B) as a cheap set-wide existence check** before the chapter loop, with
  the analyst's Phase-0 NO-ACCESS remaining the authoritative per-chapter gate. (C's redundancy objection is
  overruled: the pre-flight gives a zero-draft-written abort on a missing file, strictly better UX and cheaper
  than discovering it mid-pipeline.)

## Convergence score

- RQ1: resolved via two-group read-set (convergent seam). Both camps' core demand honored.
- RQ2-RQ6: consensus from Round 0, with B's rigor (uncertainty-propagation, AND-predicate, T4/T5 fix) grafted.
- No irreconcilable differences remain. **Convergence ≈ 0.86** (> 0.75 threshold). **PASS.**
