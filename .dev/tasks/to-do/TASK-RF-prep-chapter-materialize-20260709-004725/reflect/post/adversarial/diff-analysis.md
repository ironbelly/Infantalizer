# Diff Analysis — 3 reviewer-card comparison

## Metadata
- Generated: 2026-07-09 (run 20260709T163452Z-prepchmat)
- Variants compared: 3 (reviewer-1 analyzer, reviewer-2 qa, reviewer-3 refactorer)
- Focus: correctness, coverage, deviation-classification

## Structural / content differences

| # | Topic | R1 (analyzer) | R2 (qa) | R3 (refactorer) | Severity |
|---|-------|---------------|---------|-----------------|----------|
| C-001 | Finding count | 3 findings | 3 findings | 1 finding | Low |
| C-002 | AC coverage | (not its lens) | AC1-AC7 all covered | (schema lens) | Low — no conflict |
| C-003 | Manifest schema + 16-row table + confidence rule | (not its lens) | (partial) | all PASS | Low — no conflict |

## Contradictions

| # | Point of conflict | R1 position | R2 position | R3 | Impact |
|---|-------------------|-------------|-------------|----|--------|
| X-001 | Finding B (prep-cordinator write-scope) class | Regression (HIGH) | Drift (MEDIUM) | not raised | MEDIUM — class dispute |
| X-002 | Finding C (test_check_boundary.py = 2nd script) | Regression (HIGH), hedged | Drift (MEDIUM), hedged | not raised | Resolved: out-of-scope |

## Unique contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | R1 | Full 6-invariant PASS matrix (boundary-contract lens) | High |
| U-002 | R2 | Explicit per-AC covered map + positive findings (inline dispatch, analyst not splitter) | High |
| U-003 | R3 | Schema-fidelity + 16-row-table + confidence-rule-verbatim + non-restatement checks all PASS | High |

## Shared assumptions

| A-NNN | Assumption | Source agreement | Classification | Promoted |
|-------|-----------|------------------|----------------|----------|
| A-001 | AC6 boundary-check passes | all 3 deferred execution to orchestrator | STATED (orchestrator ran it live: exit 0, PASS) | No |

## Summary
- Structural/content differences: 3 (all Low, no conflict)
- Contradictions: 2 (X-001 class dispute; X-002 out-of-scope)
- Unique contributions: 3 (High — complementary lenses)
- Shared assumptions surfaced: 1 (STATED, resolved live)
- Convergence is high: all reviewers agree on AC coverage, invariant pass, and Finding A. Divergence is confined to the CLASS of Finding B and the SCOPE of Finding C — both resolved by blind calibration + orchestrator verification.
