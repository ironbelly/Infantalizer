# Fix Proposal 4 — M3: writer.md Mode-V residual comment pointer

## Problem
The ADOPTED-PATCHED (writer.md) Mode-V gap is **explicitly documented and tested** — not a defect. The exclusion is acknowledged at `check_boundary.py:517`, in the workflow header (`boundary.yml:27-33`, "ADOPTED-PATCHED ... ABSOLUTE guarantee requires Mode U ... deferred follow-up OQ-4"), in `CLAUDE.md`, in `VENDOR.md`, and in two regression tests (`test_writer_is_not_reanchored_in_mode_v`, `test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v` marked `DOCUMENTED-RESIDUAL`).

The only actionable ask: the `else:` block at line 598 (where Rule C is skipped in Mode V) prints a NOTE but does **not** name writer.md or OQ-4. A reader of just that code path has to infer the writer.md-specific residual from the inverse-direction comment at line 517.

## Proposed change
Add a one-line comment at the `else:` block (line 598) explicitly naming the writer.md residual and OQ-4, so the Mode-V skip is self-documenting without reading the workflow header:

```python
    else:
        # Mode V (no --upstream): Rules B/C skipped. ADOPTED-PATCHED writer.md's
        # additive-body guarantee is a documented residual here — its absolute
        # proof is Mode-U Rule C (OQ-4: Mode U in CI is deferred). Backstopped by
        # branch protection + human review of any upstream_sha256 diff.
        print("NOTE: verify running without --upstream — Rules B and C (upstream-diff "
              ...)
```

## Evidence
- `check_boundary.py:517-519` (exclusion comment, inverse direction)
- `check_boundary.py:598-601` (`else` block, no writer.md/OQ-4 pointer)
- `.github/workflows/boundary.yml:27-33` (OQ-4 referenced in workflow, not in code)

## Risks
- **Zero.** Comment-only change. No behavior change, no hash change, no test change.

## Test plan
1. `uv run python scripts/check_boundary.py` → still exits 0 (comment-only).
2. `uv run python scripts/test_check_boundary.py` → still OK (no behavior change).
