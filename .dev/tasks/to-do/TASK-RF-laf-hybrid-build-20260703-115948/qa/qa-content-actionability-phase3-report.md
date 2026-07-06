# QA Report — Phase-3 ACTIONABILITY lens (content-qualitative)

**Topic:** LAF hybrid build — Phase-3 cross-tier / safety / hard-gate actionability
**Date:** 2026-07-04
**Phase:** doc-qualitative (ACTIONABILITY lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY

---

## Overall Verdict: FAIL

Five actionability gaps found (3 IMPORTANT, 2 MINOR). All three checks land on the same
structural failure: every report asserts its **empty-set happy path** (`conflicts:[]`,
`evidence:[]`, GREEN) but does **not surface the actionable non-empty contract** that a
reviewer would need to act on a conflict / a safety FAIL / a RED gate. The contracts DO exist
and ARE actionable — but they live in the *source agents* (`tier-coordinator.md:151-154`,
`safety-verifier.md:61-76`) and the *research template* (`research/06:118`), NOT in the three
Phase-3 output reports under review. The reports are hollow on the failure path.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cross-tier report states empty-conflict precondition that let chronicler run | **PARTIAL/FAIL** | `ch-01-cross-tier.md:37-38` shows `status: RECONCILED` + `conflicts: []` and the A/B/C checks all PASS, but the report never states (a) that empty-conflicts is the precondition for chronicler promotion, nor (b) the conflict-object schema `{type, tier, element/disclosure, detail}` a non-empty entry carries, nor (c) the downstream action (muse re-dispatches offending tier's writer). That linkage exists only in the *gate report* (`phase-3-hard-gate-report.md:26`) and the *source agent* (`tier-coordinator.md:151-154`) — not in the cross-tier report itself. A reader of the cross-tier report alone cannot act on a conflict. |
| 2 | Safety report explains a FAIL populates `evidence` with `{section, location}` writer-actionable entries | **FAIL** | `ch-01-t1.md:59` ends with a bare `evidence: []` inside a PASS block; the report never explains that a FAIL populates `evidence` with located `{section, word, location}` entries. The actual actionable shape (`{section: forbidden_content, word: "sword", location: "para 4, sentence 2"}` → "concrete, located revision targets" fed back to the writer) is defined only in `safety-verifier.md:61-76` and paraphrased in `gate-cond2-safety.md:14-17` — NOT in the safety report under review. Adversarial "vague safety evidence" confirmed: the report shows the empty artifact but not the located-target contract. |
| 3 | Gate report's RED path names the specific failing condition + remediation pointer + HALT | **FAIL** | `phase-3-hard-gate-report.md:17` shows `OVERALL GATE VERDICT: 🟢 GREEN`. The report is 100% GREEN-path: neither the verdict line, the "Run context", nor the "Final statement" states what a RED verdict looks like, that a RED gate would HALT, or that it would name the specific failing gate condition with a remediation pointer. The HALT-on-any-FAIL contract exists in `research/06-proof-gate-workflow-template.md:118` ("If any FAIL → HALT") but is not surfaced in the gate report. A reader cannot tell from this report what happens on RED. |

## Summary
- Checks passed: 0 / 3 (all three checks surface an actionability gap)
- Checks failed: 3
- Critical issues: 0
- Important issues: 3
- Minor issues: 2
- Issues fixed in-place: 0 (fix_authorization FALSE — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `ch-01-cross-tier.md:37-38` | The report ends at `status: RECONCILED` / `conflicts: []` with no statement of the empty-conflict **precondition** (that empty-conflicts is what allows chronicler step-11 promotion). The gate report knows this (`:26`) but the cross-tier report — the actual reconciliation artifact — does not. | Add a closing line: "conflicts:[] ⇒ RECONCILED is the precondition for chronicler (step 11) to promote per-tier canon; a non-empty list blocks promotion and returns to the caller (muse)." Cross-ref `tier-coordinator.md:36,151-154`. |
| 2 | IMPORTANT | `ch-01-cross-tier.md` (whole) | Unactionable-conflict gap: the report never defines the conflict-object schema `{type, tier, element/disclosure, detail}` nor the three conflict types (`unsourced`, `disclosure_leak`, `monotonicity`) it screens for. On a real CONFLICT run, a reader could not act on `conflicts:[...]` from this report alone. | State the conflict schema and the remediation action (muse re-dispatches the offending tier's writer with the conflict as a revision note) so the RECONCILED result and its failure counterpart are both legible. Ground in `tier-coordinator.md:61-89,153-154`. |
| 3 | IMPORTANT | `ch-01-t1.md:59` | Vague safety evidence: `evidence: []` appears with no explanation that a FAIL populates it with **located** `{section, word, location}` entries the writer can act on. The report proves PASS but does not make the FAIL→revision path legible from the artifact itself. | Add a note beneath the verdict block: "On FAIL, `evidence` is non-empty and lists located revision targets, e.g. `{section: forbidden_content, word: \"sword\", location: \"para 4, sentence 2\"}`, fed back to the writer at workflow step 3." Cross-ref `safety-verifier.md:61-76`. |
| 4 | MINOR | `phase-3-hard-gate-report.md:17,30-36` | RED-path absent: the gate report never states what a RED verdict would look like, that it names the specific failing condition, or that it HALTs. GREEN is over-narrated; RED is silent. Because the per-condition rows (`:11-15`) each carry an evidence pointer, the RED contract is *reconstructible* but not *stated*. | Add one line under the OVERALL GATE VERDICT: "A RED verdict fires if any of the 5 conditions = FAIL; the gate names the failing condition + its `reviews/gate-cond*` evidence pointer as the remediation entry point and HALTs ('0.1 is not done'). See `research/06:118`." Severity MINOR because the row-level evidence pointers make the RED path reconstructible. |
| 5 | MINOR | `ch-01-t1.md:59` vs `gate-cond2-safety.md:15-17` | The FAIL→evidence loop contract is described in the *gate-cond2 review* (`:15-17`) but not in the *safety report* it audits, and neither states the full field set (`gate-cond2` says "return to step 3 with verdict.evidence" without the `{section, word, location}` shape). The actionable contract is split across two artifacts and complete in neither. | Consolidate: the safety report should carry the located-evidence example (fix #3); the gate-cond2 review should cite the `{section, word, location}` shape rather than the bare field name. |

## Actions Taken
None — `fix_authorization: FALSE` (report only). All five findings are documented above with
specific, located remediation.

## Self-Audit (reliance vs verification)

**(a) Reliance list — items taken as machine-verified, not re-derived:**
- Relied on the structural existence of all cited source files (verified by `ls`, not re-read
  in full): `reviews/gate-cond1..5-*.md`, `work/drafts/ch-01-t{1,3,5}-*.md`, `kb/tiers/tier_1.yaml`,
  `work/analysis/ch-01.yaml` all present.

**(b) Independent semantic checks (≥1 required):**
- **Check-1 counterpart** — did not accept the gate report's claim that "empty conflict list is
  the precondition" at face value; independently grepped `tier-coordinator.md` and confirmed the
  precondition + conflict schema + remediation at lines 36, 61-89, 151-154. Confirmed the
  cross-tier report itself omits all three.
- **Check-2 counterpart** — did not accept "evidence:[] means PASS" as sufficient; independently
  read `safety-verifier.md:61-76` to confirm the FAIL `{section, word, location}` evidence shape
  and the step-3 writer feedback loop, then confirmed the safety report under review contains
  none of it.
- **Check-3 counterpart** — independently grepped for RED/HALT and located the
  "any FAIL → HALT" contract at `research/06:118,184`, confirming the gate report never surfaces it.
- **Reconciliation anchors** — cross-checked the cross-tier report's 6 shared anchors
  (`ch-01-cross-tier.md:10-15`) against `work/analysis/ch-01.yaml:14-28`; all 6 (Sauron, Denethor,
  Théoden, Éowyn, Nazgûl, city-holds/host-withdraws) trace to CERTAIN facts in the analysis. The
  reconciliation's traceability claim (check A, `:28-29`) is sound — the gaps are about failure-path
  actionability, not about false anchors.

**Confidence:** Verified: 3/3 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 6 | Grep: 1 (multi-target) | Glob: 0 | Bash: 2

## Recommendations
- Treat all 5 findings as blocking before Phase-3 reports are presented as evidence of "0.1 done."
  The GREEN/PASS/RECONCILED verdicts themselves are sound (anchors trace, sections pass, boundary
  holds); the defect is that the three reports are **not self-contained on their failure paths** —
  a reader who hits a real conflict, safety FAIL, or RED gate cannot act from the report alone and
  must reach into the source agents. Surface the three contracts (conflict schema + muse re-dispatch;
  located `{section, word, location}` evidence; RED = named-condition + evidence-pointer + HALT) into
  the reports themselves.
- No CRITICAL findings: because the actionable contracts genuinely exist upstream and the empty-set
  verdicts are honestly derived, these are surfacing/forward-reference gaps (IMPORTANT/MINOR), not
  fabricated-safety or wrong-verdict defects.

## QA Complete
