# Blind Calibration Card — T1 reflection (Wave 1D)

**Calibrator class:** sonnet (gpt-5.5) — disjoint from T1 reviewer class per §11.3
**Calibrator_diversity:** full (calibrator class NOT in reviewer pool)
**Input:** T1 reflection card ONLY (no formation context, no coverage matrix, no spec)

## 5-dimension re-grade

| Dimension | T1 self-report | Calibrated | Delta | Reasoning |
|-----------|----------------|------------|-------|-----------|
| Citation grounding | 0.96 | 0.94 | -0.02 | Card claims high citation density but the calibrator cannot verify the cited line numbers without the spec; the claim is plausible given the per-step pattern described, but unverified. Slight down-grade for inability to confirm. |
| Coverage completeness | 1.00 | 0.97 | -0.03 | Card asserts 45/45 mapped with empty unmapped set. The structural argument (16 parsed + 29 inferred, all MATCH) is internally consistent, but "100% coverage" on a 151-item tasklist against a 7-file spec pack is a strong claim — the calibrator reserves 0.03 for unsampled spec corners (e.g., agent-schemas §6 dispatch-param summary, kb-formats §5 shared-vs-per-tier split — cited in frontmatter but not exhaustively mapped in the card's visible portion). |
| Deviation-classification clarity | 0.92 | 0.90 | -0.02 | Six findings classified as NOT-a-defect or NECESSARY. The two spec-internal-tension findings (F2 analyst active_tier, F3 four-vs-five keys) are correctly resolved, but the card's recommendation to "surface F2 to spec author" is a process suggestion, not a defect classification — slight over-reach. |
| Risk surface coverage | 0.90 | 0.88 | -0.02 | Card notes process additions (POST reflect gate, 5 lens-QA gates per phase) and correctly flags them for T2 debate. The down-grade reflects genuine uncertainty: are 5 lens agents × 5 gates (+ post-completion 6 agents) proportionate, or theatrical? The card raises this but doesn't resolve it. |
| Recommendation actionability | 0.95 | 0.95 | 0.00 | The per-step "Read → write → verify → log" pattern is concretely actionable; no change. |

## Calibrated confidence (arithmetic mean)

C_calibrated = (0.94 + 0.97 + 0.90 + 0.88 + 0.95) / 5 = **0.928**

## Escalation recommendation

- C_calibrated = 0.928 ≥ 0.90, BUT:
  - S_scope (tasklist items) = 151 ≫ 5 (rule 1 ceiling) and ≫ 10 (rule 2 ceiling)
  - S_domains: the tasklist touches code (Python script), infra (.githooks, CI), docs (CLAUDE.md, NOTICE, UPSTREAM-SYNC.md), config (YAML kb), tests (boundary gate runs), agent/skill definitions — ≥5 distinct domains ≫ 3 (rule 4 ceiling)
  - `--depth deep` hard override (§5.1) → ALWAYS escalate to T2
  - Regression-irrelevant (PRE mode), but multi-domain + scale force T2 per rules 4/5/6/8 regardless of confidence.

**Decision: ESCALATE to Tier 2.** Fired rule: §5.1 hard override (`--depth deep`) + §5.3 rule 4 (S_domains ≥ 3) + rule 5/6 (scale). The calibrated confidence is high enough that T2 is calibration-confirming rather than calibration-rescuing, but the deep override and multi-domain scope make T2 mandatory.

## Notes for T2
- T1 card is well-grounded; T2 should focus on the 4 "concerns to debate" (F2 spec wording, process-add proportionality, PC.6 --fix/--promote auto-mutation, Step 1.2 git coupling).
- The 0.928 calibrated confidence means T2 reviewers should NOT expect to find defects in the tasklist's spec coverage — the coverage is genuinely complete. T2 value-add is debating the process additions and the auto-promote posture, not re-litigating coverage.
