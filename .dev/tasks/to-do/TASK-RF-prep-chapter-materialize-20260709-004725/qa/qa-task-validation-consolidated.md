# Consolidated Task-File Validation Findings (A.10 + A.10.25)

Task file: `TASK-RF-prep-chapter-materialize-20260709-004725.md`
Gate verdicts: B2 self-containment = PASS(minor); Phase-structure = **FAIL**(2 IMPORTANT); Research-alignment = PASS(minor).

Apply ALL fixes below IN-PLACE to the task file. Preserve everything else byte-for-byte.

## IMPORTANT (must fix — from structure lens)

**I-1: M3 final gate agent count vs I22 `standard` floor (7).**
- The `### Key Constraints` prose (~L133) declares the M3 gate uses "7 agents (3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain lens)", but Phase 6 Steps 6.2 + 6.3 only spawn 6 lens agents (3 rf-qa + 3 rf-qa-qualitative). QA_INTENSITY is `standard`, whose I22 final/assembled-output floor is 7. No domain-lens `- [ ]` exists.
- FIX (preferred — satisfy the floor, do not lower it): ADD a 7th lens agent as a new `- [ ]` item in Phase 6 alongside 6.2/6.3 — an rf-qa-qualitative agent with a LAF-**domain** lens: "boundary-contract-domain accuracy" (verifies the authored artifacts honor the LAF provenance model: NATIVE-vs-ADOPTED classification correct, `check_boundary.py` untouched, VENDOR `/**` NATIVE row correct, `.claude/` symlink convention, ADR-006 sole-script/no-runtime, path-contract single-source-of-truth). Report-only (fix_authorization: false), fully embedded adversarial lens prompt matching the style of 6.2/6.3. Renumber subsequent Phase-6 steps if needed and update the consolidation step (6.4) to read/expect 7 lens reports (4 rf-qa-qualitative + 3 rf-qa, or 3+3+1 domain — state the exact count). Ensure the I19/I22 floor statement in the item is consistent (final gate ≥7 at standard).

**I-2: Phase 6 title over-claims.**
- Phase 6 is titled "...POST Reflect, and Completion" but the POST reflect + Update-status-to-Done items live in the `## Post-Completion Actions` section (Steps 7.x), not Phase 6.
- FIX: retitle Phase 6 to accurately describe its contents (e.g. "Phase 6: Final QA Gate (M3 Lens-Based + M4 Source-Fidelity)"), dropping "POST Reflect, and Completion" from the title. Do NOT move the POST/Completion items — `## Post-Completion Actions` is the legitimate template-02 section for them.

## MINOR (fix — cheap, improves executor accuracy)

**M-1: path-contract line anchors off-by-one.** In the Phase-4 path-contract item(s): `## 5.` write-ownership heading is at L75 (not L76); the `work/prep/<slug>/*` row is L79 (insert the +3 write-ownership rows after L79, not "L80"). Correct these two line numbers; keep the content anchors.

**M-2: classify() line cite.** Phase-1 item cites classify() NATIVE default at "line 367" — actual is L368. Correct (cosmetic; file is byte-frozen, never edited).

**M-3: POST reflect `--diff` base.** Step 7.3 runner defaults `--diff HEAD..HEAD` (empty range). Tighten the instruction: resolve the diff base to the commit before this task's work (e.g. `git merge-base HEAD <integration-branch>` or the pre-task HEAD) and only fall back to `HEAD..HEAD` when nothing is committed; keep the existing fallback sentence.

**M-4: Step 7.3 blocker branch.** The blocker branch can mark-complete without a verdict. Add: if the runner returns RUN_INCOMPLETE after the bounded retries, set status "⚪ Blocked" with `blocker_reason` rather than marking the item complete (7.4's guard already backstops, but make 7.3 explicit).

## NOT-A-DEFECT (do NOT "fix" — flagged so a reviewer doesn't reverse a correct choice)
- Mirror verification uses `readlink` (correct — `.claude/` is symlinked), NOT `diff -r`. Do not change to copy/diff.
- "Sole script (ADR-006)" enforcement is scoped to NOT adding a NEW script; the pre-existing `test_check_boundary.py` is not a violation.
- Step 2.1 (author SKILL.md) is a long multi-section item — acceptable as one file with incremental-authoring instruction (B2.6 one-file-per-item holds).
