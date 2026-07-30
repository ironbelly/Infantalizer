---
topic: "Next version of /laf:rewrite — per-chapter source ingestion + manifest-driven adaptation across chapters 1..N"
domain: architecture
strategy: systematic
depth: deep
proposals: 3
models: [claude-opus-4-8, gpt-5.5, glm-5.2]
convergence_score: 0.86
adversarial_status: pass
merge_base: B (analyzer lens)
grafts: [C two-group read-set framing + minimal surface + provenance NOTE; A extension framing + per-chapter drift blast radius + partial-set WARN]
base_softened: [B D3 partial-set hard-halt → A/C WARN+intersect]
created: 2026-07-09T00:45:07+00:00
upstream: ".dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md"
---

# Merged Requirements — `/laf:rewrite` v-next: Manifest-Driven Per-Chapter Adaptation

## 1. Summary

`/laf:rewrite --work <slug>` becomes a **manifest-driven per-chapter driver**. The command ingests the
prep-v-next chapter set (`source/<slug>/ch-<NN>.txt`) plus its `source/<slug>/chapter-manifest.yaml` sidecar as
the **authoritative iteration domain**, enumerates the chapter set from the manifest, checks source integrity
against the manifest's frozen claims, and drives the existing per-chapter 11-step workflow across chapters 1..N
(or a selected range) — reusing the entire workflow unchanged, with **tier fan-out as the inner loop** and
`chronicler` as the sole canon writer. Resume is filesystem-derived from the chronicler accept-triple (no state
file). No new command, no new script/runtime, no adopted-body edit; `check_boundary.py` stays green.

The single load-bearing decision (RQ1) is resolved by making the **prep-package / source-side distinction
explicit in the read-set**: the frozen 3 prep-package reads stay byte-unchanged, and a clearly-labeled
**source-side enumeration** group names the manifest + chapter files as rewrite's chapter-set inputs (consumed by
a new NATIVE `chapter-iterate` skill on `muse`) — explicitly *not* Rule-F hash-pinned. This honors the
manifest's role as a structural dependency while preserving its source-side provenance. Drift and missing-manifest
cases degrade **loudly into propagated uncertainty** (analyst forced to PARTIAL; facts ≤ PROBABLE) rather than
silently into cumulative canon.

This spec is scoped to **rewrite-phase chapter ingestion + manifest trust + resume**. It consumes the prep-v-next
manifest but does not redefine it; per-chapter *production craft* (the 11-step workflow itself) is unchanged.

## 2. Goals & Non-Goals

**Goals**
- G1. `/laf:rewrite --work <slug>` enumerates the chapter set from the manifest (not by bare convention) and
  drives per-chapter adaptation for chapters 1..N (or a selected range).
- G2. An explicit, justified resolution of the frozen `rewrite_phase_reads` seam (RQ1) — manifest declared as a
  structural input, prep-package/source-side distinction made explicit, frozen-3 byte-unchanged.
- G3. A per-chapter analysis decision (RQ2) — inline at workflow step 1, reusing the existing tier-invariant
  analyst; no new stage.
- G4. A clear resume/idempotency story (RQ3) — filesystem-derived from the chronicler accept-triple, no state
  file; selection via `--chapter`/`--chapters`.
- G5. Manifest-drift handling (RQ4) — source-drift (D1), un-greenlit/needs-review (D2), partial set (D3) each
  with a defined detect→decide→act, defaulting to loud-degrade-with-uncertainty over silent fallback.
- G6. Preserve every hard contract: ADR-006 (one script, no runtime), zero adopted-body edits, `source/`
  read-only, `chronicler` sole canon writer, tier axis first-class, greenlight guard retained.

