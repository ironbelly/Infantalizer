# QA Report — Adversarial Lens: Evidence-Quality

**Topic:** TASK-remediation-check-boundary-hardening-20260704-172254 — verify every claim of completion in the Task Log is backed by on-disk evidence
**Date:** 2026-07-04
**Phase:** evidence-quality lens (post-execution audit of Task Log claims against reproducible on-disk state)
**Fix cycle:** N/A (report-only; `fix_authorization: false`)

---

## Overall Verdict: PASS (with 2 documentation-completeness findings — non-blocking, evidence itself is sound)

Every load-bearing claim of completion in the Task Log (test counts, gate exit codes, the OQ-1 CORRECTED hash, file-scope, QA phase report verdicts, DoD sign-off) is **independently reproducible from on-disk state**. Two findings are documentation-completeness gaps in the Task Log itself — they do NOT undermine the evidence quality of what was actually done, only the completeness of what was *recorded*.

---

## Items Reviewed

| # | Claim in Task Log | Result | Evidence |
|---|-------------------|--------|----------|
| 1 | "21/21 tests pass" (DoD #2; Phase 4 entry line 277; Phase 5 report G3) | PASS | `uv run python laf-adaptation/scripts/test_check_boundary.py` → `Ran 21 tests in 0.056s / OK`, exit 0. Direct count of `def test_` methods in source = 21. |
| 2 | "Real-tree Mode V verify exit 0" (Execution Log; DoD #3) | PASS | `uv run python laf-adaptation/scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.`, exit code 0. |
| 3 | "`--report` exit 0" (Execution Log; DoD #4) | PASS | `uv run python laf-adaptation/scripts/check_boundary.py --report` → exit code 0. |
| 4 | "64 rows (55 ADOPTED-CLEAN, 1 ADOPTED-PATCHED, 5 NATIVE, 3 BUILD-NEW)" (Execution Log line 235; DoD #3) | PASS | `--report` summary prints exactly `ADOPTED-CLEAN 55 / ADOPTED-PATCHED 1 / NATIVE 5 / BUILD-NEW 3 / TOTAL rows 64`. |
| 5 | OQ-1 CORRECTED: `sha256(prefix_unrewrite(brainstormer)) == aa736c5d…` (Resolutions; Phase 3 Findings line 268) | PASS | Independent recompute via `hashlib.sha256(cb.prefix_unrewrite(disk))` = `aa736c5d23c3930576d449dbda56dfaf45d9c5f5273c466b9e1f36525117fa73` — byte-exact match to VENDOR.md `upstream_sha256` cell for brainstormer.md. Forward direction `sha256(disk) = 5c827eff…` also matches `laf_sha256`. Inverse formula is mathematically correct. |
| 6 | "file-scope respected — no adopted body touched" (DoD implicit; Phase 2/3/4 entries "file-scope clean") | PASS (with framing caveat — see Finding F-1) | Working-tree status `git status --short laf-adaptation/` shows ONLY: `M scripts/check_boundary.py`, `M VENDOR.md`, `M CLAUDE.md`, `?? scripts/test_check_boundary.py`. NONE of `laf-adaptation/agents/`, `skills/`, `kb/`, `templates/` modified in working tree. The lens-prompt's literal command (`git diff b51633d4 -- laf-adaptation/{agents,skills,kb,templates}/`) returns a 298KB diff — but only because `b51633d4` is the repo's INITIAL commit (predates ALL laf-adaptation files); the meaningful baseline is working-tree-vs-HEAD, which IS empty for those dirs. |
| 7 | "10/10 tests pass" at Phase 2 (line 264) | PASS (progression consistent) | Phase 2 QA report (`qa-phase-2-report.md`) Check #16 + Actions Taken: "10/10 pass". Current test file has 21 methods; class breakdown (CleanCorpus=1, ParserHardening=5, PathSafety=3, ReportContract=1) = 10 tests attributable to Phase 2's scope, with Phase 3 (TrustRoot=4, WriterOnly=2, Resources=2 = 8 → 18) and Phase 4 (PrefixRewrite=1, ModeUHeadPin=2 = 3 → 21) adding the remainder. Progression 10 → 18 → 21 is internally consistent. |
| 8 | "18/18 tests pass" at Phase 3 (line 272) | PASS (progression consistent) | Phase 3 QA report Check #18: "Full test suite green (18 tests) — Ran 18 tests". Matches. |
| 9 | Phase 2 QA report verdict = PASS (Task Log line 260 "phase-gate QA PASS") | PASS | `reviews/qa-phase-2-report.md` exists; `## Overall Verdict: PASS (after 2 in-place fixes applied during this gate)`. Task Log Phase 2 entry documents F-1/F-2 fixes consistently. |
| 10 | Phase 3 QA report verdict = PASS (implicit in "COMPLETED") | PASS | `reviews/qa-phase-3-report.md` exists; `## Overall Verdict: PASS`. 21/21 checks; 0 issues. |
| 11 | Phase 4 QA report verdict = PASS (implicit in "COMPLETED") | PASS | `reviews/qa-phase-4-report.md` exists; `## Overall Verdict: PASS (after 2 in-place fixes)`. **BUT** the Task Log Phase 4 entry (lines 274–277) does NOT mention the 2 in-place fixes the QA report applied (vacuous-assertion fix + em-dash pin-parsing fix) — see Finding F-2. |
| 12 | Phase 5 QA report verdict = PASS (implicit in "COMPLETED") | PASS | `reviews/qa-phase-5-report.md` exists; `## Overall Verdict: PASS`. 12/12 checks; 0 issues. |
| 13 | OQ-2: "Project runs Python 3.13.13; no `requires-python` pin; no `.python-version`" (Resolutions) | PASS | `uv run python --version` → Python 3.13.13. `pyproject.toml` does not exist at repo root (exit-1 from grep). `.python-version` does not exist. `Path.is_relative_to` available. |
| 14 | upstream_sha pin = `3338495f0fabf778720effdda9386ab56d4ebf6e` (Execution Log line 237) | PASS | `grep upstream_sha laf-adaptation/VENDOR.md` → `upstream_sha:  3338495f0fabf778720effdda9386ab56d4ebf6e`. Byte-exact match. |
| 15 | DoD #7: "Pure-stdlib preserved (argparse, hashlib, subprocess, sys, pathlib)" | PASS | `prefix_unrewrite` at `check_boundary.py:87`; `_checkout_head` uses `subprocess.run` (list-form, no `shell=True`). All stdlib. |
| 16 | CH-8 doc alignment: boundary.yml + CLAUDE.md §2 + VENDOR.md header aligned (DoD #6; Phase 5) | PASS | boundary.yml header (lines 5–17) describes Rule A′ / CH-1 / scoped malicious-drift gate. CLAUDE.md §2 lines 105–106 carry the scoped "malicious-drift gate against single-field `laf_sha256` forgery" phrasing. VENDOR.md header documents raw-upstream hash semantics. No over-claiming of absolute guarantees (Phase 5 QA report Check #8 verified). |

## Summary

- Claims verified: **16 / 16**
- Claims that FAILED verification: **0**
- Critical issues: **0**
- Findings (documentation completeness, non-blocking): **2** (F-1, F-2)
- Issues fixed in-place: **0** (`fix_authorization: false` — report only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| F-1 | MINOR | Task framing in lens prompt (not the Task Log itself) | The lens prompt's prescribed command for the file-scope claim — `git diff b51633d4 -- laf-adaptation/{agents,skills,kb,templates}/` — produces a 298KB diff showing every adopted body as newly Added. This is NOT a Task Log defect: `b51633d4` is the repo's INITIAL commit, predating the entire LAF 0.1 tree. The correct baseline for "file-scope respected" is the working-tree-vs-HEAD diff, which IS empty for those four subtrees (only `M scripts/check_boundary.py`, `M VENDOR.md`, `M CLAUDE.md`, `?? scripts/test_check_boundary.py` under `laf-adaptation/`). The Task Log's "file-scope clean" claim is therefore substantiated by the correct baseline. The Phase 3 QA report (Check #19) already noted this framing hazard explicitly. Recorded here so future lens prompts use `git status --short` (working-tree) not `git diff <initial-commit>`, for tasks whose `start_commit` is the repo's initial commit. | None to the Task Log. Update future lens-prompt templates to use working-tree status when `start_commit` is the initial commit. |
| F-2 | MINOR | Task Log → Phase 4 Findings entry (lines 274–277) | The Phase 4 entry claims "21/21 tests pass … Mode V gate + `--report` green; file-scope clean" with NO mention of the 2 in-place fixes the Phase 4 QA gate applied. The QA report `qa-phase-4-report.md` documents: (1) IMPORTANT fix — vacuous assertion in `test_upstream_matching_sha_passes_head_check` (was inspecting only the empty preamble before the BOUNDARY banner; a CH-5 HEAD-mismatch regression would have false-passed); (2) MINOR fix — `parse_upstream_sha` treated the em-dash `NO_HASH` placeholder as a truthy pin, masking the "no pin" branch. Both were fixed and verified during the Phase 4 gate. By contrast, the Phase 2 Task Log entry DOES document its F-1/F-2 in-place fixes (line 265). The Phase 4 entry's silence is a documentation-completeness gap, NOT an evidence-quality defect — the fixes are real, applied, and verified in the QA report; they are just not surfaced in the Task Log's Phase Findings narrative. | Add a bullet to the Phase 4 Findings entry noting the 2 QA-applied in-place fixes (vacuous-assertion + em-dash pin-parsing), matching the documentation transparency of the Phase 2 entry. |

### Non-issues investigated and dismissed

- **Test-count regression check:** Phase 2 claimed 10 tests, Phase 3 claimed 18, Phase 4 claimed 21. Current run = 21. The progression is monotonic and consistent with the test classes added per phase (Phase 2: 10 baseline; Phase 3: +8 TrustRoot/WriterOnly/Resources; Phase 4: +3 PrefixRewrite/ModeUHeadPin). No regression.
- **`--report` exit code on malformed manifest:** Task Log DoD #4 claims `--report` exits 0; verified exit 0 on the real (well-formed) manifest. The Phase 2 QA gate also added `test_report_exits_0_on_malformed` covering the malformed-manifest contract.
- **Inverse-formula generalization (not just brainstormer):** Phase 3 QA report Check #1 documents an exhaustive sweep across all 55 ADOPTED-CLEAN rows — 55/55 equal, 0 mismatches — including the 10 literal-bearing agent rows where the inverse is non-trivially exercised. I independently verified brainstormer; the QA report's exhaustive sweep is the authoritative evidence for the generalization.
- **CH-7 prefix-rewrite positive test non-vacuity:** Phase 4 QA Check #12 confirms `test_prefix_rewrite_positive` asserts 4 meaningful sub-properties; Phase 3 QA Check #14 documents the fail-test vacuity probe across all 6 fail-tests (all flip when their rule is stubbed). Not vacuous.
- **Subprocess injection in `_checkout_head`:** Phase 4 QA Check #4 confirms list-form `subprocess.run` (no `shell=True`). I re-read `check_boundary.py:147–159`; confirmed.

---

## Actions Taken

None (report-only; `fix_authorization: false`). The two findings are documentation-completeness gaps, not evidence-quality defects. The load-bearing evidence itself is sound and reproducible.

---

## Recommendations

- **F-1:** No Task Log change required. Future lens-prompt templates should default to `git status --short <scope>` for file-scope verification when the task's `start_commit` resolves to the repo's initial commit (or whenever the diff-vs-start-commit would include unrelated prior work). The Phase 3 QA report already encodes the correct framing (Check #19 parenthetical).
- **F-2:** Add a one-line bullet to the Task Log Phase 4 Findings entry (after line 277) documenting the 2 in-place QA fixes, mirroring the Phase 2 entry's transparency. This brings the Task Log into parity with its own QA reports.
- **Green light:** All claims of completion are substantiated by reproducible on-disk evidence. The remediation work is verified correct. (Note: this lens addresses EVIDENCE QUALITY only; the task's own item 6.3 — the lens-based QA gate on the diff — and item 6.4 — the reflect post-gate — remain unchecked `[ ]` per the task file. Those are separate gates, not evidence-quality claims.)

---

## Confidence

- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 (task file, qa-phase-{2,3,4,5}-report.md) | Grep: 4 (test methods, prefix fns, upstream_sha, CLAUDE.md §2) | Glob: 0 | Bash: 9 (test suite, verify gate, report gate, file-scope diff x2, brainstormer hash recompute, python version, report count, boundary.yml header)
- **Tavily/Web:** 0 (all verification was local source-truth; no external claims to check)

Every load-bearing claim verified with cited tool output (command + result for behavioral checks; file:line for structural checks; byte-exact hash recompute for the OQ-1 CORRECTED claim).

## QA Complete
