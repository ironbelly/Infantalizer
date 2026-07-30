# Codebase Enrichment — rewrite-chapter-ingestion

> Quality tier: **primary** (Auggie codebase-retrieval + native Glob/Read, clean). `--no-research`, so no
> research artifact. Source of truth: in-tree agent/skill/command bodies, cross-checked against live `work/`
> and `kb/adaptations/` filesystem state.

## E1. The current chapter loop is informal — there is no iteration driver

`rewrite.md` (lines 20-22): *"This command begins **chapter 1**; the existing per-chapter 11-step workflow
continues for chapters 2..N (each chapter re-reads the same prep package … by the hardcoded
`rewrite_phase_reads` paths)."* The 11-step workflow is **per-chapter** (one chapter flows
`analyst → muse → writer → critic → editor → writer → continuity-checker → safety-verifier → reader-sim →
tier-coordinator → chronicler`). There is **no enumerated chapter set, no chapter counter, no resume state**.
Chapters 2..N are produced by the operator re-invoking / re-aiming `muse` informally. **This is the gap the
new manifest ingestion must fill.** (Drives RQ3, RQ5.)

## E2. Tier fan-out is the INNER loop; chapter is the OUTER loop (preserve this)

`tier-coordinator.md`: *"You fan one source chapter across tiers"* and *"chronicler runs **per tier**,
each writing that tier's continuity/canon-delta keyed (work,tier,chapter)."* The structure is:

```
for chapter in chapter_set:                 # OUTER loop — currently informal
    analyst(source_path = source/<slug>/ch-NN.txt)        # step 1 (tier-invariant)
    muse → writer → critic → editor → writer → continuity-checker
    safety-verifier (per (chapter, tier))                  # step 8
    reader-sim                                             # step 9
    tier-coordinator.reconcile(chapter, tiers)             # step 10 → RECONCILED | CONFLICT
    if RECONCILED:
        for tier in tiers: chronicler(work, chapter, tier) # step 11 — ONLY canon writer
```

So per-chapter tier fan-out is already correct; the new design must make the **outer chapter loop**
manifest-driven, not add a second tier axis. (Resolves RQ6's structural part: tier fan-out sits **inside**
chapter iteration — do not invert.)

## E3. Resume / done-state is ALREADY derivable from the filesystem (ADR-006-friendly)

Live filesystem state (confirmed by `find`) gives unambiguous per-(chapter, tier) done-markers — **no new
state file is needed for resume**:

| State | Path (existence = done) |
|---|---|
| Per-chapter source analysis done | `work/analysis/ch-<NN>.yaml` (exists + `status: OK`) |
| Cross-tier reconciled | `work/analysis/ch-<NN>-cross-tier.md` (exists + `status: RECONCILED`) |
| Per-(chapter,tier) safety verdict | `work/safety-reports/ch-<NN>-t<N>.md` |
| Per-(chapter,tier) draft produced | `work/drafts/ch-<NN>-t<N>-v<M>.md` |
| **Per-(chapter,tier) ACCEPTED & canon-promoted** | `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/{adapted.md,canon-delta.md,analysis.yaml}` |

The chronicler's accept-promotion triple (`adapted.md` + `canon-delta.md` + `analysis.yaml` under one
`ch-<NN>/` dir) is the **definitive DONE marker** for `(work, tier, chapter)`. narnia confirms this is real:
ch-01 and ch-02 both have the full triple across tiers 1, 2, 3, 5. A resume walk can Glob these to compute
"done / in-flight / not-started" per chapter — pure read, no new writes, ADR-006-clean. (Drives RQ3 + RQ4.)

## E4. No manifest exists yet; the partial-set is the real test case

`find laf-adaptation -name '*manifest*'` → **empty**. `source/narnia/` holds only `ch-01.txt … ch-04.txt`
(**4 of 17 chapters** — LWW has 17). `source/tolkien/` holds `ch-01.txt` (single-chapter fixture). So:
- prep-v-next's manifest is **spec-only** today; rewrite-v-next must tolerate a **missing** manifest
  (graceful degrade to convention-discovery) and a **partial** manifest/chapter set (narnia's 4/17).
- The `--chapters 1-5` selection must intersect cleanly with a manifest that may list 17 but where only 4
  source files exist → that's an RQ4 drift/gap case (manifest promises more than source has). (Drives RQ4 + RQ5.)

## E5. Read-set is genuinely frozen and self-aware of this seam

`path-contract.md §4`: *"reads **exactly** these three files, by hardcoded path."* The prep-v-next spec §12
explicitly anticipated: *"chapter-manifest.yaml is a source/ sidecar, deliberately NOT in rewrite_phase_reads;
the rewrite phase discovers chapters by the source/<slug>/ch-<NN>.txt convention."* So the **default, already
justified** resolution of RQ1 is: **convention-discovery, manifest-as-audit-only, read-set stays frozen at 3**.
Any proposal that *adds a 4th entry* must overcome this stated default with a concrete payoff (e.g. needing
manifest fields like `output_sha256` for drift detection, `chapter_count` for completeness, or per-chapter
`needs_human_review`) that convention-discovery cannot provide. (Drives RQ1 — the crux.)

## E6. Provenance / boundary-clean insertion points (for the bill of materials)

- `muse` (NATIVE, `model: opus`, `laf_sha256 = —`) — body-edit-clean; already the orchestrator. Candidate for
  a +1 `skills:` line + a short chapter-iteration procedure paragraph. **Body untouched for adopted agents.**
- `analyst` (NATIVE) — already takes `granularity: chapter` and a `source_path`; **already runs once per
  chapter**. So RQ2's "inline in muse's workflow" path is nearly free: step 1 *is* the per-chapter analyst.
  A separate pre-rewrite analysis stage would just pre-batch step-1 across chapters.
- New NATIVE skill (analog to prep-v-next's `chapter-materialize`) — cleanest home for
  manifest-parse / chapter-enumerate / drift-check / resume-walk logic; attached to `muse` via one additive
  `skills:` line. Clears Rule E (no upstream collision) + Rule F (manifested in VENDOR.md).
- `.claude/commands/laf/rewrite.md` (NATIVE mirror) — gains `--chapter`/`--chapters` + manifest pointer.
- `path-contract.md` (NATIVE) — §4 note + §5 write-ownership unaffected (rewrite writes nothing new; chronicler owns canon).

No adopted body touched; `check_boundary.py` (Mode V) green by construction.