**Non-Goals**
- N1. No new command (`/laf:ingest` etc. rejected). No second script / parser binary / runtime (ADR-006).
- N2. No change to the per-chapter 11-step workflow or any adopted agent body. No new agent.
- N3. No rewrite of `chapter-manifest.yaml` (it is prep's artifact; rewrite reads it, never writes it).
- N4. No `--source`/`--manifest` path overrides (single source of truth; overrides invite unvetted source).
- N5. No persisted progress/state file (resume is filesystem-derived).

## 3. RQ1 resolution (the crux) — explicit two-group read-set

`path-contract.md §4 rewrite_phase_reads` is restructured into two labeled groups. The **frozen 3 prep-package
reads are byte-unchanged**; a new **source-side enumeration** group names the chapter-set inputs.

```
PREP-PACKAGE READS (frozen — byte-unchanged):
  work/prep/<slug>/30-mapping.yaml
  work/prep/<slug>/40-prep-brief.md
  work/prep/<slug>/10-challenges.yaml

SOURCE-SIDE ENUMERATION READS (the iteration domain, consumed by chapter-iterate at loop entry):
  source/<slug>/chapter-manifest.yaml   # the authoritative chapter-set descriptor
  source/<slug>/ch-<NN>.txt             # per-chapter source files (read inline at step 1 by the analyst)
```

**Justification (surviving prep §12's default — C5).** prep §12 anticipated: *"chapter-manifest.yaml is a
source/ sidecar, deliberately NOT in rewrite_phase_reads; the rewrite phase discovers chapters by the …
convention."* That default was reasoned when the manifest was hypothetical and **without weighing canon
cumativity**: `chronicler`'s per-tier `continuity.md` is running state across chapters, so a silent source error
at chapter N compounds and surfaces chapters later as an unattributable `disclosure_leak`/`meaning_diff`. The
manifest is the **only** artifact that can convert three silent-corruption modes into detectable halts:

- **source drift** → `output_sha256` comparison (impossible without the manifest);
- **partial set** → `chapter_count` vs files-on-disk;
- **un-greenlit/needs-review source** → `review.status` / `needs_human_review`.

Convention-discovery's failures are **silent and canon-corrupting**; reading the manifest makes them **loud,
named, recoverable**. That payoff clears C5's bar.

**Why two groups, not a flat 4th entry (the merge of the A/B and C positions).** A flat 4th entry would imply
the manifest is a *prep-package member* (a provenance lie) and would invite a `check_boundary.py` Rule-F
hash-pinning expectation on a source-side file (scope creep against ADR-006). Two labeled groups satisfy both
demands: the manifest is a **declared structural input** (discoverability — A/B) that is **explicitly not a
prep-package member and not Rule-F hash-pinned** (provenance accuracy — C). The frozen-3 are untouched; the
manifest joins a clearly-categorized source-side group. (From base-selection Round 3.)

**The §4 NOTE (provenance):** *"The source-side enumeration reads are the chapter-set inputs consumed by
`chapter-iterate`. They are not prep-package members and are not covered by the Rule-F hash-pin glob; their
integrity is verified at runtime (§5 D1-D3), not by `check_boundary.py`."*

## 4. RQ2 resolution — inline analyst at step 1; loop-entry pre-flight

Per-chapter source-fidelity analysis runs **inline at workflow step 1** of each chapter's pass — the existing
`analyst` agent (`granularity: chapter` default, tier-invariant, ABORT-on-NO-ACCESS, writes
`work/analysis/ch-<NN>.yaml`). Its contract is **unchanged**. No separate pre-rewrite analysis stage (it would
duplicate step 1, add orchestration boundary + state marker + resume edge case for zero output gain; rejected
unanimously by A, B, C).

A **loop-entry pre-flight** (cheap, set-wide) confirms each in-scope `source/<slug>/ch-NN.txt` **exists and is
non-empty** before the chapter loop body begins. Missing/empty → halt at chapter-set construction, zero drafts
written, zero canon touched. The analyst's Phase-0 NO-ACCESS ABORT remains the **authoritative** per-chapter
gate. (A+B graft; C's redundancy objection overruled: the pre-flight gives a zero-cost, zero-draft abort.)

## 5. RQ4 resolution — manifest trust & drift (detect → decide → act)

**Trust principle (B):** the manifest is **trusted as a claim, verified against filesystem reality at runtime.**
No manifest field is taken on faith for the chapters actually being adapted — each claim is re-checked at the
point of use. Zero-trust at the phase seam.

| Class | Detect | Decide | Act |
|---|---|---|---|
| **D1 — source drift** | at each chapter's loop entry, recompute `sha256(source/<slug>/ch-NN.txt)`, compare to `manifest.chapters[NN].output_sha256` | mismatch ⇒ source the prep package describes ≠ source about to enter canon | **HALT chapter C** before step 1 (named diff: expected vs actual). Accept per-chapter via `--accept-source-drift ch-NN` (recorded in `work/analysis/ch-NN.yaml.metadata`; analyst forced to PARTIAL; facts ≤ PROBABLE). Or re-prep. Never auto-proceed. |
| **D2 — un-greenlit / needs-review source** | read `manifest.review.status` + scan in-scope `chapters[].needs_human_review` at command entry, *after* greenlight, *before* the loop | PENDING manifest OR any in-scope `needs_human_review:true` ⇒ source set unratified | **HALT before the loop** (source-side gate, additional to greenlight per C7). Resolve in `/laf:prep` (manifest → CONFIRMED), or override per-chapter `--accept-review-flag ch-NN` (facts UNCERTAIN). |
| **D3 — partial set** | `len(Glob source/<slug>/ch-*.txt)` vs `manifest.chapter_count` | N < M ⇒ manifest promises more than source delivers | **Default (no `--chapter`/`--chapters`): WARN + intersect** (run manifest∩disk), stamp downstream artifacts `scope: partial (N of M)`. `--chapters 1-5` on 4 files → run 1-4, WARN ch-05 absent. `--chapter 9` on 4 files → **HALT** (explicit request of a missing chapter is not a silent skip). |

**Missing manifest (E4 reality — none exists today).** This is the merged resolution of the strictness gradient:
- **Default (no flag, no manifest): HALT** with "run `/laf:prep` or pass `--allow-no-manifest`." (Loud.)
- **`--allow-no-manifest`: loud degrade.** Convention-discover (`Glob ch-*.txt`, natural-sort) + one loud
  warning ("no manifest; source set unverified; D1/D2/D3 undetectable") + **force every `analyst` to PARTIAL
  access** (facts ≤ PROBABLE, never CERTAIN), so any uncertainty rides `/source-fidelity` into reconciliation as
  *visible* lower confidence — not a silent fallback into canon.

(The merge softens base B's D3 hard-halt to A/C's WARN+intersect by default — keeps the live 4-of-17 pilot
runnable — while preserving B's "explicit request of a missing chapter halts" rule.)

## 6. RQ3 resolution — selection + resume (no state file)

**Selection.**
```
/laf:rewrite --work <slug> [--chapter <N> | --chapters <range|list>] [--tiers <set>]
```
- `--chapter N` — single chapter.
- `--chapters 1-5` / `--chapters 1,3,5` — range/list (model-parsed, no runtime — ADR-006).
- `--tiers 1,3,5` — restrict the tier fan-out (default = work's full set from `30-mapping.yaml`/tier profiles;
  ⊆ {1,2,3,5}; T4 interpolated on demand). `--tiers` is load-bearing for resume: a run with `--tiers 1` against
  a chapter whose accept-triple exists only for tier 3 is NOT done.
- Default (no chapter flag) = all manifest chapters ∩ files-on-disk. Natural sort always (never lexicographic).

**Resume — pure read of the chronicler accept-triple (E3), no state file.** For each selected chapter, Glob the
done-markers and classify:

| State | Filesystem test | Action |
|---|---|---|
| **DONE per (chapter, tier)** | chronicler accept-triple complete: `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/{adapted.md, canon-delta.md, analysis.yaml}` | skip |
| **DONE-across-all-tiers** | DONE for every tier in the requested `tiers` set | skip chapter entirely |
| **In-flight** | some artifacts, triple incomplete | resume at earliest missing step (existing partial artifacts read, not clobbered) |
| **Not-started** | no `work/analysis/ch-<NN>.yaml` | full 11-step |

**Formal DONE predicate (B, with T4/T5 fix):**
```
DONE(work, C, T) :=
    exists(kb/adaptations/<work>/tier-<T>/chapters/ch-<C>/adapted.md)
  ∧ exists(kb/adaptations/<work>/tier-<T>/chapters/ch-<C>/canon-delta.md)
  ∧ exists(kb/adaptations/<work>/tier-<T>/chapters/ch-<C>/analysis.yaml)
```
Chapter DONE iff `DONE(work, C, T)` for every `T` in the requested set. The three-way AND (not one-of-three)
closes false-positives: a pre-accept `adapted.md` lacks siblings ⇒ NOT-DONE; a step-11 crash leaves a partial
triple ⇒ NOT-DONE; a stale `work/analysis` is never promoted ⇒ irrelevant to the predicate. **The predicate does
NOT require a T4/T5 safety report** — T4-T5 SKIP with `verdict: N/A` by design (`safety-verifier.md`); the triple
(not the safety report) is the unified DONE signal. (Validated against the live narnia tree: no
`ch-*-t5.md` exist, yet ch-01/ch-02 are correctly DONE.) `--force` re-runs DONE chapters (intentional override).

## 7. RQ5 resolution — command surface; two guards

```
/laf:rewrite --work <slug>
  [ --chapter <N> | --chapters <range|list> ]
  [ --tiers <set> ]
  [ --allow-no-manifest ]               # loud degrade; analyst→PARTIAL; facts ≤ PROBABLE
  [ --accept-source-drift <ch-list> ]   # per-chapter D1 accept; analyst→PARTIAL; facts ≤ PROBABLE
  [ --accept-review-flag <ch-list> ]    # per-chapter D2 accept; facts UNCERTAIN
  [ --force ]                           # ignore DONE predicate; re-run selected
```
- `--work <slug>` only. **No `--source`/`--manifest` path overrides** (invite unvetted source = reopen the
  silent-corruption surface D1-D3 close). Manifest is convention-discovered at `source/<slug>/chapter-manifest.yaml`.
- **Two guards, in order:** (1) greenlight — `work/prep/<slug>/50-greenlight.md: status: CONFIRMED` (retained,
  C7 — ratifies prep's *decisions*); (2) manifest — D2 (review.status + needs_human_review) + D3 (count vs disk)
  at entry, D1 (hash) per-chapter at loop entry (additional to greenlight — ratifies the *source set's integrity*).
- Accept flags are **per-chapter, auditable, never blanket** (a blanket `--accept-all-drift` is intentionally
  absent — it would recreate the silent-canon-corruption mode).

## 8. RQ6 resolution — tier fan-out inner loop; safety per (chapter, tier)

Confirmed and preserved (E2): **chapter = OUTER loop** (now manifest-driven); **tier fan-out = INNER loop**.
`analyst` tier-invariant (step 1, once per chapter). `safety-verifier` runs per (chapter, tier) at step 8 (T1-2
blocking, T3 advisory, T4-5 SKIP→N/A). `tier-coordinator.reconcile()` step 10 → RECONCILED | CONFLICT (Checks
A/B/C/D). On RECONCILED, `chronicler` runs **per tier** at step 11 (sole canon writer). On CONFLICT, `muse`
resolves (re-dispatch offending tier's writer) before any canon write. **Do not invert the axis.**

## 9. Pipeline diagram

```
/laf:rewrite --work <slug> [--chapter/--chapters] [--tiers] [escapes]
  │
  ▼
[G0 greenlight]  work/prep/<slug>/50-greenlight.md == CONFIRMED?  ── no → HALT (retained, C7)
  │
  ▼
[READ source-side enumeration group]  source/<slug>/chapter-manifest.yaml (+ ch-<NN>.txt at step 1)
  │  absent + no flag → HALT ("run /laf:prep or --allow-no-manifest")
  │  absent + --allow-no-manifest → LOUD DEGRADE: convention-discover + analyst→PARTIAL + facts ≤ PROBABLE
  │
  ▼
[G1 D2 — review]  manifest.review.status==CONFIRMED ∧ no in-scope needs_human_review?  ── no → HALT / --accept-review-flag
  │
  ▼
[BUILD chapter set]  selected = manifest.chapters ∩ (--chapter/--chapters) ∩ files-on-disk   (natural sort)
  │
  ▼
[G2 D3 — partial]  N < M?  → default WARN+intersect+stamp "scope: partial (N of M)"; explicit-missing-chapter → HALT
  │
  ▼
[PRE-FLIGHT]  each in-scope ch-NN.txt exists & non-empty?  ── no → HALT at construction (zero drafts)
  │
  ▼
[RESUME WALK]  for each (C,T): DONE(work,C,T)? (chronicler triple, three-way AND) → skip; else run; --force runs all
  │
  ▼
╔════════════ CHAPTER LOOP (OUTER, manifest-driven) ═════════════╗
║ for C in selected:                                             ║
║   [G3 D1 — drift]  sha256(ch-C.txt) == manifest.output_sha256? ║
║   │                              ── no → HALT ch-C / --accept-source-drift ch-C (→ PARTIAL)
║   ▼                                                            ║
║   analyst(source/<slug>/ch-C.txt)        # step 1 (tier-invariant; ABORT-on-NO-ACCESS authoritative)
║   muse → writer → critic → editor → writer → continuity-checker   # steps 2-7
║   ┌──────── TIER FAN-OUT (INNER, E2 — unchanged) ────────┐     ║
║   │ for T in tiers:                                      │     ║
║   │   safety-verifier(active_tier=T)   # step 8          │     ║
║   │     T1-2 blocking, T3 advisory, T4-5 SKIP (N/A)      │     ║
║   │   FAIL(T1-2) → writer revision loop (constraint #3)  │     ║
║   └──────────────────────────────────────────────────────┘     ║
║   reader-sim                                            # step 9
║   tier-coordinator.reconcile(C, tiers)                  # step 10 → RECONCILED | CONFLICT
║     CONFLICT → muse resolves before any canon write
║     RECONCILED → ↓                                          ║
║   for T in tiers: chronicler(work, C, T)                # step 11 — ONLY canon writer
║     writes kb/adaptations/<work>/tier-<T>/chapters/ch-<C>/{adapted.md,canon-delta.md,analysis.yaml}
║   ; chapter_state[C] = DONE (triple present)                ║
╚═══════════════════════════════════════════════════════════════╝
  │
  ▼
DONE — all selected chapters DONE across all selected tiers
```

## 10. Boundary-Contract Compliance & Bill of Materials

| File | Provenance | Change |
|---|---|---|
| `laf-adaptation/skills/chapter-iterate/SKILL.md` | **NEW NATIVE** | manifest-read, enumeration, pre-flight, drift checks (D1/D2/D3), selection parse, resume walk, chapter-loop procedure (rewrite-phase analog to prep's `chapter-materialize`) |
| `laf-adaptation/skills/chapter-iterate/resources/drift-rules.yaml` | NEW NATIVE | declarative D1/D2/D3 detect→decide→act table; `--accept-*` semantics; DONE-predicate map (data, not code) |
| `laf-adaptation/agents/muse.md` | NATIVE (`laf_sha256 = —`) | **+1 additive `skills:` line** (`- laf-adaptation:chapter-iterate`) + one chapter-iteration pointer paragraph (body-edit-clean; muse is NATIVE) |
| `laf-adaptation/skills/prep/resources/path-contract.md` | NATIVE | **§4 restructure into two groups** (frozen-3 prep-package reads byte-unchanged + new source-side enumeration group naming `chapter-manifest.yaml` + `ch-<NN>.txt`) + the §4 provenance NOTE (not Rule-F hash-pinned); §5 write-ownership **unchanged** (rewrite writes nothing new; chronicler owns canon) |
| `.claude/commands/laf/rewrite.md` | NATIVE mirror | +`--chapter`/`--chapters`/`--tiers`/`--allow-no-manifest`/`--accept-source-drift`/`--accept-review-flag`/`--force`; manifest guard + ordering note; `argument-hint` update |
| `laf-adaptation/VENDOR.md` | NATIVE | +1 NATIVE row for `chapter-iterate/SKILL.md` (Rule F manifestation; Rule E — no upstream collision) |

**Zero adopted-body edits.** The 10 ADOPTED-CLEAN agents + 12 ADOPTED skills untouched; `writer.md` (the sole
ADOPTED-PATCHED file) untouched. `check_boundary.py` (sole script, validator) untouched — the §4 restructure adds
the manifest to a source-side group explicitly **outside** the Rule-F hash-pin glob, so Mode V scope is unchanged.
`source/` read-only; `chronicler` sole canon writer. New skill clears Rule E (no upstream name collision) and Rule
F (manifested). **Mode V green by construction.** All new logic = prompt + YAML (ADR-006 / C1).

## 11. path-contract.md §4 Delta (diff-style)

```
  §4 rewrite_phase_reads (the hardcoded read-set)
-
- `/laf:rewrite --work <slug>` reads **exactly** these three files, by hardcoded path, no other arguments:
-   work/prep/<slug>/30-mapping.yaml
-   work/prep/<slug>/40-prep-brief.md
-   work/prep/<slug>/10-challenges.yaml
+ `/laf:rewrite --work <slug>` reads its inputs in two groups, by hardcoded path, no other arguments:
+
+   PREP-PACKAGE READS (frozen — byte-unchanged):
+     work/prep/<slug>/30-mapping.yaml
+     work/prep/<slug>/40-prep-brief.md
+     work/prep/<slug>/10-challenges.yaml
+
+   SOURCE-SIDE ENUMERATION READS (the chapter-set iteration domain, consumed by chapter-iterate at loop entry):
+     source/<slug>/chapter-manifest.yaml   # authoritative chapter-set descriptor (prep-v-next)
+     source/<slug>/ch-<NN>.txt             # per-chapter source (read inline at step 1 by the analyst)
+
+   NOTE (provenance): the source-side enumeration reads are NOT prep-package members and are NOT covered by
+   the Rule-F hash-pin glob; their integrity is verified at runtime (D1/D2/D3), not by check_boundary.py.
+   The frozen-3 prep-package reads are byte-unchanged. (Resolves prep spec §12/§15 deferred seam.)
```
```
  §5 write-ownership .................................. UNCHANGED (rewrite writes nothing new; chronicler owns canon)
```

## 12. Acceptance Criteria

- **AC1.** `/laf:rewrite --work <slug>` reads the two-group read-set (frozen-3 prep-package + source-side
  enumeration) and enumerates the chapter set *from the manifest* (`manifest.chapters[]` ∩ files-on-disk ∩
  selection), in manifest order (natural sort) — not by bare lexicographic glob.
- **AC2 (D1).** Editing `source/<slug>/ch-03.txt` after prep and running rewrite HALTs at chapter 3's loop entry
  with a named sha256 diff, having written nothing to `kb/`. `--accept-source-drift ch-03` proceeds with analyst
  forced to PARTIAL and ch-03 facts tagged ≤ PROBABLE in `work/analysis/ch-03.yaml`.
- **AC3 (D2).** A manifest with `review.status: PENDING` or an in-scope `needs_human_review: true` HALTs before
  the loop, even when `50-greenlight.md` is CONFIRMED (proves the manifest guard is additional, not folded).
- **AC4 (D3).** A manifest declaring `chapter_count: 17` against 4 files on disk: default run → WARN + intersect
  + downstream `scope: partial (4 of 17)`; `--chapters 1-5` → run 1-4 + WARN ch-05; `--chapter 9` → HALT.
- **AC5 (resume).** Re-running after ch-01/ch-02 completed across {1,2,3,5} skips them (logs "skipped DONE")
  and resumes at ch-03. Deleting one file of a chronicler accept-triple makes that chapter read NOT-DONE and
  re-run (proves the three-way AND). `--force` re-runs a DONE chapter.
- **AC6 (missing manifest).** No manifest + no flag → HALT ("run /laf:prep or --allow-no-manifest"). No manifest
  + `--allow-no-manifest` → proceeds with one loud warning, analyst forced to PARTIAL, all facts ≤ PROBABLE
  (verified in `work/analysis/ch-NN.yaml`).
- **AC7 (tier/safety fidelity).** Safety reports produced per (chapter, tier) for T1-T3 only; T4-T5 SKIP (N/A)
  and are NOT required by the DONE predicate. `chronicler` runs per tier only on RECONCILED. Tier fan-out is the
  inner loop.
- **AC8 (boundary).** `uv run python scripts/check_boundary.py` (Mode V) exits 0; no adopted body edited;
  `writer.md` byte-unchanged; one new NATIVE skill manifested; frozen-3 prep-package reads byte-unchanged; the
  §4 restructure is additive (new source-side group + NOTE), not a deletion.

## 13. Release-Blocking Risks (silent-failure-first)

1. **[SILENT] D1 implemented as cached/stale hash compare instead of fresh `sha256` recompute at loop entry.**
   Source drift enters canon silently — the exact failure this spec exists to prevent. *Mitigation:*
   `drift-rules.yaml` mandates a fresh recompute; AC2 tests a live edit.
2. **[SILENT] DONE predicate degraded to one-of-three (a lone `adapted.md` reads as DONE).** Would skip the
   safety gate and chronicler for that chapter. *Mitigation:* three-way AND; AC5's delete-one-sibling case.
3. **[SILENT] `--allow-no-manifest` failing to force analyst→PARTIAL.** The loud-degrade becomes a silent
   fallback. *Mitigation:* driver passes `access_hint=PARTIAL`; the analyst's observable-test honors a caller
   ceiling; AC6 asserts ≤ PROBABLE tags.
4. **[LOUD] Manifest schema drift between prep-v-next and this spec** (e.g. `output_sha256` vs `sha256`). Every
   run halts at G1. *Mitigation:* `drift-rules.yaml` keys off exact prep §5 field names; integration test runs
   prep then rewrite on the tolkien single-chapter fixture.
5. **[LOUD] Hash halt is coarse** (a trailing-newline normalization halts). *Mitigation:* coarse-but-safe;
   operator re-preps or accepts per-chapter. Documented as honest trade.
6. **[LOUD] Convention-fallback can mask a missing manifest** (drift detection unavailable). *Mitigation:* the
   degrade is surfaced as a loud warning + PARTIAL-forcing; the honest trade for running on today's 4-of-17.

## 14. Open Tensions (deferred)

- **T4 interpolated state.** If a run requests `--tiers 4`, the DONE predicate must treat T4 like any other tier
  (chronicler writes a `tier-4/` triple) — but T4 is interpolated on demand and "never stored as a file" (CLAUDE
  §3). Resolution: T4 is produced on demand for a run and its `tier-4/` artifacts *are* written for that run
  (the "never stored" rule concerns the *profile*, not per-chapter adaptation artifacts). Confirm against
  `adaptation-tiers` before implementation.
- **D2 vs greenlight ordering under partial acceptance.** `--accept-review-flag` is per-chapter, but D2's
  `review.status: PENDING` is manifest-wide. If the manifest is PENDING but the operator accepts flags for the
  in-scope chapters, should the run proceed? Default: yes (the per-chapter accept is the escape valve); confirm
  in `drift-rules.yaml`.

## Next Step

This spec materializes one NATIVE skill (`chapter-iterate`) + one additive `muse` line + a path-contract §4
restructure + a command-mirror update. Implement via `/sc:design @.dev/brainstorms/rewrite-chapter-ingestion/merged-requirements.md`
for the skill body, or `/sc:tasklist` for sprint planning, or `/sc:implement` for direct execution. Validate
boundary with `uv run python scripts/check_boundary.py` after every file touch.
