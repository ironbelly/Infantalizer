# Phase Gate 2 — Fix-Applied Summary (Step PG2.5)

**Applied:** 2026-07-03 | **Fix agent:** rf-qa (single authorized fixer, fix_authorization: TRUE)
**Post-fix boundary:** `check_boundary.py` exit **0** (PASS, rules A–F)
**Carried-verbatim payload touched:** NONE (no `yaml` fences, no `kb/`, no `templates/`, no Mars keys)

All edits confined to the four authorized BUILD-NEW native bodies under
`/config/workspace/Infantalizer/laf-adaptation/`. E3 was placed in `tier-coordinator.md` (the
"tier-coordinator.md OR CLAUDE.md" option), so CLAUDE.md was NOT modified.

---

## Genuine build defects (D1–D4)

### D1 — children.md: full verbatim T3 Denethor quote (was truncated paraphrase)
**File:** `skills/adaptation-safety/resources/children.md`
**Edit:** Replaced the abbreviated stitched T3 quote (which dropped sentences and used `…` inside the
quote marks, reading as a false verbatim carry) with the FULL verbatim T3 passage read from
`prompts/transformation/tier_3_transform.md` (its "Example: Denethor Scene" worked example). The T3 line
now reads in full:
> "Denethor had given up hope. The palantír had shown him only darkness. When Faramir was carried in
> wounded, something broke inside him. Gandalf found him preparing a terrible thing. But Pippin was
> already running to find help. They pulled Faramir from danger just in time. Denethor was lost to his
> despair. But Faramir survived."

This is now a true verbatim quote (full-verbatim path chosen over the relabel-as-abridged fallback).

### D2 — children.md: corrected attribution (plural → single prompt)
**File:** `skills/adaptation-safety/resources/children.md`
**Edit:** Changed the worked-example attribution from "the Denethor scene, from the transform prompts"
(plural) to "the Denethor scene, from `prompts/transformation/tier_3_transform.md`'s T1→T3 worked
example". Both T1 and T3 halves of the Denethor example live in `tier_3_transform.md`; the T1 transform
prompt's own worked example is Éowyn, not Denethor.

### D3 — chronicler.md: added on-accept `analysis.yaml` promotion to write targets
**File:** `agents/chronicler.md`
**Edit:** Added `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/analysis.yaml — copy of
work/analysis/ch-<NN>.yaml, promoted ON ACCEPT` to the PER-TIER write-targets block, plus a prose note:
on accept the chronicler copies `work/analysis/ch-<NN>.yaml` (the `analysis_path` INPUT) into the
per-chapter dir, closing the previously-unowned promotion (kb-formats §4). The note clarifies `adapted.md`
is NOT a chronicler write — it is the provided `adapted_path` INPUT already at that path from the tier
pipeline; the chronicler only adds the sibling `analysis.yaml` (and `canon-delta.md`) alongside it.

### D4 — adaptation-safety/SKILL.md: aligned `next` with safety-verifier's deterministic F6 rule
**File:** `skills/adaptation-safety/SKILL.md`
**Edit:** Kept the carried aggregation formula `next = "revise" if overall == FAIL else "promote"`
intact, and appended an "Operational reading of `next`" note stating the authoritative deterministic
predicate matching `safety-verifier.md`: `next = revise` ONLY when (`mode == blocking` AND
`result == FAIL`); every other case → `promote`. Concretely: advisory (T3) → promote even on rubric FAIL;
skipped (T4-5) → promote; PASS (any mode) → promote. The two files now agree that a T3-advisory FAIL still
promotes (report-only). Additive annotation; the carried formula line was not deleted.

---

## Executability-gap operational-reading notes (E1–E3)

### E1 — tier-coordinator.md: grounded `maturity()`, `permitted_at`, `disclosures`
**File:** `agents/tier-coordinator.md`
**Edit:** Added an "Operational reading" section AFTER the Check A/B/C spec pseudocode (pseudocode left
intact). Grounds `maturity()` in two concrete inputs — the element's governing `mode:` on the transform
ladder (`mandatory` < `optional` < `preserve`) plus `kb/tiers/tier_<N>.yaml` `thresholds.violence.level` &
`thresholds.moral_ambiguity.level` (ladder mode first, thresholds as tiebreak, compared ordinally). Grounds
`permitted_at`/`disclosures` in the tier's `transformation_rules` death/conflict strategy: T1 defers death
via `journey_or_sleep` ⇒ a death disclosure is NOT permitted at T1 (leak); T1-2 convert battle→cooperation
⇒ named-battle disclosure not permitted at T1-2. Notes key-tolerant reads for the carried schema drift
(`death_euphemism`|`death_handling`, `conflict_to_cooperation`|`conflict_handling`).

### E2 — chronicler.md: key-materialization + Inv.3 name-check operational note
**File:** `agents/chronicler.md`
**Edit:** Added an "Operational reading — how the invariants are mechanically checkable" section after the
three invariants (invariants left intact). States how `(work, tier, chapter)` is materialized: `work`+`tier`
in the directory path (`kb/adaptations/<work>/tier-<N>/`); `chapter` in the per-chapter path
(`chapters/ch-<NN>/`) for chapter-scoped files AND stamped on each appended `continuity.md`/`decisions.md`
entry — `continuity.md` is per-tier RUNNING state across chapters by design, so the chapter lives on the
entry, not the dir. Documents Inv.3 name-check: before writing shared canon, compare the fact's name
against the source name in `analysis.yaml` (the oracle); source name → promote, tier-transformed name →
route to per-tier layer.

### E3 — tier-coordinator.md: one-line step-number pointer
**File:** `agents/tier-coordinator.md`
**Edit:** Added a one-line pointer note (blockquote near the top) that the step numbers ("step 10", "step
11", "steps 3-9") reference the per-chapter 11-step workflow (analyst → muse → writer → critic → editor →
writer → continuity-checker → safety-verifier → reader-sim → tier-coordinator → chronicler), proven
end-to-end by the Phase-3 hard gate. Placed in tier-coordinator.md; CLAUDE.md untouched.

---

## Verification

- **Files edited (4, all authorized BUILD-NEW native bodies):** `agents/chronicler.md`,
  `agents/tier-coordinator.md`, `skills/adaptation-safety/SKILL.md`,
  `skills/adaptation-safety/resources/children.md`. CLAUDE.md NOT edited (E3 went to tier-coordinator.md).
- **No adopted file touched.** No carried-verbatim `yaml` fence, `kb/` file, or `templates/` file touched.
  All edits are native prose (corrective for D1–D4, additive operational-reading notes for E1–E3 labeled as
  such). No spec-carried text deleted or contradicted.
- **No Mars keys introduced.**
- **Boundary gate:** `uv run python laf-adaptation/scripts/check_boundary.py` → exit **0** (PASS, rules
  A–F) both pre-fix and post-fix.

## Fixes applied: 7 (D1, D2, D3, D4, E1, E2, E3)
