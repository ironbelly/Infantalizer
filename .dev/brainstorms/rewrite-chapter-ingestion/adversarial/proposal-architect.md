# Proposal A — Manifest-Authoritative Iteration Domain (architect lens)

> Archived verbatim from the architect-lens agent (opus). Variant A of 3.

## 1. One-paragraph thesis

The chapter set is the rewrite phase's **iteration domain**, and `chapter-manifest.yaml` is already (per prep §15) the authoritative descriptor of that domain — so rewrite must read it as a first-class 4th entry in `rewrite_phase_reads`, not re-derive the chapter set by filename convention. This single decision buys three things convention-discovery structurally cannot: (1) drift detection via `output_sha256`, (2) a single source of truth for order/title/provenance/confidence that prep already paid to compute, and (3) an extension channel for future per-chapter metadata. The manifest is consumed by a new NATIVE skill `chapter-ingest` attached additively to `muse`; the existing 11-step per-chapter workflow, inner-loop tier fan-out, and chronicler-as-sole-canon-writer contract are all preserved unchanged. A documented compatibility shim degrades to convention-discovery only when no manifest exists (the narnia 4-of-17 reality today).

## 2. RQ1 resolution (the crux) — manifest joins `rewrite_phase_reads` as the 4th entry

**Choice: `rewrite_phase_reads` gains a 4th entry — `source/<slug>/chapter-manifest.yaml`.**

```
work/prep/<slug>/30-mapping.yaml
work/prep/<slug>/40-prep-brief.md
work/prep/<slug>/10-challenges.yaml
source/<slug>/chapter-manifest.yaml       # NEW — iteration-domain descriptor
```

**Why this overrides prep §12's stated default.** prep §12's default was reasoned when the manifest was *hypothetical*. prep-v-next §5 now makes it **real and authoritative**, and prep §15 explicitly defers the read-set decision to this spec. Three architect arguments defeat the default:

**Argument 1 — an authoritative artifact the consuming phase ignores is dead documentation that rots.** prep produces `order`, `title`, confidences, `provenance`, `normalization_events`, `needs_human_review` per chapter, plus `chapter_count`, `review.status`, `ambiguous_splits`. Under convention-discovery none are consumed — the manifest becomes write-only and drifts from reality silently.

**Argument 2 — convention-discovery creates two sources of truth for the chapter set.** prep computed canonical order/titles/confidence via a 5-signal evidence process. Convention-discovery forces rewrite to re-derive a weaker set from filenames, losing provenance/confidence and silently re-implementing prep's natural-sort + count logic. Two paths producing "the chapter set" diverge.

**Argument 3 — drift detection and extension scaffolding are only reachable through the manifest.** `output_sha256` enables source-drift detection; `chapter_count` enables partial-set detection; `needs_human_review` enables per-chapter review gating. These are integrity properties convention-discovery cannot provide.

**Compatibility shim (E4 reality).** narnia has no manifest yet. `chapter-ingest` reads the manifest when present; when absent degrades to convention-discovery (glob `ch-*.txt`, natural-sort) + a one-line NOTICE that the run lacks drift protection. The shim is a migration bridge, visibly temporary.

## 3. RQ2 — inline at step 1 (no pre-rewrite stage)

The `analyst` already runs once per chapter (tier-invariant), takes `source_path`, ABORTs on NO-ACCESS, writes `work/analysis/ch-<NN>.yaml`. A separate pre-rewrite analysis stage adds an orchestration boundary for zero gain (no cross-chapter analysis dependency). Inline.

## 4. RQ3 — selection + resume via filesystem done-markers (no state file)

Selection: `--chapter N` / `--chapters 1-5` / `--chapters 1,3,5` / omitted = all. Natural sort always.

Resume (pure read, ADR-006-clean): the chronicler accept-triple
(`kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/{adapted.md,canon-delta.md,analysis.yaml}`) is the
definitive DONE marker per (work,tier,chapter). DONE iff triple exists for **all** requested tiers.
In-flight = partial; not-started = no analysis. Glob+Read walk, no state file. Idempotency is a free
consequence.

## 5. RQ4 — drift / PENDING / partial set

1. **Hash mismatch** → HALT that chapter with surfaced diff; operator accepts-risk (transcript) or re-preps. Per-chapter, not run-level.
2. **`review.status: PENDING`** → HALT the whole run. Distinct from greenlight (decisions) vs manifest (integrity).
3. **Partial set** → runnable set = intersection of manifest ∩ existing files. Missing chapters surfaced as WARNING, not halt. `--chapter 9` against 4 files HALTs (explicitly requested missing).

## 6. RQ5 — `--work` only + selection; two distinct guards

```
/laf:rewrite --work <slug> [--chapter N | --chapters 1-5 | --chapters 1,3,5] [--tiers 1,3,5]
```

No `--source`/`--manifest` overrides (single source of truth). Two guards: greenlight (decisions) + manifest (integrity: `review.status: CONFIRMED` + hash check).

## 7-13. (pipeline diagram, BOM, resume story, ACs, risks, rejections)

New NATIVE skill `chapter-ingest` + `resources/drift-rules.yaml`; +1 `skills:` line on `muse` (NATIVE) + one procedure paragraph; path-contract §4 +4th entry + §2 note; `.claude/commands/laf/rewrite.md` +flags; VENDOR.md +1 NATIVE row. Zero adopted-body edits; `check_boundary.py` Mode V green by construction. Tier fan-out stays inner loop (E2). Rejected: convention-discovery (write-only manifest / two sources of truth / no drift detection); pre-rewrite stage; path overrides.
