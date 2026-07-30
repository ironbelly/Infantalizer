# Task-File Validation Fix Report (A.10 serialized-fix pass)

**Task file:** `TASK-RF-prep-chapter-materialize-20260709-004725.md`
**Source findings:** `qa/qa-task-validation-consolidated.md`
**Fix authorization:** true (in-place edits)
**Date:** 2026-07-09

All IMPORTANT (I-1, I-2) and MINOR (M-1..M-4) findings applied in-place. NOT-A-DEFECT items left untouched. Every edit re-verified by re-reading/grepping the affected span.

---

## IMPORTANT

### I-1 — M3 final gate agent count vs I22 `standard` floor (7)
Added a 7th M3 lens agent and propagated the ≥7-at-standard count consistently.

- **New lens item added** (Step 6.3, now L286): an `rf-qa-qualitative` agent with a **LAF domain lens: boundary-contract-domain accuracy**, `fix_authorization: false` (report-only), fully embedded adversarial prompt in the same style as the 6.2/6.3 lens items. It verifies NATIVE classification of the new skill, Rule-E non-collision, the single U+2014 VENDOR glob row, `check_boundary.py` untouched/sole-script (ADR-006), no adopted-body edit / additive-only spine wiring, `.claude/` symlink convention, path-contract single-source-of-truth, and no 9th numbered package file. Writes to `qa/qa-domain-boundary-contract-report.md`. Verdict: FAIL if any issue of any severity.
- **Consolidation updated** (Step 6.4, L290): now Globs **seven** reports across `qa-structural-*`, `qa-content-*`, AND the new `qa-domain-*-report.md`; blocker branch now fires if **fewer than seven** reports are found (was "no reports").
- **Step 6.3 header** (L278): retitled to "content + domain lens agents … 3 content lenses + 1 domain lens".
- **Phase 6 intro** (L264): now states the M3 gate spawns SEVEN report-only lens agents (3 rf-qa structural + 3 rf-qa-qualitative content + 1 rf-qa-qualitative domain), satisfying the ≥7 standard floor.
- **Key Objective 5** (L91): changed "min 6 agents" → "7 agents at standard intensity (3+3+1), satisfying the I22 standard final-gate floor of ≥7".
- **Key Constraints prose** (L133): tightened to state the 7 agents "meet the I22 standard final/assembled-output floor of ≥7 agents" and that the 7th (domain) lens "raises the count to the standard ≥7 floor". Now consistent with the Phase-6 items.
- **Consistency verified:** the ≥7-at-standard count now agrees across Key Constraints (L133), Key Objective 5 (L91), Phase 6 intro (L264), Step 6.3 header (L278), the 7 spawn items (L270–286, grep count = 7), and Step 6.4 (L290).

### I-2 — Phase 6 title over-claims
- **Phase 6 header** (L262): retitled from "…, POST Reflect, and Completion" → **"Phase 6: Final QA Gate (M3 Lens-Based + M4 Source-Fidelity)"**. The POST reflect (Step 7.3) and Update-status-to-Done (Step 7.4) items were NOT moved — they remain under the legitimate `## Post-Completion Actions` (template-02) section.

---

## MINOR

### M-1 — path-contract line anchors off-by-one (Step 4.1, L236)
- `## 5.` write-ownership heading anchor: **L76 → L75** (verified: heading is at path-contract.md L75).
- `work/prep/<slug>/*` row anchor for the +3 write-ownership row insert: **L80 → L79** (verified: row is at path-contract.md L79). Content anchors kept; the `after L73 / BEFORE ## 5.` and `after L91` anchors were already correct and left intact.

### M-2 — classify() line cite (Step 1.5, L196)
- "classify() default NATIVE at line 367" → **"line 368"**, per the consolidated finding. (File is byte-frozen/never edited; cite is cosmetic provenance only.)

### M-3 — POST reflect `--diff` base (Step 7.3 runner prompt, L336)
- Rewrote instruction step 1 to **resolve the diff base FIRST**: determine the commit immediately preceding this task's work and use `<resolved-base>..HEAD`; resolve via `git merge-base HEAD <integration-branch>` or the pre-task HEAD SHA; **fall back to `HEAD..HEAD` ONLY when nothing is committed yet**. The `Skill(...)` invocation now uses `--diff <resolved-base>..HEAD` with the substitution rule stated. Existing fallback sentence preserved (as the explicit "only when nothing committed" branch).

### M-4 — Step 7.3 blocker branch (L344)
- Added an explicit RUN_INCOMPLETE handling clause: if the runner returns `RUN_INCOMPLETE` after the bounded re-spawn retries (or cannot run the skill), **set frontmatter `status` to "⚪ Blocked" and populate `blocker_reason`**, log the blocker, and **leave the item unchecked** so the Step 7.4 done-guard cannot proceed — rather than marking the item complete with an empty/partial `reflect_post`. The normal-completion path (full run → real `{verdict, run_id, report}` → mark complete) is preserved.

---

## NOT-A-DEFECT (left untouched — verified)
- Mirror verification still uses `readlink` (5 occurrences intact); the 3 "do NOT use `diff -r`" warnings preserved. No copy/diff conversion made.
- "Sole script (ADR-006)" enforcement wording unchanged (scoped to not adding a NEW script).
- Step 2.1 (author SKILL.md) left as a single long multi-section item.

---

## Verification summary
- Total checklist `- [ ]` items: 36 → **37** (one added for the 7th lens).
- Step 6.2+6.3 `Spawn` lens items: **7** (grep-confirmed).
- No stale "six lens reports" / "all six" / "min 6" references remain except the intentional BUILD_REQUEST-minimum framing in Key Constraints (correctly contrasted against the ≥7 floor).
- All six finding edits re-read/grepped in place after application.

## VERDICT: FIXED (all applied)
