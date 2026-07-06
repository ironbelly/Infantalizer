# QA Report — Report Validation (EVIDENCE-QUALITY lens on Phase-3 Hard-Gate)

**Topic:** Phase-3 HARD-GATE report — evidence-quality / zero-trust audit
**Date:** 2026-07-04
**Phase:** report-validation (evidence-quality lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY
**Stance:** ADVERSARIAL — assume >=5 errors until each PASS is independently reproduced.

---

## Method

For each of the 5 gate conditions, I (1) confirm the cited review artifact exists on disk, (2) open it and confirm the claimed evidence is actually present, (3) trace the review back to the underlying runtime artifact under `laf-adaptation/` and independently verify (grep / ls / re-run) rather than trusting the review's word, and (4) cross-check the two run-summaries against `ls` for fabricated steps/artifacts.

## Overall Verdict: PASS (with 1 IMPORTANT documentation finding + 3 MINOR)

The substantive gate is sound: every one of the 5 PASS verdicts is backed by a concrete on-disk artifact whose claimed evidence I independently reproduced (grep / ls / file read / **re-running `check_boundary.py` in both modes**). No fabricated artifact, no fabricated step, no assumed-without-evidence run. The GREEN verdict is **defensible**.

However, adversarial audit surfaced a real evidence-quality defect: the **T1 raw-capture file contains a self-contradictory `FAIL:` line on the Inv.3 no-shared-canon-leak check** that no downstream summary or review acknowledges or reconciles. Ground truth is clean (my independent grep = NONE), so this is a buggy capture-script line rather than a real leak — but a raw-evidence artifact that literally prints "FAIL: transformed name leaked to shared canon" while every summary reports "✓ verified by grep" is exactly the kind of unreconciled contradiction a hard-gate must not paper over.

---

## Items Reviewed

| # | Check | Result | Evidence (independently reproduced) |
|---|-------|--------|-------------------------------------|
| C1 | cond1 review artifact exists + claim true | PASS | `reviews/gate-cond1-tags.md` exists. Read `work/analysis/ch-01.yaml`: `status: OK`, `source_access: FULL`. `grep -c confidence:` = 19; `grep -c CERTAIN` = 16; PROBABLE = 4 (3 on essentials + 1 metadata worst-case). Report's "16 CERTAIN + 3 PROBABLE" = accurate for essentials. |
| C2 | cond2 review artifact exists + claim true | PASS | `reviews/gate-cond2-safety.md` exists. Read `work/safety-reports/ch-01-t1.md`: verdict block `result: PASS`, `tier: 1`, `mode: blocking`, `next: promote`, all 6 sections PASS, `automatic_failures: []`. Matches review exactly. |
| C3 | cond3 review artifact exists + per-tier canon present + no shared-canon leak | PASS (claim wording MINOR-inaccurate) | `reviews/gate-cond3-canon.md` exists. `find kb/adaptations` → all T1/T3/T5 continuity.md + chapters/ch-01/canon-delta.md + decisions.md + analysis.yaml + adapted.md present (5×3). Independent `grep -rniE "grumpy\|sad leader\|grumpy rider" kb/canon/ kb/timeline/` → **exit 1, NONE** = no leak, confirmed. Shared canon holds source names (Sauron/Denethor/Théoden/Éowyn/Nazgûl). See MINOR-1 re "only under tier-1" wording. |
| C4 | cond4 review artifact exists + 4 distinct quartet outputs | PASS | `reviews/gate-cond4-quartet.md` exists. All 4 cited files present; `head -1` of each shows a distinct agent header (critic / editor "never folded — G3" / continuity-checker / reader-sim). `agents/editor.md` present (Rule D). safety-verifier distinct 5th at `work/safety-reports/ch-01-t1.md`. |
| C5 | cond5 review artifact exists + `check_boundary.py` green (RE-RUN MYSELF) | PASS (disclosure MINOR) | `reviews/gate-cond5-boundary.md` exists. **I re-ran both modes.** Plain: `PASS — all rules (A-F) satisfied`, EXIT 0. `--upstream <real checkout at .dev/releases/current/0.1/creative-writing-skills>`: `PASS`, EXIT 0. Review's "exit 0 both modes; Rules B/C incl." is **reproducible**. See MINOR-2 (plain mode silently skips B/C) + MINOR-3 (review doesn't record which checkout path). |
| S1 | phase3-t1-run-summary.md faithful to `ls` | PASS-with-IMPORTANT | Every artifact path in the summary exists on disk (verified via `ls`/`find`). No fabricated step. BUT the raw-capture it points to (`phase3-t1-run-raw.txt`) records `FAIL: transformed name leaked to shared canon` on Inv.3 — contradicting the summary's "Inv.3 ✓". See IMPORTANT-1. |
| S2 | phase3-fanout-summary.md faithful to `ls` | PASS | Every path exists; per-tier table (adapted/continuity/canon-delta/analysis/decisions ×3) matches `find`. cross-tier `status: RECONCILED · conflicts: []` confirmed in `work/analysis/ch-01-cross-tier.md`. T3 safety `result: PASS / mode: advisory` confirmed; T5 safety file correctly absent (N/A). fan-out raw-capture correctly shows "'Grumpy King' in shared kb/canon/: NONE". |
| S3 | runtime-artifacts-review faithful | PASS | Every "Actual" cell reproduced: drafts t1 v1+v2 / t3 v1 / t5 v1 present; promoted analysis.yaml `grep -c confidence:` = **19 per tier** (T1/T3/T5) as claimed; tier renderings ("grew very tired and sat right down" T1 / "Théoden died" T3 / "he fell" T5) all present in the actual adapted.md files. |

