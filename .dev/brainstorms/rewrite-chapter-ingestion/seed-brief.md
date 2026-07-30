---
topic: "Next version of /laf:rewrite that ingests the individual per-chapter source files and chapter-manifest.yaml produced by /laf:prep v-next, and drives per-chapter adaptation across chapters 1..N"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-07-09T00:45:07+00:00
---

# Seed Brief: rewrite-chapter-ingestion

## Problem Statement

Today `/laf:rewrite --work <slug>` reads only the work-level prep package and **implicitly locates chapter
text by convention** — there is no formal chapter-set input. The command hands chapter 1 to `muse`; chapters
2..N re-read the same work-level package, but nothing enumerates the chapter set, its order, its provenance, or
its integrity. Now that prep-v-next (see upstream `merged-requirements.md`) materializes a canonical
`source/<slug>/ch-<NN>.txt` set plus a first-class, confidence-tagged `source/<slug>/chapter-manifest.yaml`
sidecar, the rewrite command must ingest **individual chapter files** as first-class input and drive the
per-chapter 11-step workflow across chapters 1..N **from that manifest** — while honoring every LAF
constraint (no new script/runtime, no adopted-body edit, `check_boundary.py` green, tier axis first-class,
`chronicler` is the only canon writer in the rewrite phase). The open question that the prior spec
deliberately deferred — whether the frozen `rewrite_phase_reads` set gains a manifest entry or stays frozen
— is the load-bearing decision this brainstorm must resolve.

## Known Context

- **Upstream artifact (MUST-read, already consumed):** the prep-v-next `merged-requirements.md` emits
  `source/<slug>/ch-<NN>.txt` + `source/<slug>/chapter-manifest.yaml`. The manifest carries, per chapter:
  `id`, `order`, `title`, `title_confidence`, `file`, `output_sha256`, `provenance`, `split_confidence`,
  `order_confidence`, `normalization_events`, `needs_human_review`. It also carries `chapter_count`,
  `review.status ∈ {PENDING, CONFIRMED}`, `mode_confidence`, and `ambiguous_splits`.
- **The deferred seam (prep spec §15):** "The manifest is authoritative for the chapter set but is **not**
  in `rewrite_phase_reads`. Whether the rewrite phase should read it (justifying a 4th read-entry) or
  discover chapters purely by convention is **the** seam between this spec and the next." (RQ1 here.)
- **Current rewrite contract (`rewrite.md`):** hardcoded read-set = exactly `[30-mapping.yaml,
  40-prep-brief.md, 10-challenges.yaml]`; confirms `50-greenlight.md: CONFIRMED` before handing to `muse`;
  multi-chapter scope is "begin chapter 1, chapters 2..N re-read the same prep package" — no chapter set,
  no resume state, no per-chapter selection.
- **Frozen read-set (`path-contract.md §4 rewrite_phase_reads`):** the three files above are the **hardcoded**
  read-set. The prep spec's §12 delta explicitly anticipated: *"chapter-manifest.yaml is a source/ sidecar,
  deliberately NOT in rewrite_phase_reads; the rewrite phase discovers chapters by the source/<slug>/ch-<NN>.txt
  convention."* — i.e. the prep author's **default** was convention-discovery, manifest-audit-only. This is
  one defensible resolution of RQ1; a 4th-entry resolution is also defensible and must be argued.
- **`analyst` is tier-invariant and runs once per chapter** (`granularity=chapter` default): it reads a
  `source_path` → `source/<work>/ch-<NN>.txt`, ABORTs on NO-ACCESS, and writes `work/analysis/ch-<NN>.yaml`.
  Per-chapter analysis was **deferred out of prep** (prep spec N1) — the rewrite phase is where it would
  naturally live. (RQ2.)
- **The per-chapter 11-step workflow** (step-numbering per `tier-coordinator.md`/`chronicler.md` pointer):
  `analyst → muse → writer → critic → editor → writer → continuity-checker → safety-verifier → reader-sim →
  tier-coordinator → chronicler`. `tier-coordinator` fans one chapter across a `tiers ⊆ {1,2,3,5}` set
  (parallel default; sequential fallback for state-heavy works), reconciles, and only on `status: RECONCILED`
  does `chronicler` run **per tier**, writing canon keyed `(work, tier, chapter)`. (RQ3, RQ6.)
