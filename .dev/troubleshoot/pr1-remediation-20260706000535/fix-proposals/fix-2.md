# Fix Proposal 2 — M1: run test_check_boundary.py in CI

## Problem
`.github/workflows/boundary.yml` runs only `check_boundary.py` against the live tree. The 25-test regression suite (`laf-adaptation/scripts/test_check_boundary.py`, confirmed passing) — covering parser hardening, Mode-U SHA pinning, prefix rewrite, resource coverage, path traversal, and trust-root forgery — runs in neither CI nor the pre-commit hook. A logic regression in the security keystone could merge as long as the live fixture happens to pass.

## Proposed change
Add one step to `.github/workflows/boundary.yml` after the existing verify step:

```yaml
      - name: Boundary checker regression tests
        working-directory: laf-adaptation
        run: uv run python scripts/test_check_boundary.py
```

This does NOT violate ADR-006's "exactly one script" rule: the rule concerns *runtime* scripts (the framework is prompt+YAML, not software). `test_check_boundary.py` is a test artifact validating the boundary tool itself, sibling to the script — it's test-time, not runtime. It already exists in `scripts/` alongside the checker.

## Evidence
- `.github/workflows/boundary.yml:49-54` (only verify step, no test step)
- `laf-adaptation/scripts/test_check_boundary.py` exists (36 KB), 25 tests, all OK (ran: `Ran 25 tests in 0.084s / OK`)
- `grep test_check_boundary .github/ laf-adaptation/.githooks/` → no references

## Risks
- **Near-zero.** Tests are stdlib-only (no deps), run in 0.08s. They already pass, so adding the step is green from the first run.
- Optional belt-and-suspenders: also add the test run to `.githooks/pre-commit` (cheap, local fast-fail). I'll include this as an optional atom.

## Test plan
1. Locally: `cd laf-adaptation && uv run python scripts/test_check_boundary.py` → OK (already confirmed).
2. After editing the workflow, the next PR/push triggers the new step in CI.