---

## Summary
- Checks passed: 8 / 8 substantive (all 5 conditions + 3 summaries backed by real, reproduced evidence)
- PASS verdicts with a real backing artifact that EXISTS + reproduces: **5 / 5**
- Fabricated artifacts: **0** · Fabricated steps: **0** · Assumed-without-evidence runs: **0** (I re-ran cond5 myself, both modes)
- Issues found: **4** (IMPORTANT: 1, MINOR: 3)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| IMPORTANT-1 | IMPORTANT | `test-results/phase3-t1-run-raw.txt` lines 3-6 vs `phase3-t1-run-summary.md` line 35 (Inv.3), `reviews/gate-cond3-canon.md` line 19, `phase3-runtime-artifacts-review.md` line 39 | The T1 **raw-capture** — the authoritative raw evidence the run-summary cites — literally prints `FAIL: transformed name leaked to shared canon`, immediately followed by lines showing shared canon actually uses SOURCE names. The capture is self-contradictory (buggy check line). Ground truth is CLEAN (my independent grep = NONE; the fan-out capture correctly prints "NONE"). But **no summary, review, or the hard-gate report acknowledges or reconciles this `FAIL:` line.** A hard-gate that green-lights on a raw artifact containing an unreconciled "FAIL" is an evidence-quality gap: a reader auditing the raw trail sees FAIL, every rollup says PASS, and nothing explains the divergence. | Fix the buggy Inv.3 check line in the T1 capture harness (it should print PASS/NONE like the fan-out capture does), OR add an explicit reconciliation note in `phase3-t1-run-summary.md` and `gate-cond3-canon.md` stating the raw line is a known false-positive and citing the corrected grep. Do not leave a bare "FAIL" in the raw evidence trail. |
| MINOR-1 | MINOR | `reviews/gate-cond3-canon.md` line 20; `phase3-runtime-artifacts-review.md` line 39-40; `phase3-fanout-summary.md` line 34 | Claim: `"Grumpy King" appears **only** under kb/adaptations/tolkien/tier-1/`. Independent `grep -rli "grumpy king" kb/` shows it **also** appears in `kb/adaptation-mapping/tolkien-mapping.yaml:28` (the tier_1 name-mapping config — an expected, legitimate location). The no-**shared-canon**-leak claim is TRUE (not in kb/canon/ or kb/timeline/), but the literal word "only under tier-1" is inaccurate. | Reword to "appears only under `kb/adaptations/tolkien/tier-1/` **and its source mapping config**, and is absent from shared `kb/canon/` + `kb/timeline/`" — scope the "only" to the shared-canon invariant it's actually asserting. |
| MINOR-2 | MINOR | `reviews/gate-cond5-boundary.md`; report line 15 | The plain `check_boundary.py` invocation (the one most readers will run) prints `NOTE: verify running without --upstream — Rules B and C (upstream-diff checks) skipped`. The review presents plain-mode "exit 0" as first-class evidence without noting that plain mode does NOT exercise Rules B/C. Only the `--upstream` run (which I reproduced = PASS) actually covers B/C. | Add a one-line note in gate-cond5 that plain mode skips B/C and that the B/C guarantee rests on the `--upstream` run. |
| MINOR-3 | MINOR | `reviews/gate-cond5-boundary.md` line 7 | The `--upstream <checkout>` claim uses a literal placeholder `<checkout>` — the actual checkout path used at run time is not recorded. I located the real checkout (`.dev/releases/current/0.1/creative-writing-skills`) and reproduced EXIT 0, so the claim is sound; but an un-recorded checkout path is a traceability gap (a future auditor can't re-run the exact command). | Record the concrete `--upstream` path (and the upstream SHA it was checked out at) in the review, so the exit-0 claim is independently re-runnable. |

---

## Independent Verification Actions (evidence I can point to)
- `grep -c confidence:` / `CERTAIN` / `PROBABLE` on `work/analysis/ch-01.yaml` → 19 / 16 / 4 (cond1).
- Read full safety verdict block in `work/safety-reports/ch-01-t1.md` → PASS/blocking/promote/6×PASS/`[]` (cond2).
- `find kb/adaptations kb/canon kb/timeline -type f` → full per-tier tree present (cond3).
- `grep -rniE "grumpy|sad leader|grumpy rider" kb/canon/ kb/timeline/` → **exit 1 / NONE** (cond3, definitive no-leak).
- `grep -rli "grumpy king" kb/` → surfaced the extra `adaptation-mapping` hit (MINOR-1).
- `head -1` on all 4 quartet files → distinct-agent headers (cond4).
- **Re-ran `check_boundary.py` plain → EXIT 0; re-ran `--upstream <real checkout>` → EXIT 0** (cond5, not assumed).
- Ran `check_boundary.py --upstream /nonexistent` → EXIT 1 / 56 violations, proving `--upstream` is a real, failable check (not a no-op).
- Read both raw-capture files → surfaced the IMPORTANT-1 self-contradictory FAIL line.
- `grep -c confidence:` on all 3 promoted analysis.yaml → 19/19/19 (S3).
- grep tier renderings in the 3 adapted.md files → all match report body claims (S3).

---

## Recommendations
- **Before promoting this gate to "0.1 DONE" for the record:** resolve IMPORTANT-1 — the raw evidence trail must not contain an unreconciled "FAIL" line. Either fix the buggy capture check or add an explicit false-positive reconciliation note. The verdict itself does not change (ground truth is clean), but the evidence trail is not audit-clean until this is reconciled.
- Apply the 3 MINOR wording/traceability fixes to gate-cond3 and gate-cond5.

## Confidence Gate
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: (embedded in Bash) | Glob: 0 | Bash: 9
- No web research required (all claims are local-artifact-bound; Principle 6 source-truth-first applied throughout).
- No UNCHECKED items. No UNVERIFIABLE items — cond5 `--upstream` was made verifiable by locating the real checkout.

## QA Complete

---