- **`chronicler` is the only canon writer in the rewrite phase** (`path-contract.md §5`); it runs only on
  muse-accept, only per tier, only after RECONCILED. `source/` is read-only-after-materialize.
- **ADR-006 (framework not software):** exactly one script, `scripts/check_boundary.py`, a **validator not a
  runtime**. Native knowledge enters adopted agents **only** via additive `skills:` frontmatter; adopted
  bodies are never edited (the boundary contract, Mode V green).
- **Existing reality:** `source/narnia/ch-01..04.txt` exist (partial set, 4 of 17 chapters); no
  `chapter-manifest.yaml` exists yet (prep-v-next is a spec, not yet run). `work/prep/narnia/` — the live
  pilots show T1 already running; `work/analysis/ch-01.yaml`, `work/critique-reports/`, `work/safety-reports/`
  exist (per git status).
- **Provenance of new knowledge:** `muse` and `prep-cordinator` are NATIVE (`laf_sha256 = —`), so body edits
  there are boundary-clean. `rewrite.md` is a NATIVE command mirror. A new NATIVE skill is the cleanest
  insertion point for chapter-iteration logic (mirrors prep-v-next's `chapter-materialize` approach).

## Constraints

- **C1 (ADR-006):** framework not software; **no second script, no runtime, no CLI**. All chapter-iteration,
  resume, and drift logic is expressed as prompt + YAML, executed by the model. `check_boundary.py` stays the
  sole script and a validator only.
- **C2 (boundary contract):** **no adopted-body edits.** New knowledge enters only via NATIVE skills and/or
  additive `skills:` frontmatter on `muse`/`prep-cordinator` (both NATIVE, boundary-clean). Adopted agents
  (`writer` is the only ADOPTED-PATCHED) are untouched. `check_boundary.py` (Mode V) must stay green.
- **C3 (source/ read-only):** `source/<slug>/ch-<NN>.txt` and `chapter-manifest.yaml` are **read** by
  rewrite, never written by it. `chronicler` is the only rewrite-phase canon writer; the rewrite phase never
  writes to `source/`.
- **C4 (tier axis first-class):** `active_tier` is explicit for `safety-verifier`/`chronicler`;
  `tier-coordinator` fans a `tiers` set ⊆ {1,2,3,5}; `analyst` is tier-invariant. T4 interpolated on demand,
  never stored.
- **C5 (frozen read-set — the crux):** `rewrite_phase_reads` is currently frozen at 3 files. Any change to it
  (RQ1) requires an **explicit justification** that survives prep spec §12's stated default
  (convention-discovery, manifest-audit-only). Touching vs. not touching the frozen contract is itself a
  decision each proposal must make and defend.
- **C6 (prefer extension over new surface):** prefer extending `muse` + the existing per-chapter 11-step
  workflow over introducing new commands or agents. A new NATIVE skill (e.g. a rewrite-phase analog to
  `chapter-materialize`) is the expected insertion point.
- **C7 (greenlight gate retained):** the existing `50-greenlight.md: CONFIRMED` guard stays. Manifest
  integrity / drift handling is an **additional** gate, not a replacement.

## Success Criteria

- **S1.** `/laf:rewrite --work <slug>` ingests the prep-v-next chapter set + `chapter-manifest.yaml` and
  drives per-chapter adaptation for chapters 1..N (or a selected range) from the manifest, not by bare
  convention.
- **S2.** An **explicit, defended resolution of RQ1** — either the manifest joins `rewrite_phase_reads` as a
  4th entry with justification, or the read-set stays frozen and the manifest is consumed another way
  (convention-discovery + audit-only), with the chosen path justified against prep spec §12's default.
- **S3.** An **explicit per-chapter analysis decision (RQ2)** — whether/where per-chapter `analyst` passes
  run (a pre-rewrite analysis stage per chapter, or inline in `muse`'s 11-step workflow), keyed
  `(work, chapter)` and canon-keyed `(work, tier, chapter)`.
- **S4.** A **clear chapter-selection + resume story (RQ3)** — `--chapter N` / `--chapters 1-5` / all-by-default;
  idempotency across multi-chapter runs (which chapters done vs. in-flight); interaction with `chronicler`'s
  per-`(work,tier,chapter)` state.
- **S5.** **Manifest-drift handling (RQ4)** — defined behavior on hash mismatch vs `output_sha256`,
  `review.status: PENDING`, partial chapter set.
- **S6.** A **defined command surface (RQ5)** — `--work <slug>` only, or `--source`/`--manifest` overrides;
  manifest guard added alongside the existing greenlight guard.
- **S7.** **Zero adopted-body edits; `check_boundary.py` green; one script; tier fan-out and per-(chapter,
  tier) safety gate placed explicitly relative to chapter iteration (RQ6).**

## Open Questions (the proposals MUST diverge on and resolve — these are the adversarial debate seeds)

- **RQ1 — Read-set change (load-bearing, frozen-contract):** Does `rewrite_phase_reads` gain a 4th entry
  (`chapter-manifest.yaml`), or does rewrite discover chapters by the `source/<slug>/ch-<NN>.txt` convention
  with the manifest as audit-only? The prep spec §12 default was convention-discovery. Each proposal must
  pick one and **explicitly justify touching/not-touching the frozen contract.**
- **RQ2 — Per-chapter analysis granularity:** Does rewrite now run per-chapter `analyst` passes (deferred
  from prep N1)? If so, where — a **pre-rewrite analysis stage** per chapter (before `muse`), or **inline**
  in `muse`'s 11-step workflow (step 1 `analyst` already exists)? Keyed `(work, chapter)`; canon
  `(work, tier, chapter)`.
- **RQ3 — Chapter selection & range:** `--chapter N`, `--chapters 1-5`, all-by-default? Resume/idempotency
  across a multi-chapter run — which chapters are done, which in-flight? Interaction with `chronicler`'s
  per-`(work,tier,chapter)` state (and the existing `work/analysis/ch-<NN>.yaml`,
  `work/safety-reports/ch-<NN>-t<N>.md` artifacts as done-markers).
- **RQ4 — Manifest trust & drift:** On hash mismatch vs `chapter-manifest.yaml.output_sha256` (chapter file
  changed since prep): halt, re-verify, or re-prep? Behavior on `review.status: PENDING` (un-greenlit
  manifest) or a partial chapter set (narnia's 4-of-17 reality)?
- **RQ5 — Command surface:** `--work <slug>` only (discover manifest), or add `--source`/`--manifest`
  overrides? Keep the existing greenlight guard and **add** a manifest guard, or fold manifest integrity into
  the greenlight gate?
- **RQ6 — Boundary/tier fidelity:** Where does per-chapter tier fan-out (`tier-coordinator` across {1,2,3,5})
  sit relative to chapter iteration — is it inner-loop (per chapter, fan tiers) or outer (per tier, iterate
  chapters)? Does the safety gate (`safety-verifier`) run per `(chapter, tier)` (it does today — confirm and
  preserve)? All new knowledge stays in NATIVE skills / `muse` frontmatter — no adopted-body edit.

## Enrichment Context

See `enrichment/codebase-context.md` (primary tier, Auggie + native Glob/Read). Key findings that constrain
all three proposals:

- **E2/E6 — tier fan-out is already the INNER loop** (one chapter → tiers → chronicler-per-tier). The new
  design must make the **outer chapter loop** manifest-driven; do **not** invert the axis. `analyst` already
  runs once per chapter at step 1, so RQ2's "inline in muse workflow" path is near-free; a separate
  pre-rewrite analysis stage is the alternative.
- **E3 — resume/done-state is already filesystem-derivable** (chronicler's accept-triple
  `adapted.md`+`canon-delta.md`+`analysis.yaml` under `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/` = the
  definitive per-(chapter,tier) DONE marker; `work/analysis/ch-<NN>.yaml` = analysis done;
  `ch-<NN>-cross-tier.md` = reconciled). **No new state file needed** — ADR-006-friendly.
- **E4 — no manifest exists yet; narnia is a 4-of-17 partial set.** Rewrite-v-next must tolerate a missing
  manifest (degrade to convention-discovery) and a partial source set (manifest lists 17, only 4 files exist).
- **E5 — the frozen read-set is self-aware of this seam.** prep-v-next §12 already justified the default as
  convention-discovery + manifest-audit-only. A 4th-entry RQ1 resolution must beat that stated default with a
  concrete payoff convention-discovery cannot give (e.g. `output_sha256` drift, `chapter_count` completeness,
  per-chapter `needs_human_review`).
